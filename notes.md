# RBL-4 — Technical Log & Meeting Notes

**Maintained by:** Nguyễn Hoàng Huy (PL) — SE190240
**Updated:** continuously during W7 (pilot) and W8 (full run)

---

## A. Random seeds & reproducibility

| Phase | Component | Seed | File |
|---|---|---|---|
| Pilot | `pilot_sample.csv` selection | **N/A — no random selection** | `data/pilot_sample.csv` |
| Pilot | LLM (Claude Sonnet 4.6) | temperature 0, fixed seed | proposal §5.3 |
| Full | `full_ground_truth` | **N/A — no random selection** | `data/full_ground_truth.csv` |
| Both | EvoMaster | `--seed 42` × 3 repeats | EvoMaster CLI |

**Why the two seeds are N/A, not missing.** `export_ground_truth.py` is deterministic: it
reads all three `faults/<sut>/catalog.json`, keeps every mutant with `status == "compiled"`,
and writes them all. No sub-sample is ever drawn, so there is no random state to seed. This
is also why `pilot_ground_truth.csv` and `full_ground_truth.csv` are byte-identical
(same MD5) — the Week-7 pilot ran on the **full** 133-mutant compilable catalog. That
identity is by design and is **not** a copy-paste error; anyone reviewing the repo should
read it as "pilot scope == full scope", per `RBL4-FULL-RUN-DESIGN.md` §4.

**EMB upstream commit hash:** _still unknown — must be read on the experiment machine._
The EMB clone is gitignored and is not on the current machine. Recover with:
`git -C <path-to-EMB> log -1 --format=%H`. Until then `data/raw/README.md`'s provenance
claim rests on the clone date (2026-06-13) alone.

---

## B. Model & API config (frozen, proposal §5.3)

- Model: `claude-sonnet-4-6`
- Temperature: 0
- top_p: 1
- max_tokens: 4096
- Strategy: few-shot from OpenAPI spec only (black-box, blind to source/faults)
- Prompt template: `scripts/llm/prompt_template.md` (verbatim — CẤM đổi)

---

## C. Statistical tests (frozen, proposal §5.6)

| RQ | Test | α | Effect size |
|---|---|---|---|
| RQ1 | 1-sample Wilcoxon (one-tailed) vs 0.90 | 0.05 | rank-biserial |
| RQ2 | Friedman + Holm-Wilcoxon + McNemar pooled | 0.05 | Cliff's δ |
| RQ3 | Paired Wilcoxon (one-tailed) | 0.05 | rank-biserial |

Multiplicity correction: Holm (RQ2 post-hoc) + Bonferroni cross-RQ (α_adj ≈ 0.017).

---

## D. Decisions log (chronological)

Format: `YYYY-MM-DD — [who] — decision — rationale`

- 2026-06-30 — PL (Huy) — Migrate pilot artifacts từ `Nguyen-Tien-Dung-SE190034/experiment/` sang root structure theo RBL-0 — chuẩn hóa cho RBL-4 full run
- 2026-07-01 — LR (Dung) — **Additive Compliance Layer** thay vì rename/migrate toàn bộ — giữ nguyên mọi path mà `proposal.md` §5 trích dẫn (frozen contract, sửa sau khi nộp trông như tampering); các file RBL-4 mandate được thêm vào như lớp mỏng gọi xuống computation thật. Chi tiết: `RBL4-FULL-RUN-DESIGN.md` §2.
- 2026-07-01 — LR (Dung) — Manual baseline cho full run = **regenerate bằng isolated Claude sub-agent**, KHÔNG phải human cohort — không có human cohort khả dụng. Disclose là **"independent-agent", không phải "independent-human"**. Đây là deviation so với `proposal.md` §7 (ghi "independent human cohort") và **phải nói rõ trong paper**.
- 2026-07-01 — LR (Dung) — **Không** thêm SUT/dataset mới — `proposal.md` §5.2 đã freeze dataset; đổi N sau khi thấy data là HARKing-adjacent.
- 2026-07-01 — LR (Dung) — LLM arm **không** regenerate — `env/tools.md` đã ghi nhận nó sinh từ isolated clean-context sub-agent, đã thỏa "separate session"; làm lại chỉ thêm churn.
- 2026-07-15 — PL — Paper RBL-5 viết theo cơ chế **macro injection**: mọi số là `\newcommand` sinh bởi `gen_paper_macros.py` từ `summary.json`. Không có số nào gõ tay trong `.tex`. Chạy lại experiment → số trong paper tự đổi. `check_paper.py` fail nếu ai đó hardcode số vào section kết quả.

---

## E. Disclosed limitations (verbatim từ `RBL4-FULL-RUN-DESIGN.md` §6 — phải vào paper)

1. Manual baseline của full run là **independent-agent**, không phải independent-human.
2. `features-service` chỉ có **4 mutants** vs 70 (ncs) / 59 (scs) — mất cân bằng có thật từ Week-7, **không** vá bằng cách thêm data sau (HARKing-adjacent); báo cáo trung thực như một giới hạn generalization.
3. Gate E1 (GV approval) chưa xác nhận: `proposal.md` header vẫn ghi "Awaiting instructor (GV) approval" (rev. 2026-06-19), trong khi `README.md` ghi "✅ GV duyệt v1.2". **Hai nguồn mâu thuẫn — PL cần xác nhận với GV.**
4. `test_api.py` test liveness của **SUT**, không phải LLM HTTP endpoint, vì LLM invocation là Claude Code sub-agent chứ không phải scriptable API client.

---

## F. Findings — audit ngày 2026-07-15

### F1. Repo lệch pha: harness Manual ≠ Manual đã đo (BLOCKING)

- `harness/src/test/java/manual/*ManualTests.java` = suite **mới** (Task 7 đã chạy; khác `manual/pilot-archive/*.java.pilot` ~1000+ dòng/file).
- `results/raw/*_kills.csv` = số từ suite **cũ** (pilot).
- Bằng chứng: `manual` `n_oracle` = 56 (ncs) / 78 (scs) — trùng đúng giá trị pilot mà `RBL4-IMPLEMENTATION-PLAN.md` Task 8 ghi là "phải KHÁC nếu đã chạy lại". Thêm: `results/raw/*` byte-identical với `experiment/results/raw/*`.
- Dấu hiệu khác: `results/full_llm_output.csv` = 0 byte; `results/full_api_log.txt` = `[dry-run, no timestamp]`.
- **Kết luận: Task 8 chưa chạy.** Chạy bằng `scripts/run_task8.py` (xem `RUNBOOK.md` §B). Máy chạy phải có JDK8 + JDK17 + Maven + mutant jars (jars bị gitignore, chỉ có trên máy thí nghiệm cũ — `env/tools.md` trỏ `C:\Users\dungm\...`).

### F2. Oracle weakness — RQ2 LLM-vs-Manual degenerate

LLM và Manual kill **y hệt** nhau mọi SUT (1/70, 7/59, 1/4). McNemar b=0, c=0 → p=1.0 **by construction**, không phải do đo. `analyze.py` đã tự phát hiện và ghi `pairwise_wilcoxon_identical_vectors: ["llm_vs_manual"]`.

Hai nguyên nhân, cần tách bạch:
1. **Same-agent authorship** (sửa được bằng Task 8).
2. **Cùng loại oracle** (KHÔNG sửa được bằng Task 8): cả hai đều assert status code sinh từ spec. Mutation đổi **giá trị tính toán** → status không đổi → test vẫn pass. EvoMaster dùng recorded-value regression oracle nên bắt được.

→ Dự đoán: chạy Task 8 xong, LLM-vs-Manual sẽ **bớt** giống nhau nhưng **không hết** giống. Đừng coi agreement rate còn cao là lỗi.

### F3. Recall tuyệt đối thấp ở cả 3 arm

Cao nhất là EvoMaster 18/133 (13.5%). Đây là finding về black-box REST testing, không phải lỗi setup — nhiều mutant đổi giá trị không bao giờ nổi lên response field. Paper §5.3 (Discussion) đã lập luận chỗ này.

### F4. Toolchain version drift

`env/tools.md` pin scipy 1.17.1 / numpy 2.4.5 / Python 3.14.5. Máy audit chạy scipy **1.18.0** / numpy **2.5.1** / Python **3.14.6**. Đã verify: `analyze.py` tái tạo `summary.json` **byte-identical** dù lệch version → kết quả robust với drift này.

### F5. Verification đã chạy (2026-07-15)

| Gate | Kết quả |
|---|---|
| `analyze.py` tái tạo `summary.json` từ `results/raw/` | ✅ byte-identical |
| `write_summary_csv.py` tái tạo `summary.csv` | ✅ identical |
| `compute_metric.py --raw-dir scripts/fixtures` (E4) | ✅ exit 0 |
| `test_api.py` (E3) | ✅ exit 0, báo đúng UNREACHABLE |
| `full_analysis.ipynb` Restart & Run All | ✅ zero errors |
| `check_paper.py` | ✅ PASS — 0 macro undefined, 0 số hardcode |

### F6. Mâu thuẫn tài liệu cần PL xử lý

| Chỗ | Mâu thuẫn |
|---|---|
| Role MS/RW | `proposal.md` §8.1: Trung Nguyen=MS, Thuan=RW. `README.md` + commit thực tế (`ThuanNg05: complete phases of Metrics & Stats`, `add RW report for SE190220`) + header `write_summary_csv.py`: **ngược lại**. Paper hiện theo README/thực tế. |
| LLM | `rq-final.md` §2 vẫn ghi GPT-4o/GPT-4-Turbo — stale từ trước "research pivot" (commit `33f524e`). `proposal.md` v1.2 + `env/tools.md` + README: Claude Sonnet 4.6. |
| GV approval | `proposal.md` header: "Awaiting approval". `README.md`: "✅ GV duyệt v1.2". |

---

## G. Error log

- 2026-07-15 — Task 8 không chạy được trên máy audit: thiếu JDK8, JDK17, Maven, EMB clone, và toàn bộ 133 mutant jars (0 file `.jar` trong repo — bị gitignore). `D:\SWT301_SU26_Group2` (root gốc theo `run_capture.sh`) và profile `C:\Users\dungm` đều không tồn tại trên máy này. → Không fabricate số; viết `run_task8.py` + `RUNBOOK.md` để chạy trên máy có artifact.
