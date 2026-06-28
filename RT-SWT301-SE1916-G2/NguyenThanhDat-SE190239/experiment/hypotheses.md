# Hypotheses — LLM-Driven Stateful REST API Testing

## RQ1: Về độ bao phủ (Operation Coverage)
- **H0:** Việc sử dụng LLM (GPT-4o CoT) KHÔNG mang lại Operation Coverage cao hơn đáng kể so với REST-ler / ARAT-RL trên tập API benchmark.
- **H1:** Việc sử dụng LLM (GPT-4o CoT) mang lại Operation Coverage CAO HƠN đáng kể so với REST-ler / ARAT-RL trên tập API benchmark.
- **Statistical test dự kiến:** Wilcoxon signed-rank test (So sánh cặp theo từng API).

## RQ2: Về hiệu suất phát hiện lỗi (Fault Detection)
- **H0:** Số lượng lỗi 5xx duy nhất phát hiện bởi hệ thống điều hướng LLM KHÔNG nhiều hơn có ý nghĩa so với các baseline.
- **H1:** Số lượng lỗi 5xx duy nhất phát hiện bởi hệ thống điều hướng LLM NHIỀU HƠN có ý nghĩa so với các baseline.
- **Statistical test dự kiến:** Mann-Whitney U test (Đánh giá phân phối lỗi trên các lượt chạy fuzzing).

## RQ3: Về sự tương quan giữa chi phí Token và Coverage
- **H0:** Không có sự khác biệt về hiệu quả chi phí (Coverage/1000 tokens) giữa chiến lược Zero-shot và Chain-of-Thought (CoT).
- **H1:** Chiến lược CoT đạt tỷ lệ hiệu quả (Coverage/1000 tokens) cao hơn có ý nghĩa nhờ khả năng dự đoán đúng phụ thuộc, giảm request sai.
- **Statistical test dự kiến:** Binomial exact test (So sánh xác suất sinh payload/trình tự hợp lệ giữa 2 chiến lược).
