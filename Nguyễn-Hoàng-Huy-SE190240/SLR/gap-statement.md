# Gap Statement — LLM for REST API Test Generation
**Evidence table:** N = 13 papers (2023–2026)

---

## Các khoảng trống phát hiện

### GAP-T (Technology): Thiếu đánh giá và so sánh các LLM ngoài hệ sinh thái OpenAI trên cùng tập dữ liệu
**Bằng chứng:** Cột Tool/LLM trong evidence table cho thấy sự thống trị của họ nhà GPT: **9/13 paper** sử dụng GPT-series làm model chính. Cụ thể: GPT-4o (#9 đạt +47.72 percentage points target coverage; #10 so sánh GPT-4o với DeepSeek V3.1), GPT-4o-mini (#11 đạt 71.78% line coverage), GPT-4-Turbo (#13), và GPT-3.5-Turbo (#2, #3, #4, #6, #8). Ngoài GPT, chỉ có **2 paper** thử nghiệm model non-GPT: #7 dùng Llama3-8B (fine-tuned trên 1.8M API parameters) và #5 dùng GPT4All/WizardLM-13B-v1.2 (chạy local, quantized Q4_0).
**Khoảng trống:** Chưa có paper nào đánh giá hoặc so sánh năng lực sinh test case zero-shot/few-shot của các LLM thương mại hàng đầu khác như **Gemini** (Google) hay **Claude** (Anthropic) trên cùng benchmark (như EMB benchmark được dùng ở #1, #5, #9).

### GAP-M (Metric): Tập trung vào Code Coverage và 500-Error, thiếu độ đo cho Edge Cases và Logical Bugs
**Bằng chứng:** Cột Metric cho thấy hầu hết các paper đo lường độ bao phủ (Coverage) và số lượng lỗi Server Crash (mã 500):
- Khía cạnh Coverage: Paper #11 đo Line (71.78%), Branch (39.98%), Method (73.06%). Paper #8 đạt 58.33% Method coverage.
- Khía cạnh Fault Detection: Chủ yếu đếm số lượng lỗi 500 Internal Server Error (paper #8 đếm được 42 operations có lỗi 500, paper #11 tìm ra 49 server crashes).
Duy nhất paper #11 cố gắng đo lường "logical issues" (tìm được 139 bugs) nhưng thừa nhận **accuracy chỉ đạt 66.19%** do còn nhiều false positives.
**Khoảng trống:** Chưa có nghiên cứu nào đưa ra độ đo cụ thể về khả năng bao phủ các trường hợp kiểm thử biên (Edge Case Coverage) dựa trên việc chủ đích vi phạm các ràng buộc (constraints) của OpenAPI spec để tìm lỗi logic tiềm ẩn, thay vì chỉ làm crash server (500 error).

### GAP-D (Dataset): Thiếu tập dữ liệu có lỗi logic được cấy sẵn (Pre-seeded Faults) để đo Recall chính xác
**Bằng chứng:** Cột Dataset chỉ ra các paper chủ yếu chạy trên benchmark hoặc hệ thống thực tế:
- EMB benchmark (11–16 REST APIs): Dùng bởi #1, #5, #9.
- Public/Real-world APIs (Spotify, FDIC, Azure...): Dùng bởi #4 (12 APIs), #6 (9 cloud services), #7 (12 services), #8 (12 services), #11 (12 systems).
Vì chạy trên hệ thống thực tế chưa biết trước tổng số lỗi (ground truth), các nghiên cứu chỉ "đếm" được số lỗi phát hiện thêm (ví dụ: #6 tìm ra 38 vulnerabilities) mà không thể tính được tỷ lệ Recall.
**Khoảng trống:** Chưa có paper nào thực nghiệm trên dataset REST APIs được cấy sẵn lỗi logic nghiệp vụ (pre-seeded business logic faults) để đánh giá định lượng chính xác Fault Detection Recall của LLM.

---

## Phát biểu GAP tổng hợp

Mặc dù các nghiên cứu từ 2023–2026 đã áp dụng thành công LLM (chủ yếu GPT-series, chiếm 9/13 paper) để nâng cao code coverage (đạt tới 71.78% Line Coverage trong #11 hoặc tăng +47.72pp Target Coverage trong #9), **hiện vẫn thiếu các nghiên cứu đối chuẩn năng lực của đa dạng mô hình (như Gemini, Claude) trong việc sinh kịch bản kiểm thử biên (edge cases), đồng thời chưa có đánh giá định lượng chính xác về tỷ lệ tìm lỗi (Recall) thông qua tập dữ liệu REST APIs được cấy lỗi có chủ đích (pre-seeded faults dataset)**.