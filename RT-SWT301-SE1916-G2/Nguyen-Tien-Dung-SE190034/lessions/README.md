# lessions — Khóa học "Zero → Hero" (chỉ để bạn đọc, KHÔNG push)

Khóa học **interactive** dạy người *chưa đọc paper/SLR* cũng thuyết trình lại được **toàn bộ 59 slide** của deck. Học khái niệm bằng ví dụ đời thường → quiz → diễn tập cả deck.

## Chạy

```bash
cd lessions
npm install          # lần đầu
npm run dev          # → http://localhost:5180
# hoặc bản tĩnh: npm run build && npm run preview  (→ 4180)
```

## Cấu trúc khóa học (7 chương · 28 bài)

| Chương | Nội dung | Slide deck |
|---|---|---|
| 🚀 Khởi động | Bài này nói về cái gì + mẹo present | 1–2 |
| 🧱 Nền tảng | API, status code, OpenAPI, **2 loại coverage**, vì sao LLM | 3–8 |
| 🔬 Phương pháp SLR | PICO, IC/EC, phễu PRISMA 280→13, chất lượng | 9–16 |
| 📚 13 Bằng chứng | Số liệu đắt + 1 lý do mỗi paper | 17–33 |
| 🎯 GAP | Ma trận so sánh + 3 khoảng trống | 34–39 |
| 🧪 Câu hỏi & Thí nghiệm | RQ tinh chỉnh, H0/H1, kiểm định | 40–48 |
| 🏆 Hero: Bảo vệ | Chuỗi nhân–quả, chính trực, Q&A, **Diễn tập 59 slide** | 49–59 |

## 🔒 Lộ trình "CHẮC CHẮN thuyết trình được"

Làm đúng 3 bước này là present được, không cần đọc paper:

1. **Học** 28 bài (đặc biệt các bài *trọng tâm*) → hiểu khái niệm + biết "nói gì".
2. **🎯 Bảo vệ thử** (nút trên thanh trên cùng): bài thi 17 câu (chuỗi nhân–quả + khái niệm random + 6 Q&A khó). **Đạt ≥ 85% = "SẴN SÀNG BẢO VỆ".** Chưa đạt thì nó chỉ chỗ ôn lại → thi lại tới khi đạt.
3. **🎤 Diễn tập** cả 59 slide cho đến khi đọc trôi.

**🧾 Phao thi (in được)** — nút trên thanh trên cùng → bấm **In / Lưu PDF**: 1–2 trang gồm chuỗi 5 câu, bảng số liệu đắt, 3 GAP, RQ/giả thuyết, 6 Q&A, và **cue 59 slide**. Cầm liếc khi đứng trên sân khấu — kể cả lỡ quên vẫn cứu được.

## Cách học hiệu quả

1. Bấm **"Bắt đầu từ con số 0"** trên trang chủ — đi theo thứ tự đề xuất.
2. Mỗi bài: đọc phần dạy (có ví dụ 💡 + hộp **🎤 "Lên sân khấu nói gì"**) → làm quiz → nhận XP.
3. Các bài **trọng tâm** (gắn nhãn): 2 loại coverage, ma trận GAP, 3 khoảng trống, H0/H1, chuỗi nhân–quả, Q&A.
4. Cuối cùng vào **🎤 Diễn tập**: hiện tên từng slide → bạn tự nói → bấm "Hiện lời thoại" so → tự chấm. Lặp tới khi trôi cả 59 slide.
5. **Thanh "% sẵn sàng"** trên trang chủ = mức Hero của bạn. Đạt ~100% là present được toàn bài.

## Tính năng

- **Journey map** với mastery ring + XP + tiến độ lưu tự động (localStorage).
- Quiz tương tác: trắc nghiệm (feedback + giải thích), đúng/sai, điền chỗ trống, flashcard lật, **sắp xếp thứ tự**.
- **Diễn tập** tái dùng đúng 59 speaker notes của deck.
- Sáng/tối · tiếng Việt chuẩn (font bundle subset vietnamese).

Stack: React 18 + Vite 6 (offline, không phụ thuộc mạng). Nội dung bám sát `../presentation` (deck + 104 trích dẫn đã verify).
