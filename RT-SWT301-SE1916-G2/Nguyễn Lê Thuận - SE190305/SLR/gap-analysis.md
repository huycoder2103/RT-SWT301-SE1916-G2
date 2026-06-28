# GAP Analysis — Automated Test Generation for Web APIs using LLMs
Evidence table: N = 11 paper | Ngày: 2026-06-16 | Thành viên: Nguyen Le Thuan (SE190305)
Nguồn: `SLR/evidence-table.md` (kế thừa RBL-1). Quy tắc: mỗi GAP trỏ về cột cụ thể + kiểm tra phản chứng từng paper.

---

## BƯỚC 1 — Kiểm tra evidence table (5 gate)

| Gate | Tiêu chí | Kết quả | Trạng thái |
|------|----------|---------|------------|
| P1: Số paper | ≥ 5 | 11 paper | ✅ Pass |
| P2: Cột Tool/LLM | ≥ 90% hàng điền | 9/11 = 82% (2 N/A: #1 diversity-based, #10 prioritization — phi-LLM, hợp lệ) | ⚠️ Borderline (N/A chính đáng) |
| P3: Cột Kết quả | ≥ 50% có số | 10/11 = 91% (chỉ #10 N/A) | ✅ Pass |
| P4: Cột Hạn chế | ≥ 50% hàng điền | 9/11 = 82% (đã backfill #1,3,4,6,9,10,11; còn #2,#7 chờ đọc thủ công) | ✅ Pass |
| P5: Cột Metric | tên metric cụ thể | 11/11 metric rõ ràng | ✅ Pass |

Sau khi bổ sung phần *Threats to Validity / Future Work* (được xác minh trực tiếp từ từng paper, có nguồn), gate P4 đạt 82% và vượt ngưỡng yêu cầu. Hai paper còn lại — Martin-Lopez (2019) và Abideen & Guo (2025) — hiện chỉ truy cập được dưới dạng paywall nên hạn chế được đánh dấu "cần đọc thủ công" thay vì suy diễn. Riêng gate P2 ở mức 82%: hai ô trống tương ứng với các phương pháp phi-LLM (diversity-based và prioritization), do đó đây là khoảng trống hợp lệ chứ không phải dữ liệu thiếu.

---

## BƯỚC 2A — Bốn loại GAP

| Loại | Cột nguồn | Phát hiện | Ví dụ ô |
|------|-----------|-----------|---------|
| **GAP-T** | Tool/LLM + Hạn chế | LLaMA-3-70B (open-source lớn) + RAG để xử lý token limit chưa được dùng cho REST API test gen | #8 "Token limit issues" (GPT-4) chưa được giải quyết |
| **GAP-M** | Metric | Không paper nào đo *semantic diversity* — chỉ đo coverage cấu trúc / execution | #1,#2,#3,#5,#6,#9 đều structural coverage |
| **GAP-D** | Dataset | Quy mô nhỏ (3–12 API), chưa đánh giá LLaMA-3-70B+RAG trên benchmark coverage chuẩn EMB (14 API) | #2:5, #7:3, #6:8, #9:12 |
| **GAP-S** | Hạn chế | 2 cụm hạn chế nổi lên nhưng mỗi cụm chỉ 3 paper < ngưỡng ceil(0.4×11)=5: (a) *generalizability/quy mô nhỏ* #1,#3,#11; (b) *phụ thuộc spec/OAS* #4,#5,#6 | Chưa đủ ngưỡng GAP-S, nhưng (a) củng cố GAP-D, (b) củng cố GAP-T |

**Ưu tiên:** GAP-T > GAP-M > GAP-D > GAP-S.

---

## BƯỚC 2B — Kiểm tra phản chứng (BẮT BUỘC)

### GAP-T tuyên bố: *Chưa có nghiên cứu nào dùng LLaMA-3-70B kết hợp RAG để khắc phục token limit khi sinh test case cho REST API.*

| # | Paper | Đã làm chưa? | Ghi chú |
|---|-------|--------------|---------|
| 1 | Biagiola'19 | Không | Diversity-based, phi-LLM |
| 2 | Martin-Lopez'19 | Không | EvoMaster (search-based), phi-LLM |
| 3 | Stallenberg'21 | Không | RESTest (clustering), phi-LLM |
| 4 | Alonso'23 (ARTE) | Không | Knowledge-base, phi-LLM |
| 5 | Kim'24 | Không | GPT-4 **thương mại**, không RAG; phụ thuộc spec quality |
| 6 | Corradini'24 (DeepREST) | Không | Deep RL, không LLM/RAG |
| 7 | Abideen'25 | **Một phần** | Dùng LLaMA-3 (open-source) **nhưng** cho Web App E2E (không phải REST API), **không RAG**, không nêu biến thể 70B |
| 8 | Stennett'25 (AutoRestTest) | Không | GPT-4; **nêu rõ "Token limit issues" nhưng KHÔNG xử lý** → củng cố gap |
| 9 | Pan'25 (SAINT) | Không | Program analysis + agents; không RAG cho token |
| 10 | Khatsko'26 | Không | Prioritization, không sinh test bằng LLM |
| 11 | Kogler'26 (RESTestBench) | Không | GPT-4o/Claude 3 **thương mại**, không RAG, pass rate chỉ 65% |

**Kết luận:** khoảng trống được xác nhận. Trường hợp gần nhất có thể bác bỏ là Abideen & Guo (2025), vốn đã dùng LLaMA-3 mã nguồn mở; tuy nhiên nghiên cứu này hướng tới kiểm thử E2E cho ứng dụng web (không phải REST API), không áp dụng RAG và không dùng biến thể 70B, nên không phủ nhận được khoảng trống.

### GAP-M tuyên bố: *Chưa paper nào đo semantic diversity của test case sinh ra.*

| # | Metric trong bảng | Đo semantic diversity? |
|---|-------------------|------------------------|
| 1,3 | Branch coverage | Không |
| 2 | Endpoint coverage | Không |
| 5 | Code coverage | Không |
| 6 | Coverage | Không |
| 9 | Integration coverage | Không |
| 4 | Validity rate | Không |
| 7 | Execution success rate | Không |
| 8 | Fault detection | Không |
| 11 | Pass rate | Không |

**Kết luận:** khoảng trống được xác nhận — toàn bộ 11 paper đều dừng ở bao phủ cấu trúc hoặc tỷ lệ thực thi, không có nghiên cứu nào đo tính đa dạng ngữ nghĩa của test case sinh ra.

### GAP-D tuyên bố: *Chưa có đánh giá LLaMA-3-70B + RAG trên một benchmark coverage chuẩn hóa.*
RESTestBench (Kogler, 2026) chỉ gồm 3 service và đánh giá theo requirements-based mutation; EvoMaster (Martin-Lopez, 2019) tuy chạy trên EMB nhưng chưa kết hợp LLM mã nguồn mở với RAG. Các nghiên cứu còn lại đều giới hạn ở ≤12 API. Khoảng trống được xác nhận và nghiên cứu này chọn EMB (14 REST API) làm tập đánh giá.

---

## BƯỚC 2C — Feasibility check (GAP primary = GAP-T)

| Tiêu chí | Câu hỏi | Mức | Ghi chú / Mitigation |
|----------|---------|-----|----------------------|
| Dataset | Benchmark coverage public, tải được? | ✅ (đã đổi) | **VERIFIED:** RESTestBench bị loại (3 API + mutation). Đổi sang **EMB (EvoMaster Benchmark) — 14 REST API JVM, public GitHub, có instrumentation coverage**. Threshold đã hạ về **≥60% line** (Case 2, neo LlamaRestTest 55.3% trên EMB) — xem design-rationale |
| Tool/API | LLaMA-3-70B có free/rẻ? | ✅ | **CHỐT: Groq free tier** host `llama-3.3-70b-versatile` (30 RPM, 100K token/ngày, không cần thẻ). Full 14 API qua paid (~$0.59/$0.79 per M token) ≈ **<$2 tổng** |
| Compute | Phần cứng để chạy? | ✅ | Hosted inference (Groq LPU) — **không cần GPU local**; backup Together AI / 4-bit Colab nếu cần version 3.0 chính xác |
| Ground truth | Cần annotation thủ công? | ✅ | Coverage đo tự động (instrumentation), validity qua schema/HTTP, diversity qua embedding — **không cần annotate tay** |
| Skills | Nhóm implement được pipeline RAG? | ⚠️ | RAG (LangChain/LlamaIndex) + EvoMaster + coverage tooling — có tutorial, cần học < 1 tuần |
| Thời gian | Hoàn thành trong số tuần còn lại? | ⚠️ | 14 API × 3 hệ thống — cần chạy song song và có thời gian dự phòng |
| Contribution | Kết quả âm tính có giá trị? | ✅ | Kể cả khi không đạt ngưỡng, đây vẫn là baseline mã nguồn mở 70B+RAG đầu tiên trên EMB |

**Kết quả:** 0 ❌ / 2 ⚠️ (Skills, Thời gian) → ✅ **An toàn — tiếp tục với GAP-T** (đạt quy tắc ≤2 ⚠️, không ❌).

**Mitigation cho 2 ⚠️ còn lại:**
1. **Skills (RAG):** dùng LlamaIndex/LangChain có sẵn tutorial; prototype RAG trên 1 API trong tuần đầu.
2. **Thời gian:** nếu tight → bỏ RQ3 (so sánh), giữ RQ1 (coverage) + RQ2 (validity) làm lõi.

**Đã giải quyết (không còn ⚠️):** Dataset (chốt EMB 14 API), Tool/API + Compute (chốt Groq free tier `llama-3.3-70b-versatile`, <$2). **Lưu ý reproducibility:** ghi rõ version LLM dùng trong báo cáo — Groq hiện phục vụ Llama 3.3-70B; nếu mentor yêu cầu đúng Llama-3.0-70B thì dùng Together AI hoặc 4-bit local.

---

## BƯỚC 2D — Ghi nhận GAP cuối cùng

### GAP Chính: **GAP-T (Technology)**
Phần lớn các nghiên cứu sinh test case cho REST API hiện vẫn phụ thuộc vào mô hình thương mại (GPT-4, GPT-4o, Claude — Kim 2024, Stennett 2025, Kogler 2026) và chịu giới hạn token, điển hình là Stennett (2025) nêu thẳng "Token limit issues" nhưng chưa xử lý. Đến nay chưa có công trình nào kết hợp LLaMA-3-70B (mã nguồn mở) với RAG để vượt giới hạn token trên các OpenAPI spec phức tạp; đây là khoảng trống công nghệ trọng tâm mà nghiên cứu hướng tới.

### GAP Secondary: **GAP-M (Metric)**
Toàn bộ các paper trong bảng đều đánh giá qua bao phủ cấu trúc hoặc tỷ lệ thực thi, và không nghiên cứu nào đo tính đa dạng ngữ nghĩa của test case. Việc bổ sung một độ đo về đa dạng ngữ nghĩa do đó là đóng góp về mặt phương pháp đánh giá.

> GAP-D giữ ở vai trò bối cảnh (đánh giá trên EMB 14 API), không phải GAP primary do rủi ro feasibility.
