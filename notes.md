# RBL-4 — Technical Log & Meeting Notes

**Maintained by:** Nguyễn Hoàng Huy (PL) — SE190240
**Updated:** continuously during W7 (pilot) and W8 (full run)

---

## A. Random seeds & reproducibility

| Phase | Component | Seed | File |
|---|---|---|---|
| Pilot | pilot_sample.csv random selection | _(điền sau)_ | `data/pilot_sample.csv` |
| Pilot | LLM (Claude Sonnet 4.6) | fixed seed | proposal §5.3 |
| Full | full_ground_truth | _(điền sau)_ | `data/full_ground_truth.csv` |
| Both | EvoMaster | `--seed 42` (default) × 3 repeats | EvoMaster CLI |

EMB upstream commit hash: _(điền sau khi clone)_

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

---
