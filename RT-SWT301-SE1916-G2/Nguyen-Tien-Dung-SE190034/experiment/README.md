# Gap-3 Experiment — Reproduction Guide

LLM vs Manual vs EvoMaster REST-API test generation on EMB APIs with **pre-seeded faults**.
Member: Nguyen Tien Dung — SE190034 (SE1916). Method: see [`protocol.md`](protocol.md).

## 0. Prerequisites (pinned)

| Tool | Version | Purpose |
|------|---------|---------|
| Temurin JDK 8 | 1.8.0_492 | build + run the EMB SUTs |
| Temurin JDK 17 | 17.0.x | run EvoMaster 6.0.0 + the REST-assured harness |
| Maven | 3.9.x | build SUTs + harness |
| Python | 3.11+ | scipy 1.17, pandas, statsmodels, matplotlib |
| EvoMaster | 6.0.0 jar | comparator arm |
| EMB | EMResearch/EMB (LGPL-3.0) | the 3 SUTs (cloned, not vendored) |

```bash
pip install --user scipy statsmodels pandas matplotlib
git clone --depth 1 https://github.com/EMResearch/EMB.git        # SUT source
curl -L -o evomaster.jar https://github.com/EMResearch/EvoMaster/releases/latest/download/evomaster.jar
```

## 1. Build + deploy the SUTs (JDK 8)

```bash
export JAVA_HOME=<jdk8>
cd EMB/jdk_8_maven
mvn -pl cs/rest/artificial/ncs,cs/rest/artificial/scs,cs/rest/original/features-service \
    -am install -DskipTests -Dmaven.test.skip=true
# deploy (each in its own shell)
java -jar cs/rest/artificial/ncs/target/rest-ncs-sut.jar               # :8080
java -jar cs/rest/artificial/scs/target/rest-scs-sut.jar --server.port=8083
java -jar cs/rest/original/features-service/target/features-service-sut.jar --server.port=8081
```

## 2. The three test arms (already committed under `harness/src/test/java/`)

- `llm/`      — Claude Sonnet 4.6, blind, frozen prompt (`llm/prompt_template.md`, transcripts in `llm/transcripts/`)
- `manual/`   — blind EP/BVA methodology (`manual/methodology.md`)
- `evomaster/`— EvoMaster 6.0.0 black-box, adapted (`scripts/adapt_evomaster.py`, see `evomaster/README.md`)

Regenerate (optional): re-run the sub-agent prompts / `evomaster --blackBox`, then `scripts/adapt_evomaster.py`.

## 3. RQ1 (coverage) + RQ3 (edge cases) — static, from SCENARIO tags

```bash
python scripts/parse_scenarios.py     # -> results/raw/{coverage,scenarios}.csv
```

## 4. RQ2 (fault detection) — seed mutants, then measure kill

```bash
export JAVA_HOME=<jdk17>
# seed faults (recompiles each mutant SUT; ground truth -> faults/<sut>/catalog.json)
python scripts/mutate.py --module EMB/.../ncs --jar rest-ncs-sut.jar --out faults/ncs \
    --jdk8 <jdk8> --files src/main/java/org/restncs/NcsRest.java
#   (likewise scs: org/restscs/ScsRest.java ; features: the 5 .../services/rest/*Resource.java)

# run every arm against the original + each mutant (kill = passed-on-original, fails-on-mutant)
python scripts/run_mutation.py --sut Ncs --jar rest-ncs-sut.jar --mutants faults/ncs --port 8080 \
    --harness harness --results results/raw --jdk8 <jdk8> --jdk17 <jdk17>
#   (scs --port 8083 ; features --port 8081 --restart-per-arm  [stateful -> clean DB per arm])
```

## 5. Statistics + figures

```bash
python scripts/analyze.py     # RQ1 Wilcoxon, RQ2 Friedman+McNemar, RQ3 paired Wilcoxon -> results/stats/
python scripts/plot.py        # -> results/figures/*.png
```

Outputs land in `results/stats/summary.json` (+ per-RQ CSVs) and `results/figures/`. The written
findings are in [`REPORT.md`](REPORT.md).

## Notes / gotchas
- SUTs build & run on **JDK 8**; EvoMaster and the harness run on **JDK 17** (separate processes).
- Stop any SUT already bound to 8080/8081/8083 before `run_mutation.py` (it manages its own instances).
- `features-service` is stateful → `run_mutation.py --restart-per-arm` gives each arm a clean DB.
- Mutants are recompiled locally and are **not** committed (regenerate via `mutate.py`); the
  ground-truth `catalog.json` and all results CSVs **are** committed.
