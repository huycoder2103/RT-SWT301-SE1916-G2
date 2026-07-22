# FISAT 2026 format compliance

**Why this format:** the university requires the paper to follow EAI FISAT 2026 formatting
for the SWT301 RBL-5 deliverable. **The team is not submitting to the conference**, so
conference deadlines, the Confy+ system and page-overage charges do not apply. Only the
format rules below are graded.

**Format reference:** <https://daihoc.fpt.edu.vn/hcm/hoi-nghi-fisat/> ·
<https://fisat.eai-conferences.org/2026/>

---

## Format requirements vs. current state

| Requirement | Required | Current | |
|---|---|---|---|
| Template | Springer **LNCS** | `llncs.cls` v2.26 | ✅ ported from IEEEtran |
| Columns | single | single | ✅ |
| Length (full paper) | 12–15 pp excl. refs | **body = pp. 1–15** | ✅ at the ceiling |
| Abstract length | ≤150 words | 150 | ✅ was 266 |
| Headings | title case | title case | ✅ 15 re-cased |
| Disclosure of Interests | `credits` env, mandatory | `\begin{credits}` + `\discintname` | ✅ |
| Figure resolution | ≥800 dpi line art | 853 / 1387 dpi | ✅ regenerated at DPI 400 |
| Self-contained sources | all files under `paper/` | figures copied in | ✅ |
| Language | English only | English | ✅ |
| Review model | **single-blind** | author names shown | ✅ do **not** anonymise |
| AI-use disclosure | required by Springer | `sections/08_declarations.tex` | ⚠️ **verify wording** |
| Bibliography style | `splncs04` | `splncs04` | ✅ |
| Build | — | 18 pp, 0 errors, 0 overfull | ✅ |
| Author name order | given name then family name | family-name-first | ⚠️ **decide — see below** |

Page budget of the built PDF: body (Introduction → Conclusion) **pp. 1–15**, declarations
p. 16, references pp. 17–18. Only the first block counts against the 12–15 limit.

---

## Building the PDF

`llncs` is on CTAN under CC BY 4.0 and ships with both MiKTeX and TeX Live
(<https://ctan.org/pkg/llncs>), so `\documentclass{llncs}` resolves with no manual
template download. MiKTeX fetches the class and `splncs04.bst` on first use.

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Two `pdflatex` passes after `bibtex` are required so that citations and cross-references
settle.

---

## Checklist

Already done and verified:

- [x] MiKTeX installed; `llncs.cls` and `splncs04.bst` auto-fetched from CTAN
- [x] `python scripts/check_paper.py` → PASS
- [x] Build clean: 0 errors, 0 undefined references, 0 overfull hboxes
- [x] Page budget within limit (body pp. 1–15)

Left for the team:

- [ ] **Read `quality/integrity_audit_2026-07-21.md`** — five substantive claim problems were
      found and fixed; three items remain open for you, including reporting the manual arm's
      coverage (94.3%, in the data, currently unreported)
- [ ] **Decide the author name order.** LNCS wants given name(s) then family name, and
      shortens given names to initials in the running head. The names are currently written
      family-first ("Nguyen Hoang Huy"), while `\authorrunning{N. H. Huy et al.}` treats
      *Huy* as the family name. Pick one:
      **(a)** Western order — `\author{Hoang Huy Nguyen \and ...}`, running head
      `H. H. Nguyen et al.`; or
      **(b)** keep family-first — brace it, `\author{{Nguyen} Hoang Huy \and ...}`, and set
      the running head to `H. H. Nguyen et al.` to match
- [ ] **Verify every sentence of `sections/08_declarations.tex`** against what the team
      actually did. It states on your behalf how AI was used; an inaccurate disclosure is
      worse than none
- [ ] Optionally add `\orcidID{...}` per author (LNCS encourages, does not require)
- [ ] Optionally add `pages` / `publisher` to the `@inproceedings` entries in
      `references.bib` — splncs04 drops them silently when absent
- [ ] **Verify author e-mail addresses in `main.tex`** — currently constructed from the
      student IDs and unverified
- [ ] **Each author reads the full manuscript aloud and revises in their own voice**
      (see `quality/ai_check_log.md` §4). This is the step that actually addresses the
      AI-detection finding; the rewrite only removed the stylistic markers
- [ ] Open the PDF and check both figures are legible at LNCS width
- [ ] Re-run `python scripts/gen_paper_macros.py` if the experiment is ever re-run

Rebuild after any edit:

```bash
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```
