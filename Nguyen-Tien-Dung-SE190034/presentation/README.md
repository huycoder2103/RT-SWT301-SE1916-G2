# Bài thuyết trình — LLM cho Sinh Test REST API (SLR & Thí nghiệm)

**SWT301 · Topic SE1916 · Nhóm 2 · Nguyễn Tiến Dũng — SE190034**

Bộ tài liệu thuyết trình cho phần SLR + thiết kế thí nghiệm, dựng từ chính các artifact trong `../SLR/` và `../experiment/`, với **mọi con số trích dẫn tới trang trong PDF gốc**.

## ⭐ Bản chính: React app interactive (`app/`)

Phiên bản tương tác — **bấm trích dẫn → mở đúng trang PDF + tô vàng đúng câu**, có chỉ mục bấm-ra-file và command palette.

```bash
cd app && npm install && npm run dev     # → http://localhost:5174
# hoặc:  npm run build && npm run preview  (production, offline)
```

Chi tiết: [`app/README.md`](app/README.md). Bản `slides/index.html` bên dưới là **deck vanilla gốc** (giữ làm backup, chạy không cần cài đặt).

## Nội dung thư mục

| Đường dẫn | Mô tả |
|---|---|
| `slides/index.html` | **Bộ slide web** (59 slide). Mở bằng trình duyệt — chạy **offline hoàn toàn**, không cần internet. |
| `slides/css/deck.css` | Design system ("CS Research Lab": teal/amber/đỏ, Space Grotesk + Inter + JetBrains Mono). Light + dark. |
| `slides/js/deck.js` | Engine: điều hướng phím, fragment reveal, speaker notes, lưới tổng quan, deep-link, in PDF. |
| `slides/fonts/*.woff2` | 7 font nhúng local (offline). |
| `THUYET-TRINH.md` | **Kịch bản nói** cho từng slide (tiếng Việt) + bảng tra cứu 13 paper. |
| `papers/*.pdf` | **13 PDF gốc** đã tải từ arXiv để hội đồng kiểm chứng. |
| `paper_text/*.txt` | Text trích từ PDF, đánh số trang (`===== PAGE N =====`) — dùng để verify trích dẫn. |
| `citations-raw.json` | **104 trích dẫn** đã verify (claim · trang · câu verbatim · lý do · trạng thái verify). |
| `fetch_papers.sh` | Script tải PDF + trích text (tái lập được). |

## Cách trình chiếu

1. Mở `slides/index.html` bằng Chrome/Edge/Firefox.
2. Phím tắt:
   - `→` / `Space` — sang bước / slide kế · `←` — lùi
   - `↑` / `↓` — nhảy slide (bỏ qua bước reveal)
   - `số` + `Enter` — tới slide số… · `Home`/`End` — đầu/cuối
   - `S` — speaker notes · `O` — lưới tổng quan · `T` — sáng/tối · `F` — toàn màn hình · `?` — trợ giúp
3. Xuất PDF: `Ctrl+P` → *Save as PDF* (mỗi slide một trang).

## Cấu trúc bài (59 slide)

1. Mở đầu (1–2) → 2. Bối cảnh (3–8) → 3. Phương pháp SLR (9–16) →
4. 13 bằng chứng (17–33) → 5. GAP (34–39) → 6. RQ (40–43) →
7. Giả thuyết & Thí nghiệm (44–48) → Kết luận + Q&A (49–52) → Phụ lục (53–59).

## Kiểm chứng trích dẫn

- **104 trích dẫn · 102/104 khớp verbatim tuyệt đối** với PDF tải về (kiểm bằng grep theo trang).
- 2 chỗ lệch trang nhỏ + 1 claim không-tường-minh đã **chủ động khai báo** ở slide 51 (Tính chính trực).
- Một đóng góp riêng của bộ slide: **gỡ được dấu † trong evidence-table** — 3 con số của RestTSLLM (#5) mà SLR đánh dấu chưa verify được, nay tìm thấy nguyên vẹn ở **Table 3, trang 9** của `papers/05_RestTSLLM_2509.05540.pdf`.

## Nguồn dữ liệu gốc (trong repo)

`../SLR/`: search-log · ie_criteria · prisma-flow · quality-assessment · evidence-table · gap-statement + 3 CSV (01/02/03).
`../experiment/`: 01_rq (PICO + RQ) · hypotheses (H0/H1 + kiểm định).
