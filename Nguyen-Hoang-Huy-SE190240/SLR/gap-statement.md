# Gap Statement — LLM for REST API Test Generation

**Evidence table:** N = 13 papers (2023–2026)

---

## GAP-T (Technology Gap): Lack of cross-model evaluation beyond the OpenAI ecosystem

**Evidence from the evidence table:**

The LLM distribution across 13 papers reveals a near-total dominance of the OpenAI ecosystem:

- **GPT-series (GPT-3.5, GPT-4, GPT-4o, GPT-4o-mini, GPT-4-Turbo)** is used as the primary model or core component in **9/13 papers** (#2, #3, #4, #6, #8, #9, #10, #11, #13). Specifically: GPT-4o achieves +47.72pp target coverage (#9); GPT-4o-mini achieves 71.78% line coverage (#11); GPT-4-Turbo achieves 89% script validity (#13); GPT-3.5 improves status code coverage by 15.7% (#4).
- **4 papers** use non-OpenAI models or no generative LLM: #1 uses traditional NLP (no generative LLM); #5 uses WizardLM-13B via GPT4All (local, quantized Q4_0); #7 uses Llama3-8B (fine-tuned, 1.8M parameters); #12 uses Qwen 3 (14B, local via LM Studio). Paper #10 also compares DeepSeek V3.1 alongside GPT-4o but only on 5 APIs.
- **0/13 papers** evaluate Gemini (Google) or Claude (Anthropic).

**Gap:** No study has evaluated or compared the zero-shot/few-shot test generation capability of **Gemini** on a standardized benchmark (such as EMB) to determine whether the positive results observed are GPT-specific or generalizable across LLMs. This lack of cross-model data leaves it unclear whether current findings are model-dependent or reflect a general LLM capability.

---

## GAP-M (Metric Gap): Focus on code coverage and server crashes (500 errors), lacking edge case coverage metrics

**Evidence from the evidence table:**

The metrics used across 13 papers cluster into two groups:

- **Code coverage:** Line coverage (#1, #5, #7, #9, #11), branch coverage (#1, #5, #7, #11), method coverage (#5, #7, #11). These measure "how much code was executed" but not "whether the code behaved correctly."
- **Fault detection via server crashes:** Most papers count 500 Internal Server Error responses (#1, #5, #7, #8, #11 — e.g., #11 finds 49 server crashes, #8 detects a 5xx on Spotify). This only catches faults that crash the server, missing logical faults where the server returns 2xx but with incorrect results.
- **Sole exception:** Paper #11 (LogiAgent) attempts to detect "logical issues" — finding 234 issues (139 bugs + 95 enhancements), but its **accuracy is only 66.19%**, meaning one-third are false positives. The authors themselves acknowledge this as a limitation.

**Gap:** No study has systematically defined and measured an **Edge Case Coverage** metric — i.e., the ability to generate test cases that deliberately violate OpenAPI spec constraints (boundary values, invalid types, missing required fields, constraint violations) to detect latent logical faults beyond 500 errors.

---

## GAP-D (Dataset Gap): No pre-seeded fault dataset for measuring Fault Detection Recall

**Evidence from the evidence table:**

The datasets used across 13 papers fall into three categories:

- **EMB benchmark (open-source REST APIs):** #1 (9 APIs), #5 (11 APIs), #9 (16 APIs), #11 (12 APIs). EMB provides source code for measuring code coverage but **contains no ground-truth bugs** — the total number of actual faults is unknown.
- **Real-world/Public APIs (Spotify, FDIC, Azure, etc.):** #2 (7 APIs), #4 (12 APIs), #6 (9 cloud services), #7 (12 services), #8 (4 services), #10 (5 APIs). As production systems, the **ground truth about total faults is unknowable**.
- **Industrial APIs:** #12 (204 operations, satellite system), #13 (10 APIs, automotive domain).

Consequence: All papers report only **absolute fault counts** (e.g., #6 finds 38 vulnerabilities, #12 finds 21 faults, #11 finds 234 logical issues) but **cannot compute Recall** = (faults found / total actual faults). Without Recall, it is impossible to assess how many faults a tool misses.

**Gap:** No paper has constructed or used a REST API dataset with **intentionally pre-seeded business logic faults** (known ground truth) to quantitatively and precisely measure Fault Detection Recall.

---

## Trích dẫn từ papers — Ctrl+F để xác minh

### GAP-T: Mỗi paper dùng LLM gì? (Copy → Ctrl+F trong PDF)

| # | PDF file | Search string | Kết quả tìm được |
|---|----------|---------------|-------------------|
| #2 | p2-3628797.3628947.pdf | `GPT-3.5 turbo` | "uses the **GPT-3.5 turbo** model through prompt engineering" |
| #3 | p3-3639476.3639769.pdf | `GPT-3.5` | RESTGPT dùng GPT-3.5 Turbo |
| #4 | p4-2407.10227v1.pdf | `gpt-3.5-turbo-1106` | "we use the version of **gpt-3.5-turbo-1106** via the provided API from OpenAI" |
| #5 | p5-3691620.3695511.pdf | `GPT4All` | "we deployed a local instance of **GPT4All** with the model **wizardlm-13b-v1.2.Q4_0.gguf**" |
| #7 | p7-3715737.pdf | `Llama` | LlamaRestTest dùng Llama3-8B fine-tuned |
| #8 | p8-2501.08600v2.pdf | `GPT-4o` | "built-in price tracking for **GPT-4o**, GPT-4o mini, o1, and o1-mini" |
| #9 | p9-2504.05738v4.pdf | `GPT-4o` | "MioHint queries **GPT-4o** for a mutation hint" |
| #10 | p10-2511.18038v1.pdf | `DeepSeek V3.1 Reasoner` | "evaluated on two LLMs, **GPT-4o** and **DeepSeek V3.1 Reasoner**" |
| #11 | p11-2503.15079v1.pdf | `GPT-4o-mini` | "an LLM (e.g., **GPT-4o-mini**)" |
| #12 | p12-...pdf | `Qwen 3` | DeepREST dùng deep RL + **Qwen 3 (14B)** local via LM Studio cho value generation |
| #13 | p13-2604.02039v1.pdf | `GPT-4-Turbo` | "model used in the experiment was **GPT-4-Turbo**" |

**Kết luận GAP-T:** Không paper nào search ra `Gemini` hoặc `Claude` → 0/13 papers dùng Gemini/Claude. Lưu ý: #12 dùng Qwen 3 (14B), không phải GPT → chỉ 9/13 dùng GPT.

---

### GAP-M: Papers đo metric gì? (Copy → Ctrl+F trong PDF)

| # | PDF file | Search string | Metric tìm được |
|---|----------|---------------|-----------------|
| #1 | p1-3597926.3598131.pdf | `branch coverage` | "11.35% to 23.10% for **branch coverage**" |
| #1 | p1-3597926.3598131.pdf | `server error` | Đếm 5XX responses |
| #5 | p5-3691620.3695511.pdf | `branch, line and method coverage` | "higher effectiveness than state-of-the-art with respect to **branch, line and method coverage**" |
| #7 | p7-3715737.pdf | `internal server errors` | Đếm 500 errors |
| #8 | p8-2501.08600v2.pdf | `unique server errors` | Chỉ đếm operations + server errors, **không** đo code coverage |
| #9 | p9-2504.05738v4.pdf | `line coverage` | "increase of **4.95%** absolute in **line coverage**" |
| #9 | p9-2504.05738v4.pdf | `target coverage` | "increase in **target coverage** of **47.72** percentage points" |
| #11 | p11-2503.15079v1.pdf | `234 logical issues` | "identifies **234 logical issues** with an accuracy of **66.19%**" |
| #11 | p11-2503.15079v1.pdf | `49 errors` | "detecting 500-code server crashes (**49 errors** identified in total)" |

**Kết luận GAP-M:** Search `edge case coverage` trong tất cả 13 papers → 0 kết quả. Không paper nào định nghĩa hoặc đo Edge Case Coverage metric.

---

### GAP-D: Papers báo cáo fault detection như thế nào? (Copy → Ctrl+F trong PDF)

| # | PDF file | Search string | Cách báo cáo |
|---|----------|---------------|--------------|
| #6 | (no PDF) | `38 vulnerabilities` | Abstract: "Detected **38 vulnerabilities**... **16 confirmed**" — chỉ đếm tuyệt đối |
| #8 | p8-2501.08600v2.pdf | `only tool to detect a 5xx` | "AutoRestTest was the **only tool to detect a 5xx** status code on the Spotify service" — chỉ đếm tuyệt đối |
| #11 | p11-2503.15079v1.pdf | `234 logical issues` | "identifies **234 logical issues**" — chỉ đếm tuyệt đối |
| #12 | p12-...pdf | `21 unique previously unknown faults` | "detection of **21 unique previously unknown faults**" — chỉ đếm tuyệt đối |

**Kết luận GAP-D:** Search `recall` hoặc `pre-seeded` hoặc `ground truth` hoặc `seeded fault` trong tất cả 13 papers → 0 kết quả liên quan đến fault detection recall trên tập lỗi đã biết trước. Tất cả chỉ báo cáo số tuyệt đối (absolute count), không tính được Recall = faults found / total faults.

---

## Synthesized Gap Statement

> Although 13 studies (2023–2026) have demonstrated that LLMs can significantly improve REST API testing — achieving up to 71.78% line coverage (#11), +47.72pp target coverage (#9), and detecting 38 real-world vulnerabilities (#6) — three critical gaps remain:
>
> **(1)** 9/13 papers rely on the OpenAI GPT ecosystem as primary model; while 4 papers use non-OpenAI models (Llama3, WizardLM, DeepSeek, Qwen 3), no study has evaluated Gemini or Claude on the same benchmark, leaving it unclear whether results generalize across all major LLM families.
>
> **(2)** Evaluation metrics focus on code coverage and server crashes (500 errors); no standardized Edge Case Coverage metric exists for measuring constraint-violation-based fault detection.
>
> **(3)** All datasets used (EMB, public APIs, industrial APIs) lack ground-truth faults, making it impossible to compute Fault Detection Recall — the most critical measure of how many faults a tool misses.
>
> These three gaps motivate: **(a)** a cross-model evaluation (Gemini vs GPT-4o) on the same benchmark, **(b)** defining an Edge Case Coverage metric, and **(c)** constructing an EMB pre-seeded faults dataset for precise Recall measurement.

---
