# Hypotheses — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Design:** On 3 REST APIs from the EvoMaster Benchmark (EMB), deployed locally with **pre-seeded faulty versions** (known fault ground truth). Three generators are compared: **LLM** (Claude Sonnet 4.6 from the OpenAPI spec), **Manual** test design, and **EvoMaster**. Significance level **α = 0.05** throughout.

> Each RQ maps to one H0/H1 pair. H0 is the negation of what we expect; H1 is the expected result.

---

## RQ1 — Endpoint coverage of LLM-generated tests

**Metric:** endpoint coverage = (endpoints exercised by ≥1 generated test) / (total endpoints in the OpenAPI spec), per API.

- **H0:** The mean endpoint coverage of LLM-generated tests is **≤ 90%** (μ_coverage ≤ 0.90).
- **H1:** The mean endpoint coverage of LLM-generated tests is **> 90%** (μ_coverage > 0.90).

**Statistical test:** one-sample **Wilcoxon signed-rank test** comparing per-API (and per-endpoint) coverage against the fixed threshold 0.90 (non-parametric, no normality assumption on a small sample).
**Interpretation:** if p < 0.05 and the median is above 0.90 → reject H0 (LLM meets the ≥90% target). Coverage is additionally **broken down by endpoint type (CRUD / authentication / error-handling)** to report *which* types are most frequently missed (descriptive, supports GAP-3).
**Rationale / source:** the ≥90% threshold is the course-set target in the initial RQ. Note it concerns **endpoint** coverage, not code coverage: operation/endpoint coverage already reaches ~95.5% in one tool (RESTifAI, `evidence-table.md` #9) and ~88.6% route discovery in another (#3), while *code* coverage stays at ~52–72% line (#8, #11). The target is therefore *plausible* but has never been verified for an LLM generator **on EMB APIs with pre-seeded faults**, nor reported with a per-endpoint-type breakdown — which is what RQ1 measures.

---

## RQ2 — Fault detection: LLM vs Manual vs EvoMaster

**Metric:** fault-detection count = number of **pre-seeded faults** detected per API (ground truth known → also expressible as Recall = detected / seeded).

- **H0:** LLM-generated tests detect **no more** pre-seeded faults than the better of {Manual, EvoMaster} (rate_LLM ≤ max(rate_Manual, rate_EvoMaster)).
- **H1:** LLM-generated tests detect **more** pre-seeded faults than {Manual, EvoMaster} (rate_LLM > the comparators).

**Statistical test:** **Friedman test** (omnibus, 3 related groups measured on the same APIs/faults) followed by **post-hoc pairwise Wilcoxon signed-rank** (LLM vs Manual, LLM vs EvoMaster) with Holm correction. With only 3 APIs, also report the **per-fault paired outcome** (McNemar / exact binomial on the seeded-fault set) and effect sizes, because n = 3 APIs limits omnibus power.
**Interpretation:** if the Friedman p < 0.05 and post-hoc LLM>comparators p < 0.05 → reject H0 (LLM is more effective at fault detection). This is the first comparison to put **LLM vs manual vs EvoMaster on one pre-seeded-fault set** (closes GAP-1 + GAP-2).
**Rationale / source:** existing papers only *count* 500-errors without ground truth (`evidence-table.md` #6, #7, #8, #11, #13), so Recall has never been computed.

---

## RQ3 — Edge-case / error-code scenarios: LLM vs Manual

**Metric:** edge-case scenario count per endpoint = number of distinct **4xx/5xx error-code + boundary-condition** scenarios generated per endpoint (e.g. invalid type, missing required field, out-of-range value, malformed auth).

- **H0:** LLM-generated tests produce **no more** edge-case scenarios per endpoint than manual test design (median_LLM ≤ median_Manual).
- **H1:** LLM-generated tests produce **more** edge-case scenarios per endpoint than manual test design (median_LLM > median_Manual).

**Statistical test:** paired **Wilcoxon signed-rank test** across endpoints (each endpoint contributes an LLM count and a Manual count → paired samples), α = 0.05.
**Interpretation:** if p < 0.05 and the median difference favours LLM → reject H0 (LLM is more effective at producing error-code/boundary scenarios). Reported alongside a 4xx-vs-5xx-vs-boundary breakdown.
**Rationale / source:** no reviewed paper measures an edge-case scenario count per endpoint; only #2 separates 2xx/4xx coverage and only #3 reports 5xx triggering (`evidence-table.md`), confirming GAP-3.

---

## Summary table

| RQ | Metric | H0 | H1 | Test | α |
|----|--------|----|----|------|---|
| RQ1 | Endpoint coverage (%) | μ ≤ 90% | μ > 90% | One-sample Wilcoxon signed-rank | 0.05 |
| RQ2 | Pre-seeded faults detected (LLM vs Manual vs EvoMaster) | rate_LLM ≤ max(others) | rate_LLM > others | Friedman + post-hoc Wilcoxon (Holm); McNemar per fault | 0.05 |
| RQ3 | Edge-case scenarios / endpoint (LLM vs Manual) | median_LLM ≤ median_Manual | median_LLM > median_Manual | Paired Wilcoxon signed-rank | 0.05 |

**Checkpoint 1.8 ✅** — every RQ has an H0 (negation) and H1 (expectation), a named statistical test, a threshold with a source, and a stated interpretation rule ("if p < 0.05 → …").
