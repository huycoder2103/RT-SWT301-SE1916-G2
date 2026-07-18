# Research Proposal — LLM-based REST API Test Generation vs Manual & EvoMaster on Pre-seeded-Fault Benchmarks

**Team:** SWT301_SU26_Group2 · **Topic code:** SE1916
**Members:** Nguyen Tien Dung (SE190034), Nguyen Hoang Huy (SE190240), Nguyen Thanh Dat (SE190239), Nguyen Le Thuan (SE190305), Vo Le Trung Nguyen (SE190220)
**Submitted:** 2026-06-13 · **Revised:** 2026-06-19 · **Version:** 1.2 · **Status:** Approved by instructor (GV) — v1.2

**Sources:** `team-synthesis/{gap-statement-final.md, rq-final.md, hypotheses-draft.md, evidence-table-merged.md}` (N = 59 papers) + each member's `experiment/*`. Week-7 pilot artifacts: `Nguyen-Tien-Dung-SE190034/experiment/`.

---

## 1. Introduction

### 1.1 Abstract
REST APIs are the backbone of modern software, and testing them thoroughly is expensive and largely manual. Large Language Models (LLMs) can read an OpenAPI specification and synthesise test cases automatically, promising large savings. Yet across 59 surveyed papers (2018–2026), **no study compares an LLM generator against both a human (manual) suite and a mature tool (EvoMaster) on the same APIs**, none computes **fault-detection Recall against a known, pre-seeded-fault ground truth**, and none reports a **per-endpoint edge-case/error-code metric**. We propose a controlled, reproducible comparison on three EvoMaster-Benchmark (EMB) REST APIs (**35 operations**) into which faults are **seeded by mutation** (so the total is known), measuring (i) endpoint coverage, (ii) mutation-kill Recall, and (iii) per-endpoint edge-case scenario counts, under a blind protocol. A Week-7 feasibility pilot (LLM = Claude Sonnet 4.6 as an available-model proxy) confirms the pipeline runs end-to-end: LLM endpoint coverage **100 %** (35/35, p ≈ 1.6e-9), LLM **217** vs Manual **141** edge-case scenarios (paired Wilcoxon p ≈ 6.2e-7), and mutation Recall EvoMaster **0.135** > LLM = Manual **0.068**. The LLM under test is **Claude Sonnet 4.6** (`claude-sonnet-4-6`), used for **both** the pilot and the full run.

### 1.2 Objective & Scope
**Objective:** quantify *when to trust* an LLM REST-API test generator and *where it fails*, relative to a human baseline and a state-of-the-art tool, using ground truth rather than raw error counts.
**In scope:** black-box test generation from OpenAPI specs; JVM REST APIs in EMB; coverage, fault-Recall, and edge-case metrics. **Out of scope (future work):** GraphQL/RPC, non-JVM stacks, and open-source/Gemini-class model ablations (GAP-T).

### 1.3 Contributions
1. **First three-way comparison** — LLM vs Manual vs EvoMaster on identical APIs (closes GAP-C).
2. **Ground-truth fault detection** — a shared **pre-seeded-fault** benchmark enabling true Recall, not live-API 500 counts (closes GAP-D).
3. **A per-endpoint edge-case/error-code metric** plus a **code-derived error-surface baseline** that enumerates, per endpoint, where each operation can emit a 4xx/5xx (closes GAP-M).
4. **A reproducible, open pipeline** (scripts + frozen prompt + JSON result artifacts) so every reported number can be regenerated and audited.

### 1.4 Team & Roles (summary)
Five members, one deliverable each, with the LLM-Runner (LR) and Metrics-&-Stats (MS) roles assigned to different people to avoid a single point of bias. Full assignment in §8.1.

---

## 2. Research Problem Statement

### 2.1 Context & Importance
REST APIs are the backbone of modern software, and testing them thoroughly is costly and manual. LLMs can read an OpenAPI specification and synthesise test cases automatically, promising large savings — e.g. RESTGPT reaches **97 % rule-extraction precision** [5]. For a QA team, the open question is not "can an LLM produce tests" but "are those tests **as good as** what a tester or a mature tool (EvoMaster) produces, on faults we can actually count."

### 2.2 State of the Art
LLM test generators are dominated by the GPT family: RESTGPT [5], KAT [1], APITestGenie [6], AutoRestTest [7] (**42** 500-errors vs EvoMaster 20), LlamaRestTest [3] (**204** faults vs EvoMaster 130), RESTifAI [10] (**128/134 ≈ 95.5 %** operation coverage). Classic baselines: EvoMaster [16] and Morest [17].

### 2.3 Research Gaps (from `gap-statement-final.md`)
Across **59** papers (2018–2026) three gaps persist in otherwise high-quality work:
- **GAP-C (Comparison):** exactly **one** study compares a tool vs *manual* tests — EvoMaster [16], a non-LLM tool that scored **below** manual (41 % vs 82 %). **No** paper puts **LLM vs manual vs EvoMaster** on the same APIs.
- **GAP-D (Dataset / ground truth):** fault detection is reported as raw 500-error **counts** on live APIs [3, 7, 9, 11, 16, 17]; with no shared **pre-seeded-fault** benchmark, **ground-truth Recall is never computed**.
- **GAP-M (Metric):** evaluation is coverage-biased; only KAT [1] splits 2xx/4xx and only RESTSpecIT [2] reports 5xx — **no per-endpoint edge-case/error-code metric** and **no endpoint-type miss profile**.

Primary cluster = **GAP-C + GAP-D** (best-evidenced, supported by most members); **GAP-M** is the metric facet. GAP-T (open-source / Gemini) is an optional ablation.

### 2.4 Motivation
If unresolved, teams adopt LLM test generators **on faith**: they cannot tell whether LLM tests miss the faults a human would catch, or merely inflate easy coverage. A controlled, ground-truth comparison tells practitioners *when* to trust an LLM generator and *where it fails* (which endpoint types, which fault kinds) — actionable guidance no current paper provides.

---

## 3. Related Work

### 3.1 Overview (≤ 10 representative papers from the 59-paper merge)

| # | Paper (year) | Tool / LLM | Dataset (size) | Metric | Best result |
|---|--------------|-----------|----------------|--------|-------------|
| 5 | RESTGPT (2024) | GPT-3.5 | 9 real APIs | rule P/R/F1, valid inputs | 97 % precision; 72.7 % valid |
| 1 | KAT (2024) | GPT-3.5-turbo | 12 services | status-code cov (2xx/4xx) | 74.9 % (+15.7 pp) |
| 2 | RESTSpecIT (2024) | DeepSeek / GPT | 10 PRAB APIs | route discovery, 5xx | 88.6 % routes; 5xx in 4 APIs |
| 7 | AutoRestTest (2025) | GPT-3.5 + MARL | 12 services | code cov, 500-errors | 58.3 % line; 42 500s vs EM 20 |
| 3 | LlamaRestTest (2025) | Llama3-8B (ft) | 12 services | code cov, faults | 55.8 % method; 204 faults vs 130 |
| 9 | LogiAgent (2025) | GPT-4o-mini | 12 systems | coverage, logical bugs, 5xx | 71.78 % line; 49 crashes |
| 10 | RESTifAI (2026) | GPT-4.1-mini | 7 services | operation / line coverage | 128/134 ops ≈ 95.5 % |
| 16 | EvoMaster (2019) | search-based | 3 services | statement cov, bugs, **vs manual** | 38 bugs; 41 % gen vs 82 % manual |
| 17 | Morest (2022) | model-based | 6 projects | coverage, bugs | 44 bugs (13 new) |
| 11 | No-Time-to-Rest (2022) | 10 tools (EMB) | 20 EMB services | line / branch cov, 500s | EvoMaster-WB 52.76 % line |

### 3.2 Pattern Analysis
1. **GPT dominates** the LLM line [1, 2, 5, 7, 9, 10] — non-OpenAI / open-source appears only sporadically.
2. **Coverage + 500-error counts dominate** the metrics; semantic / edge-case quality is rarely isolated (only [1] splits 2xx/4xx, only [2] reports 5xx).
3. **Baselines are automated-only** — LLM tools beat EvoMaster on 500s [3, 7] but **no** study adds a *manual* suite; the lone manual comparison [16] predates LLMs and found the tool *below* manual.
4. **Fault detection lacks ground truth** — every fault number [3, 7, 9, 11, 16, 17] is a live-API count, never a Recall against a known seeded-fault total.

### 3.3 Gap Mapping
| GAP | Evidence (papers) | Status |
|-----|-------------------|--------|
| GAP-C (LLM vs manual vs EvoMaster) | [16] only manual comparison (non-LLM, below manual); [3, 7, 11] automated-only | **Confirmed** |
| GAP-D (pre-seeded faults / Recall) | [3, 7, 9, 11, 16, 17] counts only; mutants only on self-built APIs elsewhere | **Confirmed** |
| GAP-M (per-endpoint edge-case + type miss) | [1] (2xx/4xx), [2] (5xx) partial; none per-endpoint | **Confirmed** |
| GAP-T (open-source / Gemini) | sporadic | Confirmed–Deferred (ablation) |

---

## 4. Research Questions

> Fixed here. After instructor approval, the RQs / metrics / thresholds are **not changed** (No-HARKing).

**Main RQ:** *How effectively can LLMs automatically generate API test cases from OpenAPI specifications, compared to manually designed tests and EvoMaster, on pre-seeded faulty EMB API versions?*

### RQ1 — Endpoint coverage (GAP-M facet) — *absolute*
> Do [P: 3 EMB REST APIs, locally deployed] × [I: LLM (Claude Sonnet 4.6) from the OpenAPI spec] reach **endpoint coverage ≥ 90 %** [O], and which endpoint types (CRUD / auth / error-handling) are most missed?
- **Claim type:** absolute threshold.
- **H0:** mean endpoint coverage **≤ 90 %** (μ ≤ 0.90). **H1:** **> 90 %**.
- **Metric:** endpoint coverage = operations exercised by ≥ 1 test / total operations (per API).
- **Threshold:** **90 %** — **Case 2**: floor 88.6 % route discovery [2], ceiling 95.5 % [10].
- **Statistical test:** one-sample **Wilcoxon signed-rank** vs 0.90 (per-endpoint), α = 0.05.

### RQ2 — Fault detection: LLM vs Manual vs EvoMaster (GAP-C + GAP-D) — *comparative*
> How many **pre-seeded faults** do LLM-generated tests detect vs manual vs EvoMaster across 3 APIs?
- **Claim type:** comparative (3 systems).
- **H0:** rate_LLM ≤ max(rate_Manual, rate_EvoMaster). **H1:** rate_LLM > both.
- **Metric:** fault-detection **Recall** = killed / total pre-seeded faults (ground truth known).
- **Threshold:** comparative — baseline = {Manual, EvoMaster}; **Case** = N/A (Recall never computed before [3, 7, 11, 16]).
- **Statistical test:** **Friedman** + post-hoc pairwise **Wilcoxon** (Holm); per-fault **McNemar** (pooled); effect size Cliff's δ. α = 0.05.

### RQ3 — Edge-case / error-code scenarios: LLM vs Manual (GAP-M) — *comparative*
> Are LLM tests more effective than manual design at producing **4xx/5xx + boundary** scenarios per endpoint?
- **Claim type:** comparative (LLM vs Manual).
- **H0:** median_LLM ≤ median_Manual. **H1:** median_LLM > median_Manual.
- **Metric:** edge-case scenario count per endpoint (distinct negative + boundary + error-code).
- **Threshold:** comparative — **Case 3**: no paper measures it (only [1] 2xx/4xx, [2] 5xx); the pilot establishes measurability.
- **Statistical test:** paired **Wilcoxon signed-rank** across endpoints; effect size rank-biserial. α = 0.05.

**Multiple-testing correction:** Holm (RQ2 post-hoc) + Bonferroni across the 3 RQ families (α_adj ≈ 0.017).

---

## 5. Experiment Protocol

> Reproducibility: exact model version + hyper-parameters + verbatim prompt, otherwise not reproducible.

### 5.1 Pipeline (5 steps)
1. Build + deploy 3 EMB SUTs locally (JDK 8 fat-jars). 2. Feed each SUT's OpenAPI spec to the LLM with the frozen prompt → REST-assured JUnit tests. 3. Author the Manual suite (EP/BVA, blind to faults) + run EvoMaster black-box. 4. Seed faults (mutation) → mutant SUTs with a ground-truth catalog. 5. Run every suite against the original + each mutant; compute coverage, mutation-kill Recall, and edge-case counts; analyse.

### 5.2 Dataset
- **Source:** EvoMaster Benchmark (EMResearch/EMB, public, LGPL). **APIs (N = 3):** `rest-ncs` (6 ops), `rest-scs` (11 ops), `features-service` (18 ops) = **35 operations** (counts verified against `EMB/statistics/table_emb.md`).
- **Faults:** standard mutation operators (relational / arithmetic / negate-boundary — PIT/Offutt families) on controller + core-logic classes; each recompiled into a mutant SUT; only compilable mutants kept; ground-truth catalog `experiment/faults/<sut>/catalog.json`. **Pilot N = 133 mutants** (ncs 70, scs 59, features 4).
- **Rationale:** EMB is the shared benchmark [3, 7, 11]; pre-seeding gives the ground-truth Recall absent in GAP-D.

### 5.3 LLM / Tool Configuration
- **Model:** `claude-sonnet-4-6` (Claude Sonnet 4.6, Anthropic). **Hyper-parameters:** temperature = 0, top_p = 1, max_tokens = 4096, fixed seed.
- **Strategy:** few-shot from the OpenAPI spec only (black-box, blind to source / faults).
- **Prompt template:** verbatim in `experiment/llm/prompt_template.md`.
- **Model choice:** the team uses **Claude Sonnet 4.6** for **both** the pilot and the full run, so the Week-7 pilot findings carry over directly (no model swap). Choosing a non-GPT model also contributes evidence outside the GPT-dominated literature (§3.2) — a partial **GAP-T** contribution. The pipeline stays model-agnostic, so the backend can be swapped if ever needed.

### 5.4 Measurement
- **Coverage:** operations exercised / total (from the spec + executed requests). **Tool:** spec parser + REST-assured run.
- **Fault Recall:** killed / total mutants (a suite kills a mutant iff a test that passes on the original fails on the mutant). Per-arm killed counts are persisted to `experiment/results/raw/<sut>_recall.json`.
- **Edge-case count:** distinct negative / boundary / error-code scenarios per endpoint, parsed from `// SCENARIO type=` tags.
- **Code-derived error-surface baseline (ground truth for GAP-M):** a static analyser (`experiment/scripts/error_surface.py`) extracts, *per endpoint*, every source location that can emit a non-2xx response — `declared` (explicit `status(4xx/5xx)`), `framework` (typed `@PathVariable` → Spring auto-400), or `potential` (uncaught exception → 500) — and writes `experiment/results/error-surface-baseline.json`. This is the tool-independent "what can fail" map against which each suite's outcomes are read.
- **Outcome capture & triggered-vs-missed:** every request a suite issues is replayed through a logging proxy against the live SUT and its **real** HTTP status recorded (`results/raw/traffic.csv`); per endpoint we then compute which error behaviours each arm **triggered** vs **missed** (`results/error-profile.json`).
- **Produced vs Detected (anti-conflation):** we report *separately* the number of tests / edge-case scenarios **produced** and the number of faults / error behaviours actually **detected** (`results/produced-vs-detected.json`), so test *volume* is never mistaken for fault-finding *effectiveness*.

### 5.5 Baselines
- **Manual:** human EP/BVA test design (blind to faults) — `experiment/manual/methodology.md`.
- **EvoMaster 6.0.0** black-box: `--blackBox true --bbSwaggerUrl … --outputFormat JAVA_JUNIT_5 --maxTime 120s`.

### 5.6 Statistical Analysis Plan
- RQ1 one-sample Wilcoxon (one-tailed) vs 0.90; RQ2 Friedman + Holm-Wilcoxon + McNemar; RQ3 paired Wilcoxon (one-tailed). α = 0.05.
- **Effect size:** Cliff's δ (RQ2), rank-biserial (RQ1/RQ3). **Power:** with n = 3 APIs the per-fault McNemar (pooled, N ≈ 133) carries the power; achieved power is reported (statsmodels). Tooling: `scipy` / `statsmodels` (`experiment/scripts/analyze.py`); consolidated machine-readable results in `experiment/results/{rq-results.json, bug-detection.json}`.

---

## 6. Evaluation Plan

### 6.1 Criteria
| RQ | Metric | Threshold | Test | Reject H0 when | Practically significant if |
|----|--------|-----------|------|----------------|----------------------------|
| RQ1 | endpoint coverage % | ≥ 90 % | 1-sample Wilcoxon | p < 0.05 ∧ median > 0.90 | coverage CI lower bound > 0.90 |
| RQ2 | fault Recall | comparative | Friedman + Holm-Wilcoxon; McNemar | Friedman p < 0.05 ∧ LLM > others post-hoc | Cliff's δ not negligible |
| RQ3 | edge-cases / endpoint | comparative | paired Wilcoxon | p < 0.05 ∧ median diff > 0 favouring LLM | rank-biserial ≥ small |

### 6.2 Interpretation
For each RQ: rejecting H0 yields the stated conclusion; a double-positive (RQ1 ∧ RQ3) → "LLM matches the coverage target **and** out-generates manual on edge cases"; a mixed outcome (e.g. RQ3 yes, RQ2 no) → "LLM is more *prolific* but not more *fault-revealing*" — reported honestly, with no metric / threshold change after seeing the data (No-HARKing). The **produced-vs-detected** report (§5.4) is cited explicitly so a high scenario count is never presented as a high bug count.

### 6.3 Sub-group analysis (pre-registered)
By endpoint type (CRUD / auth / error-handling) for the RQ1 miss-profile; by fault location (controller vs logic) for RQ2 — decided **before** running, to explain *where* each arm wins or loses.

---

## 7. Threats to Validity
| Type | Threat | Mitigation (concrete) |
|------|--------|------------------------|
| **Internal** | LLM & Manual authored by the same agent (Claude) in the pilot → author bias | Blind protocol (suites built **before** faults seeded; sub-agent tool-logs show spec-only input); full run uses an independent human cohort for Manual + a separate Claude Sonnet 4.6 session for LLM |
| **Internal** | Lenient `anyOf` status oracles miss boundary-shift mutants | Report kill-by-fault-type; add exact-status assertions where the spec is precise; disclose oracle strength per arm |
| **External** | 3 small EMB APIs; n = 3 limits Friedman power | Per-fault McNemar pooled (N ≈ 133) is the primary RQ2 test; name "EMB-only, JVM-only" as a generalisation limit; GAP-T ablation as future work |
| **Construct** | Mutation kill ≠ real-fault detection; coverage ≠ test quality | Use standard PIT/Offutt operators [cited]; report Recall + coverage + edge-case jointly, not one alone |
| **Conclusion** | Small n → unstable p-values | Non-parametric tests + effect sizes + power analysis reported, not p alone; Holm / Bonferroni for multiplicity |

---

## 8. Timeline & Resources

### 8.1 Role assignment (1 deliverable each; **LR ≠ MS** enforced)
| Member | Role | Deliverable |
|--------|------|-------------|
| **Nguyen Hoang Huy (SE190240)** | **PL** — Project Lead | coordinate, merge, submit proposal, instructor liaison (does **not** run the experiment) |
| Nguyen Thanh Dat (SE190239) | **DG** — Data & Ground Truth | dataset + fault catalog + §3 Related Work |
| **Nguyen Tien Dung (SE190034)** | **LR** — LLM Runner | experiment harness + LLM / EvoMaster runs + cost log (built the pilot) |
| Nguyen Le Thuan (SE190305) | **MS** — Metrics & Stats | metric implementation + statistical tests + §6 |
| Vo Le Trung Nguyen (SE190220) | **RW** — Report Writer | §7 threats + final formatting + defense slides |

### 8.2 Resource Inventory
| Resource | Status | Owner | Note |
|----------|:------:|-------|------|
| Dataset (EMB) | ✅ | DG | cloned + 3 SUTs built / deployed (pilot) |
| Anthropic API — Claude Sonnet 4.6 | ✅ | LR | used in the pilot; same model for the full run |
| EvoMaster 6.0.0 | ✅ | LR | free jar, runs on JDK 17 |
| Compute | ✅ | LR | local CPU (JDK 8 SUTs + JDK 17 harness) |
| Ground truth | ✅ | DG / MS | mutation catalog (no human annotation needed) |

**Budget.** All tooling is free — EMB dataset (LGPL), EvoMaster 6.0.0, and local-CPU compute cost **$0**. The only paid item is the **Claude Sonnet 4.6** API (Anthropic): **$3 / 1M input tokens, $15 / 1M output tokens**. Estimated usage ≈ 25k tokens per SUT generation × 3 SUTs + repeats ≈ **< 300k tokens → ≈ $3–5** (prompt caching / batch processing reduce this further). **Total project cost ≈ negligible (< $10).**

### 8.3 Timeline
| Week | Activity | Output |
|------|----------|--------|
| 5–6 | Finalise + submit proposal; instructor approval | this `proposal.md` + defense slides |
| **7 (Pilot — DONE)** | N ≈ 133 mutants; LLM (Claude Sonnet 4.6) / Manual / EvoMaster on 3 SUTs | `experiment/results/raw/*.csv`, `results/stats/summary.json`, result JSONs, `figures/` |
| 8 (Full) | Scale up the run with Claude Sonnet 4.6 on the approved protocol; finalise analysis | `full_results_analysis` + figures + report |

**Preliminary pilot signal (Week-7, supports feasibility — NOT final):** RQ1 LLM endpoint coverage **100 %** (35/35, p ≈ 1.6e-9 > 90 %); RQ3 LLM **217** vs Manual **141** edge-case scenarios (median 5 vs 4, paired Wilcoxon **p ≈ 6.2e-7**); RQ2 mutation Recall EvoMaster **0.135** > LLM **0.068** = Manual **0.068** (McNemar LLM-vs-EvoMaster p ≈ 0.064) — i.e. EvoMaster's recorded-value oracle catches computational faults that the spec-derived status oracles of LLM / Manual miss. The outcome error-profile additionally shows the LLM suite triggering **31/31** documented HTTP error behaviours (incl. a 500 server crash) vs Manual 22/31. The full (scaled) run with the same model will confirm.

### 8.4 Contingency
- Proposal not approved by Week 6–7 → run **RQ1 only**, report to instructor.
- API rate / quota limits → use batch + prompt caching (near-free) and disclose any fallback model.
- EvoMaster instability → fixed 120 s budget, 3 repeats.
- n = 3 underpowered → rely on the pooled per-fault McNemar + effect sizes.

---

## 9. References

[1] *KAT: Dependency-aware Automated API Testing with Large Language Models*, ICST, 2024. DOI: 10.1109/ICST60714.2024.00017.
[2] *You Can REST Now: Automated Specification Inference and Black-Box Testing of RESTful APIs (RESTSpecIT)*, arXiv, 2024. DOI: 10.48550/arXiv.2402.05102.
[3] *LlamaRestTest: Effective REST API Testing with Small Language Models*, FSE, 2025. DOI: 10.1145/3715737.
[5] *Leveraging Large Language Models to Improve REST API Testing (RESTGPT)*, ICSE-NIER, 2024. DOI: 10.1145/3639476.3639769.
[6] *APITestGenie: Automated API Test Generation through Generative AI*, preprint 2024 / AST 2026. DOI: 10.1145/3793654.3793743.
[7] *AutoRestTest: A Tool for Automated REST API Testing Using LLMs and MARL*, ICSE, 2025. DOI: 10.1109/ICSE55347.2025.00179.
[9] *LogiAgent: Automated Logical Testing for REST Systems*, arXiv, 2025. DOI: 10.48550/arXiv.2503.15079.
[10] *RESTifAI: An LLM Workflow for Reusable REST API Testing*, ICSE (Demo), 2026. DOI: 10.48550/arXiv.2512.08706.
[11] *Automated Test Generation for REST APIs: No Time to Rest Yet*, ISSTA, 2022. DOI: 10.1145/3533767.3534401.
[16] A. Arcuri, *RESTful API Automated Test Case Generation with EvoMaster*, ACM TOSEM, 2019. DOI: 10.1145/3293455.
[17] *Morest: Model-based RESTful API Testing with Execution Feedback*, ICSE, 2022. DOI: 10.1145/3510003.3510133.

*Full 59-paper evidence base: `team-synthesis/evidence-table-merged.md` (DOI / arXiv per entry; primary-verified subset marked).*

---

## Appendix A — Cross-section consistency (self-check)
§2 Gaps ↔ §4 RQs (C/D/M → RQ1/2/3) ✓ · §4 metric / threshold ↔ §5.4 / §6 (coverage 90 %, Recall, edge-count) ✓ · §4 comparative ↔ §5.5 baselines (Manual + EvoMaster) ✓ · §5 metric threats ↔ §7 (oracle, mutation) ✓ · §6 criteria ↔ §8.3 timeline ✓.

**After instructor approval:** the RQs / metrics / thresholds are frozen; the next step is the full run per §5.
