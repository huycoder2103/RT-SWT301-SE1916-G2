# Evidence Table — LLM REST API Test Generation

**Thành viên:** [Tên của bạn]  
**Ngày tạo:** 2026-06-03 | Cập nhật: 2026-06-04  
**Nguồn dữ liệu:** String 1 (OpenAlex) + String 2 (OpenAlex)  
**Số paper final included:** 28

> **Lưu ý:** Tất cả thông tin trong bảng này đều được trích xuất trực tiếp từ abstract/metadata trong 2 file CSV (String 1 và String 2). Không bịa số liệu. Các ô "N/A" hoặc "Không đề cập trong abstract" là bình thường vì abstract không phải lúc nào cũng chứa đầy đủ thông tin chi tiết.

---

## Bảng Evidence Table

| # | Paper (Tên + Năm + Venue) | DOI/URL | Search String | Tool/LLM | Dataset | Metric | Kết quả chính | Hạn chế tự nêu |
|---|---------------------------|---------|---------------|----------|---------|--------|---------------|-----------------|
| 1 | LlamaRestTest: Effective REST API Testing with Small Language Models — Kim et al. (2025) — Proc. ACM Softw. Eng. | [10.1145/3715737](https://doi.org/10.1145/3715737) | String 1, String 2 | **Llama3-8B** (fine-tuned, quantized 2/4/8-bit); so sánh với RESTGPT (GPT-powered) | 12 real-world REST services (bao gồm Spotify) | Code coverage, Internal server errors (5xx), Parameter-dependency rules detected | Fine-tuned small LM outperform larger models trong detecting parameter-dependency rules và generating valid inputs; LlamaRestTest vượt RESTler, MoRest, EvoMaster, ARAT-RL về code coverage và 5xx errors | Ablation study cho thấy mỗi component đóng góp riêng; giới hạn chưa rõ từ abstract |
| 2 | KAT: Dependency-Aware Automated API Testing with Large Language Models — Le et al. (2024) — ICST 2024 | [10.1109/icst60714.2024.00017](https://doi.org/10.1109/icst60714.2024.00017) | String 1 | **GPT** (LLM) + advanced prompting techniques | 12 real-world RESTful services | Test coverage, Undocumented status codes, False positives | Cải thiện test coverage, phát hiện nhiều undocumented status codes hơn, giảm false positives so với state-of-the-art tool | N/A — Không đề cập cụ thể trong abstract |
| 3 | TAPE: Technology Adoption Performance Evaluation applied to testing industrial REST APIs — Poth et al. (2024) — Autom. Softw. Eng. | [10.1007/s10515-024-00477-2](https://doi.org/10.1007/s10515-024-00477-2) | String 1 | **StarCoder** (LLM) + **EvoMaster** (evolutionary) + **OpenAPI Generator** (deterministic) | Industrial REST APIs tại Volkswagen AG (enterprise scale) | Test coverage, Scalability, Integration capability | Đánh giá so sánh 3 approaches (deterministic, evolutionary, LLM) trong industrial setting; StarCoder dùng cho LLM-based test gen | Chưa rõ kết quả số liệu cụ thể từ abstract; tập trung vào enterprise integration |
| 4 | SAINT: Service-level Integration Test Generation with Program Analysis and LLM-based Agents — Pan et al. (2025) — arXiv | [10.48550/arxiv.2511.13305](https://doi.org/10.48550/arxiv.2511.13305) | String 1 | **LLM-based agents** (không nêu cụ thể model) + static analysis | 8 Java applications (bao gồm 1 proprietary enterprise app) | Code coverage, Database interaction coverage, Fault detection, Developer survey endorsement | Hiệu quả trong coverage, fault detection và scenario generation; developer survey đánh giá cao scenario-based tests | White-box approach — yêu cầu source code; chưa thử nghiệm với black-box |
| 5 | RESTestBench: A Benchmark for Evaluating LLM-Generated REST API Test Cases from NL Requirements — Kogler et al. (2026) — arXiv | [OpenAlex W7159547511](https://openalex.org/W7159547511) | String 1, String 2 | **Multiple state-of-the-art LLMs** (không nêu cụ thể) | 3 REST services (precise + vague NL requirements) | Requirements-based mutation testing metric (fault-detection effectiveness) | Test effectiveness giảm đáng kể khi generator interact với faulty/mutated code, đặc biệt với vague requirements | Incorporating actual SUT behaviour là không cần thiết khi requirement detail đủ cao |
| 6 | Assessing REST API Test Generation Strategies with Log Coverage — Reinikainen et al. (2026) — arXiv / EASE 2026 | [OpenAlex W7153670734](https://openalex.org/W7153670734) | String 1 | **Claude Opus 4.6, GPT-5.2-Codex** + EvoMaster + human-written Locust tests | Light-OAuth2 authorization microservice system | Log coverage (unique log templates) | Claude Opus 4.6: +28.4% unique log templates vs human; GPT-5.2-Codex: −38.6% vs human; EvoMaster: −26.1% vs human; Combined human+Claude: +78.4%/+38.9% | Chỉ đánh giá trên 1 hệ thống; future work mở rộng sang multiple systems |
| 7 | RESTSpecIT: You Can REST Now — Automated REST API Documentation and Testing via LLM-Assisted Request Mutations — Decrop et al. (2024) — arXiv | [10.48550/arxiv.2402.05102](https://doi.org/10.48550/arxiv.2402.05102) | String 1 | **DeepSeek V3, GPT-4.1, GPT-3.5** | Nhiều REST APIs (không nêu số cụ thể) | Routes found (%), Query parameters found (%), Server errors detected | Trung bình 88.62% routes và 89.25% query parameters được infer; phát hiện undocumented API data và server errors | Yêu cầu minimal input (chỉ API name + LLM key); giới hạn với APIs không có documentation |
| 8 | DynER: Optimized Test Case Generation for RESTful API Fuzzers Guided by Dynamic Error Responses — Chen et al. (2024) — Electronics | [10.3390/electronics13173476](https://doi.org/10.3390/electronics13173476) | String 1, String 2 | **LLM** (prompting để hiểu error response semantics) + RESTler | 2 real-world services: WordPress, GitLab | Pass rate, Unique request types tested, Bugs found | WordPress: +41.21% pass rate, +12.50% unique request types vs foREST; GitLab: +26.33% pass rate, +22.80% unique types; phát hiện 3 new bugs | N/A — Không đề cập threats to validity trong abstract |
| 9 | AutoRestTest: A Multi-Agent Approach for REST API Testing with Semantic Graphs and LLM-Driven Inputs — Kim et al. (2024) — arXiv | [10.48550/arxiv.2411.07098](https://doi.org/10.48550/arxiv.2411.07098) | String 1, String 2 | **LLMs** (cho domain-specific value generation) + MARL + SPDG | 12 real-world REST services | Code coverage, Operation coverage, Fault detection (5xx errors) | Outperform 4 leading black-box tools (kể cả khi dùng RESTGPT-enhanced specs); duy nhất trigger internal server error trên Spotify | Ablation study chỉ ra mỗi component (SPDG, LLM, MARL) đều cần thiết |
| 10 | Automating REST API Postman Test Cases Using LLM — Sri et al. (2024) — arXiv | [10.48550/arxiv.2404.10678](https://doi.org/10.48550/arxiv.2404.10678) | String 1, String 2 | **OpenAI** (LLM cụ thể không nêu rõ) | Manually collected Postman test cases cho nhiều REST APIs | Không đề cập metric cụ thể trong abstract | LLM sinh được các test scenarios đa dạng và phức tạp cho Postman; cải thiện efficiency | Không đề cập cụ thể limitations trong abstract; thiếu metric đánh giá định lượng rõ ràng |
| 11 | APITestGenie: Automated API Test Generation through Generative AI — Pereira et al. (2024) — arXiv | [10.48550/arxiv.2409.03838](https://doi.org/10.48550/arxiv.2409.03838) | String 1, String 2 | **LLMs** (không nêu model cụ thể) + RAG + prompt engineering | 10 real-world APIs | Valid test script rate (%) | 57% valid test scripts (1 attempt); tăng lên 80% với 3 attempts | Cần human intervention để validate/refine trước CI/CD; tool là productivity assistant, không thay thế tester |
| 12 | Carolinesnt/ai_agent_starter: AI Agent-based BAC Testing Framework — Susanto (2026) — Zenodo | [10.5281/zenodo.18524562](https://doi.org/10.5281/zenodo.18524562) | String 1 | **GPT-4.1** + AI Agent pipeline | REST API endpoints (BAC testing) | Authorization test generation, BAC vulnerability detection | Framework tự động generate authorization test cases cho REST APIs; phát hiện Broken Access Control vulnerabilities | N/A — Framework mới, chưa có peer-reviewed evaluation |
| 13 | REST API Fuzzing Using API Dependencies and Large Language Models — Liu et al. (2026) — Eng. Proc. | [10.3390/engproc2025120042](https://doi.org/10.3390/engproc2025120042) | String 1 | **LLMs** (cho API dependency analysis) | REST APIs (không nêu cụ thể) | Không đề cập metric cụ thể trong abstract | Kết hợp LLM với API dependency analysis để cải thiện REST API fuzzing | N/A — Không đề cập từ abstract |
| 14 | ARMeta: Multi-Agent LLM-based Metamorphic Testing for REST APIs — Khan et al. (2026) — arXiv | [OpenAlex W7162817974](https://openalex.org/W7162817974) | String 1, String 2 | **LLM-based multi-agent** (model cụ thể không nêu) | 2 publicly available web applications với REST interfaces | So sánh với scenario-based testing baseline | ARMeta tạo ra behaviors bổ sung cho existing scenario-based testing; Given-When-Then format | Chỉ so sánh với 1 baseline; 2 ứng dụng là số lượng nhỏ |
| 15 | LRASGen: LLM-based RESTful API Specification Generation — Deng et al. (2026) — ACM TOSEM | [10.1145/3810241](https://doi.org/10.1145/3810241) | String 1 | **LLM** (cho OpenAPI spec generation từ source code) | RESTful API services (không nêu số cụ thể) | Specification completeness, Accuracy | LLM-based approach sinh OpenAPI specs từ source code; hỗ trợ downstream test generation | N/A — Không đề cập cụ thể trong abstract |
| 16 | Leveraging Large Language Models to Improve REST API Testing — Kim et al. (2023) — arXiv | [10.48550/arxiv.2312.00894](https://doi.org/10.48550/arxiv.2312.00894) | String 1 | **LLMs** (predecessor của LlamaRestTest / RESTGPT) | REST API services | Code coverage, Fault detection | LLM cải thiện REST API testing bằng cách sinh realistic parameter values và discover operation dependencies | Predecessor paper — kết quả sơ bộ trước khi phát triển thành LlamaRestTest |
| 17 | An Intelligent Agent for Automated Test Generation from OpenAPI Specifications — Vilela et al. (2025) — WBoTS | [10.5753/wbots.2025.15217](https://doi.org/10.5753/wbots.2025.15217) | String 1 | **LLM-based intelligent agent** | REST APIs with OpenAPI specs | Test generation success, Coverage | Agent tự động sinh test cases từ OpenAPI specs sử dụng LLM | N/A — Không đề cập trong abstract |
| 18 | LoBREST: Log-based, Business-aware REST API Testing — Yang et al. (2026) — arXiv | [OpenAlex W7153671616](https://openalex.org/W7153671616) | String 1, String 2 | **LLMs** (cho business-rule extraction từ logs) | REST API with production logs | Log coverage, Business rule coverage | Kết hợp production logs với LLM để sinh business-aware test cases cho REST APIs | N/A — Không đề cập cụ thể từ abstract |
| 19 | APITestGenie (v2): Generating Web API Tests from Requirements and API Specifications with LLMs — Pereira et al. (2026) — arXiv | [10.1145/3793654.3793743](https://doi.org/10.1145/3793654.3793743) | String 1, String 2 | **LLMs** + RAG + prompt engineering | 10 real-world APIs (8 industrial APIs ~1,000 endpoints, automotive domain) | Valid test script rate (%) | 89% valid test scripts (tối đa 3 attempts); phát hiện previously unknown defects, bao gồm integration issues | API complexity và level of detail trong requirements ảnh hưởng success rate |
| 20 | Generating REST API Tests With Descriptive Names — Garrett et al. (2025) — arXiv | [10.48550/arxiv.2512.01690](https://doi.org/10.48550/arxiv.2512.01690) | String 1, String 2 | **LLMs** (cho test naming + generation) + EvoMaster | REST APIs | Test readability, Naming accuracy, Traceability | LLMs sinh test cases với descriptive names cho REST APIs; cải thiện traceability và readability | N/A — Không đề cập cụ thể từ abstract |
| 21 | RestTSLLM: Combining TSL and LLM to Automate REST API Testing — Barradas et al. (2025) — SBES 2025 | [10.5753/sbes.2025.9670](https://doi.org/10.5753/sbes.2025.9670) | String 1, String 2 | **Claude 3.5 Sonnet, Deepseek R1, Qwen 2.5 32b, Sabiá 3** | REST APIs (cụ thể không nêu trong abstract) | Success rate, Test coverage, Mutation score | Claude 3.5 Sonnet outperform tất cả models khác trên mọi metric | N/A — Không đề cập limitations cụ thể trong abstract |
| 22 | RBCTest: Leveraging LLMs to Mine and Verify Oracles of API Response Bodies for RESTful API Testing — Huynh et al. (2025) — arXiv | [10.48550/arxiv.2504.17287](https://doi.org/10.48550/arxiv.2504.17287) | String 1 | **LLMs** + Observation-Confirmation (OC) prompting scheme | 19 real-world APIs | Constraint mining precision (%), Test case precision (%), Mismatches detected | OC prompting: precision 85.1%–93.6% constraint mining; 86.4%–91.7% test case generation; phát hiện 46 mismatches across 19 APIs, 4 reported to developers | N/A — Không đề cập cụ thể từ abstract |
| 23 | AutoRestTest Tool Paper — Stennett et al. (2025) — arXiv | [10.48550/arxiv.2501.08600](https://doi.org/10.48550/arxiv.2501.08600) | String 1, String 2 | **LLMs** + MARL + SODG (Semantic Operation Dependency Graph) | REST services (cụ thể không nêu số trong tool paper) | Successful operation count, Unique server errors, Time elapsed | Tool paper — 5 agents (operation, parameter, value, dependency, header) | Tool paper, chưa có full evaluation |
| 24 | SmartAPIForge: A No-Code Platform for Automated REST API Generation from Natural Language — Divya et al. (2025) — IJARCCE | [10.17148/ijarcce.2025.141262](https://doi.org/10.17148/ijarcce.2025.141262) | String 1 | **LLMs** (cho NL → code generation) + Firecracker micro-VMs | 3,079 API creation tasks from real-world scenarios | Deployment success rate (%), Code compilation rate (%), OpenAPI validation (%) | Deployment: 96% success; Code compilation: 94% success; OpenAPI specs: 97% passed validation | N/A — Không đề cập cụ thể từ abstract |
| 25 | From Requirements to Executable Tests: LLM-Based System Test Generation for REST APIs — Kochanovskis & Slotkienė (2026) — Vilnius Univ. | [10.15388/lmitt.2026.13](https://doi.org/10.15388/lmitt.2026.13) | String 1 | **LLMs** + OpenAPI specifications | 2 real-world APIs | Endpoint reachability coverage, Test executability | Sinh executable pytest tests; đạt full endpoint reachability coverage; stable automated test execution | Chỉ đánh giá trên 2 APIs |
| 26 | BOSQTGEN: Breaking the Sound Barrier in Test Generation — Asif et al. (2025) — arXiv | [10.48550/arxiv.2510.19777](https://doi.org/10.48550/arxiv.2510.19777) | String 1 | **LLMs** (cho coherent strata suggestion) + combinatorial testing | RESTful benchmarks (nhiều services) | Code coverage (%) | Trung bình 82% code coverage trên RESTful benchmarks; thường tăng ≥20% so với prior state-of-the-art; gần bằng hand-written test suites | Fully API-driven approach (black-box) |
| 27 | MioHint: LLM-assisted Mutation for Whitebox API Testing — Li et al. (2025) — arXiv | [10.48550/arxiv.2504.05738](https://doi.org/10.48550/arxiv.2504.05738) | String 1 | **LLM** (cho code comprehension) + static analysis (def-use analysis) + EvoMaster | 16 real-world REST API services | Line coverage (%), Mutation accuracy | +4.95% absolute line coverage vs EvoMaster baseline; 67x improvement in mutation accuracy | White-box approach — cần source code; giới hạn bởi LLM context length |
| 28 | RESTifAI: LLM-Based Workflow for Reusable REST API Testing — Kogler et al. (2025) — arXiv | [OpenAlex W7114820659](https://openalex.org/W7114820659) | String 1, String 2 | **LLM** (so sánh với AutoRestTest, LogiAgent) | Industrial services + public APIs | So sánh với AutoRestTest và LogiAgent | RESTifAI performs on par với latest LLM tools; ưu điểm về reusability, oracle complexity, CI/CD integration | Không đề cập cụ thể trong abstract |

---

## Ghi chú về quá trình lọc

### Tổng quan screening:
- **Tổng raw records:** String 1 (223) + String 2 (40) = **263**
- **Sau dedup:** **206** unique records
- **V1 Screening (title + abstract):** 174 EXCLUDE, 27 INCLUDE, 5 Unsure → **32 pass**
- **V2 Screening (full-text):** 4 EXCLUDE → **28 final included**

### Papers bị EXCLUDE — ví dụ tiêu biểu:

**EC4 (Out of Domain) — 103 papers "No REST API testing context":**
Phần lớn papers trong kết quả search chứa từ khóa LLM + test nhưng không liên quan REST API testing (về unit testing, code generation, security, mobile testing, v.v.)

**EC4 (Unit testing) — 10 papers:**
- ChatGPT vs SBST (Tang et al., 2024), Mutation-Guided Unit Test (Wang et al., 2026), LLM-based Unit Test via Property Retrieval (Zhang et al., 2024), v.v.

**EC4 (General survey) — 9 papers:**
- Deep learning-based SE (Chen et al., 2024), A Survey on Network Protocol Fuzzing (Zhang et al., 2023), Fuzzing frameworks for server-side web applications (Dharmaadi et al., 2025), v.v.

**IC1 (Non-English) — 3 papers:**
- Tiêu đề bằng tiếng Ukraina, Phần Lan

**EC3 (Replication package/dataset) — 3 papers:**
- Co-Evo (Zenodo), Assessing REST API replication package (Zenodo)

### Papers INCLUDE (đã có trong evidence table):
Các paper #1–#28 ở bảng trên đều thỏa mãn IC1 (English) + IC2 (≥2018) + IC3 (REST API/OpenAPI/Web API testing) + IC4 (có dùng LLM) + IC5 (có empirical results).

---

## Tổng hợp nhanh theo cột

### Tool/LLM sử dụng:
| LLM/Tool                                    | Số paper |
|----------                                   |----------|
| GPT family (GPT-3.5, GPT-4.1, GPT-5.2-Codex)|     6    |
| Llama family (Llama3-8B fine-tuned)         |     1    |
| Claude (Opus 4.6, 3.5 Sonnet)               |     2    |
| DeepSeek (V3, R1)                           |     2    |  
| StarCoder                                   |     1    | 
| Qwen 2.5 32b                                |     1    |
| Sabiá 3                                     |     1    |
| LLM (không nêu cụ thể model)                |     18   |

### Metric phổ biến:
| Metric                                           | Số paper sử dụng |
|--------|-------------------|
| Code/Operation/Line coverage                            | 10 |
| Fault/Bug detection (5xx errors, bugs, mismatches)      | 7 |
| Pass rate / Valid script rate                           | 5 |
| Mutation score / accuracy                               | 3 |
| Log coverage                                            | 2 | 
| API/Endpoint reachability coverage                      | 2 |
| Constraint mining precision                             | 1 |
| Reproducibility                                         | 1 |
| Deployment/Compilation success rate                     | 1 |

### Dataset scale:
| Quy mô                  | Số paper |
|---------                |----------|
| ≥ 10 real-world services    | 6 |
| 2–9 services                | 6 |
| 1 service                   | 2 |
| Industrial / enterprise     | 4 |
| Benchmark chuyên dụng       | 2 |
| Không rõ từ abstract        | 8 |
