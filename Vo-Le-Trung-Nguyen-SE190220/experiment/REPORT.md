# RBL-4 Experiment Report — LLM-based REST-API Test Generation vs Manual & EvoMaster on Pre-seeded-Fault Benchmarks

**Course:** SWT301 — Research-Based Learning · **Group:** SE1916-G2 (Summer 2026)
**Author (RW — Report Writer):** Vo Le Trung Nguyen — SE190220
**Instructor:** L.T.Q. Chi
**Deliverable:** RBL-4 (Experiment, Weeks 7–8) · **Run reported:** Week-7 pilot (full 133-mutant catalog)
**Primary sources for every figure in this report:** `results/rq-results.json`, `results/stats/summary.json`, `results/stats/master_summary.csv`, `results/stats/rq2_recall_per_sut.csv` (all committed under `Nguyen-Tien-Dung-SE190034/experiment/`).

> **Traceability note (RW).** Every number in this report is copied from a committed raw/stats file — none is hand-computed or estimated. Where a value is derived (e.g. a mutant kill count from a recall fraction), the derivation is shown inline so a grader can reproduce it.

---

## 1. Executive summary

We compare three REST-API test-generation "arms" — **Claude Sonnet 4.6 (LLM)**, **Manual (Equivalence Partitioning + Boundary Value Analysis)**, and **EvoMaster 6.0.0** — on **3 EvoMaster-Benchmark (EMB) REST services** totalling **35 operations**, using **133 systematically pre-seeded mutation faults** as ground truth. Three research questions are answered under a pre-registered protocol (α = 0.05):

| RQ | What it measures | Headline result | Statistical verdict |
|----|------------------|-----------------|---------------------|
| **RQ1** | LLM endpoint coverage vs the ≥90% target | LLM reaches **100%** (35/35 operations) | **Reject H0** (Wilcoxon W=630, p ≈ 1.6×10⁻⁹) |
| **RQ2** | Fault-detection Recall: LLM vs Manual vs EvoMaster | LLM = Manual = **0.0677**; EvoMaster = **0.1353** | **Fail to reject H0** (McNemar LLM vs EvoMaster p ≈ 0.064) |
| **RQ3** | Edge-case scenarios per endpoint: LLM vs Manual | LLM **217** vs Manual **141** (median 5 vs 4) | **Reject H0** (Wilcoxon W=493, p ≈ 6.2×10⁻⁷) |

**Overall verdict.** The LLM saturates endpoint coverage and generates significantly more edge-case scenarios than manual design, but it does **not** out-detect the baselines on ground-truth faults — it ties the manual suite exactly and is beaten by EvoMaster. This is reported honestly as a negative RQ2 result and is explained mechanistically in §7 (a lenient, existence-based oracle shared by both the LLM and Manual arms).

---

## 2. Research profile

**Problem.** A 13-paper systematic literature review (`SLR/`, N=13) found that 2019–2026 work applies LLMs to REST-API test generation and reports endpoint coverage and raw 500-error *counts*, but leaves three gaps:

- **GAP-1** — no study compares **LLM vs Manual vs EvoMaster** on the *same* APIs.
- **GAP-2** — no study uses a **shared pre-seeded-fault** dataset, so fault-detection **Recall** is never computed.
- **GAP-3 (our focus, GAP-M "Metric")** — no study reports a **per-endpoint edge-case / error-code metric**, nor an endpoint-type miss analysis.

**Goal.** On locally deployed EMB APIs instrumented with pre-seeded faults of known ground truth, measure the three arms' effectiveness on one common footing, answering RQ1–RQ3.

---

## 3. Research track (traceability chain)

`SLR/evidence-table.md` (N=13) → `SLR/gap-statement.md` (GAP-1/2/3) → `experiment/01_rq.md` (RQ1–RQ3, PICO) → `experiment/hypotheses.md` (H0/H1, tests, α=0.05) → `experiment/protocol.md` (pre-registered method) → **this experiment**.

Every design choice is traceable to that chain: 3 EMB SUTs (most-used benchmark in #6, #7, #11, #13); the LLM arm implemented with **Claude Sonnet 4.6** (the SLR's finding #5 identifies the Claude Sonnet line as the strongest available LLM, substituting the GPT family named in the earlier RQ draft); EvoMaster as the most-reused automated baseline (#10); pre-seeded faults to make Recall computable (closes GAP-2).

---

## 4. Method (condensed from `protocol.md`)

**Systems under test (EMB, JDK 8).**

| SUT | Operations | Domain focus | Pre-seeded mutants (ground truth) |
|-----|-----------:|--------------|----------------------------------:|
| `rest-ncs` | 6 | numeric / boundary | 70 |
| `rest-scs` | 11 | string / boundary | 59 |
| `features-service` | 18 | CRUD + constraints | 4 |
| **Total** | **35** | — | **133** |

**Arms (uniform black-box REST-assured harness).**
- **I = LLM** — Claude Sonnet 4.6, blind, frozen prompt, generated from the OpenAPI spec only.
- **C1 = Manual** — blind EP/BVA test design.
- **C2 = EvoMaster 6.0.0** — black-box search-based generation.

All suites were produced **before** faults were seeded (blind protocol).

**Faults (ground truth).** Standard mutation operators (relational / arithmetic / negate-boundary — the PIT/Offutt families) were seeded systematically into the controller layer; each mutant was recompiled into a standalone SUT; only compilable mutants were kept. Catalog = `faults/<sut>/catalog.json`.

**Kill rule.** An arm *kills* a mutant iff a test that **passes on the original** SUT **fails on the mutant**. **Recall = killed / total mutants.**

**Metrics.** RQ1 = endpoint coverage (% of operations exercised) vs a 90% target, plus endpoint-type miss analysis. RQ2 = mutation-kill Recall per arm. RQ3 = edge-case scenario count (negative + boundary + error-code) per endpoint.

**Statistics (α = 0.05, pre-registered in `hypotheses.md`).** RQ1: one-sample Wilcoxon signed-rank vs 0.90. RQ2: Friedman omnibus + post-hoc pairwise Wilcoxon (Holm-corrected) + pooled per-mutant McNemar + Cliff's δ. RQ3: paired Wilcoxon signed-rank (LLM vs Manual per endpoint) + rank-biserial. A stricter Bonferroni threshold across the 3 RQ families (α_adj ≈ 0.0167) is additionally reported for transparency.

---

## 5. Results

### 5.1 Suite sizes (tests generated and executed on the real SUTs)

| SUT | LLM | Manual | EvoMaster |
|-----|----:|-------:|----------:|
| `rest-ncs` | 86 | 60 | 30 |
| `rest-scs` | 109 | 82 | 27 |
| `features-service` | 100 | 55 | 30 |
| **Total** | **295** | **197** | **87** |

*Source: `results/stats/master_summary.csv`.*

### 5.2 RQ1 — Endpoint coverage of the LLM suite (vs ≥90% target)

The LLM suite exercises **35/35 operations = 100%** endpoint coverage (ncs 6/6, scs 11/11, features 18/18). One-sample Wilcoxon of per-operation coverage against 0.90: **W = 630, p ≈ 1.6×10⁻⁹ < 0.05 → reject H0**; rank-biserial = 1.0. LLM endpoint coverage significantly exceeds the 90% target.

**Endpoint-type miss analysis.** With operation-level coverage saturated at 100%, *no* endpoint type (numeric-validation / string-validation / CRUD / constraint) is missed at the routing level. The gap therefore is not *which* endpoints are reached, but *what is asserted* once they are reached — which is exactly what RQ2 and RQ3 probe.

*Figure: `results/figures/rq1_coverage.png`.*

### 5.3 RQ2 — Fault-detection Recall: LLM vs Manual vs EvoMaster

Pre-seeded mutants (ground truth): ncs = 70, scs = 59, features = 4 (total 133).

| SUT | LLM Recall | Manual Recall | EvoMaster Recall | (killed / mutants) |
|-----|-----------:|--------------:|-----------------:|--------------------|
| `rest-ncs` | 0.0143 | 0.0143 | 0.1714 | LLM 1/70 · Man 1/70 · Evo 12/70 |
| `rest-scs` | 0.1186 | 0.1186 | 0.0847 | LLM 7/59 · Man 7/59 · Evo 5/59 |
| `features-service` | 0.2500 | 0.2500 | 0.2500 | LLM 1/4 · Man 1/4 · Evo 1/4 |
| **Overall** | **0.0677** | **0.0677** | **0.1353** | LLM 9/133 · Man 9/133 · Evo 18/133 |

*Source: `results/stats/rq2_recall_per_sut.csv` + `results/stats/summary.json`.*

**Tests.**
- **Friedman** (3 arms × 3 SUTs): χ² = 0.0, p = 1.0 — no omnibus difference (driven by the exact LLM = Manual tie on every SUT).
- **Post-hoc pairwise Wilcoxon (Holm-corrected):** LLM vs Manual p = 1.0; LLM vs EvoMaster p = 1.0 (per-SUT recall vectors; the LLM/Manual vectors are identical by construction).
- **Pooled per-mutant McNemar:** LLM vs Manual — discordant pairs b = 0, c = 0, p = 1.0 (the two suites kill exactly the same mutants). LLM vs EvoMaster — b = 5 (LLM-only kills), c = 14 (EvoMaster-only kills), statistic = 5.0, **p ≈ 0.064 > 0.05 → fail to reject H0**; approximate achieved power ≈ 0.46.
- **Cliff's δ:** LLM vs Manual = 0.0; LLM vs EvoMaster = −0.068 (a small effect *against* the LLM).

**Verdict.** **H0 is not rejected.** The LLM does not detect more ground-truth faults than the baselines: it ties the Manual suite exactly (0.0677 = 0.0677) and is out-detected by EvoMaster (0.1353), though the LLM-vs-EvoMaster gap is not statistically significant at α = 0.05 and the study is underpowered (n = 3 SUTs). This negative result is reported as-is; §7 explains why.

*Figure: `results/figures/rq2_recall.png` and `figures/fig1_distribution.png`.*

### 5.4 RQ3 — Edge-case / error-code scenarios per endpoint: LLM vs Manual

The LLM suite produces **217** edge-case scenarios (negative + boundary + error-code) versus Manual **141** across the 35 endpoints; median **5 vs 4** per endpoint. Paired Wilcoxon (LLM − Manual per endpoint): **W = 493, p ≈ 6.2×10⁻⁷ < 0.05 → reject H0**; rank-biserial = 0.988. The LLM produced strictly more edge-case scenarios on **30/35** endpoints, fewer on **1**, and tied on **4**.

**Verdict.** **H0 is rejected.** The LLM is significantly more prolific at generating error-code / boundary scenarios than the manual EP/BVA methodology.

*Figure: `results/figures/rq3_edgecases.png` and `figures/fig2_comparison.png`.*

### 5.5 Multiplicity

Per-RQ conclusions above use the pre-registered raw α = 0.05. Under a stricter Bonferroni correction across the 3 RQ families (α_adj ≈ 0.0167), RQ1 (p ≈ 1.6×10⁻⁹) and RQ3 (p ≈ 6.2×10⁻⁷) remain significant; RQ2 remains non-significant. The conclusions are therefore robust to the multiplicity adjustment.

---

## 6. Answers to the research questions

- **RQ1 — "Do LLM tests achieve ≥90% endpoint coverage?"** → **Yes.** 100% coverage, significantly above 90% (p ≈ 1.6×10⁻⁹). No endpoint type is missed at the routing level.
- **RQ2 — "Do LLM tests detect more pre-seeded faults than Manual and EvoMaster?"** → **No.** The LLM ties Manual exactly (Recall 0.0677) and is out-detected by EvoMaster (0.1353); the difference from EvoMaster is not significant (p ≈ 0.064). H0 stands.
- **RQ3 — "Are LLM tests more prolific at edge-case / error-code scenarios than Manual?"** → **Yes.** 217 vs 141 scenarios, more on 30/35 endpoints (p ≈ 6.2×10⁻⁷).

---

## 7. Threats to validity

**Construct.** The RQ2 tie between LLM and Manual is not an accident of sampling: both arms assert **existence, not value** (e.g. `body("resultAsDouble", notNullValue())`, `hasKey(...)`), so both are structurally blind to *silent arithmetic* mutants on `rest-ncs` and `rest-scs`. This is `protocol.md`/proposal §7's pre-registered "lenient oracle" threat, **empirically confirmed** (identical kill/no-kill on all 133 mutants) — not a pipeline bug. It is reported as a finding, not corrected post-hoc (which would be HARKing). EvoMaster uses recorded-value regression oracles, a disclosed difference (`evomaster/README.md`) that partly explains its higher Recall on ncs.

**Same-author baseline.** In the Week-7 pilot the LLM and Manual arms were authored in the same agent session. The RBL-4 Week-8 design (`RBL4-FULL-RUN-DESIGN.md` §3) mitigates this by re-authoring the Manual suite with an **independent, isolated agent** (spec-only, blind to the fault catalog and the LLM output) — disclosed as *independent-agent*, not *independent-human*. Numbers in this report reflect the pilot; if the Week-8 full-run Manual numbers differ, §5.3/§5.4 must be updated accordingly before RBL-5.

**External.** Only 3 small EMB APIs (n = 3) limits Friedman power, so the pooled per-mutant McNemar is the primary RQ2 test. The `user-management` (MySQL) service was excluded, so authentication endpoints are under-represented. `features-service` carries only **4** seeded mutants versus 70 (ncs) / 59 (scs) — a real pre-existing imbalance from the Week-7 mutation run; it is reported honestly as a generalisation limit and **not** patched by adding data post-hoc.

**Internal.** Mutations were seeded in the controller layer (observable faults). LLM output is non-deterministic; the raw generated suites are frozen and committed for reproducibility.

**Conclusion validity.** Given small samples, non-parametric tests and effect sizes (Cliff's δ, rank-biserial) are reported alongside p-values, and approximate achieved power is disclosed for the RQ2 comparison.

---

## 8. Conclusion

On a shared pre-seeded-fault benchmark, an LLM (Claude Sonnet 4.6) **reaches 100% endpoint coverage** (well above the 90% target) and **generates significantly more edge-case scenarios** than manual EP/BVA design, confirming the GAP-M contribution that the SLR identified as missing. However, breadth of scenarios does **not** translate into ground-truth fault detection: on Recall the LLM **ties the manual suite exactly and is beaten by EvoMaster**, with no significant advantage over either. The limiting factor is oracle strength, not endpoint reach or scenario volume — a test suite that asserts response *existence* rather than response *value* will miss silent faults regardless of how many scenarios it enumerates. The practical implication for LLM-assisted API testing is that prompting must target **assertion strength / value-oracles**, not just scenario coverage.

---

## 9. Reproducibility & artifacts

- **Pre-registered method:** `experiment/protocol.md`, `experiment/hypotheses.md`, `experiment/01_rq.md`.
- **Ground truth:** `experiment/faults/<sut>/catalog.json`; exported CSVs under `experiment/data/`.
- **Raw results:** `experiment/results/raw/*` (kill matrices, recall JSON, scenarios, coverage).
- **Stats:** `experiment/results/stats/summary.json`, `master_summary.csv`, `rq2_recall_per_sut.csv`; one-row-per-RQ in `results/summary.csv`.
- **Figures (≥300 DPI):** `results/figures/rq{1,2,3}_*.png`, `figures/fig1_distribution.png`, `figures/fig2_comparison.png`.
- **Executed notebooks:** `results/pilot_analysis.ipynb`, `results/full_analysis.ipynb` (Restart & Run All clean).

**Open items to confirm before RBL-5 (flagged by RW):** (1) whether the final report should reflect the pilot or the Week-8 independent-Manual full run; (2) Gate E1 (instructor approval of proposal v1.2) status, still recorded as unconfirmed in `notes.md`.

---

*Prepared by Vo Le Trung Nguyen (SE190220), Report Writer, for RBL-4. All statistics traceable to committed raw files; no value in this document was hand-typed or estimated.*
