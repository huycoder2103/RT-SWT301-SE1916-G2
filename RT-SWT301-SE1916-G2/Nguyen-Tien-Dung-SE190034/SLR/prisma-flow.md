# PRISMA Flow Diagram — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Search date:** 2026-05-27 · **Sources:** `01_all_records.csv` → `02_after_screening_v1.csv` → `03_final_included.csv` → `evidence-table.md`

---

## Stage counts

| Stage | Label | N | Notes |
|-------|-------|---|-------|
| Identification | Google Scholar raw hits — String 1 (≈197) + String 2 (≈83); arXiv API cross-check 26 | **≈ 280** | GS estimated totals, 2026-06-04; reproducible queries in `search-log.md` §3 |
| Compilation + de-dup | Directly-relevant records, de-duplicated by title/DOI | **30** | = `01_all_records.csv` (≥30 checkpoint met); String 1 → 20, String 2 → 10 |
| Screening V1 | Title + abstract screened | 30 | All 30 decided in `02_after_screening_v1.csv` |
| Screening V1 | Excluded at title + abstract | 7 | EC4 = 4, EC5 = 3 |
| Screening V1 | Carried to full-text (INCLUDE + Unsure) | 23 | 22 INCLUDE + 1 Unsure |
| Screening V2 | Full-text assessed | 23 | Decisions in `03_final_included.csv` |
| Screening V2 | Excluded after full-text | 10 | EC1 = 7, IC5 = 1, EC4 = 1, EC3 = 1 |
| Included | Included in the evidence table | **13** | Final set for `evidence-table.md` |

---

## ASCII flow

```
                 IDENTIFICATION
[ Records identified from database searching (N ~= 280) ]
   Google Scholar: String 1 ~= 197  +  String 2 ~= 83   (estimated totals, 2026-06-04)
   arXiv API cross-check: 26 preprints
                        |
                        v
[ Directly-relevant records compiled & de-duplicated by title/DOI (N = 30) ]
   ( = 01_all_records.csv: 20 LLM studies + 10 baselines; ~250 off-topic long-tail not retained )
                        |
                        v
================= SCREENING (Title + Abstract) =================
[ Screened (N = 30) ]
   |--- Excluded (N = 7):
   |        EC4 (out of domain: reverse direction / spec generation) = 4   [#16,#18,#19,#20]
   |        EC5 (out of phase: test amplification / naming)          = 3   [#6,#7,#17]
                        |
                        v
[ Passed to full-text (N = 23) = 22 INCLUDE + 1 Unsure ]
                        |
                        v
==================== ELIGIBILITY (Full-text) ===================
[ Full-text assessed (N = 23) ]
   |--- Excluded (N = 10):
   |        EC1 (duplicate / superseded / retained only as comparator) = 7  [#13,#23,#24,#25,#27,#28,#29]
   |        IC5 (no coverage/fault metrics; redundant)                 = 1  [#5]
   |        EC4 (narrowed to security testing)                         = 1  [#8]
   |        EC3 (short workshop paper)                                 = 1  [#9]
                        |
                        v
                    INCLUDED
[ Included in evidence table (N = 13) ]
   9 LLM-based studies + 4 classic baselines/empirical references
```

---

## Reconciliation check

- 30 screened = 7 excluded + 23 carried forward ✓
- 23 full-text = 10 excluded + 13 included ✓
- 13 included = 9 LLM-based (#1–#9 in evidence table) + 4 baselines (#10–#13) ✓
- Final 13 within the recommended 5–15 range (checkpoint 1.4) ✓
