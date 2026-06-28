import csv
import os

SLR = r'd:\SWT-RBL\SLR'

# 1. Check file existence
required_files = [
    'search-log.md', '01_all_records.csv', '02_after_screening_v1.csv',
    '03_final_included.csv', 'ie_criteria.md', 'prisma-flow.md',
    'evidence-table.md', 'gap-statement.md'
]
exp_files = ['01_rq.md', 'hypotheses.md']

print("=== FILE EXISTENCE CHECK ===")
for f in required_files:
    path = os.path.join(SLR, f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = "OK" if exists else "MISSING"
    print(f"  [{status}] SLR/{f} ({size:,} bytes)")

for f in exp_files:
    path = os.path.join(r'd:\SWT-RBL\experiment', f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = "OK" if exists else "MISSING"
    print(f"  [{status}] experiment/{f} ({size:,} bytes)")

# 2. CSV consistency check
print("\n=== CSV CONSISTENCY CHECK ===")

# Count rows in 01
with open(os.path.join(SLR, '01_all_records.csv'), 'r', encoding='utf-8-sig') as f:
    r01 = list(csv.DictReader(f))
print(f"  01_all_records.csv rows: {len(r01)}")

# Count decisions in 02
with open(os.path.join(SLR, '02_after_screening_v1.csv'), 'r', encoding='utf-8-sig') as f:
    r02 = list(csv.DictReader(f))
v1_include = sum(1 for r in r02 if r.get('v1_decision') == 'INCLUDE')
v1_unsure = sum(1 for r in r02 if r.get('v1_decision') == 'Unsure')
v1_exclude = sum(1 for r in r02 if r.get('v1_decision') == 'EXCLUDE')
print(f"  02_after_screening_v1.csv rows: {len(r02)}")
print(f"    V1 INCLUDE: {v1_include}")
print(f"    V1 Unsure: {v1_unsure}")
print(f"    V1 EXCLUDE: {v1_exclude}")
print(f"    V1 pass (INCLUDE + Unsure): {v1_include + v1_unsure}")

# Count decisions in 03
with open(os.path.join(SLR, '03_final_included.csv'), 'r', encoding='utf-8-sig') as f:
    r03 = list(csv.DictReader(f))
v2_include = sum(1 for r in r03 if r.get('v2_decision') == 'Include')
v2_exclude = sum(1 for r in r03 if r.get('v2_decision') == 'Exclude')
print(f"  03_final_included.csv rows: {len(r03)}")
print(f"    V2 Include (final): {v2_include}")
print(f"    V2 Exclude: {v2_exclude}")

# 3. PRISMA consistency
print("\n=== PRISMA CONSISTENCY ===")
total_raw = 263
after_dedup = len(r01)
v1_pass = v1_include + v1_unsure
final = v2_include

checks = [
    (len(r01) == len(r02) == len(r03), f"All CSVs same row count: {len(r01)} == {len(r02)} == {len(r03)}"),
    (v1_exclude + v1_include + v1_unsure == after_dedup, f"V1 decisions sum = after_dedup: {v1_exclude}+{v1_include}+{v1_unsure} = {after_dedup}"),
    (v2_include + v2_exclude == v1_pass, f"V2 assessed = V1 pass: {v2_include}+{v2_exclude} = {v1_pass}"),
]

for ok, desc in checks:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")

print(f"\n=== PRISMA NUMBERS ===")
print(f"  Total raw: {total_raw}")
print(f"  After dedup: {after_dedup}")
print(f"  Duplicates removed: {total_raw - after_dedup}")
print(f"  V1 Excluded: {v1_exclude}")
print(f"  V1 Pass (assessed): {v1_pass}")
print(f"  V2 Excluded: {v2_exclude}")
print(f"  Final included: {final}")

# 4. Evidence table paper count
with open(os.path.join(SLR, 'evidence-table.md'), 'r', encoding='utf-8') as f:
    et_content = f.read()
et_paper_count = et_content.count('| ')  # rough count of table rows
# Count actual rows with paper numbers
import re
et_rows = len(re.findall(r'^\| \d+ \|', et_content, re.MULTILINE))
print(f"\n=== EVIDENCE TABLE ===")
print(f"  Papers in evidence table: {et_rows}")
print(f"  Final included in CSV: {final}")
match = "MATCH" if et_rows == final else f"MISMATCH ({et_rows} vs {final})"
print(f"  Consistency: [{match}]")
