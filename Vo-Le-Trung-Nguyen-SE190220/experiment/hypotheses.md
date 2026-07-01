# Hypotheses — LLM REST API Test Generation

## Bối cảnh

Các giả thuyết dưới đây được xây dựng dựa trên:
- **Gap Statement:** GAP-T (thiếu so sánh open-source LLM), GAP-M (thiên lệch metric), GAP-D (thiếu benchmark).
- **Research Questions:** RQ1 (code coverage), RQ2 (fault detection), RQ3 (valid test rate).
- **Evidence table:** N = 28 papers, với các thresholds cụ thể từ literature.

---

## RQ1: Code Coverage

> "Open-source LLM-based approach có đạt code coverage ≥ mức của EvoMaster và RESTler trên cùng tập REST APIs không?"

**H0 (Null Hypothesis):** Không có sự khác biệt có ý nghĩa thống kê về code coverage giữa open-source LLM-based approach và baseline tools (EvoMaster, RESTler) trên cùng tập REST APIs.

**H1 (Alternative Hypothesis):** Open-source LLM-based approach đạt code coverage cao hơn có ý nghĩa thống kê so với baseline tools (EvoMaster, RESTler).

**Cơ sở từ evidence table:**
- LlamaRestTest (Paper #1): Llama3-8B fine-tuned outperform RESTler, MoRest, EvoMaster, ARAT-RL về code coverage trên 12 real-world services.
- KAT (Paper #2): GPT-based approach cải thiện test coverage so với state-of-the-art tools trên 12 services.
- AutoRestTest (Paper #4): Outperform 4 leading black-box tools về code coverage trên 12 services.

**Statistical test dự kiến:** Wilcoxon signed-rank test (one-sided)
- **Lý do:** Code coverage là biến liên tục (%), đo trên cùng tập APIs (paired data). Không giả định phân phối chuẩn vì sample size nhỏ (≥ 10 APIs). Wilcoxon signed-rank phù hợp cho paired non-parametric comparison.
- **Significance level:** α = 0.05
- **Effect size:** Cliff's delta (để đánh giá magnitude of difference)

---

## RQ2: Fault Detection

> "Open-source LLM-based approach có phát hiện được nhiều hơn hoặc bằng số lượng 5xx errors/bugs so với baseline tools không?"

**H0 (Null Hypothesis):** Không có sự khác biệt có ý nghĩa thống kê về số lượng unique 5xx errors/bugs phát hiện được giữa open-source LLM-based approach và baseline tools.

**H1 (Alternative Hypothesis):** Open-source LLM-based approach phát hiện được nhiều unique 5xx errors/bugs hơn có ý nghĩa thống kê so với baseline tools.

**Cơ sở từ evidence table:**
- LlamaRestTest (Paper #1): Outperform về 5xx error detection so với RESTler, MoRest, EvoMaster, ARAT-RL.
- AutoRestTest (Paper #4): Duy nhất trigger internal server error trên Spotify — fault mà 4 tools khác không phát hiện.
- DynER (Paper #6): Phát hiện 3 new bugs trên WordPress và GitLab; tăng +41.21% pass rate trên WordPress.

**Statistical test dự kiến:** Mann-Whitney U test (one-sided)
- **Lý do:** Số lượng faults là biến đếm (count data), có thể không paired nếu các tools phát hiện faults trên các endpoints khác nhau. Mann-Whitney U phù hợp cho independent non-parametric comparison.
- **Bổ sung:** Nếu so sánh trên cùng tập APIs (paired), dùng Wilcoxon signed-rank test thay thế.
- **Significance level:** α = 0.05
- **Effect size:** Cliff's delta

---

## RQ3: Valid Test Rate

> "Open-source LLM-based approach có đạt valid test script rate ≥ 80% không?"

**H0 (Null Hypothesis):** Valid test script rate của open-source LLM-based approach không vượt quá ngưỡng 80% (threshold từ APITestGenie).

**H1 (Alternative Hypothesis):** Valid test script rate của open-source LLM-based approach vượt quá 80%.

**Cơ sở từ evidence table:**
- APITestGenie (Paper #8): 57% valid scripts (1 attempt), tăng lên 80% với 3 attempts.
- APITestGenie v2 (Paper #9): 89% valid test scripts (tối đa 3 attempts) trên 10 real-world APIs (8 industrial, ~1,000 endpoints).
- Ngưỡng 80% được chọn vì đây là mức mà APITestGenie v1 đạt được sau retry mechanism, và là mức tối thiểu để approach có giá trị thực tế trong CI/CD pipeline.

**Statistical test dự kiến:** Binomial exact test (one-sided)
- **Lý do:** Valid test rate là tỷ lệ (proportion) — mỗi test script sinh ra hoặc valid hoặc invalid (binary outcome). Binomial exact test phù hợp để kiểm tra xem tỷ lệ quan sát được có vượt ngưỡng kỳ vọng hay không.
- **Significance level:** α = 0.05
- **Minimum sample size:** ≥ 100 generated test scripts (để đảm bảo statistical power)

---

## Tổng hợp thiết kế thống kê

| RQ | Biến đo | Loại dữ liệu | Statistical test | H1 Direction | α |
|----|---------|---------------|------------------|--------------|---|
| RQ1 | Code coverage (%) | Continuous, paired | Wilcoxon signed-rank | One-sided (>) | 0.05 |
| RQ2 | Unique faults (count) | Discrete, independent/paired | Mann-Whitney U / Wilcoxon | One-sided (>) | 0.05 |
| RQ3 | Valid test rate (%) | Binary proportion | Binomial exact test | One-sided (>) | 0.05 |

**Lưu ý về multiple testing:** Với 3 RQs, cân nhắc áp dụng Bonferroni correction (α_adjusted = 0.05/3 ≈ 0.017) hoặc Holm-Bonferroni method để kiểm soát family-wise error rate.

**Lưu ý về effect size:** Ngoài p-value, luôn report effect size (Cliff's delta cho RQ1/RQ2) để đánh giá practical significance, không chỉ statistical significance.
