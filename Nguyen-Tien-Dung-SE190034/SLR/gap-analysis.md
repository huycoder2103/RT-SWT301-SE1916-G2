# GAP Analysis — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Evidence table:** N = 13 papers (`SLR/evidence-table.md`, 2019–2026) | **Ngày:** 2026-06-13
**Rule:** every GAP must point to a column in the evidence table and survive a per-paper
counter-check (phản chứng). No source = invalid.

---

## Bảng GAP (4 loại)

| Cột nguồn | Phát hiện từ evidence table | Loại GAP | Phản chứng |
|-----------|------------------------------|----------|------------|
| Tool/LLM | GPT family dominates (#1,#2,#4,#6,#8,#9); Claude only in 1 multi-LLM study (#5); no head-to-head of current frontier models on one shared REST benchmark | GAP-T | ❌ scanned 13 papers — none benchmarks current Claude/Gemini vs GPT head-to-head on a shared API set |
| Dataset | Fault detection reported as **counts on live APIs** (#2,#6,#7,#8,#11,#13); no shared **pre-seeded-fault** set → Recall never computed | GAP-D | ❌ scanned 13 — only #5 has a mutation score (auto-mutants, 6 self-built APIs); no shared seeded-fault benchmark |
| **Metric** | Papers report **aggregate** coverage + 500-error **counts**; only #2 separates 2xx/4xx, only #3 reports 5xx — **none** measures an **edge-case/error-code scenario count per endpoint**, and **none** breaks coverage down by **endpoint type** (CRUD/validation/error-handling) | **GAP-M** | ❌ scanned 13 — see counter-check table below; confirmed absent |
| Hạn chế | Small/varied datasets + "spec ≠ implementation" oracle uncertainty acknowledged by most LLM papers (#2,#4,#8,#10) | GAP-S | ❌ ~8/13 papers note small data / oracle uncertainty as a shared limitation |

**Ưu tiên (per RBL-2):** GAP-T > GAP-M > GAP-D > GAP-S. GAP-T needs frontier-API access + cost;
GAP-D needs a seeded-fault benchmark (build effort). **GAP-M is the lowest-risk, highest-feasibility**
(implement a metric — typically library-backed) — and it is the one this member finalises.

---

## GAP Chính (primary): **GAP-M — Metric**

> No reviewed paper measures, **per endpoint**, the number of distinct **edge-case scenarios**
> (4xx/5xx error-code + boundary-condition cases produced by intentionally violating the OpenAPI
> contract), nor reports a **coverage breakdown by endpoint type** (CRUD / input-validation /
> error-handling) showing *which* endpoint types are most often missed. We propose this
> **per-endpoint edge-case-scenario metric + endpoint-type miss profile** and use it to compare
> LLM-generated vs manually-designed REST API tests.

## GAP Secondary (deferred, NOT this experiment's focus): GAP-D

> Ground-truth fault-detection **Recall** (LLM vs manual vs EvoMaster on a pre-seeded-fault set) is
> also missing. It is a *separate* gap (GAP-D) — recorded here for completeness and explicitly **out
> of scope** for the GAP-M experiment. (A feasibility pilot for it was run; see `design-rationale.md`
> §Feasibility — it is kept as supporting evidence, not as the GAP-M deliverable.)

---

## Chi tiết kiểm tra phản chứng — GAP-M (quét từng paper)

Question scanned for each paper: *does it measure an edge-case/error-code scenario count **per
endpoint**, or a coverage breakdown **by endpoint type**?*

| # | Paper (Tool) | Metric reported | Per-endpoint edge-case count? | Endpoint-type miss profile? |
|---|--------------|-----------------|:-----------------------------:|:---------------------------:|
| 1 | RESTGPT | rule P/R/F1, value validity | No | No |
| 2 | KAT | status-code cov (2xx,4xx), 500s | No (aggregate 2xx/4xx only) | No |
| 3 | RESTSpecIT | route discovery, 5xx in 4 APIs | No (aggregate 5xx) | No |
| 4 | APITestGenie | valid-script rate | No | No |
| 5 | RestTSLLM | branch cov, mutation score | No | No |
| 6 | AutoRestTest | method/line/branch cov, 500s | No | No |
| 7 | LlamaRestTest | coverage, 204 faults (500s) | No | No |
| 8 | LogiAgent | coverage, 49 5xx crashes | No | No |
| 9 | RESTifAI | operation coverage 128/134 | No (operation count, not edge-case) | No |
| 10 | EvoMaster | statement cov, 5xx, bugs | No | No |
| 11 | No-Time-to-Rest | line/branch cov, 500s (10 tools) | No | No |
| 12 | Morest | coverage, 44 bugs | No | No |
| 13 | DeepREST | branch cov, unique faults | No | No |

**Kết luận phản chứng:** 0/13 papers measure a per-endpoint edge-case-scenario metric or an
endpoint-type miss profile. GAP-M is **confirmed** (not already solved by any reviewed paper).

---

## Feasibility Check — GAP-M

A pre-proposal feasibility pilot was actually executed (build + deploy + generate + measure) on 3 EMB
APIs; results below are the evidence for each ✅. (Pilot artifacts: `experiment/` harness, transcripts,
`results/`.)

| Tiêu chí | Mức | Ghi chú (bằng chứng) |
|----------|:---:|----------------------|
| Dataset | ✅ | EMB (EMResearch/EMB, public, LGPL) — cloned, built + deployed `rest-ncs`, `rest-scs`, `features-service` locally (JDK 8) |
| Tool/API | ✅ | LLM = Claude Sonnet 4.6 via isolated sub-agent (no paid external key); manual = our own; EvoMaster 6.0.0 free jar |
| Compute | ✅ | Local CPU only (Maven + JDK 8/17); no GPU/cluster |
| Ground truth | ✅ | Metric needs **no human annotation**: edge-case count parsed from machine-readable `// SCENARIO type=` tags; coverage from the OpenAPI spec |
| Skills | ✅ | Implemented: REST-assured JUnit harness + spec/tag parser + scipy stats — already working |
| Thời gian | ✅ | Full pilot completed within the design session (suites generated + executed) |
| Contribution | ✅ | First per-endpoint edge-case metric + endpoint-type miss profile for LLM REST-API testing; baseline for the topic |

**Kết quả:** **7 ✅ / 0 ⚠️ / 0 ❌ → An toàn.** GAP-M is finalised as the primary gap; no downscope needed.

**Pilot signal (pre-proposal, supports the design):** on 35 endpoints the LLM suite produced **217**
edge-case scenarios vs Manual **141** (median 5 vs 4 per endpoint), and reached **100%** endpoint
coverage — i.e. the metric is implementable and discriminating. Used as the Case-3 basis in
`design-rationale.md`.
