#!/usr/bin/env python3
"""
Writes results/{pilot,full}_llm_output.csv and results/{pilot,full}_api_log.txt
per the RBL-4 file tree.

Adaptation note (see notes.md): this project's LLM invocation is a Claude Code
isolated sub-agent call (env/tools.md), not a metered HTTP API -- there is no
per-call token/$ cost the way the RBL-4 template assumes for e.g. OpenAI. The
"api_log" here instead logs each sub-agent invocation: timestamp, model id,
SUT, spec reference, and (for the pilot) the tool-use-count blindness evidence
already recorded in llm/transcripts/*.md.

Usage:
  python write_llm_output_and_logs.py --stage pilot
  python write_llm_output_and_logs.py --stage full
"""
import argparse
import csv
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
RESULTS = os.path.join(ROOT, "results")
TRANSCRIPTS = os.path.join(ROOT, "llm", "transcripts")


def parse_transcript_header(path):
    text = open(path, encoding="utf-8").read()

    def field(*names, default="n/a (not recorded in this transcript)"):
        for name in names:
            m = re.search(rf"\|\s*(?:\*\*)?{name}(?:\*\*)?\s*\|\s*(.+?)\s*\|", text)
            if m:
                return m.group(1)
        return default

    return {
        "sut": os.path.splitext(os.path.basename(path))[0],
        "model_field": field("LLM under test"),
        "subagent_id": field("Sub-agent id"),
        "date": field("Date"),
        "input_spec": field("Input spec"),
        "blindness": field("Blindness evidence", "Blindness"),
        "usage": field("Usage", "Size"),
    }


def write_llm_output_csv(out_path, arm_filter="llm"):
    sc = os.path.join(RAW, "scenarios.csv")
    rows = []
    with open(sc, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["arm"] == arm_filter:
                rows.append(row)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sut", "op", "type", "count"])
        w.writeheader()
        for r in rows:
            w.writerow({"sut": r["sut"], "op": r["op"], "type": r["type"], "count": r["count"]})
    return len(rows)


def write_pilot_log(out_path):
    lines = [
        "# results/pilot_api_log.txt -- Week-7 pilot LLM-arm invocation log",
        "# Adaptation: invocation = Claude Code isolated sub-agent call (see env/tools.md),",
        "# NOT a metered HTTP API -- no per-call $ cost applies (Claude Code subscription covers it).",
        "",
    ]
    for path in sorted(glob.glob(os.path.join(TRANSCRIPTS, "*.md"))):
        h = parse_transcript_header(path)
        lines.append(
            f"[{h['date']}] sut={h['sut']} model={h['model_field']} "
            f"subagent_id={h['subagent_id']} spec={h['input_spec']} "
            f"blindness={h['blindness']} usage={h['usage']} "
            f"transcript={os.path.relpath(path, ROOT)}"
        )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines) - 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["pilot", "full"], required=True)
    args = ap.parse_args()

    out_csv = os.path.join(RESULTS, f"{args.stage}_llm_output.csv")
    n = write_llm_output_csv(out_csv, arm_filter="llm")
    print(f"wrote {out_csv} ({n} rows, arm=llm)")

    if args.stage == "pilot":
        out_log = os.path.join(RESULTS, "pilot_api_log.txt")
        n_entries = write_pilot_log(out_log)
        print(f"wrote {out_log} ({n_entries} sub-agent invocation entries)")
    else:
        print("full_api_log.txt is appended separately in Task 7's post-generation step "
              "(needs the 3 Manual-regeneration sub-agent ids/durations from that run).")


if __name__ == "__main__":
    main()
