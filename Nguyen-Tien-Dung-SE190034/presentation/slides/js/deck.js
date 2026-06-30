/* SLR deck engine — vanilla, offline. Keyboard-first, fragment reveal,
   speaker notes, overview grid, theme toggle, responsive scale, print/PDF. */
(() => {
  const stage = document.getElementById('stage');
  const slides = [...document.querySelectorAll('.slide')];
  const progress = document.getElementById('progress');
  const counter = document.getElementById('counter');
  const ftitle = document.querySelector('#chrome .ftitle');
  const notes = document.getElementById('notes');
  const notesTxt = notes.querySelector('.ntxt');
  const overview = document.getElementById('overview');
  const help = document.getElementById('help');

  let cur = 0;      // current slide index
  let frag = 0;     // current fragment step on this slide

  // ---- responsive scale: fit 1280x720 into viewport ----------------------
  function fit() {
    const sx = window.innerWidth / 1280;
    const sy = (window.innerHeight - 30) / 720; // leave room for chrome
    const s = Math.min(sx, sy);
    slides.forEach(sl => { sl.style.transform = `scale(${s})`; });
  }
  window.addEventListener('resize', fit);

  // ---- fragments ---------------------------------------------------------
  const fragsOf = i => [...slides[i].querySelectorAll('.frag')];
  function applyFrags() {
    fragsOf(cur).forEach((f, k) => f.classList.toggle('in', k < frag));
  }

  // ---- render ------------------------------------------------------------
  function render(enter = true) {
    slides.forEach((sl, i) => {
      sl.classList.toggle('active', i === cur);
      if (i === cur && enter) { sl.classList.remove('enter'); void sl.offsetWidth; sl.classList.add('enter'); }
    });
    applyFrags();
    const pct = ((cur) / (slides.length - 1)) * 100;
    progress.style.width = pct + '%';
    counter.textContent = String(cur + 1).padStart(2, '0') + ' / ' + slides.length;
    const t = slides[cur].dataset.title || slides[cur].querySelector('.title,h1')?.textContent || '';
    ftitle.textContent = t;
    const sn = slides[cur].querySelector('.snote');
    notesTxt.innerHTML = sn ? sn.innerHTML
      : '<p class="muted">— (chưa có speaker note cho slide này)</p>';
    location.hash = 'slide-' + (cur + 1);
    if (overview.classList.contains('show')) markOverview();
  }

  // ---- navigation --------------------------------------------------------
  function next() {
    const fs = fragsOf(cur);
    if (frag < fs.length) { frag++; applyFrags(); return; }
    if (cur < slides.length - 1) { cur++; frag = 0; render(); }
  }
  function prev() {
    if (frag > 0) { frag--; applyFrags(); return; }
    if (cur > 0) { cur--; frag = fragsOf(cur).length; render(); applyFrags(); }
  }
  function go(i, showLastFrag = false) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    frag = showLastFrag ? fragsOf(cur).length : 0;
    render();
  }

  // ---- overview grid -----------------------------------------------------
  function buildOverview() {
    let html = '';
    slides.forEach((sl, i) => {
      if (sl.classList.contains('divider')) {
        html += `<h3>${sl.querySelector('.title')?.textContent || ''}</h3>`;
      }
      const t = sl.dataset.title || sl.querySelector('.title,h1')?.textContent || ('Slide ' + (i + 1));
      html += `<div class="ov" data-i="${i}"><div class="ovn">${String(i + 1).padStart(2, '0')}</div><div class="ovt">${t}</div></div>`;
    });
    overview.innerHTML = html;
    overview.querySelectorAll('.ov').forEach(o =>
      o.addEventListener('click', () => { toggleOverview(false); go(+o.dataset.i); }));
  }
  function markOverview() {
    overview.querySelectorAll('.ov').forEach(o => o.classList.toggle('current', +o.dataset.i === cur));
  }
  function toggleOverview(force) {
    const show = force ?? !overview.classList.contains('show');
    overview.classList.toggle('show', show);
    if (show) markOverview();
  }

  // ---- toggles -----------------------------------------------------------
  const toggleNotes = () => notes.classList.toggle('show');
  const toggleHelp = f => help.classList.toggle('show', f);
  function toggleTheme() {
    const d = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', d ? 'light' : 'dark');
    try { localStorage.setItem('deck-theme', d ? 'light' : 'dark'); } catch (e) {}
  }
  function fullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  // ---- keyboard ----------------------------------------------------------
  let jumpBuf = '';
  window.addEventListener('keydown', e => {
    if (help.classList.contains('show') && e.key !== '?' && e.key !== 'Escape') { toggleHelp(false); }
    switch (e.key) {
      case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'PageUp': e.preventDefault(); prev(); break;
      case 'ArrowDown': e.preventDefault(); go(cur + 1); break;
      case 'ArrowUp': e.preventDefault(); go(cur - 1); break;
      case 'Home': go(0); break;
      case 'End': go(slides.length - 1); break;
      case 's': case 'S': toggleNotes(); break;
      case 'o': case 'O': toggleOverview(); break;
      case 't': case 'T': toggleTheme(); break;
      case 'f': case 'F': fullscreen(); break;
      case '?': toggleHelp(); break;
      case 'Escape': if (overview.classList.contains('show')) toggleOverview(false); else toggleHelp(false); break;
      default:
        if (/[0-9]/.test(e.key)) { jumpBuf += e.key; }
        else if (e.key === 'Enter' && jumpBuf) { go(+jumpBuf - 1); jumpBuf = ''; }
    }
  });

  // click zones (left third = back, rest = forward) — but ignore on interactive
  stage.addEventListener('click', e => {
    if (e.target.closest('a,button,.ov,table')) return;
    (e.clientX < window.innerWidth * 0.28) ? prev() : next();
  });

  // swipe
  let tx = 0;
  stage.addEventListener('touchstart', e => tx = e.changedTouches[0].clientX, { passive: true });
  stage.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) (dx < 0 ? next() : prev());
  }, { passive: true });

  // ---- controls buttons --------------------------------------------------
  document.getElementById('c-prev')?.addEventListener('click', prev);
  document.getElementById('c-next')?.addEventListener('click', next);
  document.getElementById('c-notes')?.addEventListener('click', toggleNotes);
  document.getElementById('c-grid')?.addEventListener('click', () => toggleOverview());
  document.getElementById('c-theme')?.addEventListener('click', toggleTheme);
  document.getElementById('c-help')?.addEventListener('click', () => toggleHelp());

  // ---- init --------------------------------------------------------------
  try { const th = localStorage.getItem('deck-theme'); if (th) document.documentElement.setAttribute('data-theme', th); } catch (e) {}
  buildOverview();
  fit();
  const m = location.hash.match(/slide-(\d+)/);
  cur = m ? Math.min(slides.length - 1, Math.max(0, +m[1] - 1)) : 0;
  render(false);

  // deep-link: respond to hash changes (and guard the render()-driven self-update)
  window.addEventListener('hashchange', () => {
    const mm = location.hash.match(/slide-(\d+)/);
    if (!mm) return;
    const target = Math.min(slides.length - 1, Math.max(0, +mm[1] - 1));
    if (target !== cur) go(target);
  });

  // minimal control surface (deep-linking / tooling); not used by the UI
  window.__deck = { go, next, prev, count: slides.length, revealAll: () => { frag = fragsOf(cur).length; applyFrags(); } };
})();
