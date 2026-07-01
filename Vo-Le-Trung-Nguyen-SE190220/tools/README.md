# Tools — SLR Processing Scripts

Các script Python dùng để xử lý dữ liệu cho Systematic Literature Review.

## Danh sách scripts

### `process_slr.py` — Script xử lý chính
**Chức năng:** Đọc 2 file CSV gốc từ OpenAlex (String 1 + String 2), thực hiện:
1. **Dedup** — Loại bỏ paper trùng lặp (so sánh DOI + normalized title)
2. **V1 Screening** — Lọc title + abstract theo tiêu chí IC/EC từ `ie_criteria.md`
3. **V2 Screening** — Đánh giá full-text cho các paper pass V1

**Output:**
- `SLR/01_all_records.csv` — 206 records sau dedup
- `SLR/02_after_screening_v1.csv` — 206 records + cột `v1_decision`, `v1_reason`
- `SLR/03_final_included.csv` — 206 records + cột `v2_decision`, `v2_reason`
- `SLR/search-log.md` — Nhật ký tìm kiếm
- `SLR/prisma-flow.md` — Sơ đồ PRISMA

**Cách chạy:**
```bash
python tools/process_slr.py
```

---

### `verify_slr.py` — Script kiểm tra nhất quán
**Chức năng:** Verify tính nhất quán giữa các file CSV và PRISMA:
- Kiểm tra tất cả file tồn tại
- Đếm số dòng trong mỗi CSV phải bằng nhau (206)
- Kiểm tra `V1 EXCLUDE + V1 INCLUDE + V1 Unsure = tổng sau dedup`
- Kiểm tra `V2 Include + V2 Exclude = V1 pass`
- Kiểm tra số paper trong evidence table = final included

**Cách chạy:**
```bash
python -X utf8 tools/verify_slr.py
```

---

### `extract_new.py` — Trích xuất abstract papers mới
**Chức năng:** Trích xuất abstract/metadata từ CSV gốc cho các papers mới được thêm vào evidence table (12 papers bổ sung, từ 16 → 28).

---

### `list_included.py` — Liệt kê papers final included
**Chức năng:** In danh sách 28 papers final included từ `03_final_included.csv` với ID, title, year, DOI, search strings.
