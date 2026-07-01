#!/usr/bin/env python3
"""
Orchestration entrypoint ("run_experiment.py -- batch-run LLM theo config Sec.5.3 proposal",
RBL-4 file-tree gate). Thin driver: does not duplicate logic, just sequences the real
scripts already in this directory for a given stage/SUT, and appends one timestamped
line to results/{pilot,full}_api_log.txt per invocation.

This project's LLM arm is generated once via an isolated Claude Code sub-agent (see
env/tools.md, llm/prompt_template.md) -- there is no per-row "batch API call" loop to
run here the way the RBL-4 template assumes for a scriptable LLM client. What IS
batch-run here is the deterministic, repeatable part: executing each arm's compiled
JUnit suite against the SUT original + every seeded mutant (scripts/run_mutation.py),
then re-deriving coverage/scenario metrics (scripts/parse_scenarios.py) and statistics
(scripts/analyze.py / compute_metric.py). This script sequences exactly that pipeline.

Usage:
  python run_experiment.py --stage full --sut ncs           # real run
  python run_experiment.py --stage full --sut ncs --dry-run # print planned commands only
  python run_experiment.py --stage full --sut all --dry-run
"""
import argparse
import datetime
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(ROOT)

SUT_CONFIG = {
    "ncs": {"class": "Ncs", "jar": "rest-ncs-sut.jar", "faults": "faults/ncs", "port": 8080},
    "scs": {"class": "Scs", "jar": "rest-scs-sut.jar", "faults": "faults/scs", "port": 8083},
    "features": {"class": "Features", "jar": "features-service-sut.jar", "faults": "faults/features", "port": 8081},
}

JDK8 = "C:/Users/dungm/tools/jdk8/jdk8u492-b09"
JDK17 = os.environ.get("JAVA_HOME", "C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot")


def planned_commands(sut_key):
    cfg = SUT_CONFIG[sut_key]
    mutation_cmd = [
        sys.executable, "scripts/run_mutation.py",
        "--sut", cfg["class"], "--jar", cfg["jar"], "--mutants", cfg["faults"],
        "--port", str(cfg["port"]), "--harness", "harness", "--results", "results/raw",
        "--jdk8", JDK8, "--jdk17", JDK17, "--restart-per-arm",
    ]
    parse_cmd = [sys.executable, "scripts/parse_scenarios.py"]
    analyze_cmd = [sys.executable, "scripts/analyze.py"]
    return [mutation_cmd, parse_cmd, analyze_cmd]


def log_invocation(stage, sut_key, dry_run):
    log_path = os.path.join(EXPERIMENT, "results", f"{stage}_api_log.txt")
    ts = "[dry-run, no timestamp]" if dry_run else f"[{datetime.datetime.now().isoformat(timespec='seconds')}]"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{ts} run_experiment.py --stage {stage} --sut {sut_key} "
                f"(orchestrates run_mutation.py + parse_scenarios.py + analyze.py)\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["pilot", "full"], required=True)
    ap.add_argument("--sut", choices=list(SUT_CONFIG.keys()) + ["all"], required=True)
    ap.add_argument("--dry-run", action="store_true", help="print planned commands, do not execute")
    args = ap.parse_args()

    suts = list(SUT_CONFIG.keys()) if args.sut == "all" else [args.sut]

    for sut_key in suts:
        cmds = planned_commands(sut_key)
        print(f"=== {args.stage} / {sut_key} ===")
        for cmd in cmds:
            print("  $", " ".join(cmd))
        if not args.dry_run:
            for cmd in cmds:
                subprocess.run(cmd, cwd=EXPERIMENT, check=True)
        log_invocation(args.stage, sut_key, args.dry_run)

    print("dry-run: no commands executed." if args.dry_run else "done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
