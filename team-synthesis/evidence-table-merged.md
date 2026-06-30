# Team Evidence Table (Merged) — LLM for REST API Test Generation

**Team:** SWT301_SU26_Group2 — members: Nguyen Tien Dung (SE190034), Nguyen Hoang Huy (SE190240), Nguyen Thanh Dat (SE190239), Nguyen Le Thuan (SE190305), Vo Le Trung Nguyen (SE190220)
**Generated:** 2026-06-04 · **Language:** English

> This is the de-duplicated UNION of the five members' final-included papers. It is **not** re-screened — every paper a member included is kept once. Where a paper is also in **DUNG's** set, DUNG's primary-source-verified numbers/venue/DOI are used as authoritative ("Verified? = yes (primary)"); otherwise the data is "as-reported" by the contributing member(s).

---

## Summary statistics

| Quantity | Value |
|----------|-------|
| Raw inclusions (sum over members) | **85** — DUNG 13 + HUY 13 + DAT 20 + THUAN 11 + NGUYEN 28 |
| Unique papers after de-duplication | **59** |
| Duplicate collapses | 26 (overlap rate **30.6%**) |
| Papers shared by ≥ 2 members | 15 |
| Papers shared by ≥ 3 members | 7 |
| Most shared (4 members) | KAT, RESTSpecIT, LlamaRestTest, DeepREST |

Overlap of ~31% is in the normal 30–60% band for a same-topic team (the members deliberately explored different sub-areas: DUNG/HUY = LLM-vs-baseline core, DAT = classic fuzzers + security, THUAN = coverage classics + RAG, NGUYEN = broad 2024–2026 frontier).

### Per-member inclusion counts
| Member | Included | Source of data |
|--------|:--------:|----------------|
| Nguyen Tien Dung (SE190034) | 13 | primary-verified (full-text + arXiv/DOI checked) |
| Nguyen Hoang Huy (SE190240) | 13 | member evidence table |
| Nguyen Thanh Dat (SE190239) | 20 | member `03_final_included.csv` (v2 = Include) |
| Nguyen Le Thuan (SE190305) | 11 | member evidence table |
| Vo Le Trung Nguyen (SE190220) | 28 | member evidence table / CSV |

---

## A. Multi-member papers (included by ≥ 2 members) — the verified core

| # | Paper (Title, Year, Venue) | Tool/LLM | Key result (specific number) | DOI / arXiv | Contributed by | Verified? |
|---|---------------------------|----------|------------------------------|-------------|----------------|-----------|
| 1 | KAT: Dependency-aware Automated API Testing with LLMs (2024, ICST) | GPT-3.5-turbo-1106 | +15.7% status-code coverage (59.2→74.9%); 24 undocumented codes | 10.1109/ICST60714.2024.00017 | DUNG, HUY, DAT, NGUYEN (4) | yes (primary) |
| 2 | You Can REST Now / RESTSpecIT (2024, arXiv) | DeepSeek V3 / GPT-4.1-mini / GPT-3.5 | 88.62% route discovery (avg); 5xx in 4 APIs | 10.48550/arXiv.2402.05102 | DUNG, HUY, DAT, NGUYEN (4) | yes (primary) |
| 3 | LlamaRestTest: Effective REST API Testing with Small LMs (2025, FSE) | Llama3-8B fine-tuned/quantized | 204 faults vs EvoMaster 130; 55.8% method coverage | 10.1145/3715737 | DUNG, HUY, THUAN, NGUYEN (4) | yes (primary) |
| 4 | DeepREST: Test Generation via Deep RL (2024, ASE) | Deep RL (curiosity-driven) | +17–77% branch coverage; +25–67% unique faults vs 5 baselines | 10.1145/3691620.3695511 | DUNG, HUY, DAT, THUAN (4) | yes (primary) |
| 5 | Leveraging LLMs to Improve REST API Testing / RESTGPT (2024, ICSE-NIER) | GPT-3.5 Turbo | 97% rule-extraction precision; 72.68% valid inputs (+329% vs ARTE) | 10.1145/3639476.3639769 | DUNG, HUY, NGUYEN (3) | yes (primary) |
| 6 | APITestGenie: API Test Generation through Generative AI (2024 preprint; 2026 AST) | GPT-4-Turbo | 57.3% valid scripts (1 try) → 80% (3 tries); v2 reports 89% | 10.1145/3793654.3793743 | DUNG, HUY, NGUYEN (3) | yes (primary) |
| 7 | AutoRestTest: Multi-Agent + Semantic Graphs + LLM inputs (2025, ICSE) | GPT-3.5 Turbo + MARL + SPDG | 58.3% method/line coverage; 42 500-errors vs EvoMaster 20 | 10.1109/ICSE55347.2025.00179 | DUNG, THUAN, NGUYEN (3) | yes (primary) |
| 8 | RestTSLLM: Combining TSL and LLM (2025, SBES) | Claude 3.5 Sonnet (best of 7 LLMs) | ≈71.7% branch coverage; ≈40.8% mutation score † | 10.5753/sbes.2025.9670 | DUNG, NGUYEN (2) | as-reported † |
| 9 | LogiAgent: Automated Logical Testing for REST (2025, arXiv) | GPT-4o-mini (3 agents) | 71.78% line coverage; 234 logical issues; 49 crashes | 10.48550/arXiv.2503.15079 | DUNG, HUY (2) | yes (primary) |
| 10 | RESTifAI: LLM Workflow for Reusable Testing (2026, ICSE Demo) | GPT-4.1-mini | 128/134 operations on OhSome; 60.87% failures = bugs | 10.48550/arXiv.2512.08706 | DUNG, NGUYEN (2) | yes (primary) |
| 11 | Automated Test Generation for REST APIs: No Time to Rest Yet (2022, ISSTA) | Empirical study of 10 tools | EvoMaster-WB 52.76% line (best); maps coverage ceilings on EMB | 10.1145/3533767.3534401 | DUNG, DAT (2) | yes (primary) |
| 12 | LLM-assisted Mutation for Whitebox API Testing / MioHint (2025, arXiv) | GPT-4o (mutation) | +47.72 pp target coverage vs EvoMaster; +4.95% line coverage | 10.48550/arXiv.2504.05738 | HUY, NGUYEN (2) | as-reported |
| 13 | AutoRestTest: A Tool for Automated REST API Testing (2025, ICSE Demo) | GPT-3.5 Turbo + MARL | tool-demo of #7; successful operations, unique 500-errors | 10.48550/arXiv.2501.08600 | THUAN, NGUYEN (2) | as-reported |
| 14 | SAINT: Service-level Integration Test Generation (2025, arXiv) | LLM agents + program analysis | code/DB-interaction coverage + fault detection on 8 Java services | 10.48550/arXiv.2511.13305 | THUAN, NGUYEN (2) | as-reported |
| 15 | RESTestBench: Benchmark for LLM-Generated Tests from NL Requirements (2026, arXiv) | GPT-4o / Claude 3 | requirements-based mutation testing; effectiveness drops on faulty code | — (arXiv 2026) | THUAN, NGUYEN (2) | as-reported |

† RestTSLLM (#8): the SBES 2025 abstract confirms Claude 3.5 Sonnet best of 7 LLMs on success/coverage/mutation, but the exact figures (≈71.7% / ≈40.8%) are from a secondary index, not re-verified from the primary PDF — provisional pending camera-ready.

---

## B. Single-member papers (44)

### B1 — DUNG (2): classic baselines, primary-verified
| # | Paper (Title, Year, Venue) | Tool/approach | Key result | DOI | Verified? |
|---|---------------------------|---------------|-----------|-----|-----------|
| 16 | RESTful API Automated Test Case Generation with EvoMaster (2019, ACM TOSEM) | EvoMaster (white-box, search-based) | 38 real bugs; generated coverage 41% vs manual 82% | 10.1145/3293455 | yes (primary) |
| 17 | Morest: Model-based RESTful API Testing with Execution Feedback (2022, ICSE) | Morest (RESTful-service Property Graph) | 44 bugs (13 previously undetectable); +26–103% coverage | 10.1145/3510003.3510133 | yes (primary) |

### B2 — HUY (5)
| # | Paper (Title, Year, Venue) | Tool/LLM | Key result | DOI / arXiv |
|---|---------------------------|----------|-----------|-------------|
| 18 | Enhancing REST API testing with NLP techniques (2023, ISSTA) | NLP (NER + embeddings) + RESTler/EvoMaster | line/branch coverage gains; +4% unique 500-errors | 10.1145/3597926.3598131 |
| 19 | An approach to generating API test scripts using GPT (2023, APSEC) | GPT-3.5 Turbo | status-code coverage (2xx/4xx/5xx) on Swagger APIs | 10.1145/3628797.3628947 |
| 20 | RESTless: Enhancing REST API fuzzing with LLMs in cloud (2024, IEEE TSC) | GPT-3.5 + RESTler/EvoMaster | 38 vulnerabilities on 9 cloud services; 16 vendor-confirmed | 10.1109/TSC.2024 (vol.17) |
| 21 | MASTEST: LLM-Based Multi-Agent System for RESTful API Tests (2025, arXiv) | GPT-4o + DeepSeek V3.1 (multi-agent) | DeepSeek better on data-type correctness; GPT-4o on operation coverage | 10.48550/arXiv.2511.18038 |
| 22 | Automated REST API Black-box Test Generation in Practice (2026, ICST) | RestTestGen + LLM value generation | industrial experience report; operation coverage + faults | — |

### B3 — DAT (16): classic fuzzers, RL baselines, security & misc
| # | Paper (Title, Year) | Tool/approach | Key result | Identifier |
|---|--------------------|---------------|-----------|-----------|
| 23 | REST-ler: Automatic Intelligent REST API Fuzzing (2018) | RESTler (stateful fuzzer) | foundational stateful fuzzing; 5xx bug discovery | 10.1109/ICSE.2019.00083 |
| 24 | Adaptive REST API Testing with Reinforcement Learning / ARAT-RL (2023) | Q-learning RL | +119% branch coverage; more unique bugs vs baselines | arXiv (CORE 149190100) |
| 25 | AI-driven web API testing (2021, ACM) | AI-based API fuzzer | code coverage + bug-discovery improvements | CORE 148775050 |
| 26 | Automated Black-box Testing of Mass Assignment Vulnerabilities in RESTful APIs (2023, IEEE) | black-box vulnerability tester | mass-assignment vulnerability detection | CORE 150890236 |
| 27 | FuzzTheREST — Intelligent Automated Blackbox RESTful API Fuzzer (2023) | black-box fuzzer | automated REST fuzzing | CORE 152127785 |
| 28 | Leveraging LLMs to Automatically Infer RESTful API Specifications (2023) | GPT-3.5 (zero-shot) | route/parameter spec inference feasibility | CORE 146186703 |
| 29 | RESTgym: Infrastructure for Empirical Assessment of REST API Testing Tools (2025) | benchmark infrastructure (ARAT-RL, DeepREST) | operation/code coverage + fault assessment on 11 APIs | CORE 295908352 |
| 30 | RESTful API Testing Methodologies: Rationale, Challenges, Solution Directions (2022) | methodology overview | taxonomy of REST API testing approaches | CORE 135436615 |
| 31 | Structure and Feedback in Cloud Service API Fuzzing (2020) | feedback-guided fuzzer | structural feedback in cloud API fuzzing | CORE 124660504 |
| 32 | API Testing on Smart City Platform (2023) | platform API testing | applied API testing case study | CORE 147642456 |
| 33 | Stateful Security Testing of Web APIs (2025) | stateful security tester | security-oriented stateful testing | CORE 294342718 |
| 34 | Security Testing of Web APIs (2025) | API security testing | web API security test generation | CORE 294350365 |
| 35 | TypeScript Application Generation from REST API Descriptions (2020) | code generation | client code generation from API descriptions | CORE 16149799 |
| 36 | A Link Generator for OpenAPI-to-GraphQL Translations (2020) | OpenAPI→GraphQL tool | utility of translated schemas | CORE 85806732 |
| 37 | Generating Backend Applications with REST API in Haskell (2025) | code generation | backend + REST API generation (Haskell) | CORE 294904871 |
| 38 | JepREST 2.0: Testing REST Applications With Customized Semantics (2025) | semantics-customized tester | REST application testing framework | CORE 300217997 |

### B4 — THUAN (6): coverage classics + RAG/LLM E2E
| # | Paper (Title, Year, Venue) | Tool/LLM | Key result | Identifier |
|---|---------------------------|----------|-----------|-----------|
| 39 | Diversity-based web test generation (2019, ESEC/FSE) | diversity-guided generator | 65% branch coverage on 6 web apps | S2 3798dce1 |
| 40 | Test coverage criteria for RESTful web APIs (2019, A-TEST@FSE) | EvoMaster | 88% endpoint coverage on 5 REST APIs | S2 822332ba |
| 41 | Improving Test Case Generation for REST APIs via Hierarchical Clustering (2021) | RESTest | 78% branch coverage on 10 REST APIs | S2 8d6e8036 |
| 42 | ARTE: Automated Generation of Realistic Test Inputs for Web APIs (2023, IEEE TSE) | ARTE (knowledge-base) | 85% input validity rate on 7 APIs | S2 c8f2430b |
| 43 | Intent-Based E2E Automated Test Case Generation for Web Apps using LLM (2025) | LLaMA-3 | 76% execution success rate on 3 web apps | S2 a2c778c2 |
| 44 | Method for Prioritizing Auto-generated Test Cases for REST APIs based on OpenAPI (2026) | prioritization method | test-case prioritization on 5 OpenAPI specs | S2 e01733cf |

### B5 — NGUYEN (15): 2024–2026 frontier (some adjacent-scope, flagged)
| # | Paper (Title, Year, Venue) | Tool/LLM | Key result | DOI / arXiv | Scope note |
|---|---------------------------|----------|-----------|-------------|-----------|
| 45 | TAPE: Technology Adoption Performance Evaluation for industrial REST APIs (2024, ASE J.) | StarCoder + EvoMaster | coverage/scalability at Volkswagen AG | 10.1007/s10515-024-00477-2 | core |
| 46 | Assessing REST API Test Generation Strategies with Log Coverage (2026, arXiv) | Claude Opus 4.6 / GPT-5.2-Codex + EvoMaster | log coverage; Claude +28.4% unique templates vs human | — | core |
| 47 | DynER: Test Case Generation for RESTful API Fuzzers Guided by Dynamic Error Responses (2024, Electronics) | LLM + RESTler | pass rate +41.21% (WordPress); 3 new bugs | 10.3390/electronics13173476 | core |
| 48 | Automating REST API Postman Test Cases Using LLM (2024, arXiv) | OpenAI LLM | diverse Postman scenarios; efficiency gain (no coverage metric) | 10.48550/arXiv.2404.10678 | core |
| 49 | REST API Fuzzing Using API Dependencies and LLMs (2026, Eng. Proceedings) | LLM + dependency analysis | dependency-aware fuzzing improvement | 10.3390/engproc2025120042 | core |
| 50 | ARMeta: Multi-Agent LLM-based Metamorphic Testing for REST APIs (2026, arXiv) | LLM multi-agent | metamorphic relations (Given-When-Then) | — | adjacent (metamorphic) |
| 51 | RBCTest: LLMs to Mine and Verify Oracles of API Response Bodies (2025, arXiv) | LLM oracle mining | constraint-mining precision 85.1–93.6%; 46 mismatches | 10.48550/arXiv.2504.17287 | adjacent (oracle) |
| 52 | LoBREST: Log-based, Business-aware REST API Testing (2026, arXiv) | LLM business-rule extraction | log + business-rule coverage | — | core |
| 53 | From Requirements to Executable Tests: LLM-Based System Test Generation (2026, Vilnius U.) | LLM + OpenAPI | endpoint reachability; full coverage on 2 APIs | 10.15388/lmitt.2026.13 | core |
| 54 | BOSQTGEN: Breaking the Sound Barrier in Test Generation (2025, arXiv) | LLM + combinatorial | 82% avg code coverage; +20% vs prior SOTA | 10.48550/arXiv.2510.19777 | core |
| 55 | Generating REST API Tests With Descriptive Names (2025, arXiv) | LLM + EvoMaster | test readability / naming accuracy | 10.48550/arXiv.2512.01690 | adjacent (naming) |
| 56 | An Intelligent Agent for Automated Test Generation from OpenAPI Specs (2025, WBOTS) | LLM agent | test-collection generation from OpenAPI | 10.5753/wbots.2025.15217 | core (short workshop) |
| 57 | LRASGen: LLM-based RESTful API Specification Generation (2026, ACM TOSEM) | LLM spec generation | OpenAPI spec completeness/accuracy | 10.1145/3810241 | adjacent (spec gen) |
| 58 | SmartAPIForge: No-Code Platform for Automated REST API Generation from NL (2025, IJARCCE) | LLM + micro-VMs | deploy success 96%; OpenAPI validation 97% | 10.17148/ijarcce.2025.141262 | adjacent (API gen) |
| 59 | AI Agent-based BAC Testing Framework (2026, Zenodo artifact) | GPT-4.1 agent pipeline | broken-access-control test generation | 10.5281/zenodo.18524562 | adjacent (security) |

---

## Most-shared papers (consensus map)

| Paper | DUNG | HUY | DAT | THUAN | NGUYEN | Total |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|
| KAT (2024) | ✓ | ✓ | ✓ | — | ✓ | **4** |
| RESTSpecIT / You Can REST Now (2024) | ✓ | ✓ | ✓ | — | ✓ | **4** |
| LlamaRestTest (2025) | ✓ | ✓ | — | ✓ | ✓ | **4** |
| DeepREST (2024) | ✓ | ✓ | ✓ | ✓ | — | **4** |
| RESTGPT (2024) | ✓ | ✓ | — | — | ✓ | **3** |
| APITestGenie (2024/2026) | ✓ | ✓ | — | — | ✓ | **3** |
| AutoRestTest (2025) | ✓ | — | — | ✓ | ✓ | **3** |
| RestTSLLM, LogiAgent, RESTifAI, No-Time-to-Rest-Yet, MioHint, AutoRestTest-demo, SAINT, RESTestBench | (various pairs) | | | | | **2 each** |

---

## Conflicts noted (resolved per template rule "re-read the original")

1. **DeepREST coverage numbers differ across members** — DAT reported "+99% branch", THUAN "90% coverage", DUNG/HUY the primary "+17–77% branch vs 5 baselines". **Kept DUNG's primary-verified range** (read from arXiv 2408.08594 / ASE 2024). DAT/THUAN figures appear to be single-baseline or mis-transcribed.
2. **KAT year** — DAT labels it 2025, others 2024. **Kept 2024** (ICST 2024, DOI 10.1109/ICST60714.2024.00017).
3. **APITestGenie venue/year** — 2024 arXiv preprint vs 2026 AST publication. **One canonical row**; published venue AST 2026 (DOI 10.1145/3793654.3793743), numbers from the assessed 2024 preprint.
4. **RestTSLLM figures** — flagged provisional (secondary source), see † above.
5. **AutoRestTest main paper (#7) vs tool-demo (#13)** — kept as two rows (different publications: ICSE 2025 research track vs ICSE 2025 Demonstrations); DUNG had excluded the demo as superseded, but THUAN/NGUYEN included it, so the union keeps it.
6. **"Leveraging LLMs to *Infer* RESTful API Specs" (DAT #28, 2023) vs "You Can REST Now / RESTSpecIT" (#2, 2024)** — same author (Decrop) but distinct works (a 2023 spec-inference paper vs the 2024 documentation+testing tool); kept as separate rows.

---

## Notes

- **Verification tiers:** 11 of the 15 multi-member rows + DUNG's 2 baselines are **primary-source verified** (DUNG's set). All other rows are **as-reported** by the contributing member and should be re-checked against the primary source before any number is quoted in the final paper.
- **Scope flags (NGUYEN B5):** a few singletons are adjacent rather than core "test generation for REST APIs" — spec generation (LRASGen), API generation (SmartAPIForge), test naming (Generating Descriptive Names), oracle mining (RBCTest), metamorphic (ARMeta), security/BAC (#59). They are retained because the member included them, but flagged so the team can drop them when narrowing to the final RQ.
- **LLM landscape across 59 papers:** GPT family dominates; non-OpenAI models appear in RestTSLLM (Claude 3.5/DeepSeek/Qwen), RESTSpecIT (DeepSeek), MASTEST (DeepSeek), AssessingLogCoverage (Claude Opus/GPT-5.2), LlamaRestTest (open-source Llama3, fine-tuned). Classic non-LLM baselines: EvoMaster, RESTler, Morest, RESTest, ARTE, ARAT-RL, DeepREST.
- **Audit trail:** per-member files under each `*/SLR/` directory; DUNG's `SLR/quality-assessment.md` scores the 13 verified papers (mean 5.73/6).
