import { useMemo, useState } from 'react';
import { slideGroups, citationsByPaper, files } from '../data';

const docFile = (path) => path.replace(/^docs\//, '');

export default function Sidebar({ idx, onGoto, onOpen }) {
  const [q, setQ] = useState('');
  const [open, setOpen] = useState({ slides: true, papers: true, slr: false, exp: false, cites: false });
  const groups = useMemo(() => slideGroups(), []);
  const citeGroups = useMemo(() => citationsByPaper(), []);
  const toggle = (k) => setOpen((o) => ({ ...o, [k]: !o[k] }));

  const query = q.trim().toLowerCase();
  const match = (s) => s.toLowerCase().includes(query);

  // flat search results across everything
  const results = useMemo(() => {
    if (!query) return null;
    const r = [];
    groups.forEach((g) => g.items.forEach((s) => { if (match(s.title)) r.push({ tag: 'slide', label: `${s.n}. ${s.title}`, act: () => onGoto(s.n - 1) }); }));
    files.papers.forEach((p) => { if (match(p.label) || match(p.sub)) r.push({ tag: 'pdf', label: p.label, sub: `arXiv:${p.arxiv}`, act: () => onOpen({ type: 'pdf', arxiv: p.arxiv, page: 1 }) }); });
    [...files.slr, ...files.experiment].forEach((d) => { if (match(d.label)) r.push({ tag: 'doc', label: d.label, act: () => onOpen({ type: 'md', file: docFile(d.path), label: d.label }) }); });
    citeGroups.forEach((cg) => cg.items.forEach((c) => { if (match(c.claim) || match(c.quote) || match(c.short)) r.push({ tag: 'cite', label: `#${c.idx} ${c.short} · p.${c.page}`, sub: c.claim.slice(0, 48), act: () => onOpen({ type: 'pdf', arxiv: c.arxiv, page: c.page, quote: c.quote }) }); }));
    return r.slice(0, 60);
  }, [query]);

  return (
    <nav className="sidebar" aria-label="Chỉ mục">
      <div className="sb-search">
        <input placeholder="Tìm slide, paper, trích dẫn…" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>
      <div className="sb-scroll">
        {results ? (
          <div className="sb-items">
            <div className="sb-sec"><button className="sb-h">{results.length} kết quả</button></div>
            {results.map((r, i) => (
              <button key={i} className="sb-item" onClick={r.act}>
                <span className="ptag" style={{ fontFamily: 'var(--mono)', fontSize: 10, border: '1px solid var(--line)', borderRadius: 5, padding: '1px 5px' }}>{r.tag}</span>
                <span>{r.label}{r.sub && <span className="sub">{r.sub}</span>}</span>
              </button>
            ))}
          </div>
        ) : (
          <>
            {/* SLIDES */}
            <Section id="slides" title="Slides" open={open.slides} onToggle={toggle}>
              {groups.map((g, gi) => (
                <div key={gi} style={{ marginBottom: 6 }}>
                  <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--teal)', padding: '4px 9px', textTransform: 'uppercase', letterSpacing: '.05em' }}>{g.label}</div>
                  {g.items.map((s) => (
                    <button key={s.id} className={`sb-item ${s.n - 1 === idx ? 'active' : ''}`} onClick={() => onGoto(s.n - 1)}>
                      <span className="ic">{String(s.n).padStart(2, '0')}</span>
                      <span>{s.title}</span>
                    </button>
                  ))}
                </div>
              ))}
            </Section>

            {/* PAPERS */}
            <Section id="papers" title={`Papers (${files.papers.length})`} open={open.papers} onToggle={toggle}>
              {files.papers.map((p) => (
                <button key={p.arxiv} className="sb-item" onClick={() => onOpen({ type: 'pdf', arxiv: p.arxiv, page: 1 })}>
                  <span className="ic">📄</span>
                  <span>{p.label}<span className="sub">{p.sub}</span></span>
                </button>
              ))}
            </Section>

            {/* SLR docs */}
            <Section id="slr" title="SLR docs" open={open.slr} onToggle={toggle}>
              {files.slr.map((d) => (
                <button key={d.path} className="sb-item" onClick={() => onOpen({ type: 'md', file: docFile(d.path), label: d.label })}>
                  <span className="ic">📝</span><span>{d.label}</span>
                </button>
              ))}
            </Section>

            {/* Experiment */}
            <Section id="exp" title="Experiment" open={open.exp} onToggle={toggle}>
              {files.experiment.map((d) => (
                <button key={d.path} className="sb-item" onClick={() => onOpen({ type: 'md', file: docFile(d.path), label: d.label })}>
                  <span className="ic">🧪</span><span>{d.label}</span>
                </button>
              ))}
            </Section>

            {/* Citation index */}
            <Section id="cites" title="Citation index (104)" open={open.cites} onToggle={toggle}>
              {citeGroups.map((cg) => (
                <div key={cg.idx} style={{ marginBottom: 4 }}>
                  <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--ink-3)', padding: '4px 9px' }}>#{cg.idx} {cg.short}</div>
                  {cg.items.map((c) => (
                    <button key={c.id} className="sb-item" onClick={() => onOpen({ type: 'pdf', arxiv: c.arxiv, page: c.page, quote: c.quote })} title={c.quote}>
                      <span className="ic">p.{c.page}</span>
                      <span style={{ fontSize: 12 }}>{c.claim.slice(0, 52)}{c.verified && <span className="vbadge"> ✓</span>}</span>
                    </button>
                  ))}
                </div>
              ))}
            </Section>
          </>
        )}
      </div>
    </nav>
  );
}

function Section({ id, title, open, onToggle, children }) {
  return (
    <div className={`sb-sec ${open ? '' : 'closed'}`}>
      <button className="sb-h" onClick={() => onToggle(id)}>{title}<span className="chev">▾</span></button>
      <div className="sb-items">{children}</div>
    </div>
  );
}
