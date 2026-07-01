#!/usr/bin/env python3
"""
Gate E4 entrypoint ("compute_metric.py chay tren data gia, khong loi").

Thin CLI wrapper around analyze.py's run_all() -- does not duplicate any statistical
logic, so the fixture run (gate E4) and the real run (Task 10, scripts/analyze.py or
--raw-dir results/raw) always exercise the exact same code path.

Usage:
  python compute_metric.py --raw-dir scripts/fixtures --out /tmp/out   # gate E4 smoke test
  python compute_metric.py --raw-dir results/raw --out results/stats  # real run (same as analyze.py)
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default=analyze.RAW,
                     help="directory with coverage.csv / scenarios.csv / <sut>_kills.csv")
    ap.add_argument("--out", default=analyze.OUT, help="directory to write stats output to")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    summary = analyze.run_all(raw_dir=args.raw_dir, out_dir=args.out)
    out_path = os.path.join(args.out, "summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"wrote {out_path}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
