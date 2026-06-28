# Hypotheses Draft — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034 | **Ngày:** 2026-06-13
**GAP:** GAP-M (Metric) — `SLR/gap-analysis.md`. **Thresholds:** `experiment/design-rationale.md`.
**Scope:** GAP-M only (edge-case metric + coverage). GAP-D fault-detection is out of scope.
α = 0.05 throughout.

---

## RQ-main — Edge-case / error-code scenarios per endpoint (LLM vs Manual) — *comparative*

- **Metric:** edge-case-scenario count per endpoint = # distinct `negative`+`boundary`+`errorcode`
  scenarios per operation (parsed from `// SCENARIO type=` tags).
- **H0:** The median edge-case-scenario count per endpoint of **LLM-generated** tests is **≤** that of
  **manual** test design (median_LLM ≤ median_Manual).
- **H1:** The median edge-case-scenario count per endpoint of LLM tests is **>** manual
  (median_LLM > median_Manual).
- **Statistical test dự kiến:** **Wilcoxon signed-rank test**, paired across the 35 endpoints
  (each endpoint contributes an LLM count and a Manual count), one-sided. (α = 0.05.)
- **Threshold/baseline source:** comparative claim → baseline = Manual system (no invented number);
  Case 3 (metric is new; pre-proposal pilot established it is measurable — LLM 5 vs Manual 4 median).
- **Reject H0 if** p < 0.05 and the median difference favours LLM.

## RQ-sub — Endpoint coverage vs the ≥ 90% target (+ endpoint-type miss) — *absolute*

- **Metric:** endpoint coverage = (operations exercised by ≥1 LLM test) / (operations in the OpenAPI
  spec), pooled over the 35 endpoints of the 3 SUTs.
- **H0:** LLM endpoint coverage is **< 90%** (p_covered < 0.90).
- **H1:** LLM endpoint coverage is **≥ 90%** (p_covered ≥ 0.90).
- **Statistical test dự kiến:** **Binomial exact test** on the covered/total endpoint count against
  p₀ = 0.90 (coverage is a pass-rate-style proportion → binomial per Bước 5B). (α = 0.05.)
- **Threshold source:** Case 2 — floor = 88.6% route discovery (RESTSpecIT #3); ceiling 95.5%
  (RESTifAI #9) → target set at **90%** (just above floor; also the course target).
- **Descriptive companion (no hypothesis):** break covered/missed operations down by endpoint type
  (CRUD / input-validation / error-handling) to report *which* types are most often missed.
- **Reject H0 if** the binomial test's lower bound on coverage exceeds 0.90 at α = 0.05.

---

## Refinement note vs RBL-1 `hypotheses.md`

`hypotheses.md` (RBL-1) listed three RQs (RQ1 coverage, RQ2 fault-detection, RQ3 edge-cases) spanning
GAP-M **and** GAP-D, and used a one-sample Wilcoxon for coverage. After finalising **GAP-M** as the
primary gap (`gap-analysis.md`):
- **RQ2 (fault detection) is removed** from scope (it targets GAP-D, not GAP-M).
- **RQ-main** here = RBL-1 RQ3 (edge-case metric); **RQ-sub** here = RBL-1 RQ1 (coverage), with the
  coverage test refined to the **Binomial exact test** (proportion → binomial, per the Bước-5B
  output→test mapping) instead of one-sample Wilcoxon.

## Checklist (RBL-2)
- [x] H0 testable with a concrete threshold/baseline (RQ-sub: 0.90; RQ-main: Manual baseline).
- [x] H1 is the logical opposite of H0.
- [x] Statistical test matches the data type (count→Wilcoxon; proportion→Binomial).
- [x] Threshold in H0 matches `design-rationale.md` (90% coverage; comparative edge-case).
