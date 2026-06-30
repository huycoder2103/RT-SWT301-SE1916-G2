# Final Research Question (Group) — LLM for REST API Test Generation

**Team:** SWT301_SU26_Group2
**Members:** Nguyen Tien Dung (SE190034), Nguyen Hoang Huy (SE190240), Nguyen Thanh Dat (SE190239), Nguyen Le Thuan (SE190305), Vo Le Trung Nguyen (SE190220)
**Derived from:** `evidence-table-merged.md` (N = 59 unique papers, 2018–2026) and the five individual `experiment/01_rq.md` files.

---

## 1. How the five individual RQs converge

Each member explored a different angle of the same topic; the group RQ keeps the assigned-topic core and folds in what each member's evidence adds.

| Member | Individual RQ focus | What it contributes to the group RQ |
|--------|--------------------|--------------------------------------|
| **DUNG** | LLM vs **manual** vs **EvoMaster** on **pre-seeded faulty** EMB APIs (endpoint coverage, fault detection, edge cases) | The assigned-topic core — adopted as the group's main RQ + RQ1–RQ3 |
| **HUY** | Which LLM family (GPT-4o vs Gemini); **edge-case coverage** via constraint violation | Sharpens RQ3 (4xx/5xx + boundary) and the choice of a strong GPT model as the representative LLM |
| **DAT** | LLM agent vs classic **fuzzers** (RESTler, ARAT-RL); **operation coverage**, 5xx faults, token efficiency | Confirms RQ1 should measure **operation/endpoint** coverage; widens the baseline landscape beyond EvoMaster |
| **THUAN** | **Open-source** LLaMA-3 + RAG; **test validity rate ≥ 90%**; RESTestBench | Adds a validity/quality lens and reinforces the need for a standard dataset |
| **NGUYEN** | **Open-source vs closed-source** LLMs; mutation/log coverage; "no shared benchmark" | Reinforces the dataset/ground-truth gap and the metric-breadth gap |

**Convergence decision:** the group adopts the assigned-topic RQ (DUNG's), using **GPT-4o / GPT-4-Turbo** as the representative LLM — justified because the GPT family dominates the merged evidence (RESTGPT, KAT, APITestGenie, AutoRestTest, MioHint, …) and is the most-compared model, while Gemini / open-source Llama (HUY, THUAN, NGUYEN) remain candidate *variants* for later ablation rather than the primary intervention.

---

## 2. Official group RQ

### Main RQ
> **"How effectively can LLMs automatically generate API test cases from OpenAPI specifications, compared to manually designed tests and EvoMaster-generated tests on pre-seeded faulty API versions?"**

### RQ1 — Coverage (targets GAP-M)
> **"Do LLM-generated API tests achieve endpoint coverage ≥ 90% on locally deployed EvoMaster-benchmark APIs, and which endpoint types (CRUD, authentication, error handling) are most frequently missed?"**

### RQ2 — Fault detection (targets GAP-D / GAP-C)
> **"How many pre-seeded faults do LLM-generated tests detect compared to manually designed tests and EvoMaster-generated tests across 3 benchmark APIs?"**

### RQ3 — Error codes & boundary (targets GAP-M)
> **"Are LLM-generated tests more effective than manual test design at producing test cases for error codes (4xx, 5xx) and boundary conditions, measured by edge-case scenario count per endpoint?"**

---

## 3. Full PICO (experiment)

- **P (Population):** 3 REST API services from the **EvoMaster Benchmark (EMB)** that ship with an OpenAPI/Swagger spec, deployed locally, instrumented with **pre-seeded faulty versions** so the total fault count (ground truth) is known.
- **I (Intervention):** an automated API-test-case generator built on an **LLM (GPT-4o / GPT-4-Turbo)** that reads the OpenAPI spec and produces positive / negative / error-code / boundary test cases. Output = a tool + GitHub repo.
- **C (Comparison):** (1) **manual test design** (human-written tests); (2) **EvoMaster** (search-based automated generation — the most-reused baseline in the merged evidence).
- **O (Outcome):**
  - **O1 — Endpoint coverage (%)**, target **≥ 90%**, with a per-endpoint-type miss breakdown (CRUD / auth / error-handling).
  - **O2 — Fault detection:** count of pre-seeded faults detected (ground-truth Recall) — LLM vs manual vs EvoMaster on the 3 APIs.
  - **O3 — Edge-case scenario count per endpoint:** 4xx/5xx + boundary scenarios (LLM vs manual).

---

## 4. Evidence-based justification of each choice

| Choice | Justified by merged evidence |
|--------|------------------------------|
| LLM = GPT-4o / GPT-4-Turbo | GPT family dominates (#5,#6,#7,#12 + many singletons); strongest, most-compared line |
| Baseline = EvoMaster + manual | EvoMaster is the most-reused baseline (#4,#7,#11,#16 comparisons); EvoMaster (#16) is the **only** paper that compares a tool against *manual* tests — and found the tool **below** manual coverage, so a fresh LLM-vs-manual test is warranted |
| Dataset = EMB + pre-seeded faults | EMB is the shared benchmark (#3,#4,#7,#11 etc.); **no** merged paper uses pre-seeded faults with ground-truth Recall |
| Metric = endpoint coverage ≥90% | operation/endpoint coverage can already exceed 90% (RESTifAI #10: 128/134 ≈ 95.5%) while *code* coverage caps ~52–72% — so RQ1's open question is the **miss-profile by endpoint type**, never reported |
| Metric = edge-case scenarios | only KAT (#1) splits 2xx/4xx and only RESTSpecIT (#2) reports 5xx; no per-endpoint edge-case metric exists |

**Checkpoint (team RQ):** dataset, LLM, baseline and metrics are all specific and each is traceable to the merged evidence table and to ≥ 1 member's individual SLR.
