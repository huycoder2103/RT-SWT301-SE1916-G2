# Gap Statement — LLM REST API Test Generation
Evidence table: N = 28 papers

## Các khoảng trống phát hiện

### GAP-T (Technology): Thiếu nghiên cứu hệ thống về LLM mã nguồn mở cho REST API test generation
**Bằng chứng:** Trong 28 paper, phần lớn sử dụng GPT family (GPT-3.5, GPT-4.1, GPT-5.2-Codex — 6 papers) hoặc không nêu rõ model cụ thể (18 papers). Chỉ duy nhất **LlamaRestTest** (#1, Kim et al., 2025) fine-tune mô hình mã nguồn mở Llama3-8B và cho kết quả vượt trội hơn cả RESTGPT (GPT-powered). **RestTSLLM** (#21, Barradas et al., 2025) là paper duy nhất so sánh nhiều LLM (Claude 3.5 Sonnet, DeepSeek R1, Qwen 2.5 32b, Sabiá 3) nhưng không bao gồm fine-tuning. **TAPE** (#3, Poth et al., 2024) đánh giá StarCoder trong industrial setting nhưng chỉ so sánh 1 LLM. Không có paper nào so sánh hệ thống nhiều open-source LLM (Llama, Mistral, DeepSeek, Qwen) cho bài toán REST API test generation, đặc biệt với kỹ thuật fine-tuning và quantization.

### GAP-M (Metric): Thiếu đa dạng trong metric đánh giá — thiên lệch về code coverage, bỏ qua semantic correctness và reproducibility
**Bằng chứng:** Code/Operation/Line coverage là metric phổ biến nhất (10/28 papers), tiếp theo là fault/bug detection (7 papers). Tuy nhiên:
- **Mutation score/accuracy** chỉ được sử dụng bởi 3 papers: **RestTSLLM** (#21), **RESTestBench** (#5), và **MioHint** (#27, Li et al., 2025 — đạt 67x improvement in mutation accuracy).
- **Reproducibility** hầu như không được đo lường trong bất kỳ paper nào.
- **Log coverage** chỉ xuất hiện trong 2 papers: **Assessing REST API** (#6) và **LoBREST** (#18, Yang et al., 2026).
- **Requirements-based evaluation** chỉ được **RESTestBench** (#5) và **APITestGenie v2** (#19) đề cập.
- **Constraint mining precision** là metric mới từ **RBCTest** (#22, Huynh et al., 2025): 85.1%–93.6%.
- Không có paper nào đánh giá đồng thời cả code coverage, mutation score, semantic correctness, và reproducibility.

### GAP-D (Dataset): Thiếu benchmark chuẩn hóa — các paper sử dụng dataset khác nhau, quy mô nhỏ, khó so sánh
**Bằng chứng:** Phần lớn evaluations chỉ dùng 2–12 services:
- **LlamaRestTest** (#1), **KAT** (#2), **AutoRestTest** (#9) đều dùng 12 real-world REST services nhưng không rõ có trùng nhau hoàn toàn hay không.
- **MioHint** (#27) dùng 16 real-world REST API services — số lượng lớn nhất.
- **RBCTest** (#22) dùng 19 real-world APIs — lớn nhất về số APIs nhưng chỉ cho oracle mining.
- **DynER** (#8) và **From Requirements to Executable Tests** (#25) chỉ dùng 2 APIs.
- **RESTestBench** (#5) là nỗ lực đầu tiên xây dựng benchmark chuyên dụng, nhưng chỉ bao gồm 3 REST services.
- **SmartAPIForge** (#24) đánh giá trên 3,079 API creation tasks nhưng là về API generation, không test generation.
- **BOSQTGEN** (#26) đạt 82% code coverage trên RESTful benchmarks với +20% so với prior SOTA.
- Không có benchmark chuẩn hóa nào được sử dụng chung giữa các papers.

## Phát biểu GAP tổng hợp

Mặc dù LLM đã chứng minh tiềm năng lớn trong REST API test generation (28 papers, 2023–2026), vẫn tồn tại ba khoảng trống nghiên cứu chính: **(1)** chưa có nghiên cứu hệ thống so sánh và fine-tune nhiều open-source LLM cho bài toán này — phần lớn phụ thuộc vào closed-source GPT models hoặc không nêu rõ model; **(2)** metric đánh giá thiên lệch về code coverage (10/28), trong khi mutation testing (3/28), semantic correctness, và đặc biệt reproducibility hầu như bị bỏ qua; **(3)** thiếu benchmark chuẩn hóa để so sánh công bằng — RESTestBench là nỗ lực đầu tiên nhưng chỉ 3 services, và các papers khác dùng 2–19 services khác nhau.
