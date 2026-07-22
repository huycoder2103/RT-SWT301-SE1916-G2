# AI-writing audit — RBL-5 paper

**Run:** 2026-07-21 · **Trigger:** external AI-detection check flagged the manuscript
**Scope:** prose only. No result, statistic, table value or claim was altered.

---

## 1. What was actually wrong

The research is not in question. The mutants, runs, kill matrices and the honest
threats-to-validity section are genuine, and `notes.md` §F records the failures
(F1, F7, F8) that a fabricated study would have hidden. The problem was confined to
**writing style**.

Measured markers, before vs after the rewrite (script:
`scratchpad/ai_tics.py`, sections 00–07):

| Marker | Before | After | Note |
|---|---:|---:|---|
Measured with `scripts/ai_style_check.py` (run it yourself; `--verbose` lists every hit):

| Marker | Before | After | Note |
|---|---:|---:|---|
| Em-dashes (`---`) | **60** | **0** | was 1 per 98 words; human academic norm is 1 per 500–1000 |
| Flagged passages, total | **26** | **10** | antithesis frames, meta-commentary, showy diction |
| "rather than" | 32* | 12 | *peaked at 32 during the first pass — see §2b |
| "not X, it is Y" frames | 1 | 0 | |
| Showy diction (`tautology`, `paradox`, `cleverer`, `crowned`, …) | 16 | 2 | |
| Rule-of-three scaffolds (`Three observations…First/Second/Third`) | 2 | 0 | |
| Verbatim self-repetition across sections | 2 | 0 | |
| Words | 5882 | 5763 | trimmed to fit the 15-page LNCS limit |
| Sentence-length stdev | 13.2 | 9.9 | **not a defect — see §2** |

## 2. A metric we were wrong to worry about

An earlier version of this log treated falling sentence-length variance (13.2 → 9.8) as a
regression. An independent audit corrected that: at CV 0.54, with 16% of sentences under
10 words and 14% over 30, the within-file distribution sits **inside** normal human
academic range. It was not the problem.

The real statistical tell is **cross-file uniformity of the mean**. All nine section files
land between 17.7 and 22.6 words per sentence, a 4.9-word band. Sections genuinely written
by different people at different times drift much further apart than that. No editing pass
fixes this, because it is a signature of single authorship, not of bad writing. Five people
each revising their own sections is what changes it.

## 2b. What the first pass got wrong

Removing the "not X, it is Y" frame by swapping the connective produced a **new** tic:
"rather than" went to 32 occurrences (now 12). Worse, swapping the connective left the
underlying construction intact — the same proposition ("it is the oracle, not the
generator") was asserted six times in the same syntactic mould across six sections. That
needed rewriting, not substitution. Fixed in the second pass.

## 3. What this audit does NOT claim

- It does **not** claim the manuscript will now pass any particular AI detector.
  No editing pass can guarantee that, and detectors disagree with each other.
- It does **not** make the prose author-original. An LLM assistant drafted and edited it.
  That is why `sections/08_declarations.tex` discloses the use explicitly, per Springer
  policy, and why LLMs are not listed as authors.

## 4. Required follow-up by the team

0. **Read `integrity_audit_2026-07-21.md` first.** A separate adversarial fact-check found
   five substantive problems, including a pre-registered analysis that had been computed,
   came out unfavourable, and was omitted. Those matter more than anything in this file.
1. **Each author reads their sections aloud and revises in their own voice.** This is the
   only step that actually changes authorship, and per §2 it is also the only thing that
   moves the cross-file uniformity signal. The rewrite gives you clean scaffolding, not a
   finished submission.
2. **Verify `sections/08_declarations.tex` sentence by sentence.** It states, on your
   behalf, how AI was used. An inaccurate disclosure is worse than no disclosure.
3. Confirm the author e-mail addresses in `main.tex` (currently constructed from the
   student IDs and unverified).

## 5. Integrity checks re-run after the rewrite

| Check | Result |
|---|---|
| `scripts/check_paper.py` | ✅ PASS — 0 undefined macros, 0 hand-typed statistics |
| Generated-statistic macros used, before vs after | ✅ **70 → 73**, none dropped; the 3 added are statistics that had been computed but never reported (see `integrity_audit_2026-07-21.md` H4) |
| LaTeX brace balance / `begin`–`end` pairing | ✅ OK |
| Table column counts vs column spec | ✅ 3 tables, all rows match |
| `pdflatex` + `bibtex` compile | ✅ clean — 0 errors, 0 undefined refs/citations |
| Overfull hboxes > 5pt | ✅ **0** (was 9 on the first LNCS build, worst 73pt) |

**Page budget** (`main.pdf`, 18 pages total):

| Part | Pages | Counts toward the 12–15 limit? |
|---|---|---|
| Introduction → Conclusion | **1–15** | ✅ yes — exactly 15, at the ceiling |
| Declarations (AI use / data / interests) | 16 | no — acknowledgements-class |
| References | 17–18 | no |

The body sits exactly on the 15-page ceiling. If more room is ever needed, the least
load-bearing text is Discussion §3 and the Related Work pattern list.
