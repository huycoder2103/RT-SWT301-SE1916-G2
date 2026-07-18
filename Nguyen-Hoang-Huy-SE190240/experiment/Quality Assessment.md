# Quality Assessment (QA) — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Hoang Huy — SE190240 (PL)
**Why this exists:** Beyond the IC/EC screening in `ie_criteria.md`, a Kitchenham-style **quality assessment** scores each of the 13 included studies so that the evidence table is not just *relevant* but *trustworthy*. This is the standard SLR step that lets a reviewer see *how strong* each piece of evidence is. Paper numbers (#1–#13) match `evidence-table.md` exactly.

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

**Inclusion-quality threshold:** ≥ 3.0 / 6.0. All 13 included papers clear it (minimum observed = 3.0, #6 — the one paywalled study), so the included evidence is retained but weighted by strength below.

---

## QA scores

| # | Paper (short) | Venue | QA1 | QA2 | QA3 | QA4 | QA5 | QA6 | **Total /6** |
|---|---------------|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | NLPtoREST (Kim et al.) | ISSTA 2023 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 2 | GPT + Katalon API scripts (Nguyen et al.) | SOICT 2023 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 3 | RESTGPT (Kim et al.) | ICSE-NIER 2024 | 1 | 1 | 1 | 1 | 1 | 0 | **5.0** |
| 4 | KAT (Le et al.) | ICST 2024 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 5 | DeepREST (Corradini et al.) | ASE 2024 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 6 | RESTless (Zheng et al.) | IEEE TSC 2024 | 1 | 0.5 | 0.5 | 0.5 | 0.5 | 0 | **3.0** |
| 7 | LlamaRestTest (Kim et al.) | FSE 2025 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 8 | AutoRestTest (Stennett, Kim et al.) | ICSE 2025 Demo | 1 | 1 | 1 | 1 | 1 | 0 | **5.0** |
| 9 | MioHint (Li et al.) | arXiv 2025 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 10 | MASTEST (Han & Zhu) | arXiv 2025 | 1 | 1 | 1 | 1 | 0.5 | 1 | **5.5** |
| 11 | LogiAgent (Zhang et al.) | arXiv 2025 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 12 | Black-box Test Gen in Practice (Corradini et al.) | ICST 2026 | 1 | 1 | 1 | 1 | 1 | 1 | **6.0** |
| 13 | APITestGenie (Pereira et al.) | AST 2026 | 1 | 1 | 1 | 1 | 0.5 | 1 | **5.5** |

**Mean = 5.54 / 6 · Min = 3.0 · Max = 6.0 · all ≥ 3.0 threshold.**

---

## Notes on the deductions (honest, not inflated)

- **QA6 = 0 for #3 (RESTGPT):** it is a 4-page ICSE **New Ideas** paper and, as recorded in `evidence-table.md`, has **no Threats-to-Validity / Limitations section**. Method and results are strong, but the missing ToV costs the full QA6.
- **QA6 = 0 for #8 (AutoRestTest):** a 4-page **tool-demo** paper with no Threats-to-Validity section (per the evidence table). Its comparative operation counts are concrete, but the demo format omits limitations.
- **#6 (RESTless) — the one weak-evidence study (3.0, exactly at threshold):** no full text was available (IEEE paywall). QA2/QA3/QA4/QA5 are scored **0.5** because the approach, dataset detail, the "38 vulnerabilities / 16 confirmed" figures, and the fuzzer baseline could **only be read from the abstract and metadata, not independently verified** (see the "No PDF" row in `evidence-table.md`); QA6 = 0 (no accessible ToV). It stays included because it meets IC1–IC5, but a reader should weight it least.
- **QA5 = 0.5 for #10 (MASTEST):** the evaluation is **model-vs-model** (GPT-4o vs DeepSeek V3.1) with no head-to-head baseline against an existing tool or manual suite, and no back-end code coverage was measured — so the comparison is internal only.
- **QA5 = 0.5 for #13 (APITestGenie):** it reports strong validity/success rates but runs **no head-to-head quantitative baseline** against another generator; the comparison to prior tools is qualitative.
- **Venue-strength caveat (not a QA criterion, recorded for transparency):** #9, #10, #11 are **arXiv preprints** (peer-review status not confirmed); #3 is a NIER short paper, #8 a demo, and #6 was assessed from abstract-only. They are retained because they meet IC1–IC5 and carry concrete empirical metrics, but the peer-reviewed venues should be weighted most heavily: **#1 (ISSTA), #2 (SOICT), #4 (ICST), #5 (ASE), #7 (FSE), #12 (ICST), #13 (AST)**.

---

## What QA adds to the gap argument

The QA confirms the gap is **not** an artifact of weak studies. The literature is strong (mean **5.54/6**, ten of thirteen at 5.5–6.0), yet across all 13 papers:

1. **No study compares LLM-generated tests against a manual (EP/BVA) baseline *and* against EvoMaster on the same pre-seeded ground-truth faults** — the exact three-arm design of this project (see `gap-statement.md`).
2. **Fault detection is counted without controlled ground truth** — most papers report "unique server errors" or "unknown defects found," not recall against a known injected-fault set.
3. **Claude (Anthropic) = 0 papers and Gemini (Google) = 0 papers** (see the LLM Distribution Summary in `evidence-table.md`) — the field is dominated by GPT-family and a few open models, so a Claude Sonnet 4.6 arm is genuinely unstudied.

Because these absences occur in otherwise **high-quality** work, the missing **LLM-vs-Manual-vs-EvoMaster on pre-seeded mutation faults** comparison is a real design gap in strong literature, not a gap left only by low-quality papers.