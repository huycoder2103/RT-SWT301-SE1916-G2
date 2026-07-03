#!/usr/bin/env python3
"""
System-level mutation generator for the Gap-3 experiment.

Seeds faults by applying standard mutation operators (the families PIT / Offutt define:
relational-operator replacement, arithmetic-operator replacement, negate/boundary conditionals)
to a SUT's REST-controller source, where a fault is OBSERVABLE through the HTTP contract --
the relevant fault population for black-box API-test effectiveness.

For each candidate mutation it: applies the single-token change, rebuilds the SUT with Maven into
a standalone "-sut.jar", keeps the mutant only if it COMPILES + yields a jar (non-compiling ones are
discarded), records a ground-truth catalog entry, and restores the pristine source (from an in-memory
copy -- robust, no VCS dependency) before the next mutation.

Output: <out>/original.jar + <out>/m<NNN>.jar + <out>/catalog.json

Usage:
  python mutate.py --module <emb_module_dir> --jar <sut-jar-name> --out <dir> \
      --jdk8 <path> --files <relpath1> [<relpath2> ...]
"""
import argparse, json, os, re, shutil, subprocess, sys

MVN = shutil.which("mvn") or shutil.which("mvn.cmd") or "mvn.cmd"  # Windows: mvn is mvn.cmd

REL = {"<=": "<", ">=": ">", "==": "!=", "!=": "==", "<": "<=", ">": ">="}
ARI = {"+": "-", "-": "+", "*": "/", "/": "*", "%": "*"}
OP_RE = re.compile(r" (<=|>=|==|!=|<|>|\+|\*|/|%|-) ")  # spaced binary ops (skips generics/unary/lambda)


def find_mutations(src):
    """Return list of (offset, line, old_op, new_op) on the given source string."""
    muts = []
    for m in OP_RE.finditer(src):
        op = m.group(1)
        line_start = src.rfind("\n", 0, m.start()) + 1
        prefix = src[line_start:m.start()]
        if "//" in prefix or prefix.lstrip().startswith(("import", "package", "*", "/*")):
            continue
        new = REL.get(op) or ARI.get(op)
        if not new:
            continue
        muts.append((m.start() + 1, src.count("\n", 0, m.start()) + 1, op, new))  # +1: skip leading space
    return muts


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def build(module, jdk8):
    env = dict(os.environ, JAVA_HOME=jdk8)
    r = subprocess.run([MVN, "-q", "-DskipTests", "-Dmaven.test.skip=true", "-Dlicense.skip=true", "package"],
                       cwd=module, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode == 0, r.stdout.decode("utf-8", "replace")[-1500:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", required=True)
    ap.add_argument("--jar", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jdk8", required=True)
    ap.add_argument("--files", nargs="+", required=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    jar_src = os.path.join(args.module, "target", args.jar)

    ok, log = build(args.module, args.jdk8)
    if not ok:
        print("PRISTINE BUILD FAILED:\n", log); sys.exit(1)
    shutil.copy(jar_src, os.path.join(args.out, "original.jar"))
    print("pristine OK ->", args.jar)

    catalog, mid = [], 0
    for rel in args.files:
        path = os.path.join(args.module, rel)
        with open(path, encoding="utf-8") as f:
            original = f.read()
        muts = find_mutations(original)
        print(f"{rel}: {len(muts)} candidate mutations")
        for (off, line, old, new) in muts:
            assert original[off:off + len(old)] == old, "offset/op mismatch on original"
            mid += 1
            tag = f"m{mid:03d}"
            try:
                write(path, original[:off] + new + original[off + len(old):])
                built, log = build(args.module, args.jdk8)
                if built and os.path.exists(jar_src):
                    shutil.copy(jar_src, os.path.join(args.out, f"{tag}.jar"))
                    catalog.append({"id": tag, "file": rel, "line": line,
                                    "operator": f"{old} -> {new}", "status": "compiled"})
                    print(f"  {tag} L{line}: {old}->{new}  [kept]")
                else:
                    catalog.append({"id": tag, "file": rel, "line": line,
                                    "operator": f"{old} -> {new}", "status": "non-compiling-discarded"})
                    print(f"  {tag} L{line}: {old}->{new}  [discarded]")
            finally:
                write(path, original)  # restore pristine from memory
    # leave the module rebuilt pristine
    build(args.module, args.jdk8)
    kept = [c for c in catalog if c["status"] == "compiled"]
    with open(os.path.join(args.out, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump({"sut_jar": args.jar, "total_candidates": len(catalog), "kept": len(kept),
                   "mutants": catalog}, f, indent=2)
    print(f"\nDONE: {len(kept)} compilable mutants / {len(catalog)} candidates -> {args.out}")


if __name__ == "__main__":
    main()
