#!/usr/bin/env python3
"""
RBL-4 gate: results/summary.csv — 1 row per RQ (schema: rq,metric,value,p_value,effect_size,n,reject_h0).
Reads results/stats/summary.json (written by compute_metric.py / analyze.py) — zero hand-typed statistics;
every number is traceable to summary.json and, transitively, to results/raw/*.

Owner: MS (Nguyen Le Thuan, SE190305)
Usage: python scripts/write_summary_csv.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "results", "stats", "summary.json")
OUT = os.path.join(ROOT, "results", "summary.csv")


def main():
    with open(STATS, encoding="utf-8") as f:
        s = json.load(f)

    rq1 = s["RQ1_endpoint_coverage"]
    rq2 = s["RQ2_fault_detection"]
    rq3 = s["RQ3_edge_cases_llm_vs_manual"]

    rows = [
        {
            "rq": "RQ1",
            "metric": "llm_endpoint_coverage_pct",
            "value": rq1["coverage_overall_pct"],
            "p_value": rq1["p_value_one_sided"],
            "effect_size": rq1["rank_biserial"],
            "n": rq1["n_operations"],
            "reject_h0": rq1["reject_H0_(coverage>90%)"],
        },
        {
            # Primary RQ2 test per proposal §5.6 / §7 (External): pooled per-fault McNemar, N=133.
            "rq": "RQ2",
            "metric": "fault_recall_llm_vs_evomaster "
                      f"(llm={rq2['overall_recall']['llm']},"
                      f"manual={rq2['overall_recall']['manual']},"
                      f"evomaster={rq2['overall_recall']['evomaster']})",
            "value": rq2["overall_recall"]["llm"],
            "p_value": rq2["mcnemar"]["llm_vs_evomaster"]["p_value"],
            "effect_size": rq2["cliffs_delta"]["llm_vs_evomaster"],
            "n": rq2["n_mutants_total"],
            "reject_h0": rq2["mcnemar"]["llm_vs_evomaster"]["reject_H0"],
        },
        {
            "rq": "RQ3",
            "metric": "edge_cases_per_op_llm_vs_manual "
                      f"(median {rq3['llm_median_per_op']} vs {rq3['manual_median_per_op']};"
                      f" total {rq3['llm_total_edge']} vs {rq3['manual_total_edge']})",
            "value": rq3["llm_median_per_op"],
            "p_value": rq3["p_value_one_sided"],
            "effect_size": rq3["rank_biserial"],
            "n": rq3["n_operations"],
            "reject_h0": rq3["reject_H0_(llm>manual)"],
        },
    ]

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rq", "metric", "value", "p_value", "effect_size", "n", "reject_h0"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
