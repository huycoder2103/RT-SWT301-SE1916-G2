# Hypotheses Draft — LLM for REST API Test Generation

**Member:** Nguyễn Hoàng Huy (SE190240)  
**Date:** 2026-06-14  
**GAP addressed:** GAP-3 (Metric) — per `SLR/gap-analysis.md`  
**Design source:** `experiment/design-rationale.md`  
**Team alignment:** `team-synthesis/hypotheses-draft.md` (RQ1 + RQ3 sub-questions)

---

## RQ1 — Endpoint Coverage with Endpoint-Type Miss Profile

**Full RQ:**
> "On locally deployed EvoMaster Benchmark (EMB) APIs instrumented with pre-seeded faults, do LLM-generated tests (Claude Sonnet 4.6) achieve endpoint coverage ≥ 90%, and which endpoint types (CRUD / authentication / error-handling) are most frequently missed?"

**H0 (Null hypothesis):**
> The mean endpoint coverage of Claude Sonnet 4.6-generated tests on EMB APIs is **≤ 90%** (μ ≤ 0.90).

**H1 (Alternative hypothesis):**
> The mean endpoint coverage of Claude Sonnet 4.6-generated tests on EMB APIs is **> 90%** (μ > 0.90).

**Statistical test:** One-sample **Wilcoxon signed-rank test** vs threshold 0.90, one-tailed (upper), **α = 0.05**.  
Effect size: rank-biserial correlation.

**Threshold source — Case 2 (from literature values, aligned with team `proposal.md` §4 RQ1):**

| Source | Value | Role |
|--------|-------|------|
| RESTSpecIT / You Can REST Now (merged #2, 2024) | 88.62% route discovery (avg) | **Floor** — observed minimum for endpoint-level discovery |
| RESTifAI (merged #10, ICSE Demo 2026) | 95.5% operation coverage on OhSome | **Ceiling** — shows ≥90% is attainable in principle |
| No-Time-to-Rest-Yet (merged #11, ISSTA 2022) | EvoMaster-WB 52.76% line coverage (best of 10 tools) | Confirms endpoint coverage >> code coverage; 90% is the right metric level |
| Team-assigned target (course requirement) | ≥ 90% | Nominal threshold |

**Derivation (Case 2):** Floor = 88.6% (merged #2) → round up → **threshold = 90%**. Ceiling = 95.5% (merged #10) confirms the target is attainable. No paper has verified ≥90% on EMB with pre-seeded faults and endpoint-type breakdown → the research question is open (confirms GAP-3).

**Interpretation:**
- p < 0.05 and median endpoint coverage > 0.90 → **reject H0** → LLMs achieve the target
- p ≥ 0.05 or median ≤ 0.90 → **fail to reject H0** → coverage falls short; inspect miss profile by endpoint type to explain why

**Additional (descriptive, not hypothesis-tested):** Report the percentage of missed endpoints by type (CRUD / Authentication / Error-handling) to answer the "which endpoint types are most frequently missed" part of RQ1. This is the novel contribution of GAP-3.

---

## RQ3 — Edge-Case Scenario Count per Endpoint (LLM vs Manual)

**Full RQ:**
> "Are Claude Sonnet 4.6-generated tests more effective than manually designed tests at producing test cases for error codes (4xx, 5xx) and boundary conditions, measured by edge-case scenario count per endpoint on EMB APIs?"

**H0 (Null hypothesis):**
> The median number of edge-case scenarios generated per endpoint by Claude Sonnet 4.6 is **no greater than** the median number produced by manual test design (median_LLM ≤ median_Manual).

**H1 (Alternative hypothesis):**
> The median number of edge-case scenarios generated per endpoint by Claude Sonnet 4.6 is **greater than** the median number produced by manual test design (median_LLM > median_Manual).

**Statistical test:** Paired **Wilcoxon signed-rank test** across endpoints (each endpoint is a paired observation: LLM count vs Manual count), one-tailed (upper), **α = 0.05**.  
Effect size: Cliff's δ (rank-biserial for paired data).

**Threshold source — Case 3 (no existing literature number):**

No paper in the 13-paper evidence table defines or measures a per-endpoint edge-case scenario count (see `SLR/gap-analysis.md` anti-evidence table: 0/13 papers). Therefore:
- An absolute threshold cannot be derived from literature (Case 1 or 2 do not apply).
- The hypothesis is **comparative** (LLM vs Manual), not absolute.
- A **mini-pilot** will be run before the main experiment: manually enumerate edge-case scenarios for a random sample of 5 endpoints (invalid type, missing required field, out-of-range, malformed auth), yielding an approximate Manual baseline for sanity-checking the scale of the measurement.

**Edge-case scenario types counted (per OpenAPI spec constraints):**

| Type | Violation applied | Expected response |
|------|------------------|-------------------|
| Invalid type | Pass a string where integer expected, or vice versa | 400 Bad Request |
| Missing required field | Omit a field marked `required` in the OpenAPI schema | 400 Bad Request |
| Out-of-range value | Pass value below `minimum` or above `maximum` | 400 Bad Request |
| Malformed / missing authentication | Missing `Authorization` header, invalid token format | 401 Unauthorized |

**Interpretation:**
- p < 0.05 with median difference > 0 (LLM > Manual) → **reject H0** → LLMs generate more edge-case scenarios per endpoint than manual testing
- p ≥ 0.05 → **fail to reject H0** → LLMs do not outperform manual on edge-case generation; report the 4xx/5xx/boundary breakdown to identify where the gap lies

---

## Summary Table

| RQ | Metric | H0 | H1 | Statistical Test | α | Threshold Source |
|----|--------|----|----|-----------------|---|-----------------|
| RQ1 — Coverage | Endpoint coverage (%) overall + by type (CRUD/auth/error-handling) | μ ≤ 0.90 | μ > 0.90 | One-sample Wilcoxon signed-rank vs 0.90 | 0.05 | Case 2: floor 88.6% (#2 merged RESTSpecIT), ceiling 95.5% (#10 merged RESTifAI) |
| RQ3 — Edge-cases | Edge-case scenario count per endpoint (LLM vs Manual) | median_LLM ≤ median_Manual | median_LLM > median_Manual | Paired Wilcoxon signed-rank across endpoints | 0.05 | Case 3: no prior measurement; comparative claim; mini-pilot for scale |

**Effect sizes reported:** rank-biserial correlation (RQ1), Cliff's δ (RQ3).

**Multiple testing:** RQ1 and RQ3 are the two metric-focused sub-hypotheses (GAP-3). The team also tests RQ2 (fault detection: Friedman + post-hoc Wilcoxon). Across all three RQs, Bonferroni-adjusted α ≈ 0.017 for cross-RQ inference; within each RQ, test at nominal α = 0.05 and report unadjusted p-values with effect sizes.

---

## Connection to Team Hypotheses (team-synthesis/hypotheses-draft.md)

| This file | Team file | Relation |
|-----------|-----------|----------|
| RQ1 H0: μ ≤ 0.90 (one-sample Wilcoxon) | RQ1 H0: μ ≤ 0.90 (one-sample Wilcoxon signed-rank) | **Identical** — Huy's RQ1 aligns fully with team RQ1 |
| RQ3 H0: median_LLM ≤ median_Manual (paired Wilcoxon) | RQ3 H0: median_LLM ≤ median_Manual (paired Wilcoxon signed-rank across endpoints) | **Identical** — Huy's RQ3 aligns fully with team RQ3 |
| RQ2 not covered here | Team RQ2: Friedman + post-hoc Wilcoxon for fault detection | RQ2 is GAP-D/GAP-C — primarily DUNG's scope; Huy contributes data for the team analysis |

**Member convergence note:** Team `hypotheses-draft.md` assigns RQ1 one-sample Wilcoxon to "DUNG, HUY, THUAN" and RQ3 paired Wilcoxon to "DUNG". This file confirms Huy's alignment with both RQ1 and RQ3 given the assigned GAP-3 (Metric) scope.
