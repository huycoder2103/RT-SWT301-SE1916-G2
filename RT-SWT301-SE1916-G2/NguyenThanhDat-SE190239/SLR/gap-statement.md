# Gap Statement — LLM REST API Test Generation
Evidence table: N = 10 paper (Core.ac.uk Database)

## Các khoảng trống phát hiện

### GAP-T (Technology): Thiếu sự tích hợp LLM vào cơ chế Stateful Navigation
**Bằng chứng:** [Cột Tool/LLM — Các nghiên cứu dùng LLM hiện nay (như KAT, RESTSpecIT) chỉ tập trung dùng mô hình để đoán/suy luận đặc tả (Specification Inference) tĩnh. Các công cụ giải quyết vấn đề trạng thái (Stateful Fuzzing) mạnh nhất (như DeepREST, ARAT-RL, REST-ler) lại sử dụng RL/Rules-based vốn không có tư duy ngữ nghĩa. Chưa có giải pháp dùng LLM làm tác tử (Agent) điều hướng trong môi trường Fuzzing phức tạp liên tục.]

### GAP-M (Metric): Tập trung vào Coverage, bỏ qua Token Efficiency
**Bằng chứng:** [Cột Metric — Đa phần các bài báo (DeepREST, ARAT-RL, RESTgym) đánh giá chủ yếu dựa trên Code/Branch Coverage. KAT có dùng LLM nhưng chưa có công trình nào đánh giá bài toán tối ưu chi phí (Token Efficiency) và khả năng sinh mã test chất lượng/dễ bảo trì so với tool Fuzzing tạo ra script tạp nham.]

### GAP-D (Dataset): Hạn chế xử lý các API thiếu hoàn toàn tài liệu (Zero-doc)
**Bằng chứng:** [Cột Dataset — Trừ RESTSpecIT thử với 10 API, phần lớn các benchmark hiện hành (như RESTgym 11 APIs, DeepREST 26 APIs) đều dựa trên giả định có sẵn file OpenAPI Spec hoàn thiện. Khoảng trống là việc tự động khám phá và kiểm thử API hoàn toàn black-box bằng suy luận LLM.]

## Phát biểu GAP tổng hợp
Trong khi LLM đã chứng minh năng lực vượt trội trong việc suy luận đặc tả và hiểu luật nghiệp vụ (KAT, RESTSpecIT), các kỹ thuật học tăng cường hoặc fuzzing truyền thống (DeepREST, REST-ler) lại đang làm chủ khả năng dò tìm trạng thái (Stateful Sequence). Sự khuyết thiếu một cơ chế kết hợp (Hybrid Agent) — nơi LLM đóng vai trò điều hướng chiến lược (Chain-of-Thought) cho quá trình sinh Stateful Test Case, kết hợp với việc đo lường Token Efficiency — là một khoảng trống quan trọng cần được giải quyết.
