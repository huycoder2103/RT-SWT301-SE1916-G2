# Integrity audit — RBL-5 paper, 2026-07-21

An adversarial fact-check of every quantitative and comparative claim in `paper/sections/`
against `results/stats/summary.json`, `results/*.json`, `results/stats/master_summary.csv`,
the fault catalogs, and `notes.md`. Each finding below was **independently re-verified
against the source data** before the paper was changed.

These are not wording problems. Four of them changed what the paper claims.

---

## H1 — Wrong pilot figure (FIXED)

**Was:** "shift the LLM-versus-EvoMaster discordant count **from six** to 4".

`notes.md` §F8 records `b: 5→4`. The disclosed cause is the loss of exactly one LLM kill
(ncs m001, `bessj` at n=2), which can move `b` by at most 1. The sentence also contradicted
itself: exact McNemar with c=14 gives p=0.064 at b=5 ("just above" α=0.05, as the sentence
says) but p=0.115 at b=6.

**Now:** "Losing that one kill shifts the discordant count from **five** to 4."

## H2 — The error-behaviour denominator is arm-derived (FIXED: disclosed)

`scripts/error_profile.py:94` — `key = sorted(set().union(*arms.values()))`.

The 31-behaviour denominator is the **union of what the three arms observed**, not an
independently defined total. The LLM's set contains the other two (missed: llm 0, manual 9,
evomaster 13), so **31/31 is forced by construction**, not measured. The paper used it as
evidence that "the LLM wins where its oracle is adequate."

Compounding it: the code-derived error-surface baseline that the paper claims as its GAP-M
contribution reports **24** error points over 35 endpoints in
`results/error-surface-baseline.json`. The reported 31 does not come from that map.

**Now:** Method defines the key explicitly as a union and says what it can and cannot show;
Threats carries a new paragraph naming this "the clearest measurement gap in this paper";
Results and Discussion no longer read the score as error-surface coverage.

## H3 — "On every metric the field reports, the LLM leads both" (FIXED)

`results/stats/master_summary.csv`: `endpoint_coverage_pct` is **blank for all three
EvoMaster rows** — never computed. Edge-case scenarios are `n/a` for EvoMaster (no
`// SCENARIO` tags). So neither coverage nor scenario count ranks all three arms, and only
test-count and 5xx tallies actually do.

**Now:** the claim names the metrics that genuinely compare each pair, and Results states the
limitation outright, including that the EvoMaster comparison therefore rests on exactly the
kind of volume proxy this paper argues against.

**Still open for the team:** the manual arm's coverage *is* in the data and is not reported
(ncs 100.0, scs 100.0, features **88.9** → 33/35 = 94.3%). Reporting it needs a new macro in
`gen_paper_macros.py`; do not hand-type it.

## H4 — A pre-registered analysis was computed, unfavourable, and omitted (FIXED)

`summary.json` → `pairwise_wilcoxon_holm`: both comparisons `p_holm = 1.0`,
`reject_H0 = false`. The macros `\RQIIholmLEp` and `\RQIIholmLMp` existed in `numbers.tex`
and were **used nowhere**. Method pre-registers "post-hoc pairwise Wilcoxon with Holm
correction" and Threats claimed "we apply Holm correction ... and report", but Results jumped
from Friedman straight to McNemar.

The same pattern hid `\RQIImcnemarLMpower` = 0.530: power was reported for the EvoMaster leg
(0.557, "below conventional adequacy") and omitted for the manual leg the headline rests on.

**Now:** Results reports both Holm p-values, and Threats reports both power figures. Macro
usage rose 70 → 73, and the three added macros are exactly these suppressed statistics.

## H5 — "No statistic in this document is typed by hand" was false (FIXED)

Hand-typed integers in results sections: "(70 mutants)", "(59 mutants)", "(4 mutants)",
"the same 12 mutants", "the pilot's 1/70", and the "six" of H1. `check_paper.py`'s detector
was `(\d+\.\d+)` — **decimals only**, so bare integers were invisible to it. That is exactly
how H1 survived the gate.

**Now:** Method and the declarations section both say "every *computed* statistic", and note
that fixed integers (mutant counts, pilot figures) are literal.

---

## Moderate (all fixed)

- **M1** "a search-based tool released in 2019" ×3. EvoMaster **6.0.0** was used; 2019 is the
  year of the cited paper. Now "an established search-based tool".
- **M2** "EvoMaster's kills strictly dominate". `b=4` mutants are killed by the LLM alone, so
  it is not a set containment — unlike the manual comparison (`c=0`), which genuinely is.
  The two were coordinated in one sentence, inviting the wrong reading. Now stated separately.
- **M3** "kills half as many mutants" beside "2.2×" in the same parenthesis. 8/18 = 0.44.
  Now "fewer than half as many".

## Verified correct — no change needed

Stated explicitly so the team knows what *was* checked:

- Mutant counts: 70+59+4 = 133 ✓; every per-subject Recall reconstructs to exact integer
  kills (ncs 0/0/12, scs 7/1/5, features 1/1/1 → 8/2/18) matching `bug-detection.json`.
- Ratios: "more than twice" (2.25) ✓, "four times" (8/2) ✓, "3.4×" (295/87) ✓, "13.5%" ✓.
- Subset claims: b=6, c=0 → manual ⊂ LLM strictly; "plus six more" ✓.
- RQ3 recomputed end to end: totals 217/113 ✓, medians 5.0/3.0 ✓, pairs 33/2/0 ✓,
  rank-biserial (626−4)/630 = 0.9873 ✓.
- Every α / Bonferroni statement is consistent across abstract, results, threats, conclusion.
- All 23 `\ref` targets resolve. All literature figures consistent across sections.

## Left for the team

1. **Report the manual arm's coverage** (94.3%) via a new macro, or state why it is omitted.
2. **RQ1's Wilcoxon is degenerate** — all 35 per-operation coverage values are 1.0, so
   W=630 is the maximum possible and rank-biserial = 1.000 by construction. `p` is then a
   pure function of n=35. Threats calls this "survives both comfortably" without saying so.
   Consider adding one sentence.
3. **Data-side inconsistencies** (do not affect the paper's numbers, but they contradict it):
   - `results/produced-vs-detected.json` → `correct_phrasing_vi` carries stale pilot numbers
     (141 vs its own 113; "9/133" vs its own 8 and 2).
   - `results/bug-detection.json` cites "785 request" while its per-arm sums give 649.
   - `results/stats/master_summary.csv` labels EvoMaster a "SOTA **white-box** fuzzer" — it
     was run `--blackBox true`, and the paper's whole oracle argument depends on that.
   - The same CSV labels the manual arm "Baseline 1 — **Human**", the framing the paper
     deliberately avoids.
