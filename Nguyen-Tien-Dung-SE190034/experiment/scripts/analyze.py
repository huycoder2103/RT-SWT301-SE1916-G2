#!/usr/bin/env python3
"""
Statistical analysis for the Gap-3 experiment (RQ1 / RQ2 / RQ3), per experiment/hypotheses.md.
Consumes the raw CSVs in experiment/results/raw/ and writes tables + p-values to
experiment/results/stats/ (and prints a summary). Gracefully skips an RQ whose inputs are absent.

Inputs:
  coverage.csv   (parse_scenarios.py)  -> RQ1
  scenarios.csv  (parse_scenarios.py)  -> RQ3
  <sut>_kills.csv (run_mutation.py)    -> RQ2   (sut in ncs,scs,features)
"""
import json, os, glob
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
OUT = os.path.join(ROOT, "results", "stats")
ALPHA = 0.05
EDGE = {"negative", "boundary", "errorcode"}
os.makedirs(OUT, exist_ok=True)
summary = {}


def rq1_coverage():
    p = os.path.join(RAW, "coverage.csv")
    sc = os.path.join(RAW, "scenarios.csv")
    if not os.path.exists(p) or not os.path.exists(sc):
        return
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
    summary["RQ1_endpoint_coverage"] = res


def rq3_edge_cases():
    sc = os.path.join(RAW, "scenarios.csv")
    if not os.path.exists(sc):
        return
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
    # effect size: matched-pairs rank-biserial
    pos = sum(1 for d in nonzero if d > 0); neg = sum(1 for d in nonzero if d < 0)
    res["pairs_llm_more"], res["pairs_manual_more"], res["pairs_tie"] = pos, neg, len(diffs) - len(nonzero)
    paired.to_csv(os.path.join(OUT, "rq3_edge_per_op.csv"), index=False)
    summary["RQ3_edge_cases_llm_vs_manual"] = res


def rq2_fault_detection():
    files = sorted(glob.glob(os.path.join(RAW, "*_kills.csv")))
    if not files:
        return
    df = pd.concat([pd.read_csv(f).assign(sut=os.path.basename(f).split("_")[0]) for f in files],
                   ignore_index=True)
    # per-SUT recall per arm (Friedman blocks)
    recall = (df.groupby(["sut", "arm"])["killed"].mean().unstack("arm"))
    arms = [a for a in ["llm", "manual", "evomaster"] if a in recall.columns]
    res = {"per_sut_recall": {s: {a: round(float(recall.loc[s, a]), 4) for a in arms}
                              for s in recall.index},
           "overall_recall": {a: round(float(df[df.arm == a]["killed"].mean()), 4) for a in arms},
           "n_mutants_total": int(df[df.arm == arms[0]].shape[0])}
    # Friedman across SUTs (3 blocks x len(arms) treatments)
    if len(arms) >= 3 and recall.shape[0] >= 2:
        try:
            chi, p = stats.friedmanchisquare(*[recall[a].tolist() for a in arms])
            res["friedman_chi2"], res["friedman_p"] = float(chi), float(p)
        except Exception as e:
            res["friedman_note"] = str(e)
    # per-mutant paired McNemar (pooled): llm vs each comparator
    wide = df.pivot_table(index=["sut", "mutant_id"], columns="arm", values="killed")
    res["mcnemar"] = {}
    try:
        from statsmodels.stats.contingency_tables import mcnemar
        for comp in [a for a in ("manual", "evomaster") if a in wide.columns and "llm" in wide.columns]:
            both = wide[["llm", comp]].dropna()
            b = int(((both["llm"] == 1) & (both[comp] == 0)).sum())  # llm kills, comp misses
            c = int(((both["llm"] == 0) & (both[comp] == 1)).sum())  # comp kills, llm misses
            tbl = [[int(((both.llm == 1) & (both[comp] == 1)).sum()), b],
                   [c, int(((both.llm == 0) & (both[comp] == 0)).sum())]]
            m = mcnemar(tbl, exact=True)
            res["mcnemar"][f"llm_vs_{comp}"] = {"llm_only(b)": b, f"{comp}_only(c)": c,
                                                "statistic": float(m.statistic), "p_value": float(m.pvalue),
                                                "reject_H0": bool(m.pvalue < ALPHA)}
    except Exception as e:
        res["mcnemar_note"] = str(e)
    recall.to_csv(os.path.join(OUT, "rq2_recall_per_sut.csv"))
    summary["RQ2_fault_detection"] = res


def main():
    rq1_coverage()
    rq3_edge_cases()
    rq2_fault_detection()
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
