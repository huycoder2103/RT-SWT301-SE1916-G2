import csv

# Papers that are in final included but NOT in the original 16-paper evidence table
new_paper_ids = [6, 51, 65, 67, 69, 70, 74, 80, 82, 86, 87, 89, 101]

# Read both CSVs to find abstracts
records = {}
for fname in [r'd:\SWT-RBL\String1-openalex_2026-06-03T16-03-30.csv', 
              r'd:\SWT-RBL\String2-openalex_2026-06-03T16-04-40.csv']:
    with open(fname, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        for row in reader:
            title = row.get('title','').strip()
            records[title] = row

# Read the 01_all_records to get mapping
with open(r'd:\SWT-RBL\SLR\01_all_records.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    id_to_title = {}
    for row in reader:
        id_to_title[int(row['id'])] = row['title']

# Print info for each new paper
for pid in new_paper_ids:
    title = id_to_title.get(pid, 'NOT FOUND')
    # Find in records
    matched = None
    for t, row in records.items():
        if t.strip() == title.strip():
            matched = row
            break
    
    if not matched:
        # Try partial match
        for t, row in records.items():
            if title[:50].lower() in t.lower():
                matched = row
                break
    
    print(f"\n{'='*100}")
    print(f"ID: {pid}")
    print(f"Title: {title}")
    if matched:
        print(f"Authors: {matched.get('authors','')[:80]}")
        print(f"Year: {matched.get('year','')}")
        print(f"Venue: {matched.get('venue','')}")
        print(f"DOI: {matched.get('doi','')}")
        abstract = matched.get('abstract','')
        print(f"Abstract ({len(abstract)} chars):")
        print(abstract[:1500] if abstract else "(NO ABSTRACT)")
    else:
        print("(NOT FOUND IN RAW CSV)")
