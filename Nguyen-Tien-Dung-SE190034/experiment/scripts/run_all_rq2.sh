#!/usr/bin/env bash
# Full RQ2 pipeline (set-and-forget): seed mutants across controller + ALL core-logic classes
# (systematically; Application classes excluded so the SUT still boots), then run every arm
# against every mutant, then run the statistics + figures. Long-running -> launch in background.
#
# NOTE: does NOT use `set -e` -- a SUT with zero compilable mutants must not abort the whole run.
ROOT=/d/SWT301_SU26_Group2/Nguyen-Tien-Dung-SE190034
EMB=/d/SWT301_SU26_Group2/_emb_work/EMB/jdk_8_maven/cs/rest
JDK8="C:/Users/dungm/tools/jdk8/jdk8u492-b09"
JDK17="C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot"
cd "$ROOT" || exit 1

free_ports(){ powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8080,8081,8083 -State Listen -ErrorAction SilentlyContinue | Select-Object -Expand OwningProcess -Unique | ForEach-Object { Stop-Process -Id \$_ -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1; }

rel_files(){ # $1 = module dir, $2.. = find roots (relative); prints relative .java paths, excl. *Application.java
  local mod="$1"; shift
  ( cd "$mod" && find "$@" -name "*.java" ! -name "*Application.java" | tr '\n' ' ' )
}

echo "################ REGEN MUTANTS (controller + all logic) ################"
NCS=$EMB/artificial/ncs
echo "--- ncs ---"
python experiment/scripts/mutate.py --module "$NCS" --jar rest-ncs-sut.jar --out experiment/faults/ncs \
  --jdk8 "$JDK8" --files $(rel_files "$NCS" src/main/java/org/restncs) 2>&1 | tail -3

SCS=$EMB/artificial/scs
echo "--- scs ---"
python experiment/scripts/mutate.py --module "$SCS" --jar rest-scs-sut.jar --out experiment/faults/scs \
  --jdk8 "$JDK8" --files $(rel_files "$SCS" src/main/java/org/restscs) 2>&1 | tail -3

FEAT=$EMB/original/features-service
echo "--- features ---"
python experiment/scripts/mutate.py --module "$FEAT" --jar features-service-sut.jar --out experiment/faults/features \
  --jdk8 "$JDK8" --files $(rel_files "$FEAT" src/main/java/org/javiermf/features/models src/main/java/org/javiermf/features/daos src/main/java/org/javiermf/features/services) 2>&1 | tail -3

echo "################ RUN MUTATION (kill matrix) ################"
free_ports
python experiment/scripts/run_mutation.py --sut Ncs --jar rest-ncs-sut.jar --mutants experiment/faults/ncs \
  --port 8080 --harness experiment/harness --results experiment/results/raw --jdk8 "$JDK8" --jdk17 "$JDK17" 2>&1 | tail -4
free_ports
python experiment/scripts/run_mutation.py --sut Scs --jar rest-scs-sut.jar --mutants experiment/faults/scs \
  --port 8083 --harness experiment/harness --results experiment/results/raw --jdk8 "$JDK8" --jdk17 "$JDK17" 2>&1 | tail -4
free_ports
python experiment/scripts/run_mutation.py --sut Features --jar features-service-sut.jar --mutants experiment/faults/features \
  --port 8081 --harness experiment/harness --results experiment/results/raw --jdk8 "$JDK8" --jdk17 "$JDK17" --restart-per-arm 2>&1 | tail -4

echo "################ ANALYZE + PLOT ################"
python experiment/scripts/parse_scenarios.py 2>&1 | tail -8
python experiment/scripts/analyze.py 2>&1 | tail -40
python experiment/scripts/plot.py 2>&1 | tail -5
echo "################ ALL RQ2 PIPELINE DONE ################"
