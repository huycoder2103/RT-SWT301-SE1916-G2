#!/usr/bin/env python3
r"""
Generates paper/generated/numbers.tex -- every statistic the paper cites, as a LaTeX macro.

Rationale (RBL-4 gate: "no hand-typed statistics"): the paper never contains a literal
number for any result. It says \RQIcoveragePct; this script binds that macro to the value
in results/stats/summary.json, which analyze.py derives from results/raw/*. Re-run the
experiment -> re-run analyze.py -> re-run this -> the paper's numbers move by themselves.
A stale paper is therefore impossible by construction.

Owner: MS (Nguyen Le Thuan, SE190305)
Usage: python scripts/gen_paper_macros.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "results", "stats", "summary.json")
PVD = os.path.join(ROOT, "results", "produced-vs-detected.json")
OUT_DIR = os.path.join(ROOT, "paper", "generated")
OUT = os.path.join(OUT_DIR, "numbers.tex")


def pval(p):
    """LaTeX-safe p-value. Small p -> scientific notation; else 3 decimals."""
    if p < 1e-4:
        mant, exp = f"{p:.2e}".split("e")
        return rf"{mant}\times10^{{{int(exp)}}}"
    return f"{p:.3f}"


def num(x, nd=3):
    return f"{x:.{nd}f}"


def main():
    with open(STATS, encoding="utf-8") as f:
        s = json.load(f)

    rq1 = s["RQ1_endpoint_coverage"]
    rq2 = s["RQ2_fault_detection"]
    rq3 = s["RQ3_edge_cases_llm_vs_manual"]
    mult = s["multiplicity"]

    m = {}

    # ---- RQ1: endpoint coverage -------------------------------------------
    m["RQIcoveragePct"] = num(rq1["coverage_overall_pct"], 1)
    m["RQIopsCovered"] = str(rq1["ops_covered"])
    m["RQIopsTotal"] = str(rq1["n_operations"])
    m["RQIn"] = str(rq1["n_operations"])
    m["RQIwilcoxonW"] = num(rq1["wilcoxon_W"], 1)
    m["RQIpvalue"] = pval(rq1["p_value_one_sided"])
    m["RQIrankBiserial"] = num(rq1["rank_biserial"], 3)
    m["RQIreject"] = "rejected" if rq1["reject_H0_(coverage>90%)"] else "not rejected"
    for sut, k in [("features", "Features"), ("ncs", "Ncs"), ("scs", "Scs")]:
        d = rq1["per_sut"][sut]
        m[f"RQI{k}Covered"] = str(d["covered"])
        m[f"RQI{k}Total"] = str(d["total"])
        m[f"RQI{k}Pct"] = num(d["pct"], 1)

    # ---- RQ2: fault detection ---------------------------------------------
    for arm, k in [("llm", "Llm"), ("manual", "Manual"), ("evomaster", "Evo")]:
        m[f"RQIIrecall{k}"] = num(rq2["overall_recall"][arm], 4)
        m[f"RQIIrecall{k}Pct"] = num(rq2["overall_recall"][arm] * 100, 1)
    m["RQIIn"] = str(rq2["n_mutants_total"])
    m["RQIIfriedmanChi"] = num(rq2["friedman_chi2"], 3)
    m["RQIIfriedmanP"] = num(rq2["friedman_p"], 3)

    mc_le = rq2["mcnemar"]["llm_vs_evomaster"]
    m["RQIImcnemarLEb"] = str(mc_le["llm_only(b)"])
    m["RQIImcnemarLEc"] = str(mc_le["evomaster_only(c)"])
    m["RQIImcnemarLEstat"] = num(mc_le["statistic"], 1)
    m["RQIImcnemarLEp"] = pval(mc_le["p_value"])
    m["RQIImcnemarLEreject"] = "rejected" if mc_le["reject_H0"] else "not rejected"
    m["RQIImcnemarLEpower"] = num(mc_le["achieved_power_approx"], 3)

    mc_lm = rq2["mcnemar"]["llm_vs_manual"]
    m["RQIImcnemarLMb"] = str(mc_lm["llm_only(b)"])
    m["RQIImcnemarLMc"] = str(mc_lm["manual_only(c)"])
    m["RQIImcnemarLMstat"] = num(mc_lm["statistic"], 1)
    m["RQIImcnemarLMp"] = pval(mc_lm["p_value"])
    m["RQIImcnemarLMreject"] = "rejected" if mc_lm["reject_H0"] else "not rejected"
    m["RQIImcnemarLMpower"] = num(mc_lm["achieved_power_approx"], 3)

    m["RQIIcliffLM"] = num(rq2["cliffs_delta"]["llm_vs_manual"], 3)
    m["RQIIcliffLE"] = num(rq2["cliffs_delta"]["llm_vs_evomaster"], 3)
    m["RQIIholmLMp"] = num(rq2["pairwise_wilcoxon_holm"]["llm_vs_manual"]["p_holm_adjusted"], 3)
    m["RQIIholmLEp"] = num(rq2["pairwise_wilcoxon_holm"]["llm_vs_evomaster"]["p_holm_adjusted"], 3)

    for sut, k in [("features", "Features"), ("ncs", "Ncs"), ("scs", "Scs")]:
        for arm, ak in [("llm", "Llm"), ("manual", "Manual"), ("evomaster", "Evo")]:
            m[f"RQII{k}{ak}"] = num(rq2["per_sut_recall"][sut][arm], 4)

    # ---- RQ3: edge-case scenarios -----------------------------------------
    m["RQIIItotalLlm"] = str(rq3["llm_total_edge"])
    m["RQIIItotalManual"] = str(rq3["manual_total_edge"])
    m["RQIIImedianLlm"] = num(rq3["llm_median_per_op"], 1)
    m["RQIIImedianManual"] = num(rq3["manual_median_per_op"], 1)
    m["RQIIIn"] = str(rq3["n_operations"])
    m["RQIIIwilcoxonW"] = num(rq3["wilcoxon_W"], 1)
    m["RQIIIpvalue"] = pval(rq3["p_value_one_sided"])
    m["RQIIIrankBiserial"] = num(rq3["rank_biserial"], 3)
    m["RQIIIpairsLlm"] = str(rq3["pairs_llm_more"])
    m["RQIIIpairsManual"] = str(rq3["pairs_manual_more"])
    m["RQIIIpairsTie"] = str(rq3["pairs_tie"])
    m["RQIIIreject"] = "rejected" if rq3["reject_H0_(llm>manual)"] else "not rejected"

    # ---- multiplicity ------------------------------------------------------
    m["alphaRaw"] = num(mult["alpha_raw_per_RQ"], 2)
    m["alphaBonf"] = num(mult["alpha_bonferroni_3family"], 4)

    # ---- produced vs detected (anti-conflation, proposal 5.4) --------------
    with open(PVD, encoding="utf-8") as f:
        pvd = json.load(f)
    prod, det = pvd["produced"], pvd["detected"]
    for arm, k in [("llm", "Llm"), ("manual", "Manual"), ("evomaster", "Evo")]:
        m[f"PDtests{k}"] = str(prod["test_cases"][arm])
        m[f"PDkilled{k}"] = str(det["mutation_faults_killed"][arm])
        m[f"PDerrTriggered{k}"] = str(det["http_error_behaviours_triggered"][arm])
        m[f"PDcrash{k}"] = str(det["server_crash_5xx_responses"][arm])
    m["PDkilledTotal"] = str(det["mutation_faults_killed"]["total"])
    m["PDerrKey"] = str(det["http_error_behaviours_triggered"]["answer_key"])
    # Derived: how much more test volume the LLM wrote than EvoMaster, and how much
    # less it detected. Computed here so the paper never hard-codes the ratio.
    m["PDvolumeRatioLlmEvo"] = num(
        prod["test_cases"]["llm"] / prod["test_cases"]["evomaster"], 1)
    m["PDkillRatioEvoLlm"] = num(
        det["mutation_faults_killed"]["evomaster"] / det["mutation_faults_killed"]["llm"], 1)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("% AUTO-GENERATED by scripts/gen_paper_macros.py -- DO NOT EDIT BY HAND.\n")
        f.write("% Source of truth: results/stats/summary.json <- analyze.py <- results/raw/*\n")
        f.write("% Regenerate: python scripts/gen_paper_macros.py\n\n")
        for k in sorted(m):
            f.write(rf"\newcommand{{\{k}}}{{{m[k]}}}" + "\n")

    print(f"wrote {OUT} ({len(m)} macros)")
    print("every number the paper prints is now bound to results/stats/summary.json")


if __name__ == "__main__":
    main()
