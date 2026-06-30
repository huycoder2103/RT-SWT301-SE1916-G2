# Experiment Design Rationale — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034 | **Ngày:** 2026-06-13
**GAP source:** `SLR/gap-analysis.md` → primary gap = **GAP-M (Metric)**.
**Rule:** every decision traces to a column/finding in `SLR/evidence-table.md`. Order of derivation:
Dataset → Metric → Threshold → Baseline → Pipeline → Hypothesis → Statistical test.

---

## Bảng Quyết định

| # | Quyết định | Giá trị | Nguồn gốc |
|---|------------|---------|-----------|
| 1 | **LLM / Tool** | **Claude Sonnet 4.6** (`claude-sonnet-4-6`), few-shot, input = OpenAPI spec only, `urlEncodingEnabled` fixed, output = REST-assured JUnit 5 | evidence #5 (Claude 3.5 Sonnet = best of 7 LLMs) + #4 APITestGenie (GPT-4 from spec). We fix the LLM (not a GAP-T claim); version pinned for reproducibility |
| 2 | **Pipeline** | OpenAPI spec → LLM (frozen prompt, blind to source) → REST-assured tests → parse per-endpoint scenarios + coverage. Reproducible (prompt + model + spec sha256 logged) | **Base paper = APITestGenie #4** (LLM + spec → executable tests); change = Claude not GPT-4, + the new per-endpoint metric |
| 3 | **Metric chính** | **Edge-case scenario count per endpoint** = # distinct `negative`+`boundary`+`errorcode` scenarios per operation. Tool: parse machine-readable `// SCENARIO op=.. type=..` tags from the generated REST-assured tests (deterministic) | **GAP-M**; evidence-table "Metrics" column — no paper has this (counter-check in `gap-analysis.md`) |
| 4 | **Metric phụ** | **Endpoint coverage %** = (operations exercised by ≥1 test) / (operations in spec); + **endpoint-type miss profile** (CRUD / input-validation / error-handling) | GAP-M secondary facet; coverage is the most common metric (#2,#6,#7,#8,#9,#11,#13) but never broken down by endpoint type |
| 5 | **Dataset** | 3 EMB REST APIs: `rest-ncs` (6 ops), `rest-scs` (11 ops), `features-service` (18 ops) = 35 operations | EMB is the standard benchmark reused by #6, #7, #11, #13; public + downloadable (feasibility ✅) |
| 6 | **Baseline** | (a) Edge-case metric → **Manual test design** (comparative system baseline); (b) Coverage → **≥ 90%** (absolute threshold) | **3A loại claim:** comparative claim → system baseline (Manual); absolute claim → threshold value |
| 7 | **Threshold** | Coverage: **≥ 90%** (Case 2). Edge-case metric: comparative, **no absolute number** (Case 3 pilot) | see "Lý giải threshold" below |
| 8 | **Statistical test** | Edge-case count (paired per endpoint) → **Wilcoxon signed-rank**; Coverage (proportion vs 0.90) → **Binomial exact test** | **Bước 5B** output→test mapping: continuous/count → Wilcoxon; pass-rate% → Binomial |

---

## Lý giải threshold (1 đoạn / threshold)

- **Coverage ≥ 90% — Case 2** (results exist in the literature, but no paper states an explicit
  threshold). Floor value from the evidence table's *operation/endpoint* coverage results: RESTSpecIT
  (#3) ≈ **88.6%** average route discovery (the floor), RESTifAI (#9) **95.5%** (128/134 operations,
  the ceiling). Per the Case-2 rule (threshold = just above the floor), and matching the course target,
  we set **endpoint coverage ≥ 90%**. This is an *endpoint/operation*-level target — distinct from
  *code* coverage, which stays ~52–72% line (#8, #11) and is NOT our threshold.

- **Edge-case scenario count per endpoint — Case 3** (no paper measures this metric → no number in the
  literature). We therefore ran a **mini-pilot PRE-PROPOSAL** (the `experiment/` harness on the 3 SUTs):
  LLM produced a median of **5** edge-case scenarios/endpoint vs Manual **4** (217 vs 141 total over 35
  endpoints). Because the claim is **comparative** (LLM vs Manual), the baseline is the Manual system —
  **no absolute threshold number is invented**; the hypothesis is directional (LLM > Manual).

---

## 5A. RQ cuối cùng (công thức)

- **RQ-main (comparative, edge-case metric — GAP-M):**
  > "Does **Claude Sonnet 4.6** (I, few-shot from the OpenAPI spec) generate **more edge-case /
  > error-code scenarios per endpoint** (4xx/5xx + boundary) than **manual test design** (C) on 3 EMB
  > REST APIs (P), measured by the **edge-case-scenario count per endpoint** (O)?"
- **RQ-sub (absolute, coverage — GAP-M facet):**
  > "Do the LLM-generated tests reach **endpoint coverage ≥ 90%** (O) on the EMB APIs (P), and **which
  > endpoint types** (CRUD / input-validation / error-handling) are most frequently missed?"

These are exactly RQ3 (edge-case metric) and RQ1 (coverage + type miss) of `01_rq.md`. **RQ2
(fault-detection Recall, LLM vs Manual vs EvoMaster) belongs to GAP-D, not GAP-M, and is therefore
OUT OF SCOPE for this experiment** (kept only as a feasibility pilot — see below).

---

## Feasibility / pilot note (supports the design; not the deliverable)

A full pre-proposal pilot was executed: 3 SUTs built + deployed; LLM/Manual/EvoMaster suites generated
(blind); the GAP-M metric implemented + measured. It confirms the design is implementable and the
metric discriminates (LLM 217 vs Manual 141 edge-cases; 100% coverage). The GAP-D fault-detection arm
was also piloted (mutation recall: EvoMaster 0.135 vs LLM/Manual 0.068) — recorded as evidence that
GAP-D is a *separate* study, intentionally excluded from this GAP-M design.
