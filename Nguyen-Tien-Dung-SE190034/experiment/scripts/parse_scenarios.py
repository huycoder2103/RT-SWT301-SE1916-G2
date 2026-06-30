#!/usr/bin/env python3
"""
Parse the committed `// SCENARIO op=.. type=..` tags from the LLM and Manual test
suites to produce the inputs for RQ1 (endpoint coverage) and RQ3 (edge-case counts).

Outputs (to experiment/results/raw/):
  - scenarios.csv : sut, arm, op, type, count           (one row per (sut,arm,op,type))
  - coverage.csv  : sut, arm, ops_covered, ops_total, coverage_pct
                    (ops_total parsed from the frozen OpenAPI specs)

EvoMaster suites carry no SCENARIO tags (they are tool-generated); EvoMaster endpoint
coverage is taken from EvoMaster's own report and added in the report, not here.
RQ3 (edge cases) is an LLM-vs-Manual comparison only, per hypotheses.md.
"""
import csv, glob, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment/
HARNESS = os.path.join(ROOT, "harness", "src", "test", "java")
SPECS = os.path.join(ROOT, "specs")
OUT = os.path.join(ROOT, "results", "raw")
TAG = re.compile(r"//\s*SCENARIO\s+op=(\S+)\s+type=(\S+)")
EDGE = {"negative", "boundary", "errorcode"}


def sut_from_class(cls):
    m = re.match(r"([A-Za-z]+?)(Llm|Manual)Tests$", cls)
    return m.group(1).lower() if m else None


def ops_total(spec_file):
    d = json.load(open(spec_file, encoding="utf-8"))
    methods = {"get", "post", "put", "delete", "patch", "head", "options"}
    return sum(1 for p in d.get("paths", {}).values() for m in p if m.lower() in methods)


def main():
    os.makedirs(OUT, exist_ok=True)
    # total ops per SUT from frozen specs
    spec_map = {"ncs": "rest-ncs.openapi.json", "scs": "rest-scs.openapi.json",
                "features": "features-service.openapi.json"}
    totals = {s: ops_total(os.path.join(SPECS, f)) for s, f in spec_map.items()}

    counts = collections.defaultdict(int)          # (sut,arm,op,type) -> count
    ops_seen = collections.defaultdict(set)         # (sut,arm) -> {op}
    for arm in ("llm", "manual"):
        for f in glob.glob(os.path.join(HARNESS, arm, "*Tests.java")):
            cls = os.path.basename(f)[:-5]
            sut = sut_from_class(cls)
            if not sut:
                continue
            for op, typ in TAG.findall(open(f, encoding="utf-8").read()):
                counts[(sut, arm, op, typ)] += 1
                ops_seen[(sut, arm)].add(op)

    with open(os.path.join(OUT, "scenarios.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["sut", "arm", "op", "type", "count"])
        for (sut, arm, op, typ), c in sorted(counts.items()):
            w.writerow([sut, arm, op, typ, c])

    with open(os.path.join(OUT, "coverage.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["sut", "arm", "ops_covered", "ops_total", "coverage_pct"])
        for (sut, arm), ops in sorted(ops_seen.items()):
            tot = totals.get(sut, 0)
            pct = round(100.0 * len(ops) / tot, 1) if tot else 0.0
            w.writerow([sut, arm, len(ops), tot, pct])

    # quick console summary
    print("ops_total per spec:", totals)
    for (sut, arm), ops in sorted(ops_seen.items()):
        edges = sum(c for (s, a, _op, t), c in counts.items() if s == sut and a == arm and t in EDGE)
        print(f"  {sut:9s} {arm:6s}: {len(ops)}/{totals[sut]} ops covered, {edges} edge-case scenarios")


if __name__ == "__main__":
    main()
