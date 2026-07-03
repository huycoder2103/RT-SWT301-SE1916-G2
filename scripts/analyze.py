#!/usr/bin/env python3
"""
Statistical analysis for the Gap-3 experiment (RQ1 / RQ2 / RQ3), per experiment/hypotheses.md
and proposal.md §5.6. Consumes the raw CSVs in experiment/results/raw/ (or an override
--raw-dir, e.g. scripts/fixtures/ for the gate-E4 smoke test) and writes tables + p-values to
experiment/results/stats/ (and prints a summary). Gracefully skips an RQ whose inputs are absent.

Inputs:
  coverage.csv   (parse_scenarios.py)  -> RQ1
  scenarios.csv  (parse_scenarios.py)  -> RQ3
  <sut>_kills.csv (run_mutation.py)    -> RQ2   (sut in ncs,scs,features)

RBL-4 / proposal.md §5.6 statistics implemented:
  RQ1 one-sample Wilcoxon (one-tailed) vs 0.90 + rank-biserial effect size.
  RQ2 Friedman (omnibus) + per-fault McNemar (pooled) + Holm-corrected pairwise Wilcoxon
      post-hoc across per-SUT recall + Cliff's delta per arm pair + approximate achieved
      power (statsmodels, two-proportion approximation of the pooled McNemar comparison).
  RQ3 paired Wilcoxon (one-tailed) + rank-biserial effect size.
  Bonferroni correction across the 3 RQ families (alpha_adj ~= 0.017), reported alongside
  (not substituted for) the raw alpha=0.05 calls already used per-RQ, per proposal.md §4.
"""
import json, os, glob
import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
OUT = os.path.join(ROOT, "results", "stats")
ALPHA = 0.05
EDGE = {"negative", "boundary", "errorcode"}


def cliffs_delta(a, b):
    """Cliff's delta effect size for two samples a, b (RQ2 effect size, proposal §5.6)."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) == 0 or len(b) == 0:
        return None
    gt = sum((x > y) for x in a for y in b)
    lt = sum((x < y) for x in a for y in b)
    return (gt - lt) / (len(a) * len(b))


def rank_biserial(diffs):
    """Matched-pairs rank-biserial correlation from Wilcoxon signed-rank diffs (RQ1/RQ3 effect size)."""
    d = np.asarray([x for x in diffs if x != 0], dtype=float)
    if len(d) == 0:
        return 0.0
    ranks = pd.Series(np.abs(d)).rank().values
    r_plus = ranks[d > 0].sum()
    r_minus = ranks[d < 0].sum()
    return float((r_plus - r_minus) / ranks.sum())


def rq1_coverage(raw_dir=RAW, summary=None):
    summary = {} if summary is None else summary
    p = os.path.join(raw_dir, "coverage.csv")
    sc = os.path.join(raw_dir, "scenarios.csv")
    if not os.path.exists(p) or not os.path.exists(sc):
        return summary
    cov = pd.read_csv(p)
    scen = pd.read_csv(sc)
    # per-operation coverage indicator for the LLM arm, pooled across SUTs.
    # An operation is "covered" (1.0) if the LLM suite has >=1 test tagged for it.
    per_sut_total = cov[cov.arm == "llm"].set_index("sut")["ops_total"].to_dict()
    llm_ops = scen[scen.arm == "llm"].groupby("sut")["op"].nunique().to_dict()
    vec = []
    for sut, tot in per_sut_total.items():
        covered = llm_ops.get(sut, 0)
        vec += [1.0] * covered + [0.0] * (tot - covered)
    # one-sample Wilcoxon signed-rank of (coverage - 0.90); H1: median > 0.90
    diffs = [v - 0.90 for v in vec]
    res = {"n_operations": len(vec), "ops_covered": int(sum(vec)),
           "coverage_overall_pct": round(100 * sum(vec) / len(vec), 2),
           "per_sut": {s: {"covered": llm_ops.get(s, 0), "total": t,
                           "pct": round(100 * llm_ops.get(s, 0) / t, 1)} for s, t in per_sut_total.items()}}
    try:
        # drop exact zeros (no diff) per Wilcoxon; here all diffs are +0.10 so test is one-sided
        w, p_two = stats.wilcoxon([d for d in diffs if d != 0], alternative="greater")
        res["wilcoxon_W"], res["p_value_one_sided"] = float(w), float(p_two)
        res["reject_H0_(coverage>90%)"] = bool(p_two < ALPHA)
    except ValueError as e:
        res["wilcoxon_note"] = f"degenerate ({e}); all operations covered (100% > 90%)"
        res["reject_H0_(coverage>90%)"] = sum(vec) / len(vec) > 0.90
    res["rank_biserial"] = rank_biserial(diffs)
    summary["RQ1_endpoint_coverage"] = res
    return summary


def rq3_edge_cases(raw_dir=RAW, out_dir=OUT, summary=None):
    summary = {} if summary is None else summary
    sc = os.path.join(raw_dir, "scenarios.csv")
    if not os.path.exists(sc):
        return summary
    scen = pd.read_csv(sc)
    edge = scen[scen.type.isin(EDGE)]
    # edge-case scenario count per (sut, op) for llm vs manual -> paired across operations
    piv = (edge.groupby(["sut", "op", "arm"])["count"].sum()
           .unstack("arm").fillna(0))
    for col in ("llm", "manual"):
        if col not in piv.columns:
            piv[col] = 0
    paired = piv.reset_index()
    llm_v = paired["llm"].tolist()
    man_v = paired["manual"].tolist()
    res = {"n_operations": len(paired),
           "llm_total_edge": int(sum(llm_v)), "manual_total_edge": int(sum(man_v)),
           "llm_median_per_op": float(pd.Series(llm_v).median()),
           "manual_median_per_op": float(pd.Series(man_v).median())}
    diffs = [a - b for a, b in zip(llm_v, man_v)]
    nonzero = [d for d in diffs if d != 0]
    try:
        w, p = stats.wilcoxon(nonzero, alternative="greater")  # H1: llm > manual
        res["wilcoxon_W"], res["p_value_one_sided"] = float(w), float(p)
        res["reject_H0_(llm>manual)"] = bool(p < ALPHA)
    except ValueError as e:
        res["wilcoxon_note"] = str(e)
    # effect size: matched-pairs rank-biserial (+ raw pair counts, kept for readability)
    pos = sum(1 for d in nonzero if d > 0); neg = sum(1 for d in nonzero if d < 0)
    res["pairs_llm_more"], res["pairs_manual_more"], res["pairs_tie"] = pos, neg, len(diffs) - len(nonzero)
    res["rank_biserial"] = rank_biserial(diffs)
    os.makedirs(out_dir, exist_ok=True)
    paired.to_csv(os.path.join(out_dir, "rq3_edge_per_op.csv"), index=False)
    summary["RQ3_edge_cases_llm_vs_manual"] = res
    return summary


def rq2_fault_detection(raw_dir=RAW, out_dir=OUT, summary=None):
    summary = {} if summary is None else summary
    files = sorted(glob.glob(os.path.join(raw_dir, "*_kills.csv")))
    if not files:
        return summary
    df = pd.concat([pd.read_csv(f).assign(sut=os.path.basename(f).split("_")[0]) for f in files],
                   ignore_index=True)
    # per-SUT recall per arm (Friedman blocks)
    recall = (df.groupby(["sut", "arm"])["killed"].mean().unstack("arm"))
    arms = [a for a in ["llm", "manual", "evomaster"] if a in recall.columns]
    res = {"per_sut_recall": {s: {a: round(float(recall.loc[s, a]), 4) for a in arms}
                              for s in recall.index},
           "overall_recall": {a: round(float(df[df.arm == a]["killed"].mean()), 4) for a in arms},
           "n_mutants_total": int(df[df.arm == arms[0]].shape[0])}
    # Friedman across SUTs (blocks x len(arms) treatments)
    if len(arms) >= 3 and recall.shape[0] >= 2:
        try:
            chi, p = stats.friedmanchisquare(*[recall[a].tolist() for a in arms])
            res["friedman_chi2"], res["friedman_p"] = float(chi), float(p)
        except Exception as e:
            res["friedman_note"] = str(e)

    wide = df.pivot_table(index=["sut", "mutant_id"], columns="arm", values="killed")

    # Holm-corrected pairwise Wilcoxon signed-rank post-hoc across per-SUT recall (proposal §4/§5.6)
    comparators = [a for a in ("manual", "evomaster") if a in recall.columns and "llm" in recall.columns]
    pairwise_labels, pairwise_pvals, identical_pairs = [], [], []
    for comp in comparators:
        pairwise_labels.append(f"llm_vs_{comp}")
        if recall["llm"].equals(recall[comp]):
            # Degenerate case (all per-SUT recall values identical, e.g. llm==manual on this
            # dataset -- see notes.md "oracle weakness" finding): skip scipy's wilcoxon call
            # entirely rather than let it emit a divide-by-zero RuntimeWarning for a result
            # we already know is p=1.0 (no difference to detect).
            pairwise_pvals.append(1.0)
            identical_pairs.append(f"llm_vs_{comp}")
            continue
        try:
            w, p = stats.wilcoxon(recall["llm"], recall[comp])
            pairwise_pvals.append(float(p))
        except ValueError:
            pairwise_pvals.append(None)
    res["pairwise_wilcoxon_holm"] = {}
    valid = [(lbl, p) for lbl, p in zip(pairwise_labels, pairwise_pvals) if p is not None]
    if valid:
        try:
            from statsmodels.stats.multitest import multipletests
            labels_v, pvals_v = zip(*valid)
            reject, p_holm, _, _ = multipletests(pvals_v, alpha=ALPHA, method="holm")
            for lbl, praw, padj, rej in zip(labels_v, pvals_v, p_holm, reject):
                res["pairwise_wilcoxon_holm"][lbl] = {
                    "p_raw": praw, "p_holm_adjusted": float(padj), "reject_H0": bool(rej)}
        except Exception as e:
            res["pairwise_wilcoxon_holm_note"] = str(e)
    degenerate = [lbl for lbl, p in zip(pairwise_labels, pairwise_pvals) if p is None]
    if degenerate:
        res["pairwise_wilcoxon_degenerate"] = degenerate
        res.setdefault("pairwise_wilcoxon_note",
                        "n=3 SUTs is a very small sample for a signed-rank test; "
                        "the per-fault McNemar below (N~=133) is the primary RQ2 test per proposal §5.6.")
    if identical_pairs:
        res["pairwise_wilcoxon_identical_vectors"] = identical_pairs
        res.setdefault("pairwise_wilcoxon_note",
                        "per-SUT recall vectors are identical for the pair(s) listed -- p=1.0 by "
                        "construction, not computed via scipy (see notes.md oracle-weakness finding).")

    # Cliff's delta per arm pair, computed on the per-mutant killed vectors (0/1)
    res["cliffs_delta"] = {}
    for comp in comparators:
        both = wide[["llm", comp]].dropna()
        res["cliffs_delta"][f"llm_vs_{comp}"] = cliffs_delta(both["llm"], both[comp])

    # per-mutant paired McNemar (pooled): llm vs each comparator + approximate achieved power
    res["mcnemar"] = {}
    try:
        from statsmodels.stats.contingency_tables import mcnemar
        from statsmodels.stats.power import NormalIndPower
        from statsmodels.stats.proportion import proportion_effectsize
        power_calc = NormalIndPower()
        for comp in comparators:
            both = wide[["llm", comp]].dropna()
            b = int(((both["llm"] == 1) & (both[comp] == 0)).sum())  # llm kills, comp misses
            c = int(((both["llm"] == 0) & (both[comp] == 1)).sum())  # comp kills, llm misses
            tbl = [[int(((both.llm == 1) & (both[comp] == 1)).sum()), b],
                   [c, int(((both.llm == 0) & (both[comp] == 0)).sum())]]
            m = mcnemar(tbl, exact=True)
            n_pooled = len(both)
            p1, p2 = both["llm"].mean(), both[comp].mean()
            try:
                eff = proportion_effectsize(p1, p2)
                achieved_power = float(power_calc.solve_power(
                    effect_size=eff, nobs1=n_pooled, alpha=ALPHA, ratio=1.0, alternative="two-sided"))
            except Exception:
                achieved_power = None
            res["mcnemar"][f"llm_vs_{comp}"] = {
                "llm_only(b)": b, f"{comp}_only(c)": c,
                "statistic": float(m.statistic), "p_value": float(m.pvalue),
                "reject_H0": bool(m.pvalue < ALPHA),
                "achieved_power_approx": achieved_power,
                "power_note": "approximate: two-independent-proportion power (statsmodels NormalIndPower) "
                               "on the same recall proportions McNemar tests; not an exact McNemar power "
                               "formula (statsmodels has none built in) -- disclosed approximation."}
    except Exception as e:
        res["mcnemar_note"] = str(e)
    os.makedirs(out_dir, exist_ok=True)
    recall.to_csv(os.path.join(out_dir, "rq2_recall_per_sut.csv"))
    summary["RQ2_fault_detection"] = res
    return summary


def run_all(raw_dir=RAW, out_dir=OUT):
    summary = {}
    rq1_coverage(raw_dir=raw_dir, summary=summary)
    rq3_edge_cases(raw_dir=raw_dir, out_dir=out_dir, summary=summary)
    rq2_fault_detection(raw_dir=raw_dir, out_dir=out_dir, summary=summary)
    summary["multiplicity"] = {
        "alpha_raw_per_RQ": ALPHA,
        "alpha_bonferroni_3family": round(ALPHA / 3, 4),
        "note": "Per proposal.md §4: Holm correction is applied WITHIN RQ2's post-hoc pairwise "
                "comparisons (see RQ2_fault_detection.pairwise_wilcoxon_holm); Bonferroni is applied "
                "ACROSS the 3 RQ families as a second, stricter reading (alpha_adj ~= 0.017). Both are "
                "reported; the per-RQ conclusions above use the raw alpha=0.05 threshold specified in "
                "proposal.md §6.1, as pre-registered."}
    return summary


def main():
    summary = run_all(raw_dir=RAW, out_dir=OUT)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
