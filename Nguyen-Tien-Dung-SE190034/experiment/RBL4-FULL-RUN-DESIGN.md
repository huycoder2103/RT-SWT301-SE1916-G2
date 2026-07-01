# RBL-4 Full-Run Design — Completion & Compliance Plan

**Status:** Approved-by-default (user did not respond to clarifying questions; proceeding with recommended options per explicit "làm ngay" instruction — all defaults are reversible and logged below).
**Date:** 2026-07-01
**Author:** Claude (agent-assisted), for Nguyen Tien Dung (SE190034)
**Contract documents (frozen, do not edit their substance):**
- `team-synthesis/proposal.md` (v1.2, RQ1+RQ2+RQ3, GAP-C+D+M) — the experimental "hợp đồng"
- RBL-4 assignment brief (`screencapture-...-2026-07-01...pdf`, © L.T.Q.Chi, SWT301 FPT) — the process/file-structure mandate

---

## 1. Problem statement

`Nguyen-Tien-Dung-SE190034/experiment/` already contains a **real, executed, sophisticated pilot** (harness, 3 arms — LLM/Manual/EvoMaster —, 133 seeded mutants with ground-truth catalogs, stats scripts, 3 figures, `REPORT.md`). It does **not**, however, match the literal folder/file tree the RBL-4 brief mandates (`data/`, `results/*.ipynb`, `results/summary.csv`, `figures/fig1_distribution.png`/`fig2_comparison.png`, `notes.md`, `scripts/test_api.py`/`run_experiment.py`/`compute_metric.py`), and it has not yet executed the proposal's own §7-mandated bias fix for the "Full" (Week-8) run: an **independent** re-authoring of the Manual baseline (the pilot's Manual suite was authored by the same agent/session as the LLM suite — a disclosed limitation).

Goal: make the folder **literally compliant** with the RBL-4 tree, **without** breaking anything `proposal.md` cites by path, and **actually execute** the Week-8 upgrade (independent Manual re-authoring + full re-analysis), producing real (not fabricated) numbers.

## 2. Chosen approach: Additive Compliance Layer

Three options considered:

| # | Approach | Verdict |
|---|----------|---------|
| **1. Additive Compliance Layer** | Keep every path `proposal.md` §5 cites (`experiment/llm/prompt_template.md`, `experiment/faults/<sut>/catalog.json`, `experiment/scripts/error_surface.py`, …) exactly where it is. **Add** the RBL-4-mandated top-level `data/`, `results/*.ipynb`+`summary.csv`, `figures/fig1_*`+`fig2_*`, `notes.md`, and 3 new `scripts/*.py` gate files as thin, well-documented layers that call into / re-export the real underlying computation. | ✅ **Chosen** — zero risk to the frozen contract's citations, zero git-history disruption, every number stays traceable to one real source. |
| 2. Full rename/migration | Physically rename existing folders/scripts to match RBL-4 names 1:1, rewriting every internal reference (pom.xml resources, script paths, proposal.md prose). | ❌ Rejected — `proposal.md` is a submitted, GV-facing frozen document; editing what it cites after submission looks like tampering, and one missed path reference breaks the Maven build or the reproducibility chain. |
| 3. Parallel clean-room rebuild | Start a brand-new `RBL-4/` folder from scratch, regenerate everything in template shape. | ❌ Rejected — discards a large amount of legitimate, already-validated work and risks a second, inconsistent "truth." |

## 3. Default decisions taken (user did not respond — reversible, logged in `notes.md`)

| # | Question | Default taken | Why |
|---|----------|---------------|-----|
| 1 | Independent Manual baseline for the Full run | **Regenerate Manual suite via a fresh, isolated Claude subagent** (separate `Agent` call, zero shared context, spec-only input, blind to LLM output / fault catalog / pilot numbers). Disclosed as **"independent-agent," not "independent-human."** | Free, executable now, meaningfully reduces (does not fully eliminate) the disclosed same-agent bias. Honesty preserved via explicit disclosure — matches the assignment's own anti-fabrication ethos. |
| 2 | "Research thêm dataset uy tín" | **Keep the frozen 3 EMB SUTs (35 ops).** No new SUT added to RQ1/2/3. "Research" is spent on writing an academically rigorous `data/raw/README.md` (verified provenance, license, citation, date). | `proposal.md` §5.2 fixes the dataset as part of the approved contract; changing N post-hoc is the fastest way to make results *disputable* (HARKing-adjacent), the opposite of "không ai cãi được." |
| 3 | Gate E1 (GV approval) status | Treated as **unconfirmed** — `proposal.md` header still literally reads "Awaiting instructor (GV) approval" (rev. 2026-06-19), no newer evidence found. | Epistemic honesty: I have no record of approval, so I don't assert one. Logged prominently in `notes.md` for Dung to confirm with GV; does not block the technical work. |

**LLM arm is *not* regenerated.** `env/tools.md` already documents it was generated via an isolated, clean-context sub-agent (spec-only) — it already satisfies "a separate Claude Sonnet 4.6 session," so re-doing it would only add churn/risk without fixing anything. EvoMaster is an automated tool baseline — no authorship-bias question applies to it, so its existing run is reused as-is.

## 4. File-by-file compliance map

| RBL-4 required path | How it's satisfied |
|---|---|
| `data/raw/README.md` | **New.** Verified via WebSearch: EMResearch/EMB source URL, LGPL-3.0 license, `jdk_8_maven` module structure, operation counts cross-checked against `EMB/statistics/table_emb.md`, download date from git log (2026-06-13). |
| `data/pilot_sample.csv`, `data/pilot_ground_truth.csv` | **New, derived.** Export of the Week-7 pilot scope (35 ops / 133 mutants) from the existing `faults/<sut>/catalog.json` — this project's "ground truth" is code-derived (mutation catalog + static error-surface), not human-annotated, so no IAA/Cohen's Kappa applies (matches `proposal.md` §8.2: "no human annotation needed"); this rationale is written explicitly into `notes.md` to satisfy gate E5's *intent*. |
| `data/full_ground_truth.csv` | **New, derived.** Same catalog, full 133-mutant scope (this *is* the full compilable catalog — nothing sampled). |
| `scripts/test_api.py` | **New.** Adapted meaning: this project's "LLM API" is Claude invoked as an isolated Claude Code sub-agent, not a scriptable HTTP client (disclosed in `env/tools.md`) — so `test_api.py` smoke-tests the actual **SUT REST APIs** (the systems under test) for liveness/one-sample-request, which is E3's real practical purpose (confirm the environment works before a big batch run). Deviation explained in `notes.md`. |
| `scripts/run_experiment.py` | **New, thin driver** — orchestrates the existing `run_mutation.py` + `parse_scenarios.py` + `error_profile.py` for a given arm/SUT, writing `results/{pilot,full}_llm_output.csv` + `*_api_log.txt`. |
| `scripts/compute_metric.py` | **New, thin wrapper** around `scripts/analyze.py` + `scripts/error_surface.py`; runnable standalone on synthetic fixtures (gate E4: "chạy trên data giả, không lỗi"). |
| `results/pilot_llm_output.csv`, `results/pilot_api_log.txt`, `results/pilot_analysis.ipynb` | **New.** Recap of the already-completed, already-committed Week-7 pilot (100% coverage, 217 vs 141 edge-cases, recall figures) — repackaged as a real, executed notebook, not re-run (pilot is historical). |
| `results/full_llm_output.csv`, `results/full_api_log.txt` | **New.** From the Week-8 run: existing LLM output (reused) + newly-generated, newly-executed Manual output. |
| `results/full_analysis.ipynb` | **New.** Executed end-to-end (via `nbclient`, not hand-typed outputs) — final RQ1/RQ2/RQ3 conclusions, effect sizes, power. Verified to survive Restart & Run All. |
| `results/summary.csv` | **New.** Exactly one row per RQ: metric, p-value, effect size, N — derived from `results/stats/summary.json` (existing) + the recomputed RQ2/RQ3 Manual numbers. |
| `figures/fig1_distribution.png` | **New** (regenerated at ≥300 DPI, title/axis/N annotations) — boxplot/violin of RQ2 fault-detection Recall across the 3 arms (the primary GAP-C+D contribution). |
| `figures/fig2_comparison.png` | **New** (≥300 DPI) — RQ3 LLM-vs-Manual edge-case comparison plot. Existing `rq1_coverage.png`/`rq2_recall.png`/`rq3_edgecases.png` are kept as-is (additive, not replaced). |
| `notes.md` | **New.** Running log: E1–E7 gate status, all decisions in §3, the disclosed limitations in §6, error log. |

Everything under `specs/`, `harness/`, `llm/`, `manual/` (existing pilot copy), `evomaster/`, `faults/`, and the existing `scripts/*.py` **stays exactly where `proposal.md` cites it.**

## 5. New execution work (the actual "Tuần 8" delta)

1. Generate fresh, isolated Manual EP/BVA test suites for the 3 SUTs (3 separate blind `Agent` calls, spec-only, no fault/LLM visibility) → new `.java` classes.
2. Compile into the Maven harness; run the new Manual suite against each SUT's original jar + all its mutants (71/60/5 runs) — reusing `run_mutation.py`.
3. Re-parse scenarios/traffic for the new Manual suite (`parse_scenarios.py`, `error_profile.py`) → updated edge-case counts + kill matrix.
4. Recompute RQ2 (Friedman + Holm-Wilcoxon + pooled McNemar + Cliff's δ) and RQ3 (paired Wilcoxon + rank-biserial) with the new Manual numbers; RQ1 is LLM-only and is unaffected (kept as pilot: 100%, p≈1.6e-9).
5. Verify `analyze.py` covers Holm/Bonferroni correction + `statsmodels` power analysis per proposal §5.6; extend if missing.
6. Build both notebooks for real (`nbclient`-executed), both figures at 300 DPI, `summary.csv`, `notes.md`, `data/raw/README.md`.
7. Commit incrementally with meaningful messages (per the RBL-4 commit-message rubric), matching "mỗi batch chạy xong → commit ngay."

## 6. Disclosed limitations (go into `notes.md` verbatim)

- Manual baseline for the Full run is **independent-agent**, not independent-human (no human cohort available in this session).
- `features-service` has only 4 seeded mutants vs. 70 (ncs) / 59 (scs) — a real, pre-existing imbalance from the Week-7 mutation run. **Not** fixed by adding data post-hoc (would be HARKing-adjacent); reported honestly as a generalization limit, consistent with `proposal.md` §7.
- Gate E1 (GV approval) status is unconfirmed as of the last written record.
- `test_api.py` tests SUT liveness, not an LLM HTTP endpoint, because the approved LLM invocation method is a Claude Code sub-agent, not a scriptable API client.

## 7. Verification before "done"

- `full_analysis.ipynb`: Restart & Run All, zero errors.
- `scripts/test_api.py`, `scripts/compute_metric.py`: run standalone, exit 0.
- `git status`: no `.env`/`api_key.txt`/`__pycache__` untracked (gate E7 checklist).
- Every number in `results/summary.csv` traceable to a raw file (no hand-typed statistics).
