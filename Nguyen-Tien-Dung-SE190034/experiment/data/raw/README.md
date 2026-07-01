# Dataset provenance — EMB (EvoMaster Benchmark)

**Do not edit the SUT source under this experiment's `specs/`, `faults/`, or the external clone at
`_emb_work/EMB/` — they are the frozen, pre-registered dataset per `team-synthesis/proposal.md` §5.2.**

## Source (verified 2026-07-01)

- **Original repository (used by this project):** `https://github.com/EMResearch/EMB` (git remote of
  the local clone at `D:\SWT301_SU26_Group2\_emb_work\EMB`, confirmed via `git remote -v`).
- **Current upstream identity:** as of EMB **v4.0.0**, the project was renamed **WFD (Web Fuzzing
  Dataset)** and now lives at `https://github.com/WebFuzzing/Dataset` (36 REST APIs in the new
  superset). This project's clone (local HEAD dated 2026-05-20, pulled into this repo 2026-06-13 —
  see `git log --diff-filter=A -- experiment/specs/`) predates that rebrand/expansion and uses the
  **original 3-SUT EMB scope**, matching the citation below.
- **Academic citation (primary, matches the version actually used):**
  A. Arcuri, M. Zhang, A. Golmohammadi, A. Belhadi, J. P. Galeotti, B. Marculescu, S. Seran.
  *"EMB: A Curated Corpus of Web/Enterprise Applications And Library Support for Software Testing
  Research."* IEEE International Conference on Software Testing, Validation and Verification
  (ICST), 2023.
  ([WebFuzzing/EvoMaster publications list](https://github.com/EMResearch/EvoMaster/blob/master/docs/publications.md))
- **Successor citation (for reference, NOT the version used here):** O. Sahin, M. Zhang, A. Arcuri.
  *"WFC/WFD: Web Fuzzing Commons, Dataset and Guidelines to Support Experimentation in REST API
  Fuzzing."* arXiv:2509.01612, 2025.

## License — correction vs. `proposal.md` (two-step correction; second is the accurate one)

`proposal.md` §5.2 describes the dataset as "public, LGPL". **Verified against the actual clone**
(`_emb_work/EMB/LICENSE`, `README.md` §License, and — the authoritative source — `README.md`'s own
**per-SUT provenance table** naming each case study's individual license, all read directly,
2026-07-01): there is no single blanket license for the dataset. The repository's own new code
(drivers, scripts) is **Apache License 2.0**, not LGPL — but the 3 SUTs used here are **not**
uniformly covered by that Apache 2.0 grant; each has its own status per EMB's own README table:

| SUT | EMB's own license listing | What it means |
|-----|---------------------------|----------------|
| `rest-ncs` | **"not-known license, artificial numerical examples coming from different sources"** | Developed by the EMB team ("artificial... developed by us") but the example content itself carries no declared license — only the EMB *driver/wrapper* code around it is Apache 2.0. |
| `rest-scs` | **"not-known license, artificial string examples coming from different sources"** | Same status as `rest-ncs`. |
| `features-service` | **"(Apache)"**, sourced from a **third party**: `https://github.com/JavierMF/features-service` | Genuinely Apache-licensed, but it is a wrapped external project, not EMB-authored code — the Apache grant here is the *original* project's, not the benchmark repo's blanket license (coincidentally the same license family). |

(An earlier draft of this file assumed all 3 SUTs were EMB-authored "artificial" case studies falling
under the repo's blanket Apache 2.0 — that was wrong for `features-service`, which is `cs/rest/
**original**/features-service`, i.e. EMB's "wrapped real third-party app" category, not `cs/rest/
artificial/`. Caught and corrected before this file was finalized; logged in `notes.md`.)
**Use here is for non-commercial academic coursework (SWT301 RBL-4)**, consistent with EMB/WFD's own
stated purpose as a research benchmark; the "not-known license" status of `rest-ncs`/`rest-scs` is
disclosed rather than glossed over, and does not block this use, but would need review before any
redistribution beyond the course.

## SUTs used (frozen scope — do not add more, per this project's dataset-scope decision)

Counts cross-verified against `_emb_work/EMB/statistics/table_emb.md` (columns: protocol, name, LOC,
#paths, **#operations**, language, JDK, build tool, DB):

| SUT | Module path (verified) | #Operations (verified) | Language | JDK | Notes |
|-----|-------------|:-:|----------|-----|-------|
| `rest-ncs` | `jdk_8_maven/cs/rest/artificial/ncs` | **6** | Java | 8 | Numerical Case Study — pure-computation endpoints (Bessel function, exponential integral, Fisher, gamma, remainder, triangle-type), response = `{resultAsDouble, resultAsInt}` |
| `rest-scs` | `jdk_8_maven/cs/rest/artificial/scs` | **11** | Java | 8 | String Case Study |
| `features-service` | `jdk_8_maven/cs/rest/**original**/features-service` (note: NOT under `artificial/`) | **18** | Java | 8 | CRUD resource API, uses H2 embedded DB; wraps the real 3rd-party project `JavierMF/features-service` |
| **Total** | | **35** | | | Matches `proposal.md` §5.2 exactly (verified, not re-derived) |

OpenAPI specs committed at `experiment/specs/{rest-ncs,rest-scs,features-service}.openapi.json`
(Swagger 2.0 format, extracted from each SUT's running `/v2/api-docs` endpoint).

## Faults (ground truth) — see `experiment/faults/<sut>/catalog.json`

Standard mutation operators (relational / arithmetic / negate-boundary — PIT/Offutt families) applied
to controller + core-logic classes; only **compilable** mutants are kept as the ground-truth catalog
(non-compiling candidates are recorded with `"status": "non-compiling-discarded"` and excluded).
Kept counts: `ncs` 70 (of 300 candidates), `scs` 59, `features` 4. **The `features-service` count is
disclosed as a known imbalance in `notes.md` — not corrected by adding more mutants post-hoc**, since
that would be a post-hoc dataset change after results were already seen (see design doc §3, decision
2, and RBL-4's own "không được tự thêm dữ liệu sau khi thấy data" rule).

## Download / integration date

- Upstream clone present locally at `_emb_work/EMB` (shared team resource, sibling to all 5 member
  folders — not duplicated per-student).
- First integrated into this student's `experiment/` (specs extracted, committed) on **2026-06-13**
  (`git log --diff-filter=A --format=%ad --date=short -- experiment/specs/`).
