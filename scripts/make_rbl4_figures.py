#!/usr/bin/env python3
"""
RBL-4 figures (>=300 DPI), additive to LR's rq1/rq2/rq3 pngs.

  figures/fig1_distribution.png  — RQ2 per-SUT/overall Recall distribution across the 3 arms
                                   (boxplot over per-mutant kill outcome, grouped by arm)
  figures/fig2_comparison.png    — RQ3 per-endpoint edge-case count, LLM vs Manual (paired bars)

Owner: MS (Nguyen Le Thuan, SE190305)
Usage: python scripts/make_rbl4_figures.py
"""
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
FIG = os.path.join(ROOT, "figures")
EDGE = {"negative", "boundary", "errorcode"}
DPI = 300
ARMS = ["llm", "manual", "evomaster"]


def fig1_distribution():
    frames = []
    for p in glob.glob(os.path.join(RAW, "*_kills.csv")):
        sut = os.path.basename(p).replace("_kills.csv", "")
        d = pd.read_csv(p)
        d["sut"] = sut
        frames.append(d)
    kills = pd.concat(frames, ignore_index=True)
    kills = kills[kills["arm"].isin(ARMS)]
    n_mutants = kills["mutant_id"].nunique() * 0 + kills.groupby("arm")["mutant_id"].nunique().max()

    # per-SUT recall points per arm (the RQ2 comparison unit) + pooled overall
    recall = (kills.groupby(["sut", "arm"])["killed"].mean().reset_index()
              .rename(columns={"killed": "recall"}))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=recall, x="arm", y="recall", order=ARMS, ax=ax,
                width=0.5, showmeans=True,
                meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": "black"})
    sns.stripplot(data=recall, x="arm", y="recall", order=ARMS, ax=ax,
                  hue="sut", size=9, jitter=False)
    overall = kills.groupby("arm")["killed"].mean()
    for i, arm in enumerate(ARMS):
        ax.annotate(f"pooled={overall[arm]:.3f}", (i, overall[arm]),
                    textcoords="offset points", xytext=(28, -4), fontsize=9)
    ax.set_title(f"RQ2 — Fault-detection Recall per SUT across arms (N={int(kills[kills.arm=='llm'].shape[0])} mutants, 3 SUTs)")
    ax.set_xlabel("Test-generation arm")
    ax.set_ylabel("Mutation-kill Recall")
    ax.legend(title="SUT", loc="upper left")
    fig.tight_layout()
    out = os.path.join(FIG, "fig1_distribution.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print("wrote", out)


def fig2_comparison():
    sc = pd.read_csv(os.path.join(RAW, "scenarios.csv"))
    edge = sc[sc["type"].isin(EDGE)]
    per_op = (edge[edge["arm"].isin(["llm", "manual"])]
              .groupby(["sut", "op", "arm"])["count"].sum().unstack(fill_value=0)
              .reset_index())
    per_op["label"] = per_op["sut"].str[:3] + ":" + per_op["op"]
    per_op = per_op.sort_values(["sut", "op"]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(13, 6))
    x = range(len(per_op))
    w = 0.4
    ax.bar([i - w / 2 for i in x], per_op["llm"], width=w, label="LLM (Claude Sonnet 4.6)")
    ax.bar([i + w / 2 for i in x], per_op["manual"], width=w, label="Manual (EP/BVA)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(per_op["label"], rotation=90, fontsize=7)
    ax.set_title(f"RQ3 — Edge-case scenarios per endpoint: LLM vs Manual (N={len(per_op)} operations)")
    ax.set_xlabel("Endpoint (sut:operationId)")
    ax.set_ylabel("Edge-case scenario count (negative+boundary+errorcode)")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig2_comparison.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    fig1_distribution()
    fig2_comparison()
