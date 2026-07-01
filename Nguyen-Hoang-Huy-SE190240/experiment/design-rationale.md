# Experiment Design Rationale — LLM for REST API Test Generation

**Member:** Nguyễn Hoàng Huy (SE190240)  
**Date:** 2026-06-14  
**GAP source:** `SLR/gap-analysis.md` — GAP-3 (Metric): no per-endpoint edge-case metric, no endpoint-type miss profile, no ≥90% endpoint-coverage verification on pre-seeded-fault EMB APIs

---

## Decision Table

| # | Decision | Choice | Source (paper) | Reason |
|---|----------|--------|----------------|--------|
| 1 | Dataset | **3 EMB APIs: `rest-ncs` (6 ops), `rest-scs` (11 ops), `features-service` (18 ops) = 35 operations total**, deployed locally as JDK 8 fat-jars, with **pre-seeded faulty versions** (PIT/Offutt mutation operators; pilot N=133 mutants: ncs 70, scs 59, features 4) | #5 (DeepREST, HUY) — uses 11 EMB APIs; #7 (LlamaRestTest, merged) — 12 EMB services; #11 (merged: No-Time-to-Rest-Yet) — establishes EMB as standard benchmark | EMB is the most-reused REST API benchmark in the merged evidence; it ships with OpenAPI specs enabling LLM generation; local deployment allows controlled pre-seeded fault injection; public on GitHub (EMResearch/EMB, LGPL). 3 small-to-medium APIs (6–18 ops) balance statistical power against experiment effort. |
| 2 | LLM (Intervention) | **`gpt-4o-2024-08-06`** (OpenAI API), temperature=0, top_p=1, max_tokens=4096, seed fixed; few-shot from OpenAPI spec only (black-box, blind to source/faults). Pilot proxy: Claude Sonnet 4.6 (model-agnostic pipeline). | #3 (RESTGPT, HUY) — GPT-3.5 pipeline; #9 (MioHint, HUY) — GPT-4o; #13 (APITestGenie, HUY) — GPT-4-Turbo + RAG; team `proposal.md` §5.3 | GPT-4o is the strongest model in the merged evidence (47.72pp target coverage improvement #9; 89% script validity #13); choice is traceable to the most-represented LLM family across 9/13 HUY papers. Exact version `gpt-4o-2024-08-06` pinned for reproducibility (temperature=0). |
| 3 | Baseline | (B1) **EvoMaster** (search-based automated), (B2) **Manual test design** (human-written tests) | #5 (DeepREST, HUY) — compares against EvoMaster; #7 (LlamaRestTest, merged) — compares against EvoMaster; #11 merged (No-Time-to-Rest-Yet) — benchmarks 10 tools incl. EvoMaster; #16 merged (EvoMaster TOSEM 2019) — the only paper comparing a tool against *manual* tests | EvoMaster is the most-reused baseline in the merged evidence (appears in 4/13 HUY papers). Manual testing is the implicit gold standard; it is the comparison missing from all LLM papers (#16 found automated tool *below* manual at 41% vs 82%), making the LLM-vs-manual comparison the highest-value research question. |
| 4 | Primary Metric | **M1: Endpoint coverage (%)** = (endpoints exercised by ≥1 test) / (total endpoints in OpenAPI spec), reported overall and **broken down by endpoint type** (CRUD: GET/POST/PUT/DELETE standard resources; Authentication: login/logout/token endpoints; Error-handling: endpoints with explicit 4xx/5xx response schemas) | #12 (AutoREST black-box, HUY) — 74% operation coverage (151/204 ops); #10 merged (RESTifAI) — 95.5% operation coverage; #11 merged (No-Time-to-Rest-Yet) — maps coverage ceilings on EMB | M1 directly addresses GAP-3 (endpoint coverage not verified on EMB); the **type breakdown** (CRUD/auth/error-handling) is the novel contribution that no prior paper reports. Endpoint coverage is the coarser metric that can reach ≥90% (unlike code coverage which caps ~52–74%). |
| 5 | Secondary Metric | **M2: Edge-case scenario count per endpoint** = count of distinct test cases targeting {invalid type, missing required field, out-of-range value, malformed/missing auth} per endpoint, for LLM-generated vs Manual tests | #2 (GPT API test, HUY) — reports 2xx/4xx/5xx separation (closest existing metric); #4 (KAT, HUY) — reports +15.7% status-code coverage including undocumented codes; no paper measures per-endpoint count | M2 is the core new metric of GAP-3. KAT (#4) shows LLMs can discover new status codes; the per-endpoint count formalizes this into a measurable, reproducible quantity. Each endpoint's constraint set (from OpenAPI `required`, `minimum`, `maximum`, `pattern`) defines the theoretical maximum; LLM/manual counts are measured against it. |
| 6 | Threshold (M1) | **≥ 90% endpoint coverage** (one-sample absolute threshold) | **Case 2:** Floor = **88.6% route discovery** (RESTSpecIT / You Can REST Now, merged #2); ceiling = **95.5% operation coverage** (RESTifAI, merged #10). Team `proposal.md` §4 RQ1. | 90% sits between the floor (88.6%, merged #2) and ceiling (95.5%, merged #10) — not self-invented. **No paper has verified this on EMB with pre-seeded faults**, confirming GAP-3. Consistent with team threshold derivation in `proposal.md`. |
| 7 | Threshold (M2) | **Comparative only — no absolute threshold** (Case 3) | **Case 3:** No paper in the 13-paper evidence table measures a per-endpoint edge-case scenario count. No floor value exists. | Since Case 3 applies, RQ3 uses a comparative H0/H1 (LLM vs Manual) rather than an absolute threshold. The team's `hypotheses-draft.md` confirms this approach (paired Wilcoxon, H0: median_LLM ≤ median_Manual). A mini-pilot (manually enumerate edge-case scenarios for 5 endpoints) will establish approximate Manual baseline before running the full experiment. |
| 8 | Statistical Test (M1) | **One-sample Wilcoxon signed-rank test** vs threshold 0.90, α = 0.05. Effect size: rank-biserial correlation. | Team `hypotheses-draft.md` (RQ1); Bước 5B of RBL-2 guide: "liên tục (cosine sim, F1, BLEU) → Wilcoxon signed-rank" | Endpoint coverage per API is a continuous proportion in [0,1]; distribution unknown → non-parametric test safer than one-sample t-test. With 3 APIs, report also exact binomial on the pass/fail per API (secondary). |
| 9 | Statistical Test (M2) | **Paired Wilcoxon signed-rank test** across endpoints (each endpoint → LLM count vs Manual count), α = 0.05. Effect size: Cliff's δ. | Team `hypotheses-draft.md` (RQ3); Bước 5B: "so sánh 2 hệ thống → Mann-Whitney U / Wilcoxon paired" | Each endpoint is a paired observation (same endpoint, two generators). Paired Wilcoxon is correct for matched pairs; Mann-Whitney would lose the pairing. |
| 10 | Pipeline base paper | **APITestGenie (#13 HUY, AST 2026)** | #13: GPT-4-Turbo + RAG + OpenAPI spec → script generation → execution → validity/fault measurement. Closest pipeline structure. | APITestGenie is the only paper in HUY's set that (a) takes OpenAPI spec as direct input, (b) generates executable test scripts, and (c) measures both coverage-like (BR success rate) and fault detection. The adapted pipeline drops the RAG component (no requirements doc available for EMB) and adds the endpoint-type classification and edge-case counting steps. |

---

## Threshold Derivation Detail

### Threshold for M1 (endpoint coverage ≥ 90%)

**Case classification: Case 2** (literature values exist but no explicit threshold proposed).

Evidence from team's merged table (primary-verified, consistent with `proposal.md` §4 RQ1):
- **#2 merged (RESTSpecIT / You Can REST Now, 2024):** 88.62% route discovery (avg across APIs). → **Floor: 88.6%**.
- **#10 merged (RESTifAI, ICSE Demo 2026):** 128/134 operations on OhSome ≈ **95.5%** operation coverage. → **Ceiling: 95.5%**.
- **#11 merged (No-Time-to-Rest-Yet, ISSTA 2022):** EvoMaster-WB 52.76% *line* coverage — confirms endpoint coverage is a *different*, more attainable metric than code coverage.

**Derivation:** Floor (88.6%) < target (90%) < ceiling (95.5%). The 90% target is not self-invented: it sits just above the observed floor (88.6%, merged #2) and well below the ceiling (95.5%, merged #10). **No paper has verified ≥90% endpoint coverage on EMB with pre-seeded faults**, confirming GAP-3.

> "RESTSpecIT (#2 merged) achieves 88.6% route discovery (2024). RESTifAI (#10 merged) achieves 95.5% operation coverage on OhSome (ICSE 2026 Demo). Threshold = 90% — Case 2 floor rounded up from 88.6% (#2 merged). Unverified on EMB with pre-seeded faults + endpoint-type breakdown." (consistent with team `proposal.md` §4 RQ1 threshold note).

### Threshold for M2 (edge-case scenarios per endpoint)

**Case 3 — No existing number.**

Search across all 13 HUY papers for "edge case coverage", "per endpoint", "boundary", "constraint violation" metric: 0 results with a numeric threshold.

Closest: KAT (#4 HUY) reports +15.7% additional status-code coverage (aggregate); RESTSpecIT (#2 merged) reports 5xx triggering in 4 APIs (aggregate). Neither provides a per-endpoint count.

**Consequence:** H0/H1 for RQ3 are comparative (LLM vs Manual), not absolute. Mini-pilot before the experiment: manually enumerate edge-case scenarios for 5 randomly sampled endpoints across the 3 APIs, count average Manual scenarios per endpoint ≈ baseline.

---

## Pipeline (adapted from #13 APITestGenie)

```
OpenAPI spec (EMB API)
        ↓
[Step 1] Endpoint classification
         → tag each endpoint as CRUD / Auth / Error-handling
         → from: HTTP method + path pattern + response schemas
        ↓
[Step 2] LLM prompt (GPT-4o / GPT-4-Turbo)
         → Prompt template: "Given this OpenAPI spec, generate REST API test cases for endpoint {path}
            covering: (a) happy path, (b) invalid type for each parameter,
            (c) missing required fields, (d) out-of-range values, (e) malformed auth.
            Output as executable Python requests."
        ↓
[Step 3] Execute tests against locally deployed EMB API
         → Record: HTTP response status code per test case
         → Record: pass/fail against pre-seeded-fault versions
        ↓
[Step 4] Measure M1 (endpoint coverage)
         → count endpoints with ≥1 executed test / total endpoints
         → break down by CRUD / Auth / Error-handling
        ↓
[Step 5] Measure M2 (edge-case scenario count)
         → per endpoint: count distinct {4xx, 5xx, boundary} test cases generated
         → compare LLM count vs Manual count (paired)
        ↓
[Step 6] Measure fault detection on pre-seeded versions
         → Recall = faults triggered / total seeded faults
         → for LLM, EvoMaster, Manual
        ↓
[Step 7] Statistical analysis
         → M1: one-sample Wilcoxon signed-rank vs 0.90
         → M2: paired Wilcoxon signed-rank (LLM vs Manual)
         → Fault detection: Friedman + post-hoc Wilcoxon (LLM vs EvoMaster, LLM vs Manual)
```

**Tools:** Python 3.11 + `requests` + `pytest` + `scipy.stats` (Wilcoxon/Friedman) + EvoMaster 1.6.x (search-based baseline).

---

## Member-specific focus within team experiment

The team's RQ covers three sub-questions (RQ1: coverage, RQ2: fault detection, RQ3: edge-cases). Huy's assigned GAP is GAP-3 (Metric), so **Huy's primary responsibility** is:

- **M1** (endpoint coverage with endpoint-type miss profile) → directly addresses the "endpoint-type miss analysis absent" part of GAP-3
- **M2** (edge-case scenario count per endpoint) → directly addresses the "edge-case / error-code coverage absent" part of GAP-3
- Contributing to M3 (fault detection / Recall) as part of the team effort for RQ2 (GAP-D / GAP-C)
