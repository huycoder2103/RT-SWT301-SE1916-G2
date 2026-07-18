# RUNBOOK — RBL-4 Task 8 + RBL-5 build

Hai thứ trong repo này cần chạy trên máy khác nhau:

| Việc | Chạy được ở đâu | Cần gì |
|---|---|---|
| **A. Phân tích + paper** (RBL-5) | **Máy nào cũng được** | Python + (LaTeX nếu muốn ra PDF) |
| **B. Task 8** — đo lại kill matrix (RBL-4) | **Chỉ máy thí nghiệm** | JDK 8 + JDK 17 + Maven + **mutant jars** |

Lý do tách: mutant jars (133 file) và EMB clone **bị gitignore**, không theo repo. Chúng chỉ nằm trên máy đã chạy `mutate.py` (theo `env/tools.md` là máy có profile `C:\Users\dungm`).

---

## A. Chạy phân tích + build paper (máy nào cũng được)

### A1. Cài Python deps (một lần)

```bash
py -m pip install pandas scipy statsmodels seaborn matplotlib nbformat nbclient ipykernel
```

### A2. Tái lập toàn bộ số liệu từ raw data

```bash
cd D:/FPT/SWT301/RT-SWT301-SE1916-G2

py scripts/analyze.py            # results/raw/*.csv  -> results/stats/summary.json
py scripts/write_summary_csv.py  # summary.json       -> results/summary.csv  (1 dòng/RQ)
py scripts/gen_paper_macros.py   # summary.json       -> paper/generated/numbers.tex
```

Kiểm chứng chuỗi số liệu không bị gõ tay:

```bash
py scripts/check_paper.py        # PASS = không macro undefined, không số hardcode trong Results
```

### A3. Các gate của RBL-4

```bash
py scripts/test_api.py                                        # E3 — luôn exit 0 (diagnostic)
py scripts/compute_metric.py --raw-dir scripts/fixtures --out /tmp/e4   # E4 — chạy trên data giả
```

### A4. Build PDF paper

Máy hiện tại **chưa có LaTeX**. Chọn 1 trong 3:

```bash
# (1) MiKTeX (Windows, khuyến nghị)
winget install MiKTeX.MiKTeX
cd paper && latexmk -pdf main.tex

# (2) Tectonic — 1 binary, tự tải package
winget install TectonicTypesetting.Tectonic
cd paper && tectonic main.tex

# (3) Không cài gì: up thư mục paper/ lên overleaf.com, compile online
```

Thứ tự thủ công nếu không dùng latexmk (cần 4 lượt cho cross-ref + bib):

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

---

## B. Task 8 — đo lại kill matrix với Manual suite mới

### B0. Tại sao phải chạy

> **✅ ĐÃ CHẠY 2026-07-17.** Task 8 đã thực thi trên máy này với toolchain đúng bản pin
> (JDK 1.8.0_492, JDK 17.0.19, Maven 3.9.16) + EMB re-clone (commit `915859…`). Mutant ground
> truth 133 tái tạo chính xác qua `scripts/build_catalog_mutants.py`; kill matrix chạy với
> Manual suite mới. `results/` giờ đã đồng bộ. Phần dưới giữ lại làm hướng dẫn tái lập.
> Kết quả + các phát hiện (ncs catalog truncation, m001 boundary) ở [notes.md](notes.md) §F.
> Để tái lập nhanh mutant đúng catalog: `build_catalog_mutants.py` (KHÔNG dùng `mutate.py`
> re-discover — xem notes §F7).

Trước Task 8, repo **lệch pha**:

- `harness/src/test/java/manual/*ManualTests.java` = Manual suite **mới** (regenerate ở Task 7)
- `results/raw/*_kills.csv` = số đo từ Manual suite **cũ** (bản pilot, giờ archive ở `manual/pilot-archive/*.java.pilot`)

Bằng chứng: `manual` `n_oracle` hiện là 56 (ncs) / 78 (scs) — trùng đúng giá trị pilot. Ai clone repo chạy lại sẽ ra số khác `summary.csv`.

Hệ quả lên kết quả: RQ2 leg **LLM-vs-Manual đang degenerate** — hai arm kill y hệt nhau (McNemar b=0, c=0). Paper hiện đã disclose và **không kết luận** từ leg này (xem `paper/sections/06_threats.tex`). Chạy Task 8 xong thì leg đó mới có ý nghĩa.

### B1. Chuẩn bị

Cần trên máy chạy:

- **JDK 8** — chạy SUT jars (Temurin 1.8.0_492 theo `env/tools.md`)
- **JDK 17** — harness + EvoMaster (Temurin 17.0.19)
- **Maven** 3.9.16 trên PATH
- **Mutant jars**: mỗi SUT một thư mục chứa `original.jar` + `m001.jar`…`mNNN.jar`

> **Nếu mutant jars đã mất:** phải sinh lại bằng `scripts/mutate.py` — **~416 lần build Maven** (ncs 300 + scs 94 + features 22 candidate), nhiều giờ. Kiểm tra kỹ máy cũ / ổ backup trước khi làm việc này.

### B2. Preflight (không chạy gì, chỉ kiểm tra)

```bash
py scripts/run_task8.py \
  --jdk8  "C:/Users/<you>/tools/jdk8/jdk8u492-b09" \
  --jdk17 "C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot" \
  --mutants-root "<thư mục chứa ncs/ scs/ features/>" \
  --dry-run
```

Script sẽ **từ chối chạy** nếu thiếu bất cứ thứ gì, và in ra chính xác cái nào thiếu. Nó cũng tự kiểm tra Manual suite trong harness có thật sự khác bản pilot không — nếu giống hệt thì Task 7 chưa áp dụng và chạy Task 8 chỉ tái tạo lại số pilot.

### B3. Smoke test 1 SUT trước

Đừng chạy cả 3 ngay. Chạy `Ncs` trước (~70 mutants × 3 arm):

```bash
py scripts/run_task8.py --jdk8 "<...>" --jdk17 "<...>" --mutants-root "<...>" --sut Ncs
```

### B4. Chạy đủ 3 SUT

```bash
py scripts/run_task8.py --jdk8 "<...>" --jdk17 "<...>" --mutants-root "<...>"
```

Quy mô: **~402 chu kỳ** (133 mutants × 3 arm + original), mỗi chu kỳ boot 1 Spring Boot app (timeout 45s) rồi chạy surefire. Để máy chạy, đừng chiếm port 8080/8081/8083.

### B5. Gate tự động

Script tự kiểm tra sau khi chạy: `manual` `n_oracle` **phải khác** giá trị pilot. Nếu vẫn bằng → suite mới không có hiệu lực (thường do `target/` cũ), script báo fail và **không** rebuild stats. Fix:

```bash
mvn -f Nguyen-Tien-Dung-SE190034/experiment/harness/pom.xml clean test-compile
```

Gate này **tự hiệu chỉnh** — nó đọc giá trị pilot đang commit chứ không hardcode, nên chạy lại nhiều lần vẫn đúng.

### B6. Sau khi xong

Script tự chạy lại: `parse_scenarios.py` → `analyze.py` → `write_summary_csv.py` → `gen_paper_macros.py` → `results_json.py`.

**Số trong paper tự đổi theo** — không phải sửa file `.tex` nào, vì mọi số là macro bind vào `summary.json`. Kiểm tra lại:

```bash
py scripts/check_paper.py
py scripts/make_rbl4_figures.py     # figures 300 DPI
```

Rồi cập nhật `paper/sections/06_threats.tex` + `04_results.tex`: nếu Manual đã độc lập, gỡ phần disclose "same-agent" và mục `sec:results-degenerate`.

### B7. Rollback nếu chạy hỏng

```bash
git checkout results/raw results/stats results/summary.csv
```

---

## C. Thứ tự khuyến nghị

1. `A2` + `A3` — xác nhận pipeline chạy được (5 phút, máy nào cũng được)
2. `B2` `--dry-run` trên máy thí nghiệm — biết còn thiếu gì
3. `B3` smoke test Ncs — bắt lỗi sớm
4. `B4` chạy đủ → `B6` rebuild
5. `A4` build PDF

## D. Việc còn thiếu ngoài Task 8

**Đã resolved (2026-07-18):**
- ✅ `presentation/RBL5_final_defense.pptx` (12 slide, số đọc từ `results/`)
- ✅ `team-synthesis/rq-final.md` + hypotheses + gen_slides.js + slide/file member: model → **Claude Sonnet 4.6** (giữ literature GPT)
- ✅ `proposal.md` §8.1 role → **Thuan=MS, Nguyen=RW** (khớp thực tế)
- ✅ GV approval → Approved v1.2 (PL xác nhận); xóa 2 bản trùng (`proposal .md`, `scripts/team-synthesis/`)

**Còn lại (member deliverable gaps — không chặn):**
- `Nguyen-Thanh-Dat-SE190239` / `Vo-Le-Trung-Nguyen-SE190220`: thiếu `SLR/gap-analysis.md`, `experiment/design-rationale.md`, `hypotheses-draft.md`
- `quality-assessment.md` mới chỉ Dung có
- `team-synthesis/slides_proposal_defense.pdf`: đã xóa bản stale (GPT-4o) — re-export từ `.pptx` sạch (cần PowerPoint/LibreOffice)
- Huy's RQ cá nhân (`01_rq.md`, `hypotheses.md`): giữ nguyên nội dung Gemini-vs-GPT-4o (nghiên cứu cá nhân), thêm banner trỏ về Claude của nhóm
