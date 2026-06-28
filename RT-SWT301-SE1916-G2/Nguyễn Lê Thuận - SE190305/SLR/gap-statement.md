# Gap Statement — Automated Test Generation for Web APIs using LLMs
Evidence table: N = 11 papers

## Các khoảng trống phát hiện

### GAP-T (Technology): Hạn chế về token limit và phụ thuộc vào model thương mại
**Bằng chứng:** [Cột Tool/LLM & Hạn chế tự nêu] Các nghiên cứu gần đây (vd: Kim et al., 2024; Stennett et al., 2025) chủ yếu sử dụng các mô hình thương mại lớn như GPT-4 để sinh test case. Tuy nhiên, Stennett et al. (2025) có nêu rõ hạn chế về "Token limit issues", đồng thời Kim et al. (2024) phụ thuộc nhiều vào chất lượng API spec. Chưa có nhiều nghiên cứu tập trung giải quyết vấn đề token limit bằng các kỹ thuật như RAG hay fine-tuning các mô hình mã nguồn mở gọn nhẹ hơn.

### GAP-M (Metric): Thiếu các độ đo về chất lượng ngữ nghĩa và độ bền bỉ (robustness) của test case
**Bằng chứng:** [Cột Metric] Hầu hết các paper (vd: Martin-Lopez et al., 2019; Stallenberg et al., 2021; Kim et al., 2024; Pan et al., 2025) chỉ tập trung đánh giá hiệu quả thông qua các độ đo về độ bao phủ cấu trúc (Branch coverage, Code coverage, Endpoint coverage, Integration coverage) hoặc tỷ lệ thực thi thành công (Execution success rate, Pass rate). Không có paper nào đo lường sâu về tính đa dạng ngữ nghĩa (semantic diversity) hay khả năng phát hiện lỗi thực tế sâu bên trong logic nghiệp vụ thay vì chỉ bao phủ code.

### GAP-D (Dataset): Quy mô bộ dữ liệu thực nghiệm còn nhỏ và thiếu tính đại diện
**Bằng chứng:** [Cột Dataset] Quy mô đánh giá trong các nghiên cứu thường khá nhỏ, ví dụ: 5 REST APIs (Martin-Lopez et al., 2019; Kim et al., 2024), 8-10 APIs (Corradini et al., 2024; Stennett et al., 2025), hoặc 3 Web Apps (Abideen & Guo, 2025). Mặc dù Kogler et al. (2026) đề xuất RESTestBench, phần lớn các nghiên cứu trước đó thiếu một bộ dữ liệu chuẩn hóa, đa dạng các domain nghiệp vụ phức tạp trong thực tế.

## Phát biểu GAP tổng hợp
Mặc dù LLM đã được ứng dụng để sinh test case cho REST APIs, các nghiên cứu hiện tại chủ yếu phụ thuộc vào các mô hình thương mại lớn bị giới hạn bởi số lượng token, thực nghiệm trên các tập dữ liệu nhỏ và chỉ đánh giá qua độ bao phủ cấu trúc (coverage) thay vì chất lượng ngữ nghĩa của test case. Do đó, cần có phương pháp sinh test case tối ưu hơn để vượt qua giới hạn token trên các API lớn, đồng thời đề xuất các độ đo đánh giá toàn diện về sự đa dạng và chất lượng ngữ nghĩa của test case trên bộ dữ liệu quy mô lớn hơn.
