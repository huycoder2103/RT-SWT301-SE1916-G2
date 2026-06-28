# Search Log — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Search date:** 2026-05-27
**Goal:** Build a focused, de-duplicated corpus of directly-relevant primary studies (plus classic non-LLM baselines required by IC4) to feed PRISMA screening and the evidence table.

---

## 1. Search strings (Query Strings)

The strings are derived from the PICO keywords (see `KeywordAndStringSelected.txt`). Boolean syntax: `AND` = both required, `OR` = either suffices, `"..."` = exact phrase.

### String 1 — LLM generates REST API tests (primary)
```
("REST API" OR "Web API" OR OpenAPI OR Swagger)
AND ("test generation" OR "test case generation" OR "automated testing")
AND (LLM OR "large language model" OR GPT OR ChatGPT)
```

### String 2 — OpenAPI / spec-based testing (supplementary)
```
("OpenAPI specification" OR Swagger OR "API specification")
AND ("test generation" OR "API testing")
AND (coverage OR executable OR "fault detection" OR "bug detection")
```

---

## 2. Databases queried

| # | Database | URL | Role |
|---|----------|-----|------|
| 1 | Google Scholar | https://scholar.google.com | Primary aggregator (broadest recall) |
| 2 | arXiv | https://arxiv.org/search/ | Preprints / cs.SE (most LLM-testing papers land here first) |
| 3 | IEEE Xplore | https://ieeexplore.ieee.org | ICST, ICSE, TSE |
| 4 | ACM Digital Library | https://dl.acm.org | ISSTA, FSE, ASE, ICSE, TOSEM |
| 5 | SpringerLink | https://link.springer.com | LNCS / conference proceedings |
| 6 | Semantic Scholar | https://www.semanticscholar.org | Cross-checking metadata & locating legal PDFs |

> **Filters:** language = English (IC1); year ≥ 2018 (IC2). Date searched: 2026-05-27.

---

## 3. Identification → consolidation funnel

The two strings were run across the databases above. Google Scholar (the broadest aggregator) reports its own estimated totals, which were recorded; the bulk of that long tail is off-topic (UI/unit/mobile testing, LLM-tool-use, spec generation, surveys). Directly-relevant records were retained and **de-duplicated by title + DOI**, yielding the 30-record corpus in `01_all_records.csv`.

| Stage | Count | Source / notes |
|-------|-------|----------------|
| Identification — Google Scholar, **String 1** | **≈ 197** | GS estimated total ("About ~197 results"); reproducible query Q1 below |
| Identification — Google Scholar, **String 2** | **≈ 83** | GS estimated total ("About ~83 results"); reproducible query Q2 below |
| Cross-check — arXiv API, String-1 core terms | 26 | `export.arxiv.org` `<opensearch:totalResults>`, 2026-06-04 (preprints only) |
| **Total raw identification (GS, both strings)** | **≈ 280** | Before relevance filtering + de-duplication |
| Directly-relevant records retained + de-duplicated by title/DOI | **30** | = `01_all_records.csv`; String 1 → 20 LLM studies, String 2 → 10 baselines; ≥ 30 checkpoint (1.2) met |

**Reproducible count queries** (run 2026-06-04 — Google Scholar totals are *estimates* and drift slowly over time):
- **Q1** (Google Scholar, String 1): `"REST API" "large language model" "test generation"` → ≈ 197 results.
- **Q2** (Google Scholar, String 2): `"OpenAPI specification" "test generation" "fault detection"` → ≈ 83 results.
- **Q3** (arXiv API cross-check): `http://export.arxiv.org/api/query?search_query=abs:"REST API" AND abs:"large language model" AND abs:"test"` → `totalResults = 26`.

Of the 30 unique records: **20 are direct LLM-based REST API test-generation studies** and **10 are classic non-LLM baseline / empirical-study references** (EvoMaster, RESTler, RestTestGen, Morest, QuickREST, DeepREST, etc.) deliberately retained under **IC4** because the research question compares LLMs against **manual** and **EvoMaster** baselines.

---

## 4. Notes on method (transparency)

- This is a **focused SLR** appropriate to the course scope: instead of carrying the full Google-Scholar long tail through screening, an explicit relevance + de-duplication pass was applied at consolidation, and the formal **IC/EC criteria are applied transparently in `02_after_screening_v1.csv` (title/abstract) and `03_final_included.csv` (full-text)**. Every exclusion records its IC/EC code so the funnel is auditable.
- **Raw-count reproducibility:** the Identification totals above are Google Scholar's own estimated result counts, recorded with the exact queries (Q1–Q2) and an independent arXiv API cross-check (Q3) so a reviewer can reproduce them. Google Scholar estimates drift slowly, so the figures are reported as approximate (≈). The large drop from ≈280 raw hits to 30 retained reflects the off-topic long tail (UI/unit/mobile testing, LLM-as-tool, spec-generation, surveys) removed by title-level relevance assessment + title/DOI de-duplication; the auditable **IC/EC screening (02 → 03)** then operates on the 30 compiled records.
- De-duplication was performed in Google Sheets, keyed on normalized title and DOI (lower-cased, trimmed), consistent with the `dedup_key` logic in the workbook template.
- All 30 records carry a resolvable `source_url` + `doi`, satisfying EC2 (legal full-text access) at the identification stage.
- The final included set (N = 13) and its exact metrics are verified against the primary sources (arXiv / publisher pages); see `evidence-table.md` for per-paper citations.

---

## 5. Summary

| String | GS raw hits (≈, 2026-06-04) | Unique relevant retained |
|--------|:---------------------------:|--------------------------|
| String 1 (LLM generates REST API tests) | ≈ 197 | 20 (records #1–#20) |
| String 2 (OpenAPI / spec-based testing — classic baselines) | ≈ 83 | 10 (records #21–#30) |
| **Total** | **≈ 280** | **30 (de-duplicated by title/DOI)** |
