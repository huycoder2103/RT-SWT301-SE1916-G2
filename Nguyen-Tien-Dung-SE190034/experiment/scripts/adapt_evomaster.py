#!/usr/bin/env python3
"""
Adapt EvoMaster's generated JUnit suites into the common harness so all three arms run
on the same footing. Mechanical, faithful transformation ONLY:
  1. prepend `package evomaster;`
  2. rename the public class EvoMaster_<kind>_Test -> <Sut>Evo<Kind>Tests
  3. make the hardcoded baseUrlOfSut read the harness `baseURI` system property
The test bodies (requests + assertions) are left byte-for-byte unchanged.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "evomaster", "raw")
DEST = os.path.join(ROOT, "harness", "src", "test", "java", "evomaster")
SUTS = {"ncs": ("Ncs", 8080), "scs": ("Scs", 8083), "features": ("Features", 8081)}
KIND = {"EvoMaster_successes_Test": "Successes",
        "EvoMaster_others_Test": "Others",
        "EvoMaster_faults_Test": "Faults"}


def main():
    os.makedirs(DEST, exist_ok=True)
    n = 0
    for sut, (Sut, port) in SUTS.items():
        for fname, kind in KIND.items():
            src = os.path.join(RAW, sut, fname + ".java")
            if not os.path.exists(src):
                continue
            code = open(src, encoding="utf-8").read()
            newcls = f"{Sut}Evo{kind}Tests"
            code = code.replace(fname, newcls)  # declaration + any self-reference
            code = re.sub(r'baseUrlOfSut\s*=\s*"http://localhost:\d+"',
                          f'baseUrlOfSut = System.getProperty("baseURI", "http://localhost:{port}")',
                          code)
            code = "package evomaster;\n\n" + code
            out = os.path.join(DEST, newcls + ".java")
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(code)
            print(f"  {sut}/{fname} -> evomaster/{newcls}.java (port {port})")
            n += 1
    print(f"adapted {n} EvoMaster files")


if __name__ == "__main__":
    main()
