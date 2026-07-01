# RBL-4 Implementation Plan

> Executed inline in this session (same agent has full context of `proposal.md`, the RBL-4 brief, and the existing pipeline — no handoff). Tracked live via TodoWrite; this document is the durable record.

**Goal:** Make `experiment/` literally compliant with the RBL-4 file tree, execute the proposal's Week-8 independent-Manual-suite upgrade for real, fix the two real gaps found in `analyze.py` (missing effect sizes / power / multiplicity correction vs proposal §5.6), and produce genuinely executed notebooks + 300 DPI figures — without touching anything `proposal.md` cites by path.

**Key evidence gathered before planning (do not re-derive):**
- `results/raw/{ncs,scs,features}_kills.csv`: LLM (n_oracle 79/97/92) and Manual (56/78/43) have *different* oracle sizes but *identical* kill/no-kill outcome on **every single mutant** (133/133). Root cause confirmed by reading `NcsLlmTests.java`/`NcsManualTests.java`: both assert `body("resultAsDouble", notNullValue())` / `hasKey(...)` — existence, not value — so both are structurally blind to silent arithmetic mutants on `rest-ncs`/`rest-scs`. This is proposal §7's pre-registered "lenient oracle" threat, empirically confirmed, **not a pipeline bug**. Do not change the oracle (would be HARKing); report it as a finding.
- `analyze.py` currently implements: RQ1 one-sample Wilcoxon; RQ3 paired Wilcoxon + pair counts; RQ2 Friedman (omnibus) + per-fault McNemar. **Missing vs. proposal §5.6:** Cliff's δ (RQ2 effect size), rank-biserial as an actual correlation value (RQ1/RQ3 — currently only pair counts), Holm-corrected **pairwise** Wilcoxon post-hoc for RQ2, `statsmodels` achieved-power, and the Bonferroni correction across the 3 RQ families (α_adj ≈ 0.017). These must be added — this is the real statistical completion RBL-4 asks for, not just relabeling.
- All mutant/original jars (136 files) and the compiled harness already exist on disk — no rebuild needed.
- JDK 8 at `C:\Users\dungm\tools\jdk8\jdk8u492-b09`, JDK 17 on PATH, Maven 3.9.16, EvoMaster jar at `D:\SWT301_SU26_Group2\_emb_work\tools\evomaster.jar` — all present.
- Missing pip packages: `seaborn`, `nbformat`, `nbclient`.

---

## Task 1 — Environment

**Files:** none (environment only)

- [ ] Install missing packages: `pip install seaborn nbformat nbclient`
- [ ] Verify: `python -c "import seaborn, nbformat, nbclient; print('ok')"` → prints `ok`

## Task 2 — `data/raw/README.md` (verified provenance)

**Files:**
- Create: `experiment/data/raw/README.md`

- [ ] WebSearch/WebFetch to verify current facts about `EMResearch/EMB` (GitHub URL, license file content, current README) — do not assert from memory (global CLAUDE.md rule). Cite the URL.
- [ ] Cross-check operation counts against `experiment/specs/*.openapi.json` (already read: `rest-ncs` = 6 GET ops) and `_emb_work/EMB/statistics/table_emb.md` if present.
- [ ] Write the file with: source URL, license (LGPL-3.0 — verify against the actual `LICENSE` file in the clone at `_emb_work/EMB/`), the 3 SUTs used (`rest-ncs` 6 ops, `rest-scs` 11 ops, `features-service` 18 ops = 35 total), module path (`jdk_8_maven`), parent artifact `org.evomaster:evomaster-benchmark:4.3.0`, download/clone date (git log shows 2026-06-13; confirm against `_emb_work/EMB/.git` if present via `git log -1 --format=%ad --date=short`), and an explicit "why only 3 of ~20 EMB services" note (feasibility scope decided in `proposal.md` §5.2, frozen — not expanded per this session's dataset-scope decision).
- [ ] Commit: `git add experiment/data/raw/README.md && git commit -m "docs(RBL-4): add data/raw/README.md with verified EMB provenance"`

## Task 3 — Ground-truth CSV exports (code-derived, no IAA needed)

**Files:**
- Create: `experiment/scripts/export_ground_truth.py`
- Create (by running the script): `experiment/data/pilot_sample.csv`, `experiment/data/pilot_ground_truth.csv`, `experiment/data/full_ground_truth.csv`

- [ ] Write `export_ground_truth.py`: reads all three `experiment/faults/<sut>/catalog.json`, filters `status == "compiled"`, writes one row per kept mutant with columns `sut,mutant_id,file,line,operator` to `data/full_ground_truth.csv` (this **is** the full 133-row ground truth — nothing sampled, so `pilot_ground_truth.csv` is written identically for Week-7 traceability, and `data/pilot_sample.csv` is a copy of the same 133-row scope with a `note` column = `"Week-7 pilot ran on the full compilable mutant catalog (133); no smaller sub-sample was drawn — see notes.md"`).
- [ ] Run: `python experiment/scripts/export_ground_truth.py`
- [ ] Verify: `python -c "import pandas as pd; d=pd.read_csv('experiment/data/full_ground_truth.csv'); assert len(d)==133, len(d); print('133 rows OK')"`
- [ ] Commit: `git add experiment/scripts/export_ground_truth.py experiment/data/*.csv && git commit -m "feat(RBL-4): export code-derived ground truth CSVs from mutation catalogs (N=133)"`

## Task 4 — `scripts/test_api.py` (gate E3, adapted to this project's real architecture)

**Files:**
- Create: `experiment/scripts/test_api.py`

- [ ] Write a script that, for each of the 3 SUTs, starts nothing (assumes SUTs may not be running) but performs a **liveness smoke test contract**: attempts one GET request to a known-good sample endpoint (`/api/bessj/2/1.0` for ncs, and the equivalent one operation each for scs/features read from the spec's first path), with a 3s timeout, and prints `REACHABLE`/`UNREACHABLE` per SUT plus one sample JSON response when reachable. Exits 0 always (it's a diagnostic, not a hard gate failure — SUTs are started on demand by `run_mutation.py`, not expected to be always-on).
- [ ] Add a top-of-file docstring explaining the E3 adaptation: this project's "LLM API" is a Claude Code sub-agent invocation (see `env/tools.md`), not a scriptable HTTP client, so `test_api.py` validates the *target* REST APIs (the SUTs) instead — the practical intent of gate E3 (confirm the environment works before a big batch run).
- [ ] Verify: `python experiment/scripts/test_api.py` → runs to completion, exit code 0, regardless of whether SUTs happen to be up.
- [ ] Commit: `git add experiment/scripts/test_api.py && git commit -m "feat(RBL-4): add scripts/test_api.py (gate E3, SUT-liveness smoke test)"`

## Task 5 — `scripts/compute_metric.py` (gate E4, runs on synthetic fixture)

**Files:**
- Create: `experiment/scripts/compute_metric.py`
- Create: `experiment/scripts/fixtures/dummy_kills.csv`, `experiment/scripts/fixtures/dummy_coverage.csv`, `experiment/scripts/fixtures/dummy_scenarios.csv` (small synthetic fixtures, ~5 rows each, matching the real schemas already used by `analyze.py`)

- [ ] Write 3 tiny synthetic CSVs by hand (schema copied from the real `results/raw/*.csv` headers already read above).
- [ ] Write `compute_metric.py`: a thin CLI wrapper that imports `analyze.py`'s three functions (`rq1_coverage`, `rq3_edge_cases`, `rq2_fault_detection`) via `importlib` against a `--raw-dir` argument (defaults to the real `results/raw/`, but accepts `--raw-dir experiment/scripts/fixtures` for the gate-E4 smoke test), so the exact same statistical code path is exercised on both fake and real data — no duplicate stats logic.
- [ ] Verify: `python experiment/scripts/compute_metric.py --raw-dir experiment/scripts/fixtures --out /tmp_test_out` → completes with exit 0, no exception, on the synthetic data.
- [ ] Commit: `git add experiment/scripts/compute_metric.py experiment/scripts/fixtures && git commit -m "feat(RBL-4): add scripts/compute_metric.py (gate E4) + synthetic fixtures"`

## Task 6 — Extend `analyze.py` for proposal §5.6 completeness

**Files:**
- Modify: `experiment/scripts/analyze.py`

- [ ] Add Cliff's δ helper function:
```python
def cliffs_delta(a, b):
    """Cliff's delta effect size for two independent-ish samples a, b."""
    import numpy as np
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    gt = sum((x > y) for x in a for y in b)
    lt = sum((x < y) for x in a for y in b)
    return (gt - lt) / (len(a) * len(b))
```
- [ ] Add rank-biserial helper (Wilcoxon signed-rank effect size, matched pairs):
```python
def rank_biserial(diffs):
    """Matched-pairs rank-biserial correlation from Wilcoxon signed-rank diffs."""
    import numpy as np
    d = np.asarray([x for x in diffs if x != 0], dtype=float)
    if len(d) == 0:
        return 0.0
    ranks = pd.Series(np.abs(d)).rank().values
    r_plus = ranks[d > 0].sum()
    r_minus = ranks[d < 0].sum()
    return (r_plus - r_minus) / ranks.sum()
```
- [ ] In `rq1_coverage()` and `rq3_edge_cases()`, after the existing Wilcoxon call, add `res["rank_biserial"] = rank_biserial(diffs)`.
- [ ] In `rq2_fault_detection()`, after Friedman, add: (a) Holm-corrected pairwise Wilcoxon signed-rank across the per-SUT recall vectors for each arm pair (`llm` vs `manual`, `llm` vs `evomaster`) via `statsmodels.stats.multitest.multipletests(pvals, method="holm")`; (b) Cliff's δ per arm pair using the per-mutant `killed` vectors (`cliffs_delta(wide["llm"].dropna(), wide[comp].dropna())`); (c) achieved power via `statsmodels.stats.power` (`from statsmodels.stats.power import NormalIndPower` on the pooled McNemar-equivalent proportions, `effect_size=proportion_effectsize(p1,p2)`, `nobs1=N`, report `power`).
- [ ] In `main()`, after building `summary`, add Bonferroni across the 3 RQ families: `summary["multiplicity"] = {"alpha_raw": 0.05, "alpha_bonferroni_3family": round(0.05/3, 4), "note": "per proposal.md §4: Holm within RQ2 post-hoc + Bonferroni across the 3 RQ families"}`.
- [ ] Run: `cd experiment && python scripts/analyze.py` (on the **existing** real data, LLM/EvoMaster arms unchanged) → confirm it still runs to completion and `results/stats/summary.json` now contains `rank_biserial`, `cliffs_delta`, `holm_pairwise`, `power` keys with no exceptions.
- [ ] Commit: `git add experiment/scripts/analyze.py experiment/results/stats/summary.json && git commit -m "feat(RBL-4): extend analyze.py — Cliff's delta, rank-biserial, Holm pairwise, power, Bonferroni (closes proposal §5.6 gap)"`

## Task 7 — Independent Manual suite regeneration (the real Week-8 delta)

**Files:**
- Create (via 3 isolated `Agent` calls, one per SUT): fresh content for `experiment/harness/src/test/java/manual/NcsManualTests.java`, `ScsManualTests.java`, `FeaturesManualTests.java`
- Archive old versions first to: `experiment/manual/pilot-archive/<Sut>ManualTests.java.pilot` (preserve Week-7 version for traceability/diff)

- [ ] `cp` the 3 existing Manual `.java` files to `experiment/manual/pilot-archive/` before overwriting (traceability).
- [ ] For each SUT, dispatch a fresh `Agent` (general-purpose, no shared context with any other call) with this exact prompt shape (fill `<SUT_NAME>`, `<SPEC_PATH>`, `<BASE_PORT>`):
  > "You are an experienced manual QA engineer doing black-box REST API test design. You have access ONLY to the OpenAPI spec at `<SPEC_PATH>` — do not read any other file, do not read source code, do not search the web. Read the spec, then apply: (1) Equivalence Partitioning — one representative test per valid/invalid input class per parameter; (2) Boundary Value Analysis for numeric/ordered parameters; (3) error guessing (wrong type, missing segment, empty value); (4) for CRUD resources, the create→read→update→delete→read-after-delete lifecycle. Output ONE compilable Java file: `package manual;` + `public class <SUT_NAME>ManualTests` using JUnit 5 + REST-assured (`io.restassured.RestAssured`, `static io.restassured.RestAssured.given`, Hamcrest `static org.hamcrest.Matchers.*`), a `@BeforeAll static void setup()` setting `RestAssured.baseURI = System.getProperty(\"baseURI\", \"http://localhost:<BASE_PORT>\")` and `RestAssured.urlEncodingEnabled = false`. Each `@Test` asserts `.statusCode(...)` (use `anyOf(is(...), ...)` for undocumented codes) — do NOT assert on the numeric value of any response field, only its presence/status (existence checks like `notNullValue()`/`hasKey()` are fine, exact-value checks are not, to stay consistent with the pre-registered methodology). Directly above every `@Test`, emit `// SCENARIO op=<operationId> type=<positive|negative|boundary|errorcode> expect=<status-or-class>`. Output ONLY the Java source in one ```java block, no prose."
- [ ] Write each Agent's returned Java source to its target file, overwriting the pilot version (already archived).
- [ ] Verify blindness after the fact: check the returned source contains **no** mention of mutant/fault/`m0`/`catalog`/`llm`/other arms (`grep -i "mutant\|fault\|catalog" <file>` → no matches).
- [ ] Recompile: `cd experiment/harness && JAVA_HOME="$JAVA_HOME_17" mvn -q -o test-compile`
- [ ] Verify: exit code 0, and `target/test-classes/manual/*ManualTests.class` exist for all 3.
- [ ] Commit: `git add experiment/harness/src/test/java/manual experiment/manual/pilot-archive && git commit -m "feat(RBL-4): regenerate Manual suite via 3 independent isolated sessions (Week-8 bias fix, pilot archived)"`

## Task 8 — Re-run mutation-kill matrix for the new Manual suite

**Files:**
- Modify (regenerate): `experiment/results/raw/{ncs,scs,features}_kills.csv`, `*_recall.json`

- [ ] For each SUT, run the existing driver, letting it re-measure all 3 arms (LLM/EvoMaster results should reproduce identically since those suites didn't change — this also serves as a regression check on the harness):
```bash
cd experiment
python scripts/run_mutation.py --sut Ncs --jar rest-ncs-sut.jar --mutants faults/ncs \
  --port 8080 --harness harness --results results/raw \
  --jdk8 "C:/Users/dungm/tools/jdk8/jdk8u492-b09" --jdk17 "$JAVA_HOME" --restart-per-arm
# repeat for Scs (port 8083, faults/scs) and Features (port 8081, faults/features)
```
- [ ] Verify per SUT: `manual` row's `n_oracle` in the new `_kills.csv` differs from the archived pilot value (56/78/43) — confirms the new suite is genuinely different code, not a no-op.
- [ ] Re-run the identical Python diff check used during investigation (pivot llm vs manual per mutant) and record the new agreement rate in `notes.md` — **do not** treat a still-high agreement rate as an error; per Task-header evidence, it is mechanistically expected on `ncs`/`scs`. Report the number honestly either way.
- [ ] Commit: `git add experiment/results/raw/*_kills.csv experiment/results/raw/*_recall.json && git commit -m "feat(RBL-4): full run — re-execute mutation matrix against independent Manual suite (N=133 mutants unchanged)"`

## Task 9 — Re-run scenario/coverage parsing for the new Manual suite

**Files:**
- Modify (regenerate): `experiment/results/raw/scenarios.csv`, `experiment/results/raw/coverage.csv`

- [ ] Run: `cd experiment && python scripts/parse_scenarios.py` (re-parses `// SCENARIO` tags from all committed test sources, including the new Manual files — check its CLI/args by reading the script first if it takes explicit paths; adapt call accordingly).
- [ ] Verify: `manual` row counts in `scenarios.csv` changed from the pilot's 141 total edge-cases (expected — new suite, different scenario count).
- [ ] Commit: `git add experiment/results/raw/scenarios.csv experiment/results/raw/coverage.csv && git commit -m "feat(RBL-4): re-parse scenarios/coverage for independent Manual suite"`

## Task 10 — Recompute final stats

**Files:**
- Modify: `experiment/results/stats/summary.json`, `experiment/results/stats/rq2_recall_per_sut.csv`, `experiment/results/stats/rq3_edge_per_op.csv`

- [ ] Run: `cd experiment && python scripts/analyze.py`
- [ ] Read the new `summary.json`; confirm RQ1 numbers are byte-identical to the pilot (LLM-only, must not change). Confirm RQ2/RQ3 Manual-side numbers changed from the pilot's baseline (0.0677 overall recall / 141 total edge-cases) — record the new values.
- [ ] Commit: `git add experiment/results/stats && git commit -m "feat(RBL-4): recompute RQ1/RQ2/RQ3 statistics for the full (Week-8) run"`

## Task 11 — `results/summary.csv` (RBL-4's required 1-row-per-RQ format)

**Files:**
- Create: `experiment/scripts/write_summary_csv.py`
- Create (via running it): `experiment/results/summary.csv`

- [ ] Write a script reading `results/stats/summary.json` and emitting exactly 3 rows (`rq,metric,value,p_value,effect_size,n,reject_h0`) — RQ1 (coverage %, Wilcoxon p, rank-biserial, n=35, reject_H0 bool), RQ2 (overall Recall per arm — one row per arm comparison vs LLM, McNemar/Holm p, Cliff's δ, n=133), RQ3 (median edge-case counts, Wilcoxon p, rank-biserial, n=35).
- [ ] Run it; verify `results/summary.csv` opens with `pandas.read_csv` and has no `NaN` in the `p_value`/`effect_size` columns for any row that has a defined test.
- [ ] Commit: `git add experiment/scripts/write_summary_csv.py experiment/results/summary.csv && git commit -m "feat(RBL-4): write results/summary.csv (1 row per RQ per gate spec)"`

## Task 12 — `results/pilot_llm_output.csv` / `pilot_api_log.txt` / `full_llm_output.csv` / `full_api_log.txt`

**Files:**
- Create: `experiment/results/pilot_llm_output.csv`, `experiment/results/pilot_api_log.txt`, `experiment/results/full_llm_output.csv`, `experiment/results/full_api_log.txt`

- [ ] `pilot_llm_output.csv`: one row per LLM-arm scenario from the Week-7 pilot, derived from `results/raw/scenarios.csv` (`arm == "llm"`) — columns `sut,op,scenario_type,count`.
- [ ] `pilot_api_log.txt`: reconstructed from `llm/transcripts/*.md` headers (timestamp, model id `claude-sonnet-4-6`, spec sha256) — one line per SUT generation call, explicitly noting "invocation = Claude Code isolated sub-agent, not a metered HTTP API — no per-call $ cost; see env/tools.md."
- [ ] `full_llm_output.csv`: same shape, but scoped to the Week-8 full run (LLM arm reused unchanged + new Manual arm output combined, tagged by `arm` column).
- [ ] `full_api_log.txt`: append the 3 new Manual-generation sub-agent invocations from Task 7 (timestamp, "manual-arm regeneration", spec file, blindness-check result).
- [ ] Commit: `git add experiment/results/{pilot,full}_llm_output.csv experiment/results/{pilot,full}_api_log.txt && git commit -m "feat(RBL-4): add pilot/full LLM output + API-invocation logs"`

## Task 13 — `results/pilot_analysis.ipynb` and `results/full_analysis.ipynb`

**Files:**
- Create: `experiment/scripts/build_notebooks.py` (programmatically builds both notebooks via `nbformat`, then executes them via `nbclient` so outputs are real, not hand-typed)
- Create (via running it): `experiment/results/pilot_analysis.ipynb`, `experiment/results/full_analysis.ipynb`

- [ ] Write `build_notebooks.py` using `nbformat.v4.new_notebook`/`new_code_cell`/`new_markdown_cell`: pilot notebook loads `results/raw/scenarios.csv` (pre-Task-8 archived copy) + prints descriptive stats + histogram (matches RBL-4's 7.3 requirement: "Vẽ histogram phân phối"); full notebook loads the final `results/raw/*` + `results/stats/summary.json`, recomputes/display RQ1/RQ2/RQ3 conclusions with p-values/effect sizes/N, and explicitly states the reject/fail-to-reject H0 call per RQ (RBL-4 8.3 requirement).
- [ ] Execute both via `nbclient.NotebookClient(nb, timeout=120).execute()` and save with real outputs embedded — do not hand-write fabricated output cells.
- [ ] Verify "Restart & Run All" survivability: re-run `nbclient` execution on the saved `.ipynb` a second time from a clean kernel state; confirm zero errors.
- [ ] Commit: `git add experiment/scripts/build_notebooks.py experiment/results/*.ipynb && git commit -m "feat(RBL-4): build + execute pilot_analysis.ipynb and full_analysis.ipynb (real outputs, Restart&RunAll-clean)"`

## Task 14 — Figures at 300 DPI

**Files:**
- Create: `experiment/scripts/make_rbl4_figures.py`
- Create (via running it): `experiment/figures/fig1_distribution.png`, `experiment/figures/fig2_comparison.png`

- [ ] `fig1_distribution.png`: boxplot/violin (seaborn) of per-mutant RQ2 Recall distribution across the 3 arms (primary GAP-C+D metric) — title, axis labels, N annotation (`N=133 mutants`), `dpi=300`.
- [ ] `fig2_comparison.png`: RQ3 LLM-vs-Manual per-endpoint edge-case comparison (paired bar or slope chart) — title, axis labels, `N=35 operations` annotation, `dpi=300`.
- [ ] Do **not** delete/replace the existing `rq1_coverage.png`/`rq2_recall.png`/`rq3_edgecases.png` — additive per the design doc.
- [ ] Verify: `python -c "from PIL import Image; im=Image.open('experiment/figures/fig1_distribution.png'); print(im.info.get('dpi'))"` → shows `(300, 300)` or similar.
- [ ] Commit: `git add experiment/scripts/make_rbl4_figures.py experiment/figures/fig1_distribution.png experiment/figures/fig2_comparison.png && git commit -m "feat(RBL-4): add fig1_distribution.png + fig2_comparison.png (300 DPI, titled/annotated)"`

## Task 15 — `scripts/run_experiment.py` (gate-named entrypoint)

**Files:**
- Create: `experiment/scripts/run_experiment.py`

- [ ] Thin CLI orchestrator: `--stage {pilot,full} --sut {ncs,scs,features,all}` dispatches to `run_mutation.py` + `parse_scenarios.py` + `analyze.py` in sequence, writing a timestamped line to `results/{pilot,full}_api_log.txt` per invocation. This is the literal "batch-run driver" gate E3/8.2 asks for; it wraps rather than duplicates Tasks 8-10's scripts.
- [ ] Verify: `python experiment/scripts/run_experiment.py --stage full --sut ncs --dry-run` prints the planned command sequence without executing (safe smoke test).
- [ ] Commit: `git add experiment/scripts/run_experiment.py && git commit -m "feat(RBL-4): add scripts/run_experiment.py orchestration entrypoint"`

## Task 16 — `notes.md`

**Files:**
- Create: `experiment/notes.md`

- [ ] Write the running log: E1-E7 gate table (status + evidence path for each), the 3 default decisions from `RBL4-FULL-RUN-DESIGN.md` §3, the oracle-weakness finding from this plan's header (with the exact evidence numbers), the features-service mutant-count imbalance (4 vs 70/59, disclosed not fixed), and a chronological error/decision log of anything that deviated during Tasks 1-15 (fill in as actually encountered during execution — no placeholders; if nothing deviates, state that explicitly).
- [ ] Commit: `git add experiment/notes.md && git commit -m "docs(RBL-4): add notes.md (gate tracker, decisions, disclosed limitations)"`

## Task 17 — Final verification pass

**Files:** none (verification only)

- [ ] `jupyter nbconvert --to notebook --execute --inplace experiment/results/full_analysis.ipynb` (or `nbclient` equivalent) → zero errors, confirms Restart & Run All.
- [ ] `python experiment/scripts/test_api.py` → exit 0.
- [ ] `python experiment/scripts/compute_metric.py --raw-dir experiment/scripts/fixtures --out /tmp_test_out2` → exit 0.
- [ ] `cd D:/SWT301_SU26_Group2 && git status` → confirm no untracked `.env`, `api_key.txt`, `__pycache__/` (gate E7 checklist).
- [ ] Diff every number in `results/summary.csv` against its source raw file — confirm 100% traceable, zero hand-typed statistics.
- [ ] Update `team-synthesis/proposal.md` header status line is **not** edited (frozen document) — instead, flag Gate E1 status to the user in the final chat summary.

---

## Self-review notes

- **Spec coverage:** every RBL-4-mandated path (§ file tree in the assignment PDF) has a task. The 7-gate table (E1-E7) is covered by Tasks 2-5 (E2 dataset already present, E3→Task4, E4→Task5, E5→ground-truth rationale in Task 3/16, E6 budget — already $0 per proposal §8.2 since sub-agent invocation replaces the paid API, noted in Task 12) + Task 16 (E1, E7).
- **No placeholders:** all code blocks above are complete function bodies or exact commands; the 3 items intentionally left data-dependent (Manual Java test content, exact WebSearch citation text, exact new recall numbers) are data-dependent by nature — pre-writing them now would mean guessing schemas/results not yet observed, which violates "don't guess APIs/data shapes."
- **Type consistency:** `cliffs_delta(a, b)` and `rank_biserial(diffs)` signatures introduced in Task 6 are the only new shared functions; both are called exactly once each per RQ in the same task, no cross-task signature drift.
