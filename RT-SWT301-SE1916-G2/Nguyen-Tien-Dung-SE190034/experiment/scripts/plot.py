#!/usr/bin/env python3
"""
Render the figures for the Gap-3 report from the analysis outputs.
Reads experiment/results/{stats,raw}; writes PNGs to experiment/results/figures/.
Safe to run after analyze.py. Skips a figure whose inputs are missing.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
STATS = os.path.join(ROOT, "results", "stats")
FIG = os.path.join(ROOT, "results", "figures")
os.makedirs(FIG, exist_ok=True)


def fig_rq2_recall():
    p = os.path.join(STATS, "rq2_recall_per_sut.csv")
    if not os.path.exists(p):
        return
    df = pd.read_csv(p, index_col=0)
    ax = df[[c for c in ["llm", "manual", "evomaster"] if c in df.columns]].plot.bar(figsize=(7, 4))
    ax.set_ylabel("Mutation-kill recall"); ax.set_xlabel("SUT")
    ax.set_title("RQ2 — Fault-detection recall by arm and SUT")
    ax.set_ylim(0, 1); ax.legend(title="arm")
    plt.tight_layout(); plt.savefig(os.path.join(FIG, "rq2_recall.png"), dpi=140); plt.close()
    print("wrote rq2_recall.png")


def fig_rq3_edge():
    p = os.path.join(STATS, "rq3_edge_per_op.csv")
    if not os.path.exists(p):
        return
    df = pd.read_csv(p)
    _, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot([df["llm"], df["manual"]], tick_labels=["LLM", "Manual"], showmeans=True)
    ax.set_ylabel("Edge-case scenarios per endpoint")
    ax.set_title("RQ3 — Edge-case scenarios per endpoint (LLM vs Manual)")
    plt.tight_layout(); plt.savefig(os.path.join(FIG, "rq3_edgecases.png"), dpi=140); plt.close()
    print("wrote rq3_edgecases.png")


def fig_rq1_coverage():
    p = os.path.join(RAW, "coverage.csv")
    if not os.path.exists(p):
        return
    df = pd.read_csv(p)
    piv = df.pivot(index="sut", columns="arm", values="coverage_pct")
    ax = piv.plot.bar(figsize=(7, 4)); ax.axhline(90, color="red", ls="--", label="90% target")
    ax.set_ylabel("Endpoint coverage (%)"); ax.set_ylim(0, 105)
    ax.set_title("RQ1 — Endpoint coverage vs 90% target"); ax.legend()
    plt.tight_layout(); plt.savefig(os.path.join(FIG, "rq1_coverage.png"), dpi=140); plt.close()
    print("wrote rq1_coverage.png")


if __name__ == "__main__":
    fig_rq1_coverage(); fig_rq2_recall(); fig_rq3_edge()
    print("figures ->", FIG)
