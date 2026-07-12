#!/usr/bin/env bash
# Capture REAL test traffic: for each (sut, arm) run the JUnit suite through the
# logging proxy so every request the suite issues (incl. dynamic paths) is recorded
# with its actual HTTP status. SUTs must already be running on their ports.
set -u
ROOT=/d/SWT301_SU26_Group2/Nguyen-Tien-Dung-SE190034
H="$ROOT/experiment/harness"
LOG="$ROOT/experiment/results/raw/traffic.csv"
MVNLOG="$ROOT/experiment/results/raw/capture_mvn.log"
PROXY=9099
export JAVA_HOME="C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot"
MVN=/c/Users/dungm/tools/apache-maven-3.9.16/bin/mvn

echo "tag,method,path,status" > "$LOG"
: > "$MVNLOG"

run() {  # $1 sut  $2 target_port  $3 test-classes  $4 arm
  echo ">>> capturing $1:$4  (target :$2)"
  python "$ROOT/experiment/scripts/logproxy.py" "$PROXY" "$2" "$LOG" "$1:$4" &
  local PP=$!
  curl -s --retry 60 --retry-delay 1 --retry-connrefused -o /dev/null "http://localhost:$PROXY/__ping__"
  ( cd "$H" && "$MVN" -q test "-Dtest=$3" "-DbaseURI=http://localhost:$PROXY" \
       -DfailIfNoTests=false -Dsurefire.failIfNoSpecifiedTests=false ) >> "$MVNLOG" 2>&1 || true
  curl -s -o /dev/null "http://localhost:$PROXY/__shutdown__" || true
  wait "$PP" 2>/dev/null || true
  local c=$(grep -c "^$1:$4," "$LOG")
  echo "    logged $c requests for $1:$4"
}

run ncs      8080 NcsLlmTests                              llm
run ncs      8080 NcsManualTests                           manual
run ncs      8080 NcsEvoSuccessesTests,NcsEvoOthersTests   evomaster
run scs      8083 ScsLlmTests                              llm
run scs      8083 ScsManualTests                           manual
run scs      8083 ScsEvoSuccessesTests,ScsEvoFaultsTests   evomaster
run features 8081 FeaturesLlmTests                         llm
run features 8081 FeaturesManualTests                      manual
run features 8081 FeaturesEvoSuccessesTests,FeaturesEvoFaultsTests evomaster

echo "=== CAPTURE DONE ==="
wc -l "$LOG"
