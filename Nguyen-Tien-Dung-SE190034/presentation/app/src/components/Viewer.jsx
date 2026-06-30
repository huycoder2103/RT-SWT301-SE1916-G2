import { useEffect, useMemo, useRef, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/TextLayer.css';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { pdfUrl, docUrl, arxivToFile, arxivMeta } from '../data';

// PDF.js worker (Vite bundles this from node_modules)
pdfjs.GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url).toString();

const norm = (s) => (s || '').toLowerCase().replace(/[“”"'’]/g, '').replace(/\s+/g, ' ').trim();
const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export default function Viewer({ view, onClose }) {
  const [numPages, setNumPages] = useState(0);
  const [page, setPage] = useState(1);
  const [mdText, setMdText] = useState('');
  const [width, setWidth] = useState(560);
  const bodyRef = useRef(null);

  const isPdf = view?.type === 'pdf';

  useEffect(() => { if (isPdf) setPage(view.page || 1); }, [view, isPdf]);

  useEffect(() => {
    if (view?.type === 'md') {
      setMdText('Đang tải…');
      fetch(docUrl(view.file))
        .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
        .then(setMdText)
        .catch(() => setMdText('> ⚠ Không tải được tài liệu: `' + view.file + '`'));
    }
  }, [view]);

  useEffect(() => {
    const el = bodyRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setWidth(Math.min((el.clientWidth || 560) - 36, 760)));
    ro.observe(el);
    return () => ro.disconnect();
  }, [view]);

  const quoteNorm = useMemo(() => norm(view?.quote), [view]);

  const textRenderer = useMemo(() => {
    if (!quoteNorm) return undefined;
    return (item) => {
      const t = norm(item.str);
      if (t.length >= 4 && quoteNorm.includes(t)) return `<mark class="cite-hl">${escapeHtml(item.str)}</mark>`;
      return escapeHtml(item.str);
    };
  }, [quoteNorm]);

  function onTextSuccess() {
    requestAnimationFrame(() => {
      bodyRef.current?.querySelector('mark.cite-hl')?.scrollIntoView({ block: 'center', behavior: 'smooth' });
    });
  }

  if (!view) return <aside className="viewer" aria-hidden="true" />;

  const meta = isPdf ? arxivMeta[view.arxiv] : null;
  const title = isPdf ? (meta ? meta.label : 'arXiv:' + view.arxiv) : (view.label || view.file);
  const sub = isPdf ? (meta ? meta.sub : '') : 'tài liệu nguồn (.md)';

  return (
    <aside className="viewer open">
      <div className="v-head">
        <div className="v-title"><div className="t">{title}</div><div className="s">{sub}</div></div>
        {isPdf && (
          <div className="v-pager">
            <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page <= 1}>‹</button>
            <span>{page}/{numPages || '…'}</span>
            <button onClick={() => setPage((p) => Math.min(numPages, p + 1))} disabled={page >= numPages}>›</button>
          </div>
        )}
        <button className="iconbtn" onClick={onClose} title="Đóng (Esc)">✕</button>
      </div>

      {isPdf && view.quote && (
        <div className="qbanner">
          <span className="lbl">Trích dẫn tô vàng · trang {view.page}</span>
          <q>{view.quote}</q>
        </div>
      )}

      <div className="v-body" ref={bodyRef}>
        {isPdf ? (
          <Document
            file={pdfUrl(arxivToFile[view.arxiv])}
            onLoadSuccess={({ numPages }) => setNumPages(numPages)}
            loading={<div className="pdf-loading">Đang tải PDF…</div>}
            error={<div className="pdf-error">Không tải được PDF.</div>}
          >
            <div className="pdf-stage">
              <div className="pdf-page">
                <Page
                  pageNumber={page}
                  width={width}
                  customTextRenderer={textRenderer}
                  onRenderTextLayerSuccess={onTextSuccess}
                  renderAnnotationLayer={false}
                />
              </div>
            </div>
          </Document>
        ) : (
          <div className="md"><ReactMarkdown remarkPlugins={[remarkGfm]}>{mdText}</ReactMarkdown></div>
        )}
      </div>
    </aside>
  );
}
