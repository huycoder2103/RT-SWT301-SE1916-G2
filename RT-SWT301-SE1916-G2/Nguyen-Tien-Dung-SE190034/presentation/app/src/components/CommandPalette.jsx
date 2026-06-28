import { useEffect, useMemo, useRef, useState } from 'react';
import { slides, files, citationsByPaper } from '../data';

export default function CommandPalette({ onGoto, onOpen, onClose }) {
  const [q, setQ] = useState('');
  const [sel, setSel] = useState(0);
  const inputRef = useRef(null);
  useEffect(() => { inputRef.current?.focus(); }, []);

  const items = useMemo(() => {
    const all = [];
    slides.forEach((s, i) => all.push({ tag: 'slide', label: `${s.n}. ${s.title}`, act: () => onGoto(i) }));
    files.papers.forEach((p) => all.push({ tag: 'pdf', label: p.label, sub: `arXiv:${p.arxiv}`, act: () => onOpen({ type: 'pdf', arxiv: p.arxiv, page: 1 }) }));
    [...files.slr, ...files.experiment].forEach((d) => all.push({ tag: 'doc', label: d.label, act: () => onOpen({ type: 'md', file: d.path.replace(/^docs\//, ''), label: d.label }) }));
    citationsByPaper().forEach((cg) => cg.items.forEach((c) => all.push({ tag: 'cite', label: `#${c.idx} ${c.short} · p.${c.page}`, sub: c.claim.slice(0, 50), act: () => onOpen({ type: 'pdf', arxiv: c.arxiv, page: c.page, quote: c.quote }) })));
    return all;
  }, []);

  const filtered = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return items.slice(0, 40);
    return items.filter((it) => (it.label + ' ' + (it.sub || '')).toLowerCase().includes(t)).slice(0, 50);
  }, [q, items]);
  useEffect(() => setSel(0), [q]);

  function key(e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); setSel((s) => Math.min(filtered.length - 1, s + 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setSel((s) => Math.max(0, s - 1)); }
    else if (e.key === 'Enter') { const it = filtered[sel]; if (it) { it.act(); onClose(); } }
    else if (e.key === 'Escape') { onClose(); }
  }

  return (
    <div className="palette-wrap" onClick={onClose}>
      <div className="palette" onClick={(e) => e.stopPropagation()}>
        <input ref={inputRef} placeholder="Đi tới slide · mở paper · mở trích dẫn (tô vàng)…" value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={key} />
        <div className="p-list">
          {filtered.map((it, i) => (
            <div key={i} className={`p-item ${i === sel ? 'sel' : ''}`} onMouseEnter={() => setSel(i)} onClick={() => { it.act(); onClose(); }}>
              <span className="ptag">{it.tag}</span>
              <span>{it.label}</span>
              {it.sub && <span className="psub">{it.sub}</span>}
            </div>
          ))}
          {filtered.length === 0 && <div className="p-item">Không có kết quả</div>}
        </div>
        <div className="p-foot"><span>↑↓ chọn</span><span>↵ mở</span><span>esc đóng</span></div>
      </div>
    </div>
  );
}
