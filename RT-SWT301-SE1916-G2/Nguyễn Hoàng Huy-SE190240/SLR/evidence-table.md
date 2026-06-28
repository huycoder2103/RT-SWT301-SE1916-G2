# Evidence Table — LLM for REST API Test Generation

**Number of papers:** N = 13  
**Period:** 2023–2026

---

| # | Paper (Title + Year + Venue) | Tool/LLM | Dataset | Metric | Key Results | Self-reported Limitations |
|---|------------------------------|----------|---------|--------|-------------|--------------------------|
| 1 | Kim et al. (2023) "Enhancing REST API testing with NLP techniques" — ISSTA 2023 — [DOI](https://doi.org/10.1145/3597926.3598131) | NLPtoREST: Traditional NLP (NER + word embedding) integrated with RESTler, EvoMaster — no generative LLM | 9 RESTful services (FDIC, Genome Nexus, LanguageTool, OCVN, OhSome, OMDb, REST Countries, Spotify, YouTube) | Precision, recall, F1 (rule extraction); statement/line coverage, branch coverage, fault detection (500 errors) | Rule extraction: 94% recall, 79% precision (after validation); enhanced spec improved coverage for 8 SOTA testing tools | Training set may not be representative; ground truth manually created by students; possible implementation errors |
| 2 | Nguyen et al. (2023) "An approach to generating API test scripts using GPT" — SOICT 2023 — [DOI](https://doi.org/10.1145/3628797.3628947) | GPT-3.5-Turbo (OpenAI API) + Katalon framework | 7 real-world APIs (157 endpoints, 179 operations): PetStore, Proshop, API Guru, CanadaHolidays, BillsAPI, RealWorld, Jikan | Status code coverage (2xx, 4xx, 5xx per category); success test case rate | 2xx coverage: PetStore 100% (vs RestTestGen 73%), Proshop 100% (vs 88%); overall outperforms RestTestGen on 2xx due to GPT's superior semantic understanding | Depends on Swagger spec quality; API call cost; 4xx coverage less stable than RestTestGen |
| 3 | Kim et al. (2024) "Leveraging LLMs to improve REST API testing" — ICSE-NIER 2024 — [DOI](https://doi.org/10.1145/3639476.3639769) | RESTGPT (GPT-3.5 Turbo) | 9 REST API services with OpenAPI spec (same dataset as #1) | Precision (rule extraction), accuracy (value generation) | 97% precision in rule extraction (vs NLPtoREST 79%); ~73% accuracy in value generation; outperforms NLPtoREST and ARTE | N/A — New Ideas paper (4 pages), no Threats to Validity / Limitations section |
| 4 | Le et al. (2024) "KAT: Dependency-aware automated API testing with LLMs" — ICST 2024 — [DOI](https://doi.org/10.1109/ICST60714.2024.00018) | GPT-3.5-turbo-1106 (OpenAI API) | 12 real-world RESTful services | Test coverage (status code), undocumented status codes, false positive rate | +15.7% status code coverage over RestTestGen; detects additional undocumented status codes; reduces false positives | Depends on Swagger file quality; OpenAI API cost; only compared against RestTestGen |
| 5 | Corradini et al. (2024) "DeepREST: Automated test case generation for REST APIs exploiting deep RL" — ASE 2024 — [DOI](https://doi.org/10.1145/3691620.3695511) | Deep RL (PPO agent) + GPT4All (WizardLM-13B-v1.2.Q4_0, local) for input value generation | 11 benchmark REST APIs (EMB); replication package on Zenodo | Branch coverage (AUC), line coverage (AUC), method coverage (AUC), fault detection (5XX) | Most effective black-box REST API testing tool on all 11 APIs for branch, line, method coverage and fault detection; all differences statistically significant (Wilcoxon signed rank test, p < 0.05) | Black-box only; depends on OpenAPI spec quality; RL training overhead |
| 6 | Zheng et al. (2024) "RESTless: Enhancing state-of-the-art REST API fuzzing with LLMs" — IEEE TSC vol.17 pp.4225–4238 — [DOI](https://ieeexplore.ieee.org/document/10740182) | GPT-3.5 + RESTler/EvoMaster fuzzer; builds RTSet dataset using LLM | 9 real-world cloud services (Microsoft Azure, AWS, Google Cloud, etc.) | Semantic quality of sequences, vulnerability count | Detected 38 vulnerabilities across 9 cloud services; 16 confirmed and fixed by vendors (abstract only — no full text available) | N/A — no full text available (IEEE paywall) |
| 7 | Kim et al. (2025) "LlamaRestTest: Effective REST API testing with small language models" — FSE 2025 — [DOI](https://doi.org/10.1145/3715737) | Llama3-8B fine-tuned + quantized (2-bit, 4-bit, 8-bit); compared with GPT via RESTGPT | 12 real-world services (Spotify, FDIC, OhSome, Genome Nexus, etc.); 1.8M+ API parameters from APIs-guru for fine-tuning | Code coverage (line, branch, method), internal server errors (500), valid request rate | Small LM (8B) matches or outperforms GPT; outperforms RESTler, EvoMaster, MoRest, ARAT-RL even when those tools use RESTGPT-enhanced specs; 2-bit quant reduces effectiveness on domain-specific APIs | Fine-tuning requires large dataset (1.8M params); black-box testing only; 2-bit quantization loses accuracy on domain-specific APIs |
| 8 | Stennett, Kim et al. (2025) "AutoRestTest: A tool for automated REST API testing using LLMs and MARL" — ICSE 2025 Demo — [DOI](https://doi.org/10.1109/ICSE-Companion66252.2025.00015) | SODG + MARL (5 agents: operation, parameter, value, dependency, header) + GPT-3.5-Turbo / GPT-4o | 4 online real-world services (FDIC, OMDb, OhSome, Spotify) | Successfully processed operations (count), unique server errors | 26 unique operations processed (vs ARAT-RL 12, EvoMaster 11, MoRest 11, RESTler 10); OhSome: 12 ops (all others: 0); only tool to detect 5xx on Spotify | N/A — tool demo paper (4 pages), no Threats to Validity / Limitations section |
| 9 | Li et al. (2025) "MioHint: LLM-assisted Mutation for Whitebox API Testing" — arXiv 2025 — [URL](https://arxiv.org/abs/2504.05738) | GPT-4o (mutation-based prompt) + EvoMaster (white-box) + static analysis | 16 real-world REST API services from EMB (4 excluded due to runtime issues) | Target coverage, line coverage, mutation hit rate | +47.72pp target coverage (9.82%→57.54%); +4.95% line coverage (48.51%→53.46%); mutation accuracy 67× over baseline; covers 57% of hard-to-cover targets | White-box requires source code access; LLM prompt cost; depends on MIO's target selection strategy |
| 10 | Han & Zhu (2025) "MASTEST: A LLM-Based Multi-Agent System for RESTful API Tests" — arXiv 2025 — [URL](https://arxiv.org/abs/2511.18038) | GPT-4o + DeepSeek V3.1 Reasoner (multi-agent: scenario gen, script gen, execution, analysis) | 5 public REST APIs | API operation coverage, status code coverage, data type correctness, script syntax correctness, bug detection, usability | DeepSeek: better data type correctness & status code detection; GPT-4o: better API operation coverage; both achieve 100% syntax correctness | LLM-generated scripts require human review; only 5 APIs and 2 LLMs tested; no back-end code coverage measured; results may vary with other LLMs or versions; input may exceed LLM token limit when many operations (requires manual subset selection) |
| 11 | Zhang et al. (2025) "LogiAgent: Automated logical testing for REST systems with LLM-based multi-agents" — arXiv 2025 — [URL](https://arxiv.org/abs/2503.15079) | GPT-4o-mini (default hyperparameters) — 3 agents: Test Scenario Generator, API Request Executor, API Response Validator | 12 real-world REST systems (from EMB, 4 excluded due to deployment issues) | Branch coverage, line coverage, method coverage, logical issues detected (accuracy), 500-code crashes | 39.98% branch, 71.78% line, 73.06% method (exceeds best baseline: 34.90%, 62.38%, 67.24% at 1000 requests); 234 logical issues (139 bugs + 95 enhancements), accuracy 66.19%; 49 server crashes | Logical oracle accuracy only 66.19% — many false positives; depends on API documentation quality |
| 12 | Corradini et al. (2026) "Automated REST API Black-box Test Generation in Practice" — ICST 2026 — [URL](https://orbilu.uni.lu/handle/10993/68146) | RestTestGen + DeepREST (industry deployment); DeepREST uses deep RL + Qwen 3 (14B, local via LM Studio) for input value generation | 5 industrial REST APIs (204 operations) in a satellite connectivity system; Java, Python, C++ | Operation coverage, fault detection, execution time, CPU/memory | Median 74% operation coverage (151/204); max 77% (DeepREST); 21 unique previously unknown faults (4/5 services); execution <10 min on commodity hardware | Industry context — limited generalizability; strict company policies hinder adoption; terminology mismatch between academic tools and practitioners |
| 13 | Pereira et al. (2026) "APITestGenie: Generating Web API Tests from Requirements and API Specs with LLMs" — AST 2026 — [URL](https://arxiv.org/abs/2604.02039) | GPT-4-Turbo + RAG + prompt engineering | 10 real-world APIs (8 from industrial partner in automotive domain, ~1000 live endpoints); requirements docs + OpenAPI spec | Script validity rate, success rate per BR, fault detection, generation time/cost | 89% script validity (max 3 attempts); 69.3% overall success rate; 88.6% of BRs had ≥1 valid test script; detected unknown defects including cross-endpoint issues; avg 126s, €0.37/generation | Depends on requirements doc quality; LLM randomness; manual inspection introduces subjectivity; API complexity affects success rate |

---

### LLM Distribution Summary

| LLM Model | Papers Using It | Paper # |
|-----------|----------------|---------|
| GPT-3.5 Turbo | 5 | #2, #3, #4, #6, #8 (with GPT-4o) |
| GPT-4 / GPT-4o / GPT-4o-mini / GPT-4-Turbo | 6 | #8, #9, #10, #11, #13 |
| Llama3-8B (fine-tuned) | 1 | #7 |
| GPT4All / WizardLM-13B (local) | 1 | #5 |
| DeepSeek V3.1 | 1 | #10 (with GPT-4o) |
| Qwen 3 (14B, local) | 1 | #12 |
| Traditional NLP (no generative LLM) | 1 | #1 |
| **Gemini (Google)** | **0** | — |
| **Claude (Anthropic)** | **0** | — |

---

### Verification Notes

| # | PDF Available? | Results Verified From |
|---|---------------|----------------------|
| 1 | Yes | Full PDF — results tables confirmed |
| 2 | Yes | Full PDF — results tables confirmed |
| 3 | Yes | Full PDF — results confirmed |
| 4 | Yes | Full PDF — "+15.7% status code coverage over RestTestGen" confirmed; 12 RESTful services confirmed |
| 5 | Yes | Full PDF — results confirmed |
| 6 | **No PDF** | Semantic Scholar + IEEE Xplore metadata only — "38 vulnerabilities, 16 confirmed" from abstract; detailed tables NOT independently verified |
| 7 | Yes | Full PDF — results confirmed |
| 8 | Yes | Full PDF — Table I confirmed (26 ops total on 4 services); **original evidence table had WRONG results** (58.33% method coverage etc. do not appear in this paper); corrected |
| 9 | Yes | Full PDF — all numbers confirmed (47.72pp, 4.95%, 57.54%) |
| 10 | Yes | Full PDF — results confirmed |
| 11 | Yes | Full PDF — results confirmed |
| 12 | Yes | Full PDF — results confirmed (74%, 21 faults) |
| 13 | Yes | Full PDF — results confirmed (89%, 69.3%, 88.6%) |

---
