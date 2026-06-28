#!/usr/bin/env python3
"""
Mutation-detection runner (RQ2 ground truth).

For one SUT: deploy the ORIGINAL and every mutant jar in turn, run each of the three
black-box arms (llm / manual / evomaster) against it, and decide -- per mutant, per arm --
whether the arm KILLS the mutant.

Kill rule (standard): an arm kills a mutant iff at least one test that PASSED on the
original SUT FAILS (or errors) on the mutant -- i.e. the suite observably distinguishes
the faulty version from the correct one. Tests that already fail on the original are
excluded as invalid oracles for that arm.

Output: <results>/<sut>_kills.csv  with columns:
   mutant_id, arm, killed(0/1), n_oracle, n_now_failing_oracle
Plus <results>/<sut>_recall.json with per-arm recall = killed/total.

Usage:
  python run_mutation.py --sut Ncs --jar rest-ncs-sut.jar \
     --mutants experiment/faults/ncs --port 8080 \
     --harness experiment/harness --results experiment/results/raw \
     --jdk8 <path> --jdk17 <path> [--restart-per-arm]
"""
import argparse, csv, glob, json, os, shutil, socket, subprocess, sys, time, xml.etree.ElementTree as ET
# NOTE: surefire reports parsed below are produced by our OWN local Maven run (trusted input),
# so stdlib ElementTree is fine here (no untrusted/remote XML -> XXE not a vector).

MVN = shutil.which("mvn") or shutil.which("mvn.cmd") or "mvn.cmd"  # Windows: mvn is mvn.cmd
ARMS = ["llm", "manual", "evomaster"]


def pattern(sut, arm):
    return {"llm": f"{sut}LlmTests", "manual": f"{sut}ManualTests",
            "evomaster": f"{sut}Evo*"}[arm]


def wait_up(port, timeout=45):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=2):
                return True
        except OSError:
            time.sleep(1)
    return False


def start_sut(jar, port, jdk8):
    java = os.path.join(jdk8, "bin", "java.exe")
    p = subprocess.Popen([java, "-jar", jar, f"--server.port={port}"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p


def stop_sut(p):
    try:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        p.terminate()
    try:
        p.wait(timeout=15)
    except Exception:
        pass


def run_suite(harness, cls_pattern, port, jdk17):
    """Run one arm's tests; return dict testname-> 'pass'|'fail'."""
    env = dict(os.environ, JAVA_HOME=jdk17)
    # clean previous reports
    rep = os.path.join(harness, "target", "surefire-reports")
    if os.path.isdir(rep):
        for f in glob.glob(os.path.join(rep, "*.xml")):
            try: os.remove(f)
            except OSError: pass
    subprocess.run([MVN, "-q", "-o", "test", f"-Dtest={cls_pattern}",
                    f"-DbaseURI=http://localhost:{port}"],
                   cwd=harness, env=env, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    results = {}
    for xmlf in glob.glob(os.path.join(rep, "*.xml")):
        try:
            root = ET.parse(xmlf).getroot()
        except ET.ParseError:
            continue
        for tc in root.iter("testcase"):
            name = f"{tc.get('classname')}.{tc.get('name')}"
            bad = any(c.tag in ("failure", "error") for c in tc)
            results[name] = "fail" if bad else "pass"
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sut", required=True)         # e.g. Ncs
    ap.add_argument("--jar", required=True)          # sut jar filename
    ap.add_argument("--mutants", required=True)      # dir with original.jar + m###.jar
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--harness", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--jdk8", required=True)
    ap.add_argument("--jdk17", required=True)
    ap.add_argument("--restart-per-arm", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.results, exist_ok=True)
    orig = os.path.join(args.mutants, "original.jar")
    mutants = sorted(glob.glob(os.path.join(args.mutants, "m*.jar")))
    if not os.path.exists(orig) or not mutants:
        print("missing original.jar or mutants in", args.mutants); sys.exit(1)

    def measure(jar):
        """Return {arm: {test: pass/fail}} for a given SUT jar, restarting as configured."""
        out = {}
        if args.restart_per_arm:
            for arm in ARMS:
                p = start_sut(jar, args.port, args.jdk8)
                if not wait_up(args.port):
                    stop_sut(p); out[arm] = {}; continue
                out[arm] = run_suite(args.harness, pattern(args.sut, arm), args.port, args.jdk17)
                stop_sut(p)
        else:
            p = start_sut(jar, args.port, args.jdk8)
            if wait_up(args.port):
                for arm in ARMS:
                    out[arm] = run_suite(args.harness, pattern(args.sut, arm), args.port, args.jdk17)
            stop_sut(p)
        return out

    print(f"[{args.sut}] baseline on original ...")
    base = measure(orig)
    oracle = {arm: {t for t, r in base.get(arm, {}).items() if r == "pass"} for arm in ARMS}
    for arm in ARMS:
        print(f"  {arm}: {len(oracle[arm])} passing oracle tests")

    rows, recall = [], {arm: {"killed": 0, "total": 0} for arm in ARMS}
    for i, mj in enumerate(mutants, 1):
        mid = os.path.splitext(os.path.basename(mj))[0]
        res = measure(mj)
        for arm in ARMS:
            now = res.get(arm, {})
            now_fail_oracle = [t for t in oracle[arm] if now.get(t) == "fail"]
            killed = 1 if now_fail_oracle else 0
            recall[arm]["killed"] += killed
            recall[arm]["total"] += 1
            rows.append({"mutant_id": mid, "arm": arm, "killed": killed,
                         "n_oracle": len(oracle[arm]), "n_now_failing_oracle": len(now_fail_oracle)})
        ks = "/".join(f"{arm[0]}{[r['killed'] for r in rows if r['mutant_id']==mid and r['arm']==arm][0]}" for arm in ARMS)
        print(f"  [{i}/{len(mutants)}] {mid}: {ks}")

    csv_path = os.path.join(args.results, f"{args.sut.lower()}_kills.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["mutant_id", "arm", "killed", "n_oracle", "n_now_failing_oracle"])
        w.writeheader(); w.writerows(rows)
    rj = {arm: {"killed": recall[arm]["killed"], "total": recall[arm]["total"],
                "recall": round(recall[arm]["killed"] / recall[arm]["total"], 4) if recall[arm]["total"] else None}
          for arm in ARMS}
    with open(os.path.join(args.results, f"{args.sut.lower()}_recall.json"), "w", encoding="utf-8") as f:
        json.dump(rj, f, indent=2)
    print(f"[{args.sut}] recall:", rj)
    print("wrote", csv_path)


if __name__ == "__main__":
    main()
