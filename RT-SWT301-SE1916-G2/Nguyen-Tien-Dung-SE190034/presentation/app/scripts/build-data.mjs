// Generates src/data/{slides,citations,files}.json from the existing vanilla deck
// (presentation/slides/index.html) + presentation/citations-raw.json.
// Re-uses 100% of the authored slide content and the 104 verified citations,
// turning citation chips + evidence quotes into clickable triggers.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const APP = join(__dirname, '..');
const PRES = join(APP, '..');
const OUT = join(APP, 'src', 'data');
if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

// paper index (1..13) -> { short, file, arxiv }
const PAPERS = [
  { idx: 1, short: 'RESTGPT', file: '01_RESTGPT_2312.00894.pdf', arxiv: '2312.00894', venue: 'ICSE-NIER 2024' },
  { idx: 2, short: 'KAT', file: '02_KAT_2407.10227.pdf', arxiv: '2407.10227', venue: 'ICST 2024' },
  { idx: 3, short: 'RESTSpecIT', file: '03_RESTSpecIT_2402.05102.pdf', arxiv: '2402.05102', venue: 'arXiv 2024' },
  { idx: 4, short: 'APITestGenie', file: '04_APITestGenie_2409.03838.pdf', arxiv: '2409.03838', venue: 'AST 2026' },
  { idx: 5, short: 'RestTSLLM', file: '05_RestTSLLM_2509.05540.pdf', arxiv: '2509.05540', venue: 'SBES 2025' },
  { idx: 6, short: 'AutoRestTest', file: '06_AutoRestTest_2411.07098.pdf', arxiv: '2411.07098', venue: 'ICSE 2025' },
  { idx: 7, short: 'LlamaRestTest', file: '07_LlamaRestTest_2501.08598.pdf', arxiv: '2501.08598', venue: 'FSE 2025' },
  { idx: 8, short: 'LogiAgent', file: '08_LogiAgent_2503.15079.pdf', arxiv: '2503.15079', venue: 'arXiv 2025' },
  { idx: 9, short: 'RESTifAI', file: '09_RESTifAI_2512.08706.pdf', arxiv: '2512.08706', venue: 'ICSE 2026 Demo' },
  { idx: 10, short: 'EvoMaster', file: '10_EvoMaster_1901.01538.pdf', arxiv: '1901.01538', venue: 'ACM TOSEM 2019' },
  { idx: 11, short: 'NoTimeToRest', file: '11_NoTimeToRest_2204.08348.pdf', arxiv: '2204.08348', venue: 'ISSTA 2022' },
  { idx: 12, short: 'Morest', file: '12_Morest_2204.12148.pdf', arxiv: '2204.12148', venue: 'ICSE 2022' },
  { idx: 13, short: 'DeepREST', file: '13_DeepREST_2408.08594.pdf', arxiv: '2408.08594', venue: 'ASE 2024' },
];
const byShort = Object.fromEntries(PAPERS.map(p => [p.short, p]));
const byArxiv = Object.fromEntries(PAPERS.map(p => [p.arxiv, p]));

// ---------- citations ----------
const raw = JSON.parse(readFileSync(join(PRES, 'citations-raw.json'), 'utf8'));
const citations = [];
for (const paper of raw.result.papers) {
  const meta = byShort[paper.paper_short];
  if (!meta) { console.warn('no meta for', paper.paper_short); continue; }
  paper.citations.forEach((c, i) => {
    citations.push({
      id: `c-${String(meta.idx).padStart(2, '0')}-${c.page}-${i}`,
      idx: meta.idx, short: meta.short, file: meta.file, arxiv: meta.arxiv, venue: meta.venue,
      page: c.page, quote: c.quote, location: c.location || '', why: c.why || '',
      claim: c.claim || '', verified: !!c.verified, present: c.present !== false,
    });
  });
}
writeFileSync(join(OUT, 'citations.json'), JSON.stringify(citations, null, 0));
console.log(`citations.json: ${citations.length} citations`);

// best citation for a (paperIdx, page) — for chips that only know paper+page
function bestCite(idx, page) {
  const pool = citations.filter(c => c.idx === idx);
  if (!pool.length) return null;
  const exact = pool.filter(c => c.page === page);
  return (exact[0] || pool[0]);
}

// ---------- slides ----------
const html = readFileSync(join(PRES, 'slides', 'index.html'), 'utf8');
const stripTags = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
const attrEsc = s => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// extract each <section class="slide ...">...</section>
const sectionRe = /<section class="(slide[^"]*)"\s+data-title="([^"]*)">([\s\S]*?)<\/section>/g;
const slides = [];
let m, n = 0;
while ((m = sectionRe.exec(html))) {
  n++;
  let cls = m[1].replace(/\bslide\b/, '').replace(/\bactive\b/, '').replace(/\benter\b/, '').trim();
  const title = m[2];
  let inner = m[3];

  // pull out the speaker note (.snote has no nested divs)
  let notes = '';
  inner = inner.replace(/<div class="snote">([\s\S]*?)<\/div>\s*$/, (mm, body) => { notes = body.trim(); return ''; });
  if (!notes) inner = inner.replace(/<div class="snote">([\s\S]*?)<\/div>/, (mm, body) => { notes = body.trim(); return ''; });

  let body = inner.trim();

  // --- transform EVIDENCE blocks into clickable PDF/MD triggers ---
  body = body.replace(/<div class="evidence([^"]*)"([^>]*)>([\s\S]*?)<\/div>/g, (full, extra, attrs, content) => {
    const qm = content.match(/<q>([\s\S]*?)<\/q>/);
    const sm = content.match(/<span class="src">([\s\S]*?)<\/span>/);
    const quote = qm ? stripTags(qm[1]) : '';
    const src = sm ? stripTags(sm[1]) : '';
    const ax = src.match(/(\d{4}\.\d{4,5})/);          // arXiv id
    const pg = src.match(/(?:trang|p\.)\s*(\d+)/i);
    const md = src.match(/([\w-]+\.md)/);
    let data = '';
    if (ax) {
      data = ` data-open="pdf" data-arxiv="${ax[1]}"${pg ? ` data-page="${pg[1]}"` : ''} data-quote="${attrEsc(quote)}"`;
    } else if (md) {
      data = ` data-open="md" data-file="${md[1]}"`;
    }
    const cls2 = `evidence${extra}${data ? ' clickable' : ''}`;
    const hint = data ? '<span class="evhint">↗ mở nguồn</span>' : '';
    return `<div class="${cls2}"${attrs}${data}>${content}${hint}</div>`;
  });

  const chipData = (idx, page) => {
    const c = bestCite(idx, page || -1);
    return ` data-open="pdf" data-arxiv="${c ? c.arxiv : ''}"${page ? ` data-page="${page}"` : (c ? ` data-page="${c.page}"` : '')}${c ? ` data-quote="${attrEsc(c.quote)}"` : ''} data-cite-idx="${idx}"`;
  };

  // --- transform CITE chips (pid + pg spans), preserving any extra attrs like style ---
  body = body.replace(/<span class="cite([^"]*)"([^>]*)>\s*<span class="pid">([\s\S]*?)<\/span>\s*<span class="pg">([\s\S]*?)<\/span>\s*<\/span>/g,
    (full, extra, attrs, pid, pg) => {
      const idx = (pid.match(/#?(\d+)/) || [])[1];
      const page = (pg.match(/p\.(\d+)/) || [])[1];
      if (!idx) return full;
      return `<button type="button" class="cite${extra}"${attrs}${chipData(+idx, page ? +page : null)}><span class="pid">${pid}</span><span class="pg">${pg}</span></button>`;
    });

  // --- fallback: chips with one pid span + loose trailing text (e.g. "#9 p.3") ---
  body = body.replace(/<span class="cite([^"]*)"([^>]*)>\s*<span class="pid">([\s\S]*?)<\/span>([^<]*)<\/span>/g,
    (full, extra, attrs, pid, tail) => {
      const idx = (pid.match(/#?(\d+)/) || [])[1];
      const page = (tail.match(/p\.(\d+)/) || [])[1];
      if (!idx) return full;
      return `<button type="button" class="cite${extra}"${attrs}${chipData(+idx, page ? +page : null)}><span class="pid">${pid}</span>${tail}</button>`;
    });

  slides.push({ n, id: `s${n}`, cls, title, body, notes });
}
writeFileSync(join(OUT, 'slides.json'), JSON.stringify(slides, null, 0));
console.log(`slides.json: ${slides.length} slides`);

// ---------- files index ----------
const files = {
  papers: PAPERS.map(p => ({ label: `#${p.idx} ${p.short}`, sub: `${p.venue} · arXiv:${p.arxiv}`, type: 'pdf', path: `papers/${p.file}`, arxiv: p.arxiv })),
  slr: [
    { label: 'Evidence Table (13 papers)', type: 'md', path: 'docs/evidence-table.md' },
    { label: 'Gap Statement', type: 'md', path: 'docs/gap-statement.md' },
    { label: 'PRISMA Flow', type: 'md', path: 'docs/prisma-flow.md' },
    { label: 'Inclusion/Exclusion Criteria', type: 'md', path: 'docs/ie_criteria.md' },
    { label: 'Quality Assessment', type: 'md', path: 'docs/quality-assessment.md' },
    { label: 'Search Log', type: 'md', path: 'docs/search-log.md' },
  ],
  experiment: [
    { label: 'Research Questions (PICO + RQ)', type: 'md', path: 'docs/01_rq.md' },
    { label: 'Hypotheses (H0/H1 + tests)', type: 'md', path: 'docs/hypotheses.md' },
  ],
};
writeFileSync(join(OUT, 'files.json'), JSON.stringify(files, null, 2));
console.log(`files.json: ${files.papers.length} papers + ${files.slr.length} SLR + ${files.experiment.length} experiment docs`);

// quick integrity log
const chips = (slides.map(s => s.body).join('').match(/class="cite/g) || []).length;
const clickableCites = (slides.map(s => s.body).join('').match(/data-open="pdf"[^>]*data-cite-idx/g) || []).length;
const evid = (slides.map(s => s.body).join('').match(/evidence[^"]*clickable/g) || []).length;
console.log(`interactive: ${clickableCites} clickable chips · ${evid} clickable evidence blocks`);
