# Experiment Report — Can LLMs generate REST-API tests as effectively as Manual design and EvoMaster, on pre-seeded faults?

**Member:** Nguyen Tien Dung — SE190034 · **Course:** SWT301 / SE1916 (LLM × REST API testing)
**Artifacts:** [`protocol.md`](protocol.md) (pre-registered method) · [`README.md`](README.md) (reproduce) ·
all suites/scripts/raw results committed under `experiment/`.

---

## 1. Research Profile

- **Problem.** A 13-paper SLR (`SLR/`) showed that 2019–2026 work applies LLMs to REST-API test
  generation and reports coverage + 500-error *counts*, but (GAP-1) never compares **LLM vs manual vs
  EvoMaster** on the same APIs, (GAP-2) never uses a **shared pre-seeded-fault** dataset so
  fault-detection **Recall** is never computed, and **(GAP-3, our focus)** provides **no edge-case /
  error-code metric per endpoint** and **no endpoint-type miss analysis**.
- **Goal.** On locally deployed EMB APIs instrumented with pre-seeded faults of known ground truth,
  measure on one common footing the three arms' effectiveness, answering RQ1–RQ3.

## 2. Research Track (traceability)

`SLR/evidence-table.md` (N=13) → `SLR/gap-statement.md` (GAP-1/2/3) → `experiment/01_rq.md` (RQ1–RQ3,
PICO) → `experiment/hypotheses.md` (H0/H1, tests, α=0.05) → **this experiment**. Every design choice
(3 EMB SUTs; GPT→**Claude** LLM with the SLR's #5 finding that Claude 3.5 Sonnet is the strongest LLM
as justification; EvoMaster as the most-reused baseline; pre-seeded faults for Recall) is traceable to
that chain.

## 3. Experiment Proposal (method, condensed from `protocol.md`)

- **SUTs (EMB, JDK 8):** `rest-ncs` (6 ops, numeric/boundary), `rest-scs` (11 ops, string/boundary),
  `features-service` (18 ops, CRUD + constraints; cited in EvoMaster #10 & DeepREST #13). 35 operations.
- **Arms (uniform black-box REST-assured harness):**
  **I = LLM** (Claude Sonnet 4.6, blind, frozen prompt) · **C1 = Manual** (blind EP/BVA) ·
  **C2 = EvoMaster 6.0.0** black-box. All produced *before* faults were seeded (blind protocol).
- **Faults (ground truth):** standard mutation operators (relational/arithmetic/negate-boundary,
  the PIT/Offutt families) seeded **systematically** into the controller layer, each recompiled into a
  standalone mutant SUT; only compilable mutants kept; catalog = `faults/<sut>/catalog.json`.
- **Kill rule:** an arm kills a mutant iff a test that **passes on the original** SUT **fails on the
  mutant**. **Recall = killed / total.**
- **Metrics:** RQ1 endpoint coverage (% ops exercised) vs the 90% target + endpoint-type miss; RQ2
  mutation-kill recall per arm; RQ3 edge-case scenarios (negative+boundary+errorcode) per endpoint.
- **Statistics (α=0.05):** RQ1 one-sample Wilcoxon vs 0.90; RQ2 Friedman + per-mutant McNemar (pooled);
  RQ3 paired Wilcoxon (LLM vs Manual per endpoint).

## 4. Results

### Suite sizes (tests generated, executed on the real SUTs)

| SUT | LLM | Manual | EvoMaster |
|-----|----:|-------:|----------:|
| ncs | 86 | 60 | 30 |
| scs | 109 | 82 | 27 |
| features | 100 | 55 | 30 |

### RQ1 — Endpoint coverage of LLM tests (vs ≥90% target)

The LLM suite exercises **35/35 operations = 100%** endpoint coverage (ncs 6/6, scs 11/11,
features 18/18). One-sample Wilcoxon of per-operation coverage vs 0.90: **W=630, p = 1.6×10⁻⁹ < 0.05 →
reject H0**; LLM endpoint coverage significantly exceeds the 90% target.
**Endpoint-type miss analysis:** with operation-level coverage saturated at 100%, *no* endpoint type
(numeric-validation / string-validation / CRUD / constraint) is missed at the routing level — the gap
is not *which endpoints are reached* but *what is asserted* once reached (see RQ2/RQ3). Figure:
`results/figures/rq1_coverage.png`.

### RQ2 — Fault-detection recall: LLM vs Manual vs EvoMaster

Pre-seeded mutants (ground truth): ncs = 8 · scs = `<N_scs>` · features = `<N_feat>` (catalogs in
`faults/*/catalog.json`).

| SUT | LLM recall | Manual recall | EvoMaster recall |
|-----|-----------:|--------------:|-----------------:|
| ncs | `<>` | `<>` | `<>` |
| scs | `<>` | `<>` | `<>` |
| features | `<>` | `<>` | `<>` |
| **overall** | `<>` | `<>` | `<>` |

Friedman (3 arms × 3 SUTs): χ²=`<>`, p=`<>`. Per-mutant McNemar (pooled): LLM vs Manual p=`<>`;
LLM vs EvoMaster p=`<>`. *[Filled from `results/stats/summary.json` after `run_mutation.py` completes
for all SUTs. Interpretation written to the data, not assumed.]* Figure: `results/figures/rq2_recall.png`.

### RQ3 — Edge-case / error-code scenarios per endpoint: LLM vs Manual

The LLM suite produces **217** edge-case scenarios (negative+boundary+errorcode) vs Manual **141**
across the 35 endpoints; median **5 vs 4** per endpoint. Paired Wilcoxon (LLM−Manual per endpoint):
**W=493, p = 6.2×10⁻⁷ < 0.05 → reject H0**; on **30/35** endpoints the LLM produced strictly more
edge-case scenarios, 1 fewer, 4 tied. → The LLM is significantly more prolific at error-code/boundary
scenario generation than the manual EP/BVA methodology. Figure: `results/figures/rq3_edgecases.png`.

## 5. Threats to validity

- **Construct:** LLM and Manual arms are both Claude-authored (different role/methodology, both blind);
  a human-tester cohort would strengthen "LLM vs human" — future work. RQ2 (the headline) does not
  depend on Manual being human. EvoMaster uses recorded-value regression oracles vs the spec-derived
  status oracles of LLM/Manual — disclosed difference (`evomaster/README.md`).
- **External:** 3 small EMB APIs; n=3 limits Friedman power → per-mutant McNemar (pooled) is the
  primary RQ2 test. user-management (MySQL) was excluded → auth endpoints under-represented.
- **Internal:** mutation seeded in the controller layer (observable faults); LLM non-determinism
  (raw outputs frozen).
- **Conclusion:** small samples → non-parametric tests + effect sizes reported, not p-values alone.

## 6. Conclusion

*[Written to the RQ2 result after measurement. RQ1: LLM reaches 100% endpoint coverage (> 90% target,
p<0.001). RQ3: LLM generates significantly more edge-case scenarios than manual design (p<0.001). RQ2
conclusion + the overall verdict on "can LLMs match/beat manual and EvoMaster on ground-truth fault
detection" filled from the data.]*
