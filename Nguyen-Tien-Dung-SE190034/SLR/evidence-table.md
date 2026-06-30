# Evidence Table — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Number of papers:** N = 13 (2019–2026)
**Verification:** every row was checked against its primary source (arXiv / publisher page) on 2026-06-04; the specific numbers below are quoted from those sources. Papers #1–#9 are LLM-based; papers #10–#13 are classic non-LLM baselines / empirical references kept under IC4 to anchor the comparison. Per-paper quality scores are in `quality-assessment.md` (mean 5.73 / 6).

> Column legend: **Tool/LLM** (model + config) · **Input** (what the approach reads) · **Dataset** · **Baseline** (what it is compared against) · **Metrics** · **Results** (specific numbers) · **Limitations** · **PICO/RQ link** (which part of the experiment RQ this informs).

---

## A. LLM-based approaches (#1–#9)

### 1. Kim et al. (2024) — "Leveraging Large Language Models to Improve REST API Testing" — ICSE-NIER 2024
- **Tool/LLM:** RESTGPT — GPT-3.5 Turbo; few-shot, extracts rules + generates values from OpenAPI + NL descriptions.
- **Input:** OpenAPI specification + natural-language descriptions in the spec.
- **Dataset:** 9 real-world REST APIs (Spotify, YouTube, LanguageTool, REST-Countries, FDIC, Genome-Nexus, OhSome, OMDb …).
- **Baseline:** NLP2REST (with/without validation), ARTE.
- **Metrics:** rule-extraction precision/recall/F1; value-generation valid-input rate.
- **Results:** rule extraction **97% precision, 92% recall, 94% F1** (vs NLP2REST 79%/91%/85%); value generation **72.68% valid inputs**, a **+329%** improvement over ARTE (16.93%).
- **Limitations:** depends on description quality in the spec; LLM cost; not yet end-to-end executable test scripts (a precursor that enriches specs).
- **PICO/RQ link:** I (LLM from spec) · O1 (input validity → coverage). [DOI 10.1145/3639476.3639769](https://doi.org/10.1145/3639476.3639769) · [arXiv:2312.00894](https://arxiv.org/abs/2312.00894)

### 2. Le et al. (2024) — "KAT: Dependency-aware Automated API Testing with Large Language Models" — ICST 2024
- **Tool/LLM:** KAT — GPT-3.5-turbo-1106 (temperature 0); structured prompts; LLM infers operation dependencies + test data.
- **Input:** OpenAPI Specification (YAML) — endpoints, parameters, request bodies, response schemas, NL descriptions.
- **Dataset:** 12 real-world RESTful services.
- **Baseline:** RestTestGen (v23.09).
- **Metrics:** status-code coverage (2xx, 4xx), generation efficiency, undocumented status codes, false positives, 500-errors.
- **Results:** **+15.7%** overall coverage (59.2% → 74.9%); **+18.1%** on 2xx (56.4% → 74.5%); **+8.4%** on 4xx (67.5% → 75.9%); **24** additional undocumented status codes; fewer false positives (94 vs 119); equal 500-error detection (23 each).
- **Limitations:** GPT hallucination risk; test-oracle uncertainty (spec ≠ implementation); only 12 services.
- **PICO/RQ link:** I · O1 (status-code coverage) · O3 (4xx error codes). [DOI 10.1109/ICST60714.2024.00017](https://doi.org/10.1109/ICST60714.2024.00017) · [arXiv:2407.10227](https://arxiv.org/abs/2407.10227)

### 3. Decrop et al. (2024) — "You Can REST Now: Automated REST API Documentation and Testing via LLM-Assisted Request Mutations" (RESTSpecIT) — arXiv
- **Tool/LLM:** RESTSpecIT — DeepSeek V3 / GPT-4.1-mini / GPT-3.5-turbo; zero-shot "in-context prompt masking" to mutate HTTP requests.
- **Input:** minimal HTTP requests + JSON config (no full spec required — it *infers* the spec while testing).
- **Dataset:** 10 public REST APIs from the PRAB benchmark (+ 3 mock local APIs for data-leakage checks).
- **Baseline:** ground-truth OpenAPI specs; RESTler used to validate the inferred specs.
- **Metrics:** route/parameter discovery accuracy, route coverage, undocumented findings, 5xx triggering, cost.
- **Results:** route **discovery** **88.62%** average (DeepSeek V3), 81.16% (GPT-4.1), 79.84% (GPT-3.5); parameter discovery up to **89.25%**; RESTler compiled and covered all routes in every generated spec; found **10 undocumented routes + 4 undocumented parameters**; triggered **5xx errors in 4 APIs**; cost as low as $0.004/run. (This is primarily a *spec-inference + black-box-testing* tool, hence "discovery" rather than test-suite coverage.)
- **Limitations:** data-leakage risk (LLM may recall training docs); false positives on inferred parameters; weak on advanced types; predominantly GET-focused benchmark.
- **PICO/RQ link:** I · O1 (route coverage) · O3 (5xx). [arXiv:2402.05102](https://arxiv.org/abs/2402.05102)

### 4. Pereira et al. (2024) — "APITestGenie: Automated API Test Generation through Generative AI" — arXiv 2024 (2409.03838); extended/published at AST 2026
- **Tool/LLM:** APITestGenie — GPT-4-Turbo (128k); RAG over the spec; three requirement-detail tiers (TELeR prompt taxonomy).
- **Input:** business requirements (user stories) **+** OpenAPI specification → executable test scripts.
- **Dataset:** 10 real-world APIs.
- **Baseline:** positions against EvoMaster / RESTGPT / RESTSpecIT (qualitative); no head-to-head coverage run.
- **Metrics:** valid-script success rate, generation time, cost, test-case validity breakdown.
- **Results:** **57.3%** valid scripts on a single attempt (43/75); **80%** chance of ≥1 valid script within 3 attempts; ~126 s and €0.37 per script; 68% of individual test cases valid; 12 real API defects surfaced; 19 hallucinations noted. (A 2026 extension, [arXiv:2604.02039](https://arxiv.org/abs/2604.02039), reports 89% over ≤3 attempts.)
- **Limitations:** results may not generalize across domains; depends on high-quality requirements + specs; reliance on closed-source LLM (security/cost); semantic errors dominate failures.
- **PICO/RQ link:** I (LLM from requirements + spec) · O (executable tests). [arXiv:2409.03838](https://arxiv.org/abs/2409.03838) (2024 preprint, assessed here) · published version [AST 2026, DOI 10.1145/3793654.3793743](https://doi.org/10.1145/3793654.3793743)

### 5. Barradas et al. (2025) — "Combining TSL and LLM to Automate REST API Testing: A Comparative Study" (RestTSLLM) — SBES 2025
- **Tool/LLM:** RestTSLLM — 7 LLMs compared (Claude 3.5 Sonnet, DeepSeek R1, Qwen 2.5-32B, Sabiá-3 …); prompt engineering with a Test Specification Language (TSL) intermediate representation; xUnit output.
- **Input:** OpenAPI specifications.
- **Dataset:** 6 REST API projects (Todo, Supermarket, Books, Hotels, Restaurants, URL-Shortener).
- **Baseline:** TSL-only baseline; cross-model comparison.
- **Metrics:** test success rate, branch coverage, mutation score.
- **Results:** the arXiv abstract confirms **Claude 3.5 Sonnet outperformed all other LLMs across success rate, coverage and mutation score**. The specific figures circulated for it — **≈71.7% branch coverage, ≈40.8% mutation score, 100% success over 230 test cases** — come from the full text / a secondary index (emergentmind), **not the abstract**, and could not be re-confirmed from the primary PDF; treat them as provisional pending the camera-ready (see † below).
- **Limitations:** small set of 6 (self-built) APIs; LLM-dependent variance; full limitations only in PDF.
- **PICO/RQ link:** I · O1 (branch coverage) · O2 (mutation score ≈ fault sensitivity). [DOI 10.5753/sbes.2025.9670](https://doi.org/10.5753/sbes.2025.9670) · [arXiv:2509.05540](https://arxiv.org/abs/2509.05540)

### 6. Kim et al. (2025) — "A Multi-Agent Approach for REST API Testing with Semantic Graphs and LLM-Driven Inputs" (AutoRestTest) — ICSE 2025
- **Tool/LLM:** AutoRestTest — GPT-3.5 Turbo + multi-agent reinforcement learning (MARL) + Semantic Property Dependency Graph (SPDG); few-shot value agent.
- **Input:** OpenAPI specification.
- **Dataset:** 12 real-world services (incl. Spotify, FDIC, OhSome + 9 open-source).
- **Baseline:** ARAT-RL, EvoMaster, MoRest, RESTler (+ RESTGPT-enhanced specs).
- **Metrics:** method/line/branch coverage, operation coverage, 500-error fault detection.
- **Results:** **58.3% method, 58.3% line, 32.1% branch** coverage (15.2–26.8 pp above the best baseline); **42** 500-errors vs **EvoMaster 20**, MoRest 20, RESTler 14, ARAT-RL 33; ablation: removing the LLM drops coverage 10.9–12.8%.
- **Limitations:** MARL training overhead; results on 12 services; cost of GPT calls.
- **PICO/RQ link:** I · **C (vs EvoMaster)** · O1 (coverage) · O2 (500-error faults). [DOI 10.1109/ICSE55347.2025.00179](https://doi.org/10.1109/ICSE55347.2025.00179) · [arXiv:2411.07098](https://arxiv.org/abs/2411.07098)

### 7. Kim et al. (2025) — "LlamaRestTest: Effective REST API Testing with Small Language Models" — FSE 2025
- **Tool/LLM:** LlamaRestTest — Llama3-8B fine-tuned + quantized (2/4/8-bit); two specialised models (LlamaREST-EX for values, LlamaREST-IPD for inter-parameter dependencies).
- **Input:** OpenAPI specification + mined parameter-example / dependency datasets.
- **Dataset:** 12 real-world services (Spotify, FDIC, OhSome, Genome-Nexus, YouTube …).
- **Baseline:** ARAT-RL, EvoMaster, RESTler, MoRest, RESTGPT.
- **Metrics:** method/line/branch coverage, operations processed, 500-error faults, value validity, dependency detection.
- **Results:** **55.8% method, 55.3% line, 28.3% branch** (above EvoMaster 45.8/45.3/17.8); **204 faults** in 10 runs vs **EvoMaster 130**, ARAT-RL 160, RESTler/MoRest 130; value validity **72.44%** (vs RESTGPT 68.82%); a small fine-tuned model matches/beats GPT.
- **Limitations:** fine-tuning needs large mined datasets; black-box only.
- **PICO/RQ link:** I (small LM) · **C (vs EvoMaster)** · O1 · O2. [DOI 10.1145/3715737](https://doi.org/10.1145/3715737) · [arXiv:2501.08598](https://arxiv.org/abs/2501.08598)

### 8. Zhang et al. (2025) — "LogiAgent: Automated Logical Testing for REST Systems with LLM-Based Multi-Agents" — arXiv preprint 2025 (not found in ICWS 2025 proceedings)
- **Tool/LLM:** LogiAgent — GPT-4o-mini; 3 agents (Scenario Generator over an API Relationship Graph, Request Executor, Response Validator as a logical oracle).
- **Input:** API specification + API Relationship Graph.
- **Dataset:** 12 systems (PetStore, UK Parliament Bills, Genome-Nexus, REST-Countries, LanguageTool …; 556–677k LOC).
- **Baseline:** RESTler, EvoMaster, Morest, ARAT-RL (1,000-request / 1-hour budgets).
- **Metrics:** branch/line/method coverage, logical-issue detection accuracy, 5xx crashes, false-positive rate.
- **Results:** **39.98% branch, 71.78% line, 73.06% method** (beats best baseline 34.90/62.38/67.24); **234** logical issues (139 bugs + 95 enhancements) at **66.19% accuracy**; **49** distinct 500-crashes; **33.81% false positives**.
- **Limitations:** logical-oracle accuracy 66.19% (still false positives from LLM hallucination); struggles on complex business-logic domains; depends on documentation quality.
- **PICO/RQ link:** I · O1 (coverage) · O2 (logical bugs) · O3 (5xx crashes). [arXiv:2503.15079](https://arxiv.org/abs/2503.15079)

### 9. Kogler et al. (2026) — "RESTifAI: LLM-Based Workflow for Reusable REST API Testing" — ICSE 2026 Demonstrations (arXiv 2025)
- **Tool/LLM:** RESTifAI — Azure OpenAI GPT-4.1-mini; LLM used selectively in a workflow (happy-path scenarios + derived negative cases) for reliability.
- **Input:** OpenAPI/endpoint definitions; produces reusable CI/CD-ready tests.
- **Dataset:** LanguageTool, Genome-Nexus, RestCountries, OhSome, FDIC + 2 real-world industrial services (CASABLANCA hotel software).
- **Baseline:** AutoRestTest, LogiAgent (APITestGenie referenced).
- **Metrics:** operation coverage, line coverage, tokens/test-case, bug-discovery rate.
- **Results:** **128/134 operations** on OhSome vs **AutoRestTest 33**; line coverage 28–72%; **~37%** more token-efficient than LogiAgent (32,370 vs 51,188 tokens/test); on a real service **60.87%** of failures revealed real bugs/enhancements.
- **Limitations:** demonstration-track scope; happy-path-first design may limit negative-case depth; single LLM backend.
- **PICO/RQ link:** I · O1 (operation/line coverage) · O2 (bug detection). [arXiv:2512.08706](https://arxiv.org/abs/2512.08706)

---

## B. Classic non-LLM baselines & empirical references (#10–#13)

### 10. Arcuri (2019) — "RESTful API Automated Test Case Generation with EvoMaster" — ACM TOSEM
- **Tool/approach:** EvoMaster — white-box, **search-based** (genetic algorithm / whole-test-suite, later MIO).
- **Input:** Swagger/OpenAPI specification (+ source code for white-box instrumentation).
- **Dataset:** 3 RESTful services (FeaturesService 18 endpoints, an industrial service 10, ScoutApi 49).
- **Baseline:** **manually written test suites** already in those projects.
- **Metrics:** statement coverage, 5xx triggered, real bugs found.
- **Results:** found **38 real bugs**; but **generated coverage was lower than manual** — FeaturesService **41% (generated) vs 82% (manual)**, industrial 18% vs 47%, ScoutApi 20% vs 43%.
- **Limitations:** string constraints, DB and external-service access limit coverage; only 3 services (external-validity threat); generated suites below human coverage.
- **PICO/RQ link:** **C (key baseline + the manual-vs-tool comparison)** · O1 (coverage) · O2 (bugs). [DOI 10.1145/3293455](https://doi.org/10.1145/3293455) · [arXiv:1901.01538](https://arxiv.org/abs/1901.01538)

### 11. Kim et al. (2022) — "Automated Test Generation for REST APIs: No Time to Rest Yet" — ISSTA 2022
- **Tool/approach:** empirical comparison of **10 REST API testing tools** (EvoMaster WB/BB, RESTler, RestTestGen, RESTest, Schemathesis, Dredd, Tcases, bBOXRT, APIFuzzer).
- **Input:** OpenAPI/Swagger (tool-dependent).
- **Dataset:** **20 open-source RESTful services** (the basis of the EvoMaster Benchmark, EMB).
- **Baseline:** cross-tool (no single baseline); 1 hour × 10 trials each.
- **Metrics:** line/branch/method coverage, unique 500-errors.
- **Results:** **EvoMaster-WB best at 52.76% line, 36.08% branch, 52.86% method**, 33.3 avg 500-errors; black-box tools 33–45% line; **no tool exceeds ~53% line coverage** — large headroom remains.
- **Limitations:** 1-hour budget; 20 services; tools use different inputs/strategies.
- **PICO/RQ link:** **C (baseline landscape + EMB benchmark)** · O1 (code-coverage ceilings: best tool ~53% line). [DOI 10.1145/3533767.3534401](https://doi.org/10.1145/3533767.3534401) · [arXiv:2204.08348](https://arxiv.org/abs/2204.08348)

### 12. Liu et al. (2022) — "Morest: Model-based RESTful API Testing with Execution Feedback" — ICSE 2022
- **Tool/approach:** Morest — **model-based** (RESTful-service Property Graph, dynamically updated with execution feedback).
- **Input:** OpenAPI/Swagger specification.
- **Dataset:** 6 projects (Petstore, SpreeCommerce, Bitbucket, LanguageTool, FeatureService, Magento; up to 315k LOC).
- **Baseline:** EvoMaster (black-box), RestTestGen, RESTler.
- **Metrics:** line coverage, operations invoked, bugs detected.
- **Results:** **+152–232% more operations**, **+26–103% coverage**, **+40–216% more bugs** vs the best baseline; **44 bugs** found, **13 previously undetectable**; 2 confirmed in Bitbucket.
- **Limitations:** empirically-set config; cannot model undocumented endpoints; spec-vs-implementation gap.
- **PICO/RQ link:** **C (baseline)** · O1 (coverage) · O2 (bugs). [DOI 10.1145/3510003.3510133](https://doi.org/10.1145/3510003.3510133) · [arXiv:2204.12148](https://arxiv.org/abs/2204.12148)

### 13. Corradini et al. (2024) — "DeepREST: Automated Test Case Generation for REST APIs Exploiting Deep Reinforcement Learning" — ASE 2024
- **Tool/approach:** DeepREST — **deep reinforcement learning** with curiosity-driven exploration + mutation; learns implicit constraints beyond the spec (no LLM).
- **Input:** OpenAPI Specification (black-box).
- **Dataset:** **11 benchmark REST APIs** (REST-Countries, User-Management, Market, Project-Tracking-System, Features-Service, NCS, SCS, Genome-Nexus, Person-Controller, Blog, LanguageTool — EMB-style).
- **Baseline:** RestTestGen, Morest, RESTler, ARAT-RL, Schemathesis.
- **Metrics:** branch/line/method coverage, unique faults; Wilcoxon signed-rank (p < 0.05).
- **Results:** **+17–77% branch coverage** and **+25–67% more unique faults** vs baselines; Project-Tracking-System **+16–62% coverage**; all major gains statistically significant.
- **Limitations:** black-box only; depends on spec quality; RL training overhead.
- **PICO/RQ link:** **C (strong RL baseline)** · O1 (coverage) · O2 (faults). [DOI 10.1145/3691620.3695511](https://doi.org/10.1145/3691620.3695511) · [arXiv:2408.08594](https://arxiv.org/abs/2408.08594)

---

## C. Cross-comparison matrix (the gap, made visible)

| # | Tool / LLM | Best coverage reported | Fault / bug result | Dataset | Uses EMB? | Compares **vs EvoMaster**? | Compares **vs manual**? | **Pre-seeded faults (ground-truth Recall)?** |
|---|------------|------------------------|--------------------|---------|:---------:|:-----:|:-----:|:-----:|
| 1 | RESTGPT (GPT-3.5) | — (94% F1, rule extr.) | 72.68% valid inputs | 9 real APIs | No | No | No | **No** |
| 2 | KAT (GPT-3.5) | 74.9% status-code | 23 500-errors; +24 undoc. codes | 12 real APIs | No | No | No | **No** |
| 3 | RESTSpecIT (DeepSeek/GPT) | ~88.6% route disc. (avg) | 5xx in 4 APIs | 10 PRAB APIs | No | No | No | **No** |
| 4 | APITestGenie (GPT-4-Turbo) | — | 57→80% valid scripts; 12 defects | 10 real APIs | No | No (qualitative) | No | **No** |
| 5 | RestTSLLM (Claude 3.5) | ≈71.7% branch † | ≈40.8% mutation † | 6 APIs | No | No | No | Partial (auto mutants) |
| 6 | AutoRestTest (GPT-3.5+MARL) | 58.3% method/line | 42 500-errors | 12 real APIs | Yes | **Yes** | No | **No** |
| 7 | LlamaRestTest (Llama3-8B) | 55.8% method | 204 faults (500s) | 12 real APIs | Yes | **Yes** | No | **No** |
| 8 | LogiAgent (GPT-4o-mini) | 71.78% line | 234 logical issues; 49 crashes | 12 systems | Partly | **Yes** (RESTler/EvoMaster/Morest/ARAT-RL) | No | **No** |
| 9 | RESTifAI (GPT-4.1-mini) | 128/134 operations | 60.87% failures = bugs | 7 services | No | No (AutoRestTest/LogiAgent) | No | **No** |
| 10 | EvoMaster (search-based) | 41% (gen) vs 82% (manual) | 38 real bugs | 3 services | (origin) | (is the baseline) | **Yes** | **No** |
| 11 | No-Time-to-Rest-Yet (study) | 52.76% line (best of 10 tools) | 33.3 500-errors | 20 EMB services | Yes | Yes (study) | No | **No** |
| 12 | Morest (model-based) | +26–103% vs baselines | 44 bugs (13 new) | 6 projects | No | Yes (EvoMaster-BB) | No | **No** |
| 13 | DeepREST (deep RL) | +17–77% branch | +25–67% unique faults | 11 EMB APIs | Yes | No (RestTestGen/Morest/RESTler/ARAT-RL/Schemathesis) | No | **No** |

> **†** RestTSLLM (#5): the abstract confirms Claude 3.5 Sonnet as the best of the compared LLMs on success rate / coverage / mutation score, but the exact percentages (≈71.7% branch, ≈40.8% mutation) are from a secondary index and are not in the arXiv abstract — flagged for re-verification against the published version.

---

## D. Notes (what the table shows)

- **LLM split:** 9/13 are LLM-based; the GPT family dominates (#1 GPT-3.5, #2 GPT-3.5-turbo-1106, #4 GPT-4-Turbo, #6 GPT-3.5, #8 GPT-4o-mini, #9 GPT-4.1-mini), with one small fine-tuned model (#7 Llama3-8B) and one multi-LLM study where **Claude 3.5 Sonnet** wins (#5). Non-OpenAI commercial models (Gemini, Claude) are barely benchmarked head-to-head.
- **Coverage — note the two different kinds.** *Operation / endpoint / route* coverage, where reported, **can be high**: RESTifAI exercises **128/134 operations ≈ 95.5%** (#9, with several services at 100%) and RESTSpecIT reaches **~88.6% average route discovery** (#3). But *code* coverage (line/branch/method) stays much lower — **~52% line across classic tools** (#11) up to **~72% line** (#8). So RQ1's open question is **not** simply "is ≥90% endpoint coverage reachable" (it sometimes is) but **(a)** whether it holds on **EMB APIs with pre-seeded faults** and **(b) which endpoint types are systematically missed** — which no paper answers.
- **Fault detection** is almost always **counted as 500-errors / server crashes on live APIs** (#2,#6,#7,#8,#11,#13) — there is **no ground truth**, so Recall/Precision cannot be computed.
- **The last column is effectively "No":** the closest case is RestTSLLM (#5), whose **mutation score** (40.8%) does measure faults killed — but against *automatically-generated syntactic mutants* on 6 self-built APIs, not a shared benchmark. **No study** uses a shared **pre-seeded-fault benchmark** (e.g. EMB faulty versions) to compute fault-detection **Recall**, and **none compares LLM vs manual vs EvoMaster simultaneously** on the same APIs. Only EvoMaster (#10) compares a tool against *manual* tests (and finds the tool **below** manual coverage). This is the quantitative core of the research gap (see `gap-statement.md`).
- **Endpoint-type miss analysis** (CRUD / authentication / error-handling) is not broken out by any paper — they report aggregate coverage only.

### Cross-comparison note vs the team baseline (`Nguyễn-Hoàng-Huy-SE190240`)
This table was rebuilt independently and re-verified against primary sources; it corrects a few details that appear in earlier drafts — e.g. RESTSpecIT (#3) uses **DeepSeek V3 / GPT-4.1-mini / GPT-3.5** (not a single GPT model) and its title is "…via LLM-Assisted Request Mutations"; EvoMaster (#10) is the 2019 TOSEM paper with the **manual-vs-generated** coverage comparison (the most directly relevant evidence for this topic's RQ).
