# Hypotheses Draft — Automated Test Generation for Web APIs using LLMs
Ngày: 2026-06-16 | Thành viên: Nguyễn Lê Thuận (SE190305)
Nguồn ngưỡng: `experiment/design-rationale.md` | α = 0.05

> File này thay thế `hypotheses.md` của RBL-1. So với bản trước, các ngưỡng đã được gắn nguồn theo Case 2 (thay vì đặt sơ bộ) và phép kiểm định thống kê được điều chỉnh cho phù hợp với thiết kế đo lặp (paired) trên cùng tập API.

## RQ final (PICO)
"Mô hình **LLaMA-3-70B + RAG** (I, temperature=0) có sinh test case cho **EMB (14 REST API)** (P) đạt **line coverage ≥ 60%** và **validity rate ≥ 90%** (O), **so với EvoMaster và GPT-4 không-RAG** (C) không?"

---

## RQ1 — Code coverage
- **H0:** LLaMA-3-70B + RAG **KHÔNG** đạt median line coverage ≥ 60% trên EMB (14 REST API).
- **H1:** LLaMA-3-70B + RAG **ĐẠT** median line coverage ≥ 60% trên EMB (14 REST API).
- **Statistical test dự kiến:** **Wilcoxon signed-rank test** (α = 0.05).
- **Lý do:** output là điểm liên tục (%) đo trên từng API → kiểm định median có ≥ ngưỡng. Ngưỡng 60% derive Case 2 từ SOTA EMB LlamaRestTest 55.3%.

## RQ2 — Validity rate
- **H0:** LLaMA-3-70B + RAG **KHÔNG** đạt tỷ lệ test case hợp lệ ≥ 90%.
- **H1:** LLaMA-3-70B + RAG **ĐẠT** tỷ lệ test case hợp lệ ≥ 90%.
- **Statistical test dự kiến:** **Binomial exact test** (α = 0.05).
- **Lý do:** validity là biến nhị phân trên từng test case (hợp lệ / không) → kiểm định tỷ lệ có ≥ ngưỡng. Ngưỡng 90% trỏ về #4 ARTE (floor 85%).

## RQ3 — So sánh với baseline (comparative)
- **H0:** **Không** có khác biệt có ý nghĩa thống kê về code coverage giữa LLaMA-3-70B + RAG và (EvoMaster / GPT-4 no-RAG).
- **H1:** LLaMA-3-70B + RAG có code coverage **cao hơn có ý nghĩa thống kê** so với (EvoMaster / GPT-4 no-RAG).
- **Statistical test dự kiến:** **Wilcoxon signed-rank test** (paired), so từng cặp trên cùng tập API; α = 0.05, hiệu chỉnh Bonferroni cho 2 so sánh.

> **Điều chỉnh so với RBL-1:** bản trước dự kiến dùng Mann-Whitney U. Tuy nhiên Mann-Whitney U dành cho hai nhóm độc lập, trong khi ở đây cả ba hệ thống được chạy trên cùng tập EMB (14 REST API), tức dữ liệu ghép cặp theo từng API. Do đó phép kiểm định phù hợp là Wilcoxon signed-rank; Mann-Whitney U chỉ thích hợp nếu các hệ thống được đánh giá trên những tập API khác nhau.

---

## Bảng tra test thống kê (đối chiếu RBL-2 Bước 5B)

| RQ | Loại output | Thiết kế | Test |
|----|-------------|----------|------|
| RQ1 | Liên tục (% coverage) | 1 mẫu vs ngưỡng | Wilcoxon signed-rank |
| RQ2 | Nhị phân (valid/invalid) | tỷ lệ vs ngưỡng | Binomial exact test |
| RQ3 | Liên tục, cùng tập API | ghép cặp (paired) | Wilcoxon signed-rank (+ Bonferroni) |

Pilot ở Tuần 7 chỉ nhằm xác nhận giả định về phân phối dữ liệu; nếu phân phối khác với dự kiến, nhóm sẽ ghi nhận điều chỉnh theo §8.6 của proposal thay vì chọn lại phép kiểm định từ đầu.
