# Hypotheses — LLM for REST API Test Generation

## RQ1: So sánh tỷ lệ phát hiện lỗi (Fault Detection Recall) giữa Gemini 1.5 Pro và GPT-4o
**H0 (Giả thuyết không):** Phương pháp sinh test case bằng Gemini 1.5 Pro KHÔNG đạt tỷ lệ phát hiện lỗi (Fault Detection Recall) cao hơn hoặc bằng so với hệ thống baseline GPT-4o trên tập dữ liệu pre-seeded faults.
**H1 (Giả thuyết đối):** Phương pháp sinh test case bằng Gemini 1.5 Pro ĐẠT tỷ lệ phát hiện lỗi (Fault Detection Recall) cao hơn đáng kể so với hệ thống baseline GPT-4o trên tập dữ liệu pre-seeded faults.

**Statistical test dự kiến:** `Mann-Whitney U test` 
*(Lý do: Dùng để so sánh giá trị trung bình của đầu ra liên tục (tỷ lệ % Recall) giữa 2 hệ thống/nhóm độc lập là Gemini và GPT-4o).*

---

## RQ2: Đánh giá khả năng bao phủ trường hợp biên (Edge Case Coverage)
**H0 (Giả thuyết không):** Phương pháp sinh test case bằng Gemini 1.5 Pro KHÔNG đạt độ bao phủ trường hợp biên (Edge Case Coverage) ≥ 80%.
**H1 (Giả thuyết đối):** Phương pháp sinh test case bằng Gemini 1.5 Pro ĐẠT độ bao phủ trường hợp biên (Edge Case Coverage) ≥ 80%.

**Statistical test dự kiến:** `Wilcoxon signed-rank test` (1-sample)
*(Lý do: Dùng để so sánh một tập kết quả đầu ra liên tục (tỷ lệ % Coverage của từng API trong tập benchmark) với một giá trị ngưỡng cố định là 80%).*
