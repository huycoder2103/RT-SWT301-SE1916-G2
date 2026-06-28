# Search Log — LLM for REST API Test Generation
**Thành viên:** Nguyễn Lê Thuận
**Ngày thực hiện:** 03/06/2026

---

## Chuỗi tìm kiếm (Query Strings)

### String A
**Query nguyên văn:**
```
("REST API" OR "Web API" OR "OpenAPI" OR "Swagger") AND ("Large Language Model" OR "LLM") AND ("test generation" OR "test case generation") AND ("coverage" OR "fault detection")
```
**Database:** Semantic Scholar
**Bộ lọc:** Không có bộ lọc
**Ngày search:** 03/06/2026  
**Số kết quả (hiển thị đầu trang):** 73
**Số paper thu thập (7 trang đầu):** 70

---

### String B
**Query nguyên văn:**
```
("REST API" OR "Web API") AND ("LLM" OR "Generative AI" OR "zero-shot" OR "few-shot") AND ("automated test generation") AND ("endpoint coverage" OR "operation coverage" OR "bug detection" OR "fault detection")`
```
**Database:** Semantic Scholar  
**Bộ lọc:** Không có bộ lọc 
**Ngày search:** 03/06/2026
**Số kết quả (hiển thị đầu trang):** 250
**Số paper thu thập (10 trang đầu):** 100

---

---

## Tổng hợp trước dedup

| Database | String   | Số paper thu thập |
|----------|----------|-------------------|
| Semantic Scholar | String A | 70        |
| Semantic Scholar | String B | 100        |
| **Tổng trước dedup** | | **170** |
| **Sau dedup**        | | **166** |
| Số bị loại (trùng)   | | 4     |

---

## Ghi chú

- Thực hiện dedup bằng: Google Sheets
- Paper trùng nhiều nhất giữa: [ví dụ: String A và String B]
- Ghi chú thêm: 