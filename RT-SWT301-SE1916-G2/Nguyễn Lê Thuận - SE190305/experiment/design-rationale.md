# Experiment Design Rationale — Automated Test Generation for Web APIs using LLMs
Ngày: 2026-06-16 | GAP source: `SLR/gap-analysis.md` | Thành viên: Nguyen Le Thuan (SE190305)
Quy tắc: mỗi quyết định trỏ về một ô cụ thể trong evidence table (N=11).

---

## Bảng Quyết Định (7 yếu tố)

| # | Quyết định | Giá trị | Nguồn gốc (ô evidence table) |
|---|------------|---------|------------------------------|
| 1 | **Dataset** | EvoMaster Benchmark (EMB) — 14 REST API JVM | GAP-D + #2 Martin-Lopez'19 (EvoMaster dùng EMB). *Đổi từ RESTestBench sau verify: RESTestBench 3 API + mutation, không hợp code coverage* |
| 2 | **Pipeline base** | #5 Kim'24 (Multi-Agent, code coverage trên REST API) — thay GPT-4 → LLaMA-3-70B + thêm RAG | #5 (paradigm coverage-on-REST gần nhất) + #8 (token limit cần giải) + #7 (tiền lệ LLaMA-3) |
| 3 | **LLM/Tool** | LLaMA-3-70B (open-source) qua **Groq** `llama-3.3-70b-versatile`, temperature = 0 | GAP-T — cột Tool/LLM (#5,#8,#11 đều thương mại) |
| 4 | **Metric chính** | Code coverage (line/branch) — coverage instrumentation | GAP-M nền + #5 (code coverage 81%), #2 (88%), #6 (90%) |
| 5 | **Metric phụ 1** | Validity rate — OpenAPI schema validator + HTTP status | #4 ARTE (validity 85%) |
| 6 | **Metric phụ 2 (mới)** | Semantic diversity — cosine similarity, `sentence-transformers/all-MiniLM-L6-v2` | GAP-M (không paper nào đo) |
| 7 | **Baseline type** | Comparative (EvoMaster, GPT-4 no-RAG) **+** Absolute threshold | Claim type RQ (RQ1/2 absolute, RQ3 comparative) |
| 8 | **Threshold RQ1 (coverage)** | ≥ 60% line | Case 2 — neo vào LlamaRestTest 55.3% (SOTA EMB); xem lý giải dưới |
| 9 | **Threshold RQ2 (validity)** | ≥ 90% | Case 2 — xem lý giải dưới |

---

## Chi tiết Pipeline (đủ để reproduce)

| Thành phần | Ghi rõ | Nguồn |
|------------|--------|-------|
| LLM | LLaMA-3-70B (open-source) — **Groq** `llama-3.3-70b-versatile` (free tier; ghi rõ version để reproduce) | GAP-T |
| RAG | Index OpenAPI spec → retrieve chunk liên quan từng endpoint → đưa vào prompt (giải token limit) | #8 "Token limit issues" |
| Prompt strategy | Few-shot (kèm ví dụ test case có cấu trúc) | Base paper #5 |
| Temperature | 0 | Reproducibility |
| Coverage tool | Instrumentation theo ngôn ngữ SUT (vd JaCoCo cho Java SUT) | #5, #6 |
| Validity tool | OpenAPI schema validation + HTTP 2xx check | #4 |
| Diversity tool | `sentence-transformers` model `all-MiniLM-L6-v2` (HuggingFace) — tính cosine pairwise giữa test inputs | GAP-M |
| Baseline 1 | EvoMaster (white-box, search-based) | #2 |
| Baseline 2 | GPT-4 **không RAG** (cùng prompt) | #5, #8 |

---

## Lý giải threshold

**Threshold RQ1 — Line coverage ≥ 60% (Case 2, derive từ SOTA trên chính EMB).**
Vì threshold phải bắt nguồn từ kết quả đã công bố trên cùng tập dữ liệu, chúng tôi tổng hợp mức bao phủ thực đo trên EMB từ các nghiên cứu gần nhất:

| Hệ thống trên EMB | Line | Method | Branch | Nguồn |
|-------------------|------|--------|--------|-------|
| EvoMaster (white-box) | ~45% | 45.8% | 17.8% | LlamaRestTest, FSE 2025 |
| EvoMaster-WB (tốt nhất trong 10 công cụ) | 52.76% | — | — | No-Time-to-Rest, ISSTA 2022 |
| **LlamaRestTest (SOTA, Llama mã nguồn mở)** | **55.3%** | **55.8%** | **28.3%** | LlamaRestTest, FSE 2025 |

Theo Case 2, mức sàn hợp lý là kết quả SOTA hiện tại trên EMB, tức 55.3% line coverage của LlamaRestTest. Chúng tôi đặt ngưỡng ở mức **≥ 60% line coverage** — cao hơn SOTA mã nguồn mở khoảng 5 điểm phần trăm — với kỳ vọng rằng quy mô lớn hơn của LLaMA-3-70B (so với Llama-8B trong LlamaRestTest) cùng cơ chế RAG để xử lý giới hạn token sẽ mang lại một cải thiện khiêm tốn nhưng có ý nghĩa. Nói cách khác, sàn 55.3% (LlamaRestTest, EMB) được làm tròn lên thành ngưỡng 60%.

Ngưỡng 85% trong bản RBL-1 đã được loại bỏ vì không có nguồn và cao gần gấp rưỡi mức SOTA thực tế trên EMB, vi phạm nguyên tắc không tự đặt threshold.

**Threshold RQ2 — Validity rate ≥ 90% (Case 2, floor từ cột Kết quả).**
ARTE (Alonso, 2023) đạt 85% validity rate trên cùng loại độ đo và là mốc tham chiếu trực tiếp; APITestGenie cũng báo cáo mức 89% test hợp lệ. Lấy 85% làm sàn, chúng tôi đặt ngưỡng ở **≥ 90% validity rate**, tức chỉ cao hơn mức cao nhất hiện có một biên độ nhỏ và do đó vẫn nằm trong vùng khả thi.

**Threshold cho semantic diversity (độ đo mới):** chưa có nghiên cứu nào công bố mức tham chiếu nên thuộc Case 3. Thay vì áp một ngưỡng pass/fail cứng, độ đo này sẽ được báo cáo dưới dạng so sánh giữa LLaMA-3-70B+RAG, GPT-4 và EvoMaster, và sẽ được hiệu chỉnh qua một mini-pilot 5–10 API trước khi nộp proposal.

> Mọi ngưỡng trong file đều trỏ về một ô kết quả cụ thể trong evidence table; không có giá trị nào được đặt theo cảm tính.
