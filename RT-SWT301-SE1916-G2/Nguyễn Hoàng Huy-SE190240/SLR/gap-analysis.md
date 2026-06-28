# GAP Analysis — LLM for REST API Test Generation

**Member:** Nguyễn Hoàng Huy (SE190240)  
**Date:** 2026-06-14  
**Evidence base:** `evidence-table.md` — N = 13 papers (2023–2026)  
**Assigned GAP (per team assignment):** GAP-3 (Metric) — Coverage + 500-error counting dominate; edge-case / error-code coverage and endpoint-type miss analysis are absent

---

## GAP Primary: GAP-M (Metric) — No per-endpoint edge-case metric and no endpoint-type miss profile

**Statement (1–2 sentences):**
> Across 13 studies on LLM-based REST API test generation, evaluation metrics cluster into code coverage (line/branch/method) and absolute 500-error counts; no paper defines or measures a **per-endpoint edge-case scenario count** (4xx/5xx + boundary conditions produced by intentionally violating OpenAPI constraints), and no paper reports which endpoint types (CRUD / authentication / error-handling) are systematically missed — leaving the qualitative edge-case generation capability of LLMs entirely unmeasured.

---

## GAP Secondary: GAP-D (Dataset) — No pre-seeded fault ground truth → Recall never computed

**Statement (1–2 sentences):**
> All 13 papers report fault detection as absolute counts on live or benchmark APIs whose total fault count is unknown; no paper constructs or uses a REST API dataset with intentionally pre-seeded business-logic faults (known ground truth), making it impossible to compute Fault Detection Recall = faults detected / total faults seeded.

---

## Anti-Evidence Check — GAP Primary (GAP-M)

**Claim:** No paper in the evidence table defines or measures (a) a per-endpoint edge-case scenario count, (b) an endpoint-type miss profile (CRUD/auth/error-handling), or (c) verifies ≥90% endpoint coverage on EMB APIs with pre-seeded faults.

**Scan results — checking each paper for all three criteria:**

| Paper | (a) Per-endpoint edge-case count? | (b) Endpoint-type miss profile? | (c) ≥90% endpoint coverage on EMB + pre-seeded? | Evidence / Quote |
|-------|:---------------------------------:|:--------------------------------:|:------------------------------------------------:|-----------------|
| #1 NLPtoREST (2023) | **No** | **No** | **No** | Measures line/branch coverage + 500-error counts across 9 APIs in aggregate |
| #2 GPT API test scripts (2023) | **Partial** | **No** | **No** | Separates 2xx/4xx/5xx status-code coverage per API, but aggregate (not per endpoint); no endpoint-type breakdown; no EMB |
| #3 RESTGPT (2024) | **No** | **No** | **No** | Reports rule-extraction precision 97% and value-generation accuracy ~73%; no coverage metric |
| #4 KAT (2024) | **No** | **No** | **No** | Reports +15.7% status-code coverage over RestTestGen; no per-endpoint edge-case count, no endpoint-type breakdown |
| #5 DeepREST (2024) | **No** | **No** | **No** | Reports AUC branch/line/method coverage + 5XX count on 11 EMB APIs; no edge-case per endpoint; no pre-seeded faults |
| #6 RESTless (2024) | **No** | **No** | **No** | Counts 38 vulnerabilities on cloud APIs; no endpoint-type breakdown; no EMB; no pre-seeded faults |
| #7 LlamaRestTest (2025) | **No** | **No** | **No** | Measures code coverage (line/branch/method) + 500 errors on 12 APIs; no edge-case metric; no pre-seeded faults |
| #8 AutoRestTest demo (2025) | **No** | **No** | **No** | Reports operation count + unique server errors (26 ops on 4 APIs); no coverage %, no type breakdown |
| #9 MioHint (2025) | **No** | **No** | **No** | White-box target coverage + line coverage; no edge-case per endpoint; no endpoint-type breakdown |
| #10 MASTEST (2025) | **No** | **No** | **No** | Reports API operation coverage + status code coverage on 5 APIs — but no per-endpoint-type breakdown, no edge-case count, no EMB, no pre-seeded faults |
| #11 LogiAgent (2025) | **No** | **No** | **No** | Detects 234 logical issues at 66.19% accuracy; measures branch/line/method coverage; no per-endpoint edge-case count or type breakdown |
| #12 AutoREST black-box (2026) | **No** | **No** | **No** | 74% operation coverage (151/204 ops) on industrial satellite APIs; no edge-case per endpoint; no endpoint-type breakdown; no EMB; no pre-seeded faults |
| #13 APITestGenie (2026) | **No** | **No** | **No** | Reports script validity rate + success rate per business requirement; no per-endpoint edge-case count or type breakdown |

**→ Conclusion: CONFIRMED.** Zero of 13 papers measures a per-endpoint edge-case scenario count; zero reports an endpoint-type miss profile; zero verifies endpoint coverage ≥90% on EMB with pre-seeded faults.

**Closest approximation (and why it still confirms the gap):**
- **#2 (GPT API test scripts):** separates 2xx/4xx/5xx status-code coverage *per API* — the only paper to do so — but this is an aggregate metric per API, not a per-endpoint count of edge-case scenarios, and it does not break down which endpoint *types* are covered or missed.
- **#4 (KAT):** reports +15.7% status-code coverage (combining 2xx + undocumented codes) — closer to edge-case awareness, but still an aggregate per-service number, not per-endpoint and not classified by endpoint type.
- **#12 (AutoREST black-box):** reports 74% operation coverage — the only endpoint-level percentage in Huy's set — but on industrial APIs (not EMB), no pre-seeded faults, no fault-type breakdown.

---

## Anti-Evidence Check — GAP Secondary (GAP-D)

**Claim:** No paper computes Fault Detection Recall on a dataset with known pre-seeded faults.

| Paper | Pre-seeded faults (ground truth known)? | Recall computed? | Evidence |
|-------|:---------------------------------------:|:----------------:|----------|
| #1 NLPtoREST | **No** | **No** | 9 live APIs; total fault count unknown |
| #5 DeepREST | **No** | **No** | 11 EMB APIs; counts 5XX in real runs, no fault ground truth |
| #6 RESTless | **No** | **No** | "38 vulnerabilities detected, 16 confirmed" — no total known |
| #7 LlamaRestTest | **No** | **No** | "204 faults vs EvoMaster 130" on live APIs; no ground truth |
| #11 LogiAgent | **No** | **No** | "234 logical issues, 49 crashes" — total real faults unknown |
| #12 AutoREST | **No** | **No** | "21 unique previously unknown faults" — by definition, total unknowable |
| All others | **No** | **No** | No pre-seeded fault methodology |

**→ Conclusion: CONFIRMED.** No paper in the evidence table uses a pre-seeded fault methodology; Recall is never reported across all 13 papers.

---

## Feasibility Check — GAP Primary (GAP-M)

| Criterion | Level | Notes |
|-----------|:-----:|-------|
| Dataset | ✅ | EMB APIs (e.g., features-service, menu-service, petstore) are publicly available on GitHub (EvoMaster repo), with OpenAPI specs, actively used in papers #5, #7, #11 |
| Tool/API | ⚠️ | GPT-4o requires OpenAI API key + budget (~$0.01–0.05 per test run); Gemini offers free tier. Budget is manageable at small scale (3 APIs × ~100 endpoints). |
| Compute | ✅ | API-based LLM calls; no GPU required. Python + pytest on any laptop. EvoMaster runs on JVM (≥8 GB RAM). |
| Ground truth | ✅ | Edge-case scenario count is defined structurally from the OpenAPI spec (count of constraints per endpoint × 4 violation types): no domain expert annotation needed. Endpoint-type classification (CRUD/auth/error-handling) can be done by reading HTTP method + path pattern. |
| Skills | ✅ | Python REST API scripting + OpenAPI parsing are standard skills; pytest for execution; scipy for Wilcoxon test. No research-level ML needed. |
| Time | ✅ | 3 APIs × ~20 endpoints each = manageable. LLM generation: ~1–2 hours per API. EvoMaster: ~1 hour per API. Analysis scripts: ~2 days. Buffer ≥ 1 week. |
| Contribution | ✅ | First study to report per-endpoint edge-case scenario count and endpoint-type miss profile on EMB APIs with pre-seeded faults. Even negative results (LLM < Manual on edge cases) are informative. |

**Result:** 0 ❌ / 1 ⚠️ → **Safe to proceed.** The only risk is API cost, which is managed by limiting to 3 APIs and using GPT-4o-mini as a fallback.

---

## Final GAP Statement (for use in proposal)

**GAP-3 (Metric) — Selected as primary:**

> Across 13 studies (2023–2026), evaluation of LLM-based REST API test generators relies exclusively on aggregate code coverage (line/branch/method) and raw 500-error counts. Only one paper (#2) separates 2xx from 4xx status-code coverage, and only one paper (#4) reports undocumented status codes — but **no paper defines or measures a per-endpoint edge-case scenario count** (the number of distinct 4xx/5xx + boundary test cases generated by intentionally violating OpenAPI constraints), and **no paper profiles which endpoint types** (CRUD, authentication, error-handling) are systematically missed by automated generators. Furthermore, although endpoint/operation coverage can reach ~74–95% on select APIs (#10 merged: RESTifAI 95.5%; #12: 74%), this has **never been verified on EMB APIs with pre-seeded business-logic faults**, nor broken down by endpoint type.

**Contribution this closes:** defines the edge-case scenario count metric, produces the first endpoint-type miss profile on EMB, and verifies whether the ≥90% endpoint-coverage target is achievable on pre-seeded-fault EMB APIs — directly closing GAP-M and contributing to GAP-D.
