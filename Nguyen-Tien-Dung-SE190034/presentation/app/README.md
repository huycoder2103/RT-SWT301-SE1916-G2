# SLR Deck — React app (interactive)

Bài thuyết trình **React + Vite** cho topic SE1916 *"LLM cho Sinh Test REST API"* (SWT301). Phiên bản interactive: chỉ mục bấm-ra-file, và **bấm trích dẫn → mở đúng trang PDF + tô vàng đúng câu**.

## Chạy

```bash
cd presentation/app
npm install          # cài deps (chỉ lần đầu)
npm run dev          # dev server → http://localhost:5174
# hoặc bản production:
npm run build        # build vào dist/
npm run preview      # phục vụ dist/ → http://localhost:4173
```

> `predev`/`prebuild` tự chạy `scripts/build-data.mjs` để sinh lại `src/data/{slides,citations,files}.json` từ deck gốc + `citations-raw.json`.

## Tính năng

| Tính năng | Mô tả |
|---|---|
| **59 slide** | Port 100% từ deck vanilla, giữ nguyên design "CS Research Lab" (light + dark). |
| **Chỉ mục (sidebar)** | Slides · 13 Papers · SLR docs · Experiment · **Citation index (104)** — bấm mở file/PDF/trích dẫn. Có ô tìm kiếm. |
| **Citation → PDF + tô vàng** | Bấm bất kỳ chip trích dẫn (21) hoặc khối evidence (16) trong slide, hoặc 104 mục trong Citation index → mở `react-pdf` đúng trang + `<mark>` vàng đúng câu quote, tự cuộn tới. |
| **Markdown viewer** | Bấm SLR/Experiment doc → render `.md` (react-markdown + GFM). |
| **Command palette** | `Ctrl/Cmd+K` — nhảy slide · mở paper · mở trích dẫn. |
| **Split view** | Slide + nguồn (PDF/doc) hiện song song để đối chiếu. |
| **Overview grid** | `O` — lưới toàn bộ slide. |

## Phím tắt

`→`/`Space` bước · `←` lùi · `↑`/`↓` nhảy slide · `B` chỉ mục · `S` notes · `O` lưới · `T` sáng/tối · `F` toàn màn hình · `Ctrl/Cmd+K` tìm nhanh · `Esc` đóng.

## Kiến trúc

```
app/
  scripts/build-data.mjs   # parse deck HTML + citations-raw.json → JSON data
  public/papers/*.pdf       # 13 PDF (phục vụ react-pdf)
  public/docs/*.md          # SLR + experiment docs (phục vụ md viewer)
  src/
    data/{slides,citations,files}.json   # generated
    data/index.js                        # data + helpers (arxiv→pdf, groupings)
    components/{Slide,Sidebar,Viewer,Overview,CommandPalette}.jsx
    styles/{deck,app}.css                # design tokens + slide + shell
    App.jsx, main.jsx
```

Stack: React 18 · Vite 6 · react-pdf 9 (pdfjs 4) · react-markdown 9 + remark-gfm. Build offline-friendly (font + pdf.worker bundle vào `dist/`).
