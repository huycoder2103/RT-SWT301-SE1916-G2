#!/usr/bin/env python3
r"""
Task 8 integration + before/after diff.

Assembles the NEW raw result set (new kill matrices + new scenario/coverage parse from the
regenerated Manual suite), recomputes summary.json into a STAGING dir, and prints a
committed-vs-new diff for every RQ -- WITHOUT touching the committed results until asked.

Inputs:
  --kills-dir   dir holding the newly measured <sut>_kills.csv (+ _recall.json)
  --scen-dir    dir holding the newly parsed scenarios.csv + coverage.csv
                (default: the member experiment/results/raw, written by the member
                 parse_scenarios.py which resolves the real harness path)
Outputs (staging, under --stage):
  results/raw/*  (assembled)   +  summary.json  + a printed diff

Promote to the committed tree only with --apply (copies staged raw -> results/raw, then
runs analyze.py + write_summary_csv.py + gen_paper_macros.py against the real tree).

Owner: MS (Nguyen Le Thuan, SE190305) / LR (Dung)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMITTED_RAW = os.path.join(ROOT, "results", "raw")
COMMITTED_SUMMARY = os.path.join(ROOT, "results", "stats", "summary.json")
MEMBER_RAW = os.path.join(ROOT, "Nguyen-Tien-Dung-SE190034", "experiment", "results", "raw")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def fmtp(p):
    return f"{p:.2e}" if p < 1e-4 else f"{p:.4f}"


def diff_report(old, new):
    print("\n================ TASK 8 BEFORE / AFTER ================")
    o1, n1 = old["RQ1_endpoint_coverage"], new["RQ1_endpoint_coverage"]
    print(f"RQ1 coverage %      : {o1['coverage_overall_pct']}  ->  {n1['coverage_overall_pct']}  "
          f"(p {fmtp(o1['p_value_one_sided'])} -> {fmtp(n1['p_value_one_sided'])}, "
          f"H0 {'reject' if n1['reject_H0_(coverage>90%)'] else 'keep'})")

    o2, n2 = old["RQ2_fault_detection"], new["RQ2_fault_detection"]
    for arm in ("llm", "manual", "evomaster"):
        print(f"RQ2 recall {arm:9s}: {o2['overall_recall'][arm]:.4f}  ->  {n2['overall_recall'][arm]:.4f}")
    om, nm = o2["mcnemar"]["llm_vs_evomaster"], n2["mcnemar"]["llm_vs_evomaster"]
    print(f"RQ2 LLM-vs-Evo McNemar p : {fmtp(om['p_value'])} -> {fmtp(nm['p_value'])} "
          f"(b={nm['llm_only(b)']}, c={nm['evomaster_only(c)']})")
    olm, nlm = o2["mcnemar"]["llm_vs_manual"], n2["mcnemar"]["llm_vs_manual"]
    print(f"RQ2 LLM-vs-Manual McNemar: b {olm['llm_only(b)']}->{nlm['llm_only(b)']}, "
          f"c {olm['manual_only(c)']}->{nlm['manual_only(c)']}  "
          f"(discordant pairs {'>0 -> NON-degenerate now' if (nlm['llm_only(b)'] or nlm['manual_only(c)']) else '=0 still degenerate'})")

    o3, n3 = old["RQ3_edge_cases_llm_vs_manual"], new["RQ3_edge_cases_llm_vs_manual"]
    print(f"RQ3 edge llm/manual : {o3['llm_total_edge']}/{o3['manual_total_edge']}  ->  "
          f"{n3['llm_total_edge']}/{n3['manual_total_edge']}  "
          f"(p {fmtp(o3['p_value_one_sided'])} -> {fmtp(n3['p_value_one_sided'])}, "
          f"rb {o3['rank_biserial']:.3f} -> {n3['rank_biserial']:.3f})")
    print("======================================================\n")


def assemble(stage, kills_dir, scen_dir):
    sraw = os.path.join(stage, "results", "raw")
    if os.path.isdir(sraw):
        shutil.rmtree(sraw)
    shutil.copytree(COMMITTED_RAW, sraw)  # base = committed, then overlay new
    # overlay new kill matrices
    for sut in ("ncs", "scs", "features"):
        for suffix in ("_kills.csv", "_recall.json"):
            src = os.path.join(kills_dir, f"{sut}{suffix}")
            if os.path.exists(src):
                shutil.copy(src, os.path.join(sraw, f"{sut}{suffix}"))
            else:
                print(f"  WARN: missing {src} -- keeping committed {sut}{suffix}")
    # overlay new scenarios + coverage (from the new Manual suite parse)
    for f in ("scenarios.csv", "coverage.csv"):
        src = os.path.join(scen_dir, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(sraw, f))
        else:
            print(f"  WARN: missing {src}")
    return sraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kills-dir", required=True)
    ap.add_argument("--scen-dir", default=MEMBER_RAW)
    ap.add_argument("--stage", default=os.path.join(ROOT, "results", "_task8_stage"))
    ap.add_argument("--apply", action="store_true",
                    help="promote staged raw into results/raw and regenerate the real tree")
    args = ap.parse_args()

    sraw = assemble(args.stage, args.kills_dir, args.scen_dir)
    sstats = os.path.join(args.stage, "results", "stats")
    os.makedirs(sstats, exist_ok=True)

    # compute staged summary via the same code path (compute_metric wraps analyze)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "compute_metric.py"),
                        "--raw-dir", sraw, "--out", sstats], cwd=ROOT)
    if r.returncode != 0:
        print("compute_metric failed on staged raw"); return 1

    new = load(os.path.join(sstats, "summary.json"))
    old = load(COMMITTED_SUMMARY)
    diff_report(old, new)

    if not args.apply:
        print(f"(dry run) staged under {args.stage}. Re-run with --apply to promote.")
        return 0

    # promote
    for sut in ("ncs", "scs", "features"):
        for suffix in ("_kills.csv", "_recall.json"):
            src = os.path.join(args.kills_dir, f"{sut}{suffix}")
            if os.path.exists(src):
                shutil.copy(src, os.path.join(COMMITTED_RAW, f"{sut}{suffix}"))
    for f in ("scenarios.csv", "coverage.csv"):
        src = os.path.join(args.scen_dir, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(COMMITTED_RAW, f))
    for script in ("analyze.py", "write_summary_csv.py", "gen_paper_macros.py"):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", script)], cwd=ROOT)
        if r.returncode != 0:
            print(f"{script} failed"); return 1
    print("APPLIED: results/raw, results/stats, results/summary.csv, paper macros updated.")
    print("Next: python scripts/check_paper.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
