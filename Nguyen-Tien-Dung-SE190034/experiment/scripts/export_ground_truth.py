#!/usr/bin/env python3
"""
Export the code-derived ground truth (mutation catalogs) into the CSV shape the
RBL-4 file tree expects (data/pilot_ground_truth.csv, data/full_ground_truth.csv,
data/pilot_sample.csv).

Why no human annotation / IAA here: this project's ground truth is DERIVED from the
mutation-seeding process itself (a mutant is objectively "compiled" or not; which
mutant a test "kills" is objectively computed by run_mutation.py) -- see
proposal.md §8.2 ("Ground truth | DG/MS | mutation catalog (no human annotation
needed)"). There is nothing for a second human annotator to agree/disagree on, so
Cohen's Kappa does not apply; this is disclosed in notes.md against RBL-4 gate E5.

The Week-7 pilot ran on the FULL compilable catalog (133 mutants) -- no smaller
10-20% sub-sample was drawn (see notes.md) -- so pilot_ground_truth.csv and
full_ground_truth.csv are identical in content; pilot_sample.csv additionally
carries a `note` column documenting that fact for traceability.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAULTS = os.path.join(ROOT, "faults")
DATA = os.path.join(ROOT, "data")
SUTS = ["ncs", "scs", "features"]


def load_kept_mutants():
    rows = []
    for sut in SUTS:
        cat_path = os.path.join(FAULTS, sut, "catalog.json")
        with open(cat_path, "r", encoding="utf-8") as f:
            cat = json.load(f)
        for m in cat["mutants"]:
            if m["status"] == "compiled":
                rows.append({
                    "sut": sut,
                    "mutant_id": m["id"],
                    "file": m["file"],
                    "line": m["line"],
                    "operator": m["operator"],
                })
    return rows


def write_csv(path, rows, extra_cols=None, extra_value=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["sut", "mutant_id", "file", "line", "operator"]
    if extra_cols:
        fieldnames = fieldnames + extra_cols
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            row = dict(r)
            if extra_cols:
                for c in extra_cols:
                    row[c] = extra_value
            w.writerow(row)


def main():
    rows = load_kept_mutants()
    assert len(rows) == 133, f"expected 133 kept mutants, got {len(rows)}"
    per_sut = {}
    for r in rows:
        per_sut[r["sut"]] = per_sut.get(r["sut"], 0) + 1
    print("kept mutants per SUT:", per_sut)

    write_csv(os.path.join(DATA, "full_ground_truth.csv"), rows)
    write_csv(os.path.join(DATA, "pilot_ground_truth.csv"), rows)
    note = ("Week-7 pilot ran on the FULL compilable mutant catalog (N=133); "
            "no smaller sub-sample was drawn (see notes.md).")
    write_csv(os.path.join(DATA, "pilot_sample.csv"), rows, extra_cols=["note"], extra_value=note)
    print(f"wrote {len(rows)} rows to data/{{full,pilot}}_ground_truth.csv and data/pilot_sample.csv")


if __name__ == "__main__":
    main()
