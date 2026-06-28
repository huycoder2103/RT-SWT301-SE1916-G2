# Search Log — LLM REST API Test Generation
**Thành viên:** Võ Lê Trung Nguyên 
**Ngày thực hiện:** 2026-06-03

---

## Chuỗi tìm kiếm (Query Strings)

### String 1
**Query nguyên văn:**
("REST API" OR "Web API" OR "OpenAPI" OR "Swagger") AND ("Large Language Model" OR "LLM") AND ("test generation" OR "test case generation") AND ("coverage" OR "fault detection")
**Database:** OpenAlex
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-03 16:03
**Số kết quả:** 223 papers

### String 2
**Query nguyên văn:**
("REST API" OR "Web API") AND ("LLM" OR "Generative AI" OR "zero-shot" OR "few-shot") AND ("automated test generation") AND ("endpoint coverage" OR "operation coverage" OR "bug detection" OR "fault detection")
**Database:** OpenAlex
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-03 16:04
**Số kết quả:** 40 papers

## Tổng hợp trước dedup
| Database |  String   | Kết quả |
|----------| --------  |---------|
| OpenAlex | String 1  |  223    |
| OpenAlex | String 2  |  40     |
| **Tổng trước dedup** | **263** |
| **Sau dedup**        | **206** |
| Số bị loại (trùng lặp)| 57     |

## Ghi chú
- Dedup bằng: Python script (so sánh DOI + normalized title)
- Search thực hiện trên OpenAlex với giao diện web
