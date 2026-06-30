# Hypotheses — Automated Test Generation for Web APIs using LLMs

## RQ1 (Về độ bao phủ mã nguồn - Code coverage)
H0: Mô hình LLaMA-3-70B + RAG KHÔNG đạt code coverage ≥ 85% trên tập dữ liệu RESTestBench.
H1: Mô hình LLaMA-3-70B + RAG ĐẠT code coverage ≥ 85% trên tập dữ liệu RESTestBench.
Statistical test dự kiến: Wilcoxon signed-rank test (do output là giá trị liên tục %).

## RQ2 (Về tỷ lệ test case hợp lệ - Validity rate)
H0: Mô hình LLaMA-3-70B + RAG KHÔNG đạt tỷ lệ sinh test case hợp lệ ≥ 90%.
H1: Mô hình LLaMA-3-70B + RAG ĐẠT tỷ lệ sinh test case hợp lệ ≥ 90%.
Statistical test dự kiến: Binomial exact test (đánh giá nhị phân trên từng test case: pass/fail).

## RQ3 (So sánh hiệu suất với baseline)
H0: Không có sự khác biệt có ý nghĩa thống kê về code coverage giữa LLaMA-3-70B + RAG và (EvoMaster / GPT-4).
H1: LLaMA-3-70B + RAG có code coverage cao hơn có ý nghĩa thống kê so với (EvoMaster / GPT-4).
Statistical test dự kiến: Mann-Whitney U test (so sánh 2 hệ thống độc lập).
