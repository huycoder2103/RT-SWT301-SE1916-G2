import slides from './slides.json';
import citations from './citations.json';
import files from './files.json';

export { slides, citations, files };

const BASE = import.meta.env.BASE_URL || './';
export const pdfUrl = (file) => `${BASE}papers/${file}`;
export const docUrl = (file) => `${BASE}docs/${file}`;

// arXiv id -> public pdf path
export const arxivToFile = Object.fromEntries(files.papers.map((p) => [p.arxiv, p.path.split('/').pop()]));
export const arxivMeta = Object.fromEntries(files.papers.map((p) => [p.arxiv, p]));

// group slides into parts using divider slides as boundaries (for the sidebar)
export function slideGroups() {
  const groups = [];
  let cur = { label: 'Mở đầu', items: [] };
  for (const s of slides) {
    if (/divider/.test(s.cls)) {
      if (cur.items.length) groups.push(cur);
      cur = { label: s.title.replace(/^Phần \d+ — /, ''), items: [] };
    }
    cur.items.push(s);
  }
  if (cur.items.length) groups.push(cur);
  return groups;
}

// citations grouped by paper index (for the citation-index section)
export function citationsByPaper() {
  const map = new Map();
  for (const c of citations) {
    if (!map.has(c.idx)) map.set(c.idx, { idx: c.idx, short: c.short, arxiv: c.arxiv, items: [] });
    map.get(c.idx).items.push(c);
  }
  return [...map.values()].sort((a, b) => a.idx - b.idx);
}
