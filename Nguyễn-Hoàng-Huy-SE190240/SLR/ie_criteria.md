# Inclusion and Exclusion Criteria (IE Criteria)

**Topic:** LLM REST API Test Generation
**Trạng thái nhóm:** Đã chốt chính thức (Chấp thuận bởi toàn bộ thành viên)

---

## 1. Inclusion Criteria (IC) - Tiêu chí lựa chọn
Các nghiên cứu được giữ lại phải thỏa mãn **tất cả** các tiêu chí lựa chọn dưới đây:

*   **IC1 (Language):** Nghiên cứu phải được viết hoàn toàn bằng tiếng Anh.
*   **IC2 (Timeline):** Nghiên cứu được xuất bản trong khoảng thời gian từ năm 2018 trở về sau (2018 – Hiện tại).
*   **IC3 (Context Scope):** Nội dung nghiên cứu liên quan trực tiếp đến REST API/Web API testing, OpenAPI/Swagger, hoặc các giải pháp sinh kiểm thử tự động cho API (API test generation).
*   **IC4 (Technology):** Nghiên cứu có sử dụng Mô hình ngôn ngữ lớn (LLM) hoặc có xây dựng một hệ thống baseline test-generation đủ liên quan, rõ ràng để phục vụ so sánh khoảng trống nghiên cứu (GAP).
*   **IC5 (Empirical Evidence):** Nghiên cứu bắt buộc phải có kết quả thực nghiệm, có số liệu và các metric đánh giá cụ thể (ví dụ: Coverage, Precision, Recall, Pass rate...), không lựa chọn các bài báo chỉ thuần mang tính chất khảo sát (survey) hoặc nêu quan điểm cá nhân (opinion).

---

## 2. Exclusion Criteria (EC) - Tiêu chí loại trừ
Một nghiên cứu sẽ bị loại ngay lập tức nếu vi phạm **chỉ cần một** trong các tiêu chí sau đây tại vòng sàng lọc:

*   **EC1 (Duplicate):** Nghiên cứu bị trùng lặp hoàn toàn về nội dung hoặc tiêu đề với bài khác đã có trong danh sách (dùng để lọc bổ sung nếu bước de-duplication tự động còn sót).
*   **EC2 (Access Limit):** Không tìm được tài liệu bản PDF hợp pháp hoặc không thể tiếp cận/tải xuống nội dung đầy đủ (Full-text).
*   **EC3 (Format & Length):** Bài báo thuộc dạng Poster, Extended Abstract, Slide thuyết trình, hoặc bài viết có độ dài quá ngắn (< 4 trang).
*   **EC4 (Out of Domain):** Nghiên cứu chỉ bàn luận về kiểm thử giao diện (UI), kiểm thử đơn vị (Unit testing), hoặc kiểm thử ứng dụng di động (Mobile testing); không liên quan đến REST API hay Web API.
*   **EC5 (Out of Phase):** Nghiên cứu chỉ tập trung vào giai đoạn thực thi kiểm thử (test execution), giám sát hệ thống (monitoring), hoặc bảo trì mã kiểm thử (test maintenance); không bàn về việc sinh kịch bản hay sinh mã kiểm thử (test generation).
*  **EC6 (Generation Focus):** Paper không chủ yếu về sinh test case — loại paper về test amplification, test oracle, test naming, metamorphic testing, robustness testing
*  **EC7 (Publication Type):** Thesis, luận văn, sách, hoặc nguồn không peer-reviewed
---

## 3. Hướng dẫn áp dụng mã tiêu chí cho các file CSV

*   **Tại vòng Screening Title/Abstract (`02_after_screening_v1.csv`):** Đọc nhanh Tiêu đề và Tóm tắt. Nếu phát hiện vi phạm rõ ràng ở các mã thuộc miền Scope như `EC4` hoặc `EC5`, hãy đổi trạng thái thành `EXCLUDE` và ghi mã tương ứng ở cột lý do. Nếu thấy bài viết có vẻ tiềm năng hoặc chưa chắc chắn, ghi `Unsure` và để trống cột lý do.
*   **Tại vòng Full-text (`03_final_included.csv`):** Đọc chi tiết toàn văn của các bài `INCLUDE` và `Unsure`. Kiểm tra kỹ điều kiện thực nghiệm (`IC5`) và độ dài/định dạng (`EC3`, `EC2`). Bài viết vượt qua hoàn toàn sẽ ghi nhận `Include` cùng lý do đạt đầy đủ `IC1-IC5`.