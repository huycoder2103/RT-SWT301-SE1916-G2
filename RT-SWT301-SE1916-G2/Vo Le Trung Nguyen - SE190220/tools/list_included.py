import csv

with open(r'd:\SWT-RBL\SLR\03_final_included.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    papers = []
    for row in reader:
        if row.get('v2_decision') == 'Include':
            papers.append(row)

print(f"Total final included: {len(papers)}\n")
print(f"{'ID':>3} | {'Title':<85} | {'Year':>4} | {'DOI':<45} | {'Strings'}")
print("-" * 200)
for p in papers:
    title = p.get('title','')[:85]
    doi = p.get('doi','')[:45]
    strings = p.get('search_strings','')
    print(f"{p['id']:>3} | {title:<85} | {p['year']:>4} | {doi:<45} | {strings}")
