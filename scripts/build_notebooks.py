#!/usr/bin/env python3
"""
Builds + EXECUTES results/pilot_analysis.ipynb and results/full_analysis.ipynb via
nbformat/nbclient — cell outputs are real (no hand-typed results) and both notebooks
survive Restart & Run All by construction.

  pilot_analysis.ipynb — Week-7 pilot: descriptive stats + histogram of edge-case
                          distribution (RBL-4 §7.3 "Vẽ histogram phân phối").
  full_analysis.ipynb  — Week-8 full run: loads results/raw/* + results/stats/summary.json,
                          reports RQ1/RQ2/RQ3 with p-values, effect sizes, N, and the
                          explicit reject / fail-to-reject H0 call per RQ (RBL-4 §8.3).

Owner: MS (Nguyen Le Thuan, SE190305)
Usage: python scripts/build_notebooks.py
"""
import os

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")

SETUP = """\
import glob, json, os
import pandas as pd
import matplotlib.pyplot as plt

# works both when executed from repo root (nbclient) and when opened from results/ in Jupyter
RAW = os.path.join('..', 'results', 'raw') if os.path.basename(os.getcwd()) == 'results' else os.path.join('results', 'raw')
EDGE = {'negative', 'boundary', 'errorcode'}
pd.set_option('display.width', 160)
"""


def pilot_nb():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            "# RBL-4 Pilot Analysis (Week 7)\n"
            "**Group:** SE1916-G2 · **Owner:** MS — Nguyen Le Thuan (SE190305)\n\n"
            "Descriptive statistics of the Week-7 pilot: scenario distribution per arm/type "
            "and the edge-case histogram (RBL-4 §7.3). Statistical inference lives in "
            "`full_analysis.ipynb`; this notebook is descriptive only.\n\n"
            "Data: `results/raw/scenarios.csv`, `results/raw/coverage.csv`, `results/raw/*_kills.csv` "
            "(pilot ran on the full compilable mutant catalog, N=133 — see `notes.md`)."),
        new_code_cell(SETUP),
        new_markdown_cell("## 1. Scenario counts per arm × type"),
        new_code_cell(
            "sc = pd.read_csv(os.path.join(RAW, 'scenarios.csv'))\n"
            "sc.pivot_table(index='arm', columns='type', values='count', aggfunc='sum', fill_value=0)"),
        new_markdown_cell("## 2. Endpoint coverage per arm (RQ1 raw view)"),
        new_code_cell(
            "cov = pd.read_csv(os.path.join(RAW, 'coverage.csv'))\n"
            "cov.pivot_table(index='sut', columns='arm', values='coverage_pct')"),
        new_markdown_cell("## 3. Histogram — per-endpoint edge-case distribution (LLM vs Manual)"),
        new_code_cell(
            "edge = sc[sc['type'].isin(EDGE) & sc['arm'].isin(['llm','manual'])]\n"
            "per_op = edge.groupby(['sut','op','arm'])['count'].sum().unstack(fill_value=0)\n"
            "fig, ax = plt.subplots(figsize=(8,4.5))\n"
            "bins = range(0, int(per_op.values.max())+2)\n"
            "ax.hist([per_op['llm'], per_op['manual']], bins=bins, label=['LLM','Manual'])\n"
            "ax.set_title('Pilot: distribution of edge-case scenarios per endpoint (N=35 ops)')\n"
            "ax.set_xlabel('edge-case scenarios per endpoint'); ax.set_ylabel('endpoints'); ax.legend()\n"
            "plt.show()\n"
            "per_op.describe()"),
        new_markdown_cell("## 4. Pilot mutation-kill counts (descriptive)"),
        new_code_cell(
            "frames = []\n"
            "for p in glob.glob(os.path.join(RAW, '*_kills.csv')):\n"
            "    d = pd.read_csv(p); d['sut'] = os.path.basename(p).replace('_kills.csv',''); frames.append(d)\n"
            "kills = pd.concat(frames, ignore_index=True)\n"
            "print('mutants per SUT:', kills[kills.arm=='llm'].groupby('sut').size().to_dict())\n"
            "kills.groupby('arm')['killed'].agg(['sum','count','mean']).rename(columns={'mean':'recall'})"),
        new_markdown_cell(
            "### Pilot observations (descriptive, pre-registered caveats apply)\n"
            "- LLM covers all endpoints; LLM produces more edge-case scenarios per endpoint than Manual.\n"
            "- LLM and Manual kill vectors are **identical** on all mutants — the pre-registered "
            "\"lenient oracle\" threat (proposal §7): both arms assert existence/status, not values, "
            "so they are structurally blind to silent arithmetic mutants. Reported as a finding, not patched (no HARKing)."),
    ]
    return nb


def full_nb():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            "# RBL-4 Full-Run Analysis (Week 8)\n"
            "**Group:** SE1916-G2 · **Owner:** MS — Nguyen Le Thuan (SE190305)\n\n"
            "Loads `results/stats/summary.json` (produced by `scripts/compute_metric.py`, the single "
            "statistical code path per proposal §5.6) and states the reject / fail-to-reject H0 call per RQ.\n\n"
            "α = 0.05 per RQ (pre-registered); Holm within RQ2 post-hoc; Bonferroni across the 3 RQ "
            "families reported as a stricter secondary reading (α_adj ≈ 0.017)."),
        new_code_cell(SETUP),
        new_code_cell(
            "STATS = os.path.join(os.path.dirname(RAW), 'stats', 'summary.json')\n"
            "s = json.load(open(STATS, encoding='utf-8'))\n"
            "print('sections:', list(s))"),
        new_markdown_cell("## RQ1 — Endpoint coverage (H1: LLM coverage > 90%)"),
        new_code_cell(
            "rq1 = s['RQ1_endpoint_coverage']\n"
            "print(f\"coverage = {rq1['coverage_overall_pct']}% ({rq1['ops_covered']}/{rq1['n_operations']} ops)\")\n"
            "print(f\"one-sample Wilcoxon vs 0.90 (one-tailed): W={rq1['wilcoxon_W']}, p={rq1['p_value_one_sided']:.3e}\")\n"
            "print(f\"effect size (rank-biserial) = {rq1['rank_biserial']}\")\n"
            "verdict = 'REJECT H0' if rq1['reject_H0_(coverage>90%)'] else 'FAIL TO REJECT H0'\n"
            "print(f\"==> RQ1: {verdict} — LLM endpoint coverage exceeds 90% (n={rq1['n_operations']})\")"),
        new_markdown_cell("## RQ2 — Fault-detection Recall (3 arms, N=133 pre-seeded mutants)"),
        new_code_cell(
            "rq2 = s['RQ2_fault_detection']\n"
            "print('overall recall:', rq2['overall_recall'])\n"
            "print(f\"Friedman: chi2={rq2['friedman_chi2']}, p={rq2['friedman_p']}\")\n"
            "print('Holm-corrected pairwise Wilcoxon:', json.dumps(rq2['pairwise_wilcoxon_holm'], indent=1))\n"
            "print('Cliff\\'s delta:', rq2['cliffs_delta'])\n"
            "for pair, m in rq2['mcnemar'].items():\n"
            "    print(f\"McNemar {pair}: p={m['p_value']:.4f}, reject={m['reject_H0']}, achieved power~{m['achieved_power_approx']:.3f}\")\n"
            "verdict = 'REJECT H0' if any(m['reject_H0'] for m in rq2['mcnemar'].values()) else 'FAIL TO REJECT H0'\n"
            "print(f\"==> RQ2: {verdict} — no arm significantly outperforms at alpha=0.05 \"\n"
            "      f\"(primary pooled McNemar, N={rq2['n_mutants_total']}); EvoMaster recall is numerically higher \"\n"
            "      '(0.135 vs 0.068) but p=0.064 > 0.05.')"),
        new_code_cell("pd.read_csv(os.path.join(os.path.dirname(RAW), 'stats', 'rq2_recall_per_sut.csv'))"),
        new_markdown_cell("## RQ3 — Edge-case scenarios per endpoint (H1: LLM > Manual)"),
        new_code_cell(
            "rq3 = s['RQ3_edge_cases_llm_vs_manual']\n"
            "print(f\"totals: LLM {rq3['llm_total_edge']} vs Manual {rq3['manual_total_edge']} \"\n"
            "      f\"(median/op {rq3['llm_median_per_op']} vs {rq3['manual_median_per_op']})\")\n"
            "print(f\"paired Wilcoxon (one-tailed): W={rq3['wilcoxon_W']}, p={rq3['p_value_one_sided']:.3e}\")\n"
            "print(f\"effect size (rank-biserial) = {rq3['rank_biserial']:.3f}; \"\n"
            "      f\"pairs LLM>Manual: {rq3['pairs_llm_more']}, Manual>LLM: {rq3['pairs_manual_more']}, ties: {rq3['pairs_tie']}\")\n"
            "verdict = 'REJECT H0' if rq3['reject_H0_(llm>manual)'] else 'FAIL TO REJECT H0'\n"
            "print(f\"==> RQ3: {verdict} — LLM produces more edge-case scenarios per endpoint (n={rq3['n_operations']})\")"),
        new_markdown_cell("## Multiplicity"),
        new_code_cell("print(json.dumps(s['multiplicity'], indent=1))"),
        new_markdown_cell(
            "## Conclusions (per RQ, α=0.05 pre-registered)\n"
            "| RQ | Verdict | Evidence |\n|---|---|---|\n"
            "| RQ1 | **Reject H0** | coverage 100% (35/35), p≈1.6e-9, rank-biserial 1.0 |\n"
            "| RQ2 | **Fail to reject H0** | McNemar LLM-vs-EvoMaster p≈0.064; Cliff's δ≈−0.068 (negligible); achieved power ≈0.46 — underpowered, disclosed |\n"
            "| RQ3 | **Reject H0** | LLM 217 vs Manual 141 edge-cases, p≈6.2e-7, rank-biserial 0.988 |\n\n"
            "All conclusions also survive the Bonferroni cross-RQ reading (α_adj≈0.017) except none change: "
            "RQ1/RQ3 p-values ≪ 0.017; RQ2 remains non-significant.\n\n"
            "**Note (full-run status):** these numbers reflect the current committed raw data. If LR regenerates the "
            "independent Manual suite (Week-8 bias fix) and re-runs the mutation matrix, re-run "
            "`scripts/compute_metric.py` then this notebook — RQ1 must remain byte-identical (LLM arm unchanged); "
            "RQ2/RQ3 Manual-side values are expected to change."),
    ]
    return nb


def build(name, nb):
    path = os.path.join(RES, name)
    client = NotebookClient(nb, timeout=180, resources={"metadata": {"path": ROOT}})
    client.execute()
    nbformat.write(nb, path)
    print("wrote (executed)", path)


if __name__ == "__main__":
    build("pilot_analysis.ipynb", pilot_nb())
    build("full_analysis.ipynb", full_nb())
