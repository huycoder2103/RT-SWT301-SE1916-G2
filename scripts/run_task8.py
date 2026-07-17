#!/usr/bin/env python3
"""
Task 8 driver -- re-measure the mutation kill matrix with the regenerated Manual suite,
then rebuild every downstream artefact (stats, summary.csv, paper macros).

WHY THIS EXISTS
---------------
The repository currently ships a Manual suite in harness/src/test/java/manual/ that is NOT
the suite which produced results/raw/*_kills.csv. The committed kill matrix was measured
with the pilot Manual suite (now archived in manual/pilot-archive/*.java.pilot). Until this
script is run, harness source and results/ describe different experiments.

This script closes that gap. It is deliberately conservative: it refuses to run unless the
toolchain and mutant jars are actually present, because a partial run that silently writes
half a kill matrix is worse than no run.

PREREQUISITES (this script checks all of them and stops if any is missing)
  - JDK 8   -- builds/runs the SUTs            (--jdk8)
  - JDK 17  -- harness + EvoMaster             (--jdk17)
  - Maven on PATH
  - Per-SUT mutant dirs containing original.jar + m###.jar  (--mutants-root)
    These are NOT in git (gitignored). They live on the machine that ran mutate.py.
    If absent, regenerate with scripts/mutate.py -- but note that is ~416 Maven builds.

USAGE
  python scripts/run_task8.py \
      --jdk8  "C:/Users/<you>/tools/jdk8/jdk8u492-b09" \
      --jdk17 "C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot" \
      --mutants-root <dir containing ncs/ scs/ features/ mutant jars>

  Add --dry-run to preflight only (checks everything, runs nothing).
  Add --sut Ncs to do a single SUT first (recommended smoke test).

Owner: LR (Nguyen Tien Dung, SE190034)
"""
import argparse
import csv
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
HARNESS = os.path.join(ROOT, "Nguyen-Tien-Dung-SE190034", "experiment", "harness")

# sut key -> (run_mutation --sut name, port, mutant subdir, jar name)
SUTS = {
    "Ncs":      {"port": 8080, "mutants": "ncs",      "jar": "rest-ncs-sut.jar",         "kills": "ncs_kills.csv"},
    "Scs":      {"port": 8083, "mutants": "scs",      "jar": "rest-scs-sut.jar",         "kills": "scs_kills.csv"},
    "Features": {"port": 8081, "mutants": "features", "jar": "features-service-sut.jar", "kills": "features_kills.csv"},
}


def log(msg):
    print(f"[task8] {msg}", flush=True)


def baseline_n_oracle(kills_path):
    """Read the CURRENT (pilot) manual n_oracle so we can prove the new run differs.

    Self-calibrating: we do not hard-code 56/78/26, we read whatever is committed now.
    """
    if not os.path.exists(kills_path):
        return None
    with open(kills_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["arm"] == "manual":
                return int(row["n_oracle"])
    return None


def preflight(args, suts):
    problems = []

    for label, path in [("JDK 8", args.jdk8), ("JDK 17", args.jdk17)]:
        java = os.path.join(path, "bin", "java.exe")
        if not os.path.exists(java):
            java_nix = os.path.join(path, "bin", "java")
            if not os.path.exists(java_nix):
                problems.append(f"{label}: no java binary under {path}/bin/")

    if not (shutil.which("mvn") or shutil.which("mvn.cmd")):
        problems.append("Maven: 'mvn' not on PATH")

    if not os.path.isdir(HARNESS):
        problems.append(f"harness not found at {HARNESS}")

    for sut in suts:
        cfg = SUTS[sut]
        mdir = os.path.join(args.mutants_root, cfg["mutants"])
        if not os.path.isdir(mdir):
            problems.append(f"{sut}: mutant dir missing: {mdir}")
            continue
        orig = os.path.join(mdir, "original.jar")
        if not os.path.exists(orig):
            problems.append(f"{sut}: original.jar missing in {mdir}")
        n_mutants = len([x for x in os.listdir(mdir)
                         if x.startswith("m") and x.endswith(".jar")])
        if n_mutants == 0:
            problems.append(f"{sut}: no m###.jar mutants in {mdir}")
        else:
            log(f"preflight {sut}: {n_mutants} mutant jars found in {mdir}")

    # Verify the Manual suite really is the regenerated one, not the pilot copy.
    archive = os.path.join(ROOT, "Nguyen-Tien-Dung-SE190034", "experiment",
                           "manual", "pilot-archive")
    for sut in suts:
        live = os.path.join(HARNESS, "src", "test", "java", "manual", f"{sut}ManualTests.java")
        arch = os.path.join(archive, f"{sut}ManualTests.java.pilot")
        if not os.path.exists(live):
            problems.append(f"{sut}: Manual suite missing at {live}")
        elif os.path.exists(arch):
            same = open(live, encoding="utf-8").read() == open(arch, encoding="utf-8").read()
            if same:
                problems.append(
                    f"{sut}: harness Manual suite is IDENTICAL to the pilot archive -- "
                    f"Task 7 (regeneration) has not actually been applied; running Task 8 "
                    f"now would just reproduce the pilot numbers.")
            else:
                log(f"preflight {sut}: Manual suite differs from pilot archive (regenerated) OK")

    return problems


def run_sut(sut, args):
    cfg = SUTS[sut]
    mdir = os.path.join(args.mutants_root, cfg["mutants"])
    cmd = [
        sys.executable, os.path.join(ROOT, "scripts", "run_mutation.py"),
        "--sut", sut,
        "--jar", cfg["jar"],
        "--mutants", mdir,
        "--port", str(cfg["port"]),
        "--harness", HARNESS,
        "--results", RAW,
        "--jdk8", args.jdk8,
        "--jdk17", args.jdk17,
    ]
    log(f"running {sut} on port {cfg['port']} -- this boots the SUT once per mutant per arm; "
        f"expect this to take a long time")
    log("  " + " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="Task 8 -- re-measure kill matrix with the new Manual suite")
    ap.add_argument("--jdk8", required=True, help="JDK 8 home (runs the SUT jars)")
    ap.add_argument("--jdk17", required=True, help="JDK 17 home (harness + EvoMaster)")
    ap.add_argument("--mutants-root", required=True,
                    help="dir containing ncs/ scs/ features/ each with original.jar + m###.jar")
    ap.add_argument("--sut", choices=list(SUTS), help="run one SUT only (smoke test)")
    ap.add_argument("--dry-run", action="store_true", help="preflight only, run nothing")
    args = ap.parse_args()

    suts = [args.sut] if args.sut else list(SUTS)

    log("=== PREFLIGHT ===")
    problems = preflight(args, suts)
    if problems:
        log("PREFLIGHT FAILED -- refusing to run (a partial kill matrix is worse than none):")
        for p in problems:
            print(f"    - {p}")
        return 1
    log("preflight OK")

    # Record the pilot baseline BEFORE we overwrite it -- this is the Task 8 gate.
    baseline = {s: baseline_n_oracle(os.path.join(RAW, SUTS[s]["kills"])) for s in suts}
    log(f"pilot manual n_oracle baseline (must change): {baseline}")

    if args.dry_run:
        log("--dry-run set: preflight passed, stopping without running.")
        return 0

    log("=== RUN ===")
    for sut in suts:
        rc = run_sut(sut, args)
        if rc != 0:
            log(f"FAILED on {sut} (exit {rc}) -- stopping. results/raw is now PARTIAL; "
                f"restore with: git checkout results/raw")
            return rc

    log("=== GATE: did the Manual suite actually change the oracle count? ===")
    gate_failed = False
    for sut in suts:
        new = baseline_n_oracle(os.path.join(RAW, SUTS[sut]["kills"]))
        old = baseline[sut]
        if old is not None and new == old:
            log(f"  GATE FAIL {sut}: manual n_oracle still {new} -- identical to the pilot. "
                f"The new suite did not take effect (stale target/ classes? wrong harness?). "
                f"Try: mvn -f {HARNESS}/pom.xml clean test-compile")
            gate_failed = True
        else:
            log(f"  GATE OK  {sut}: manual n_oracle {old} -> {new}")
    if gate_failed:
        log("Gate failed: numbers would be indistinguishable from the pilot. Not rebuilding stats.")
        return 1

    log("=== REBUILD DOWNSTREAM ARTEFACTS ===")
    for step in [
        ["scripts/parse_scenarios.py"],
        ["scripts/analyze.py"],
        ["scripts/write_summary_csv.py"],
        ["scripts/gen_paper_macros.py"],
        ["scripts/results_json.py"],
    ]:
        script = step[0]
        if not os.path.exists(os.path.join(ROOT, script)):
            log(f"  skip {script} (not present)")
            continue
        log(f"  {script}")
        r = subprocess.run([sys.executable, script], cwd=ROOT)
        if r.returncode != 0:
            log(f"  FAILED: {script} exit {r.returncode}")
            return r.returncode

    log("=== DONE ===")
    log("results/raw, results/stats/summary.json, results/summary.csv and")
    log("paper/generated/numbers.tex are now all consistent with the NEW Manual suite.")
    log("The paper's numbers have moved automatically -- no .tex edit needed.")
    log("Next: python scripts/check_paper.py   then rebuild figures/notebooks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
