# Quality Assessment (QA) — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Why this exists:** Beyond the IC/EC screening, a Kitchenham-style **quality assessment** scores each of the 13 included studies so that the evidence table is not just *relevant* but *trustworthy*. This is the standard SLR step that lets a reviewer see *how strong* each piece of evidence is. Paper numbers (#1–#13) match `evidence-table.md`.

---

## QA criteria (each scored Yes = 1 · Partly = 0.5 · No = 0)

| Code | Question |
|------|----------|
| **QA1** | Are the research aims / objectives clearly stated? |
| **QA2** | Is the approach/technique described clearly enough to be reproducible? |
| **QA3** | Is the evaluation context (APIs / dataset / subjects) adequately described? |
| **QA4** | Are metrics defined and results reported with **concrete numbers**? |
| **QA5** | Is there a **baseline / comparison** (tool, model, or manual)? |
| **QA6** | Are limitations / threats to validity explicitly discussed? |

**Inclusion-quality threshold:** ≥ 3.0 / 6.0. All 13 included papers clear it (minimum observed = 5.0), confirming the included evidence is high quality.

---

## QA scores

| # | Paper (short) | Venue | QA1 | QA2 | QA3 | QA4 | QA5 | QA6 | **Total /6** |
|---|---------------|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | RESTGPT | ICSE-NIER 2024 | 1 | 1 | 1 | 1 | 1 | 0.5 | **5.5** |
| 2 | KAT | ICST 2024 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 3 | RESTSpecIT (You Can REST Now) | arXiv 2024 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 4 | APITestGenie | AST 2026 | 1 | 1 | 1 | 1 | 0.5 | 1 | **5.5** |
| 5 | RestTSLLM | SBES 2025 | 1 | 1 | 1 | 0.5 | 1 | 0.5 | **5.0** |
| 6 | AutoRestTest | ICSE 2025 | 1 | 1 | 1 | 1 | 1 | 0.5 | **5.5** |
| 7 | LlamaRestTest | FSE 2025 | 1 | 1 | 1 | 1 | 1 | 0.5 | **5.5** |
| 8 | LogiAgent | arXiv 2025 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 9 | RESTifAI | ICSE 2026 Demo | 1 | 1 | 1 | 1 | 1 | 0.5 | **5.5** |
| 10 | EvoMaster | ACM TOSEM 2019 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 11 | No Time to Rest Yet | ISSTA 2022 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 12 | Morest | ICSE 2022 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 13 | DeepREST | ASE 2024 | 1 | 1 | 1 | 1 | 1 | 0.5 | **5.5** |

**Mean = 5.73 / 6 · Min = 5.0 · Max = 6.0 · all ≥ 3.0 threshold.**

---

## Notes on the deductions (honest, not inflated)

- **QA4 = 0.5 for #5 (RestTSLLM):** the comparative claim (Claude 3.5 Sonnet best of 7 LLMs) is confirmed by the abstract, but the exact figures (≈71.7% branch, ≈40.8% mutation) could not be re-verified from the primary PDF (only a secondary index) — see the † note in `evidence-table.md`. Scored half until the camera-ready is checked.
- **QA5 = 0.5 for #4 (APITestGenie):** it situates itself against EvoMaster / RESTGPT / RESTSpecIT but runs **no head-to-head quantitative baseline**, so the comparison is qualitative.
- **QA6 = 0.5 (#1, #6, #7, #9, #13):** these report results thoroughly but either are short/demo-format (#1 NIER, #9 demo) or their threats-to-validity section was not fully extractable from the accessed source; scored conservatively rather than assumed.
- **Venue-strength caveat (not a QA criterion but recorded for transparency):** #3, #8 are arXiv preprints (peer-review status not confirmed); #9 is a demonstration paper; #4's published form is AST 2026 (the 2024 preprint was assessed). They are retained because they meet IC1–IC5 and carry concrete empirical metrics, but a reader should weight the peer-reviewed venues (#1, #2, #6, #7, #10, #11, #12, #13 + #5 at SBES) most heavily.

---

## What QA adds to the gap argument

The QA confirms the gap is **not** an artifact of weak studies: the papers that *fail to compare against manual tests* (every LLM paper #1–#9) and that *count faults without ground truth* (#2,#6,#7,#8,#11,#13) are otherwise **high-quality (5.0–6.0/6)** work. So the missing **LLM-vs-manual-vs-EvoMaster on pre-seeded faults** comparison (see `gap-statement.md`) is a genuine design gap in strong literature, not a gap left only by low-quality papers.
