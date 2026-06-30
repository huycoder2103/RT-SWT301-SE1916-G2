#!/usr/bin/env bash
# Migrate pilot artifacts from Nguyen-Tien-Dung-SE190034/experiment/ to root structure
# Owner: LR (Nguyen Tien Dung) — run from repo root
# Created by PL (Huy) per RBL-0 standard structure

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

SRC="Nguyen-Tien-Dung-SE190034/experiment"
if [ ! -d "$SRC" ]; then
  echo "ERROR: source dir not found: $SRC"
  exit 1
fi

echo "=== Migrating pilot artifacts to root structure ==="

# 1. Scripts — copy all Python scripts (root expects compute_metric.py, run_experiment.py, test_api.py + extras)
mkdir -p scripts
cp -v "$SRC/scripts/"*.py scripts/ 2>/dev/null || true
cp -v "$SRC/scripts/"*.sh scripts/ 2>/dev/null || true

# Rename to RBL-0 standard names where applicable
[ -f scripts/analyze.py ]      && cp -v scripts/analyze.py      scripts/compute_metric.py
[ -f scripts/run_mutation.py ] && cp -v scripts/run_mutation.py scripts/run_experiment.py

# 2. Results — pilot artifacts
mkdir -p results/raw
cp -rv "$SRC/results/raw/"* results/raw/ 2>/dev/null || true
cp -v  "$SRC/results/"*.json results/ 2>/dev/null || true

# 3. Data — ground truth + samples
mkdir -p data/raw
# (Dataset itself is in EMB submodule — don't copy heavy SUTs; just catalog refs)
[ -f "$SRC/faults/ncs/catalog.json" ]      && mkdir -p data/faults/ncs      && cp -v "$SRC/faults/ncs/catalog.json"      data/faults/ncs/
[ -f "$SRC/faults/scs/catalog.json" ]      && mkdir -p data/faults/scs      && cp -v "$SRC/faults/scs/catalog.json"      data/faults/scs/
[ -f "$SRC/faults/features/catalog.json" ] && mkdir -p data/faults/features && cp -v "$SRC/faults/features/catalog.json" data/faults/features/

# 4. Figures
mkdir -p figures
cp -v "$SRC/results/figures/"*.png figures/ 2>/dev/null || true

# 5. LLM prompt template (frozen, must be at known location)
mkdir -p scripts/llm
cp -v "$SRC/llm/prompt_template.md" scripts/llm/ 2>/dev/null || true

echo ""
echo "=== Done. Review:"
echo "  scripts/   $(ls scripts/ | wc -l) files"
echo "  results/   $(find results -type f | wc -l) files"
echo "  figures/   $(ls figures/ 2>/dev/null | wc -l) files"
echo "  data/faults/ $(find data/faults -type f 2>/dev/null | wc -l) files"
echo ""
echo "Next steps:"
echo "  1. git status — review changes"
echo "  2. git add -A && git commit -m '[RBL-4] migrate pilot artifacts to root structure'"
echo "  3. git push"
