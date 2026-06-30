# Hypotheses Draft (Group) — LLM for REST API Test Generation

**Team:** SWT301_SU26_Group2
**Design:** 3 REST APIs from the EvoMaster Benchmark (EMB), deployed locally with **pre-seeded faulty versions** (known fault ground truth). Three generators compared: **LLM** (GPT-4o / GPT-4-Turbo from the OpenAPI spec), **Manual** test design, **EvoMaster**. Significance level **α = 0.05**. Thresholds are taken from the merged evidence (`evidence-table-merged.md`).

> The five members independently proposed Wilcoxon / Mann-Whitney / Binomial / Friedman tests; the group draft below reconciles them per RQ.

---

## RQ1 — Endpoint coverage of LLM-generated tests
**Metric:** endpoint coverage = endpoints exercised by ≥ 1 generated test / total endpoints in the OpenAPI spec, per API.

- **H0:** mean endpoint coverage of LLM-generated tests is **≤ 90%** (μ ≤ 0.90).
- **H1:** mean endpoint coverage of LLM-generated tests is **> 90%** (μ > 0.90).
- **Test:** one-sample **Wilcoxon signed-rank** vs the 0.90 threshold (per-API / per-endpoint), α = 0.05.
- **Interpretation:** p < 0.05 with median > 0.90 → reject H0. Report the **endpoint-type miss profile** (CRUD / auth / error-handling) descriptively.
- **Threshold source:** course-set ≥90%; merged evidence shows operation/endpoint coverage can reach ~95% (RESTifAI #10) while code coverage caps ~52–72% (#11, #9) — so the target is plausible but unverified on pre-seeded-fault EMB.

## RQ2 — Fault detection: LLM vs Manual vs EvoMaster
**Metric:** number of **pre-seeded faults** detected per API (ground truth known → Recall = detected / seeded).

- **H0:** LLM detects **no more** pre-seeded faults than the better of {Manual, EvoMaster} (rate_LLM ≤ max(rate_Manual, rate_EvoMaster)).
- **H1:** LLM detects **more** pre-seeded faults than {Manual, EvoMaster}.
- **Test:** **Friedman** omnibus (3 related generators on the same APIs/faults) → **post-hoc pairwise Wilcoxon signed-rank** (LLM vs Manual, LLM vs EvoMaster) with Holm correction. With only 3 APIs, also report a **per-fault McNemar / exact binomial** on the seeded-fault set + effect sizes (n = 3 limits omnibus power).
- **Interpretation:** Friedman p < 0.05 and post-hoc LLM > comparators p < 0.05 → reject H0. First study to put LLM vs manual vs EvoMaster on one pre-seeded-fault set (closes GAP-C + GAP-D).
- **Threshold source:** merged evidence reports only live-API 500-error *counts* (#3,#7,#9,#11,#16,#17) — Recall never computed.

## RQ3 — Edge-case / error-code scenarios: LLM vs Manual
**Metric:** edge-case scenario count per endpoint = distinct **4xx/5xx + boundary** scenarios per endpoint (invalid type, missing required field, out-of-range, malformed auth).

- **H0:** LLM produces **no more** edge-case scenarios per endpoint than manual (median_LLM ≤ median_Manual).
- **H1:** LLM produces **more** edge-case scenarios per endpoint than manual.
- **Test:** paired **Wilcoxon signed-rank** across endpoints (each endpoint → LLM count vs Manual count), α = 0.05.
- **Interpretation:** p < 0.05 with median difference favouring LLM → reject H0; report 4xx-vs-5xx-vs-boundary breakdown.
- **Threshold source:** no merged paper measures a per-endpoint edge-case count (only KAT #1 splits 2xx/4xx; RESTSpecIT #2 reports 5xx) — confirms GAP-M.

---

## Summary table

| RQ | Metric | H0 | H1 | Test | α |
|----|--------|----|----|------|---|
| RQ1 | Endpoint coverage (%) | μ ≤ 90% | μ > 90% | One-sample Wilcoxon signed-rank | 0.05 |
| RQ2 | Pre-seeded faults (LLM vs Manual vs EvoMaster) | rate_LLM ≤ max(others) | rate_LLM > others | Friedman + post-hoc Wilcoxon (Holm); McNemar per fault | 0.05 |
| RQ3 | Edge-case scenarios / endpoint (LLM vs Manual) | median_LLM ≤ median_Manual | median_LLM > median_Manual | Paired Wilcoxon signed-rank | 0.05 |

**Multiple-testing control:** Holm (RQ2 post-hoc) and Bonferroni across the 3 RQ families (α_adj ≈ 0.017) as proposed by NGUYEN; always report effect size (Cliff's δ / rank-biserial).

**Member convergence:** RQ1 one-sample Wilcoxon (DUNG, HUY, THUAN); RQ2 group comparison via Friedman/Mann-Whitney (DUNG, DAT, HUY, NGUYEN); RQ3 paired Wilcoxon (DUNG). Binomial exact for any binary valid-rate sub-metric (THUAN, NGUYEN).
