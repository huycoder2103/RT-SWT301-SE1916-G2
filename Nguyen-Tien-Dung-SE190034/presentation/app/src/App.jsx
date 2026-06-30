import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { slides } from './data';
import Slide from './components/Slide.jsx';
import Sidebar from './components/Sidebar.jsx';
import Viewer from './components/Viewer.jsx';
import Overview from './components/Overview.jsx';
import CommandPalette from './components/CommandPalette.jsx';

const fragCounts = slides.map((s) => (s.body.match(/class="[^"]*\bfrag\b[^"]*"/g) || []).length);

export default function App() {
  const [idx, setIdx] = useState(() => {
    const m = location.hash.match(/slide-(\d+)/);
    return m ? Math.min(slides.length - 1, Math.max(0, +m[1] - 1)) : 0;
  });
  const [frag, setFrag] = useState(0);
  const [view, setView] = useState(null);
  const [scale, setScale] = useState(1);
  const [sidebar, setSidebar] = useState(true);
  const [notes, setNotes] = useState(false);
  const [overview, setOverview] = useState(false);
  const [palette, setPalette] = useState(false);
  const [theme, setTheme] = useState(() => document.documentElement.getAttribute('data-theme') || 'light');
  const stageRef = useRef(null);

  const slide = slides[idx];

  // ---- scale to fit ----
  useLayoutEffect(() => {
    const el = stageRef.current;
    if (!el) return;
    const fit = () => {
      const w = el.clientWidth, h = el.clientHeight;
      setScale(Math.min((w - 36) / 1280, (h - 56) / 720));
    };
    fit();
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // ---- hash sync ----
  useEffect(() => { history.replaceState(null, '', '#slide-' + (idx + 1)); }, [idx]);

  // ---- navigation ----
  const goto = useCallback((i, lastFrag = false) => {
    const n = Math.max(0, Math.min(slides.length - 1, i));
    setIdx(n);
    setFrag(lastFrag ? fragCounts[n] : 0);
  }, []);
  const next = useCallback(() => {
    setFrag((f) => {
      if (f < fragCounts[idx]) return f + 1;
      if (idx < slides.length - 1) { setIdx(idx + 1); return 0; }
      return f;
    });
  }, [idx]);
  const prev = useCallback(() => {
    setFrag((f) => {
      if (f > 0) return f - 1;
      if (idx > 0) { setIdx(idx - 1); return fragCounts[idx - 1]; }
      return f;
    });
  }, [idx]);

  const openView = useCallback((v) => setView(v), []);
  const toggleTheme = useCallback(() => {
    setTheme((t) => {
      const nt = t === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nt);
      try { localStorage.setItem('deck-theme', nt); } catch (e) {}
      return nt;
    });
  }, []);

  // ---- keyboard ----
  useEffect(() => {
    const onKey = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if (e.key === 'Escape') e.target.blur();
        return;
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); setPalette((p) => !p); return; }
      switch (e.key) {
        case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next(); break;
        case 'ArrowLeft': case 'PageUp': e.preventDefault(); prev(); break;
        case 'ArrowDown': e.preventDefault(); goto(idx + 1); break;
        case 'ArrowUp': e.preventDefault(); goto(idx - 1); break;
        case 'Home': goto(0); break;
        case 'End': goto(slides.length - 1); break;
        case 's': case 'S': setNotes((n) => !n); break;
        case 'o': case 'O': setOverview((o) => !o); break;
        case 'b': case 'B': setSidebar((s) => !s); break;
        case 't': case 'T': toggleTheme(); break;
        case 'f': case 'F': document.fullscreenElement ? document.exitFullscreen?.() : document.documentElement.requestFullscreen?.(); break;
        case 'Escape':
          if (view) setView(null); else if (overview) setOverview(false); else if (palette) setPalette(false);
          break;
        default: break;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [idx, next, prev, goto, toggleTheme, view, overview, palette]);

  const progress = (idx / (slides.length - 1)) * 100;

  return (
    <div className="app">
      <div className="progress" style={{ width: progress + '%' }} />

      <header className="topbar">
        <button className="iconbtn" onClick={() => setSidebar((s) => !s)} title="Chỉ mục (B)">☰</button>
        <div className="brand"><span className="dot" />SLR · LLM × REST API Testing</div>
        <div className="ttitle">{slide.title}</div>
        <div className="counter">{String(idx + 1).padStart(2, '0')} / {slides.length}</div>
        <div className="tools">
          <button className="iconbtn" onClick={() => setPalette(true)} title="Tìm nhanh (Ctrl/Cmd+K)">⌕</button>
          <button className={`iconbtn ${overview ? 'on' : ''}`} onClick={() => setOverview((o) => !o)} title="Tổng quan (O)">▦</button>
          <button className={`iconbtn ${notes ? 'on' : ''}`} onClick={() => setNotes((n) => !n)} title="Speaker notes (S)">≡</button>
          <button className={`iconbtn ${theme === 'dark' ? 'on' : ''}`} onClick={toggleTheme} title="Sáng/Tối (T)">◐</button>
        </div>
      </header>

      <div className="main">
        {sidebar && <Sidebar idx={idx} onGoto={(i) => goto(i)} onOpen={openView} />}

        <div className="stage-wrap">
          <div className="stage" ref={stageRef}>
            <Slide key={slide.id} slide={slide} scale={scale} frag={frag} onOpen={openView} />
            <div className="stage-nav">
              <button onClick={prev} title="Lùi (←)">‹</button>
              <span className="pos">{idx + 1} · {slides.length}</span>
              <button onClick={next} title="Tiếp (→)">›</button>
            </div>
          </div>

          {notes && (
            <div className="notes">
              <h4>Speaker notes — slide {idx + 1}</h4>
              <div className="ntxt" dangerouslySetInnerHTML={{ __html: slide.notes || '<p class="muted">—</p>' }} />
            </div>
          )}
        </div>

        <Viewer view={view} onClose={() => setView(null)} />
      </div>

      {overview && <Overview idx={idx} onGoto={(i) => goto(i)} onClose={() => setOverview(false)} />}
      {palette && <CommandPalette onGoto={(i) => goto(i)} onOpen={openView} onClose={() => setPalette(false)} />}
    </div>
  );
}
