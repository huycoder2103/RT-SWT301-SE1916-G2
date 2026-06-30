# LLM-based REST API Test Generation vs Manual & EvoMaster on Pre-seeded-Fault Benchmarks

**Topic:** RT-SWT301-SE1916-G2
**Môn:** SWT301 — Research-Based Learning
**Nhóm:** SE1916-G2 — Summer 2026
**Thành viên:**
- Nguyễn Hoàng Huy (SE190240) — **PL** (Project Lead)
- Nguyen Thanh Dat (SE190239) — **DG** (Data & Ground Truth)
- Nguyen Tien Dung (SE190034) — **LR** (LLM Runner)
- Nguyen Le Thuan (SE190305) — **MS** (Metrics & Stats)
- Vo Le Trung Nguyen (SE190220) — **RW** (Report Writer)

**GV hướng dẫn:** L.T.Q.Chi

> Compare three test-generation arms — **Claude Sonnet 4.6 (LLM)** vs **Manual (EP/BVA)** vs **EvoMaster 6.0.0** — on 3 EMB REST APIs (35 operations) with **pre-seeded mutation faults** as ground truth. Three RQs: endpoint coverage (RQ1), fault-detection Recall (RQ2), per-endpoint edge-case scenarios (RQ3).

## Tiến độ

- [x] RBL-1: Tìm paper (Tuần 3-4)
- [x] RBL-2: Phân tích GAP (Tuần 5)
- [x] RBL-3: Proposal (Tuần 5-6) — ✅ GV duyệt v1.2
- [ ] RBL-4: Thực nghiệm (Tuần 7-8) — Pilot done, Full run in progress
- [ ] RBL-5: Báo cáo & Trình bày (Tuần 9-10)

## Cấu trúc thư mục (RBL-0 standard)

```
RT-SWT301-SE1916-G2/
├── [member-name]/SLR/       SLR per-member (RBL-1, RBL-2)
├── team-synthesis/          Proposal, gap statement, RQ, plan-rbl4
├── data/                    Pilot/full ground truth + raw EMB dataset
├── scripts/                 test_api.py, run_experiment.py, compute_metric.py
├── results/                 LLM output, api log, analysis notebooks, summary.csv
├── figures/                 fig1_distribution.png, fig2_comparison.png (≥300 DPI)
├── paper/                   LaTeX paper (RBL-5)
├── presentation/            Slides (RBL-3, RBL-5)
└── notes.md                 Technical decisions + meeting log
```
