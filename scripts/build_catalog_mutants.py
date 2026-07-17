#!/usr/bin/env python3
r"""
Build EXACTLY the mutant jars named in a committed fault catalog -- no more, no less.

Why not just re-run mutate.py? Because mutate.py re-DISCOVERS and re-COMPILES every
candidate, and on a clean toolchain it keeps mutants that the original (pilot) run marked
"discarded" -- notably rest-ncs, whose pilot catalog is contiguous m001..m070 then nothing,
the signature of a mutation run that broke after candidate 70. Re-running would therefore
enlarge the fault population, changing the RQ2 denominator. The proposal froze that
population (no HARKing); Task 8 re-authors only the Manual suite, so the ground truth must
stay byte-for-byte the committed 133 mutants.

This builder reuses mutate.py's exact discovery (find_mutations, same --files order -> same
m-id assignment on identical source) but BUILDS ONLY the m-ids the committed catalog marks
status=="compiled", and asserts each built mutant's (line, operator) equals the catalog's.
Result: a mutants dir whose jars correspond 1:1 to the committed ground truth.

Usage:
  python scripts/build_catalog_mutants.py --sut ncs \
      --module <emb>/artificial/ncs --jar rest-ncs-sut.jar \
      --catalog data/faults/ncs/catalog.json --out <mutants>/ncs \
      --jdk8 <jdk8> --files src/main/java/org/restncs

Owner: LR (Dung) -- Task 8 reproducibility tool.
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_mutate():
    spec = importlib.util.spec_from_file_location("mutate", os.path.join(ROOT, "scripts", "mutate.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sut", required=True)
    ap.add_argument("--module", required=True)
    ap.add_argument("--jar", required=True)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jdk8", required=True)
    ap.add_argument("--files", nargs="+", required=False,
                    help="(unused) kept for CLI compatibility; file set is taken from the catalog")
    args = ap.parse_args()

    mutate = load_mutate()
    committed = json.load(open(args.catalog, encoding="utf-8"))
    all_muts = committed["mutants"]
    n_want = sum(1 for m in all_muts if m["status"] == "compiled")
    print(f"[{args.sut}] committed: {len(all_muts)} candidates, {n_want} compiled to build")

    os.makedirs(args.out, exist_ok=True)
    jar_src = os.path.join(args.module, "target", args.jar)

    # 1) pristine original
    ok, log = mutate.build(args.module, args.jdk8)
    if not ok:
        print("PRISTINE BUILD FAILED:\n", log[-800:]); return 1
    shutil.copy(jar_src, os.path.join(args.out, "original.jar"))
    print(f"[{args.sut}] original.jar OK")

    # 2) Per-file positional match: the catalog lists a file's mutants in discovery order,
    #    which is exactly find_mutations() order on identical source. Group by file (keeping
    #    m-id order), zip with find_mutations candidates, and build the compiled ones. This is
    #    independent of the ACROSS-file processing order, so it can't drift on directory order.
    by_file = {}
    for m in all_muts:
        by_file.setdefault(m["file"], []).append(m)

    built = []
    for rel, fmuts in by_file.items():
        path = os.path.join(args.module, rel.replace("/", os.sep))
        original = open(path, encoding="utf-8").read()
        cands = mutate.find_mutations(original)
        assert len(cands) == len(fmuts), (
            f"{rel}: catalog has {len(fmuts)} candidates but discovery finds {len(cands)} "
            f"-- source drift, aborting")
        for m, (off, line, old, new) in zip(fmuts, cands):
            if m["status"] != "compiled":
                # Discarded candidates are not built and not part of the ground truth. Their
                # recorded operator can legitimately disagree with a clean re-discovery when the
                # original run's source-restore was interrupted (e.g. rest-ncs truncated after
                # m070); we only need exact fidelity on the COMPILED set, checked below.
                continue
            assert m["line"] == line and m["operator"] == f"{old} -> {new}", (
                f"{m['id']} ({rel}): COMPILED mutant mismatch -- catalog L{m['line']} "
                f"{m['operator']} != discovery L{line} {old}->{new} -- aborting")
            tag = m["id"]
            try:
                mutate.write(path, original[:off] + new + original[off + len(old):])
                good, blog = mutate.build(args.module, args.jdk8)
                if not (good and os.path.exists(jar_src)):
                    print(f"  WARN {tag} did not compile here (committed said it did): {blog[-200:]}")
                    continue
                shutil.copy(jar_src, os.path.join(args.out, f"{tag}.jar"))
                built.append(tag)
                if len(built) % 10 == 0:
                    print(f"  [{args.sut}] built {len(built)}/{n_want}")
            finally:
                mutate.write(path, original)

    mutate.build(args.module, args.jdk8)      # leave module pristine
    want_ids = {m["id"] for m in all_muts if m["status"] == "compiled"}
    missing = sorted(want_ids - set(built))
    print(f"[{args.sut}] built {len(built)}/{n_want} mutant jars"
          + (f"  MISSING: {missing}" if missing else "  (exact match to committed compiled set)"))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
