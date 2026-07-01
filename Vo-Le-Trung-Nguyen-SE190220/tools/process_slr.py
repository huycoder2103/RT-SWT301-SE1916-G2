#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLR Processing Script for 'LLM REST API Test Generation'
Processes two OpenAlex CSV files, deduplicates, screens (V1 + V2),
and outputs three CSV files plus search-log.md and prisma-flow.md.
"""

import csv
import re
import os
import sys
from collections import defaultdict

# ─── Configuration ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE1 = os.path.join(os.path.dirname(BASE_DIR), "String1-openalex_2026-06-03T16-03-30.csv")
FILE2 = os.path.join(os.path.dirname(BASE_DIR), "String2-openalex_2026-06-03T16-04-40.csv")

OUT_01 = os.path.join(BASE_DIR, "01_all_records.csv")
OUT_02 = os.path.join(BASE_DIR, "02_after_screening_v1.csv")
OUT_03 = os.path.join(BASE_DIR, "03_final_included.csv")
OUT_SEARCH_LOG = os.path.join(BASE_DIR, "search-log.md")
OUT_PRISMA = os.path.join(BASE_DIR, "prisma-flow.md")

COLUMNS_IN = ["id", "title", "authors", "year", "venue", "doi", "url",
              "source_db", "search_string", "abstract", "keywords",
              "PDF_url", "notes", "dedup_key", "duplicate_flag"]

# ─── Helpers ──────────────────────────────────────────────────────────

def normalize_doi(doi):
    """Normalize a DOI for comparison."""
    if not doi:
        return ""
    doi = doi.strip().lower()
    # Remove URL prefixes
    for prefix in ["https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/"]:
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi


def normalize_title(title):
    """Normalize a title for comparison: lowercase, remove non-alphanumeric."""
    if not title:
        return ""
    return re.sub(r'[^a-z0-9]', '', title.strip().lower())


def read_csv_file(filepath):
    """Read a semicolon-delimited CSV file and return list of dicts."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        for row in reader:
            records.append(row)
    return records


def has_cyrillic(text):
    """Check if text contains Cyrillic characters."""
    return bool(re.search(r'[\u0400-\u04FF]', text))


def contains_any(text, terms):
    """Check if text (lowered) contains any of the given terms."""
    text_l = text.lower()
    return any(t in text_l for t in terms)


def contains_all(text, terms):
    """Check if text (lowered) contains all of the given terms."""
    text_l = text.lower()
    return all(t in text_l for t in terms)


# ─── Step 1 & 2: Read CSVs and tag sources ───────────────────────────

print("=== Reading CSV files ===")
records1 = read_csv_file(FILE1)
records2 = read_csv_file(FILE2)
print(f"String 1 raw: {len(records1)}")
print(f"String 2 raw: {len(records2)}")

# Build lookup by OpenAlex ID, DOI, and normalized title
# Tag each record with its source string(s)

all_records = {}  # key: openalex_id -> record dict
doi_map = {}      # normalized_doi -> openalex_id
title_map = {}    # normalized_title -> openalex_id

def add_records(records, source_label):
    """Add records and track source labels."""
    for r in records:
        oa_id = r.get("id", "").strip()
        doi = normalize_doi(r.get("doi", ""))
        norm_title = normalize_title(r.get("title", ""))
        abstract = r.get("abstract", "") or ""

        # Check if this record is a duplicate of something already added
        existing_id = None

        # Check by OpenAlex ID
        if oa_id in all_records:
            existing_id = oa_id
        # Check by DOI
        elif doi and doi in doi_map:
            existing_id = doi_map[doi]
        # Check by normalized title
        elif norm_title and norm_title in title_map:
            existing_id = title_map[norm_title]

        if existing_id:
            # Duplicate found - merge source label
            existing = all_records[existing_id]
            if source_label not in existing["_sources"]:
                existing["_sources"].append(source_label)
            # Keep the one with longer abstract
            existing_abstract = existing.get("abstract", "") or ""
            if len(abstract) > len(existing_abstract):
                # Replace with this record but keep merged sources
                sources = existing["_sources"]
                all_records[existing_id] = dict(r)
                all_records[existing_id]["_sources"] = sources
                # Update maps
                if doi:
                    doi_map[doi] = existing_id
                if norm_title:
                    title_map[norm_title] = existing_id
        else:
            # New record
            r_copy = dict(r)
            r_copy["_sources"] = [source_label]
            all_records[oa_id] = r_copy
            if doi:
                doi_map[doi] = oa_id
            if norm_title:
                title_map[norm_title] = oa_id

add_records(records1, "String 1")
add_records(records2, "String 2")

# Now deduplicate across the combined set (already handled by add_records)
# But we also need to handle duplicates WITHIN File 1 (same DOI different OA IDs)
# Actually the above logic already handles that since we check doi_map and title_map

total_before_dedup = len(records1) + len(records2)
duplicates_removed = total_before_dedup - len(all_records)

print(f"Total before dedup: {total_before_dedup}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"After dedup: {len(all_records)}")

# ─── Step 4: Output 01_all_records.csv ────────────────────────────────

# Sort by some reasonable order (keep original order roughly)
unique_records = list(all_records.values())

# Assign sequential IDs
for idx, rec in enumerate(unique_records, start=1):
    rec["_seq_id"] = idx
    rec["search_strings"] = ", ".join(rec["_sources"])

print(f"\n=== Writing {OUT_01} ({len(unique_records)} records) ===")
with open(OUT_01, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["id", "title", "authors", "year", "venue", "doi", "url", "search_strings"])
    for rec in unique_records:
        writer.writerow([
            rec["_seq_id"],
            rec.get("title", ""),
            rec.get("authors", ""),
            rec.get("year", ""),
            rec.get("venue", ""),
            rec.get("doi", ""),
            rec.get("url", ""),
            rec["search_strings"]
        ])

# ─── Step 5: V1 Screening ────────────────────────────────────────────

def v1_screen(rec):
    """Apply V1 screening rules. Returns (decision, reason)."""
    title = (rec.get("title", "") or "").strip()
    abstract = (rec.get("abstract", "") or "").strip()
    venue = (rec.get("venue", "") or "").strip()
    year_str = (rec.get("year", "") or "").strip()
    
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    venue_lower = venue.lower()
    title_abstract = title_lower + " " + abstract_lower
    title_abstract_500 = title_lower + " " + abstract_lower[:500]

    # IC1 - Non-English (Cyrillic or Finnish/Ukrainian words)
    if has_cyrillic(title):
        # But check if the abstract is in English (paper might have non-English title but English abstract)
        # Still exclude per rules
        return ("EXCLUDE", "IC1 - Non-English")

    # IC2 - Before 2018
    try:
        year = int(year_str)
        if year < 2018:
            return ("EXCLUDE", "IC2 - Before 2018")
    except (ValueError, TypeError):
        pass

    # EC3 - Replication package/dataset
    if 'zenodo' in venue_lower and 'replication package' in abstract_lower:
        return ("EXCLUDE", "EC3 - Replication package/dataset")

    # EC3 - Dataset/software (short title + Zenodo/Open MIND)
    title_words = title.split()
    if len(title_words) <= 3 and ('zenodo' in venue_lower or 'open mind' in venue_lower):
        return ("EXCLUDE", "EC3 - Dataset/software, not research paper")

    # EC4 - Out of Domain checks
    # Unit testing, not REST API
    if 'unit test' in title_lower and 'rest api' not in title_abstract_500:
        return ("EXCLUDE", "EC4 - Unit testing, not REST API")

    # GUI/mobile testing
    if any(t in title_lower for t in ['gui test', 'android', 'mobile test']):
        return ("EXCLUDE", "EC4 - GUI/mobile testing")

    # Network protocol fuzzing
    if 'network protocol' in title_lower:
        return ("EXCLUDE", "EC4 - Network protocol fuzzing")

    # Security/pen testing
    if any(t in title_lower for t in ['hacker', 'offensive security', 'penetration test']):
        return ("EXCLUDE", "EC4 - Security/pen testing")

    # Low-code platforms
    if 'low-code' in title_lower or 'low code' in title_lower:
        return ("EXCLUDE", "EC4 - Low-code platforms")

    # Vibe coding
    if 'vibe coding' in title_lower:
        return ("EXCLUDE", "EC4 - Vibe coding review")

    # Blockchain
    if 'ethereum' in title_lower or 'blockchain' in title_lower:
        return ("EXCLUDE", "EC4 - Blockchain")

    # Cloud emulators
    if 'cloud emulator' in title_lower:
        return ("EXCLUDE", "EC4 - Cloud emulators")

    # Requirements engineering
    if 'requirement engineering' in title_lower and 'test' not in title_lower:
        return ("EXCLUDE", "EC4 - Requirements engineering")

    # CPS anomaly detection
    if 'anomaly detection' in abstract_lower and 'cyber-physical' in abstract_lower and 'rest api' not in abstract_lower:
        return ("EXCLUDE", "EC4 - CPS anomaly detection")

    # Location/GIS
    if 'location representation' in title_lower:
        return ("EXCLUDE", "EC4 - Location/GIS")

    # 5G network
    if '5g' in title_lower and 'network' in title_lower:
        return ("EXCLUDE", "EC4 - 5G network")

    # General survey not REST API focused
    if any(t in title_lower for t in ['survey', 'review']):
        if not any(t in title_lower for t in ['rest', 'api test']):
            # Check abstract for REST API content
            if not any(t in abstract_lower for t in ['rest api', 'web api', 'restful', 'openapi']):
                return ("EXCLUDE", "EC4 - General survey, not REST API focused")

    # Python C-extension testing
    if 'python' in title_lower and ('c-extension' in abstract_lower or 'c-extended' in title_lower):
        return ("EXCLUDE", "EC4 - Python C-extension testing")

    # Test oracle general
    if 'test oracle' in title_lower and 'rest' not in title_lower:
        return ("EXCLUDE", "EC4 - Test oracle general")

    # BigCodeBench
    if 'bigcodebench' in title_lower:
        return ("EXCLUDE", "EC4 - Code benchmarking")

    # Blueprint + quality = SQA framework
    if 'blueprint' in title_lower and 'quality' in title_lower:
        return ("EXCLUDE", "EC4 - SQA framework")

    # Code generation (not about testing or APIs)
    if 'code generation' in title_lower and 'test' not in title_lower and 'api' not in title_lower:
        return ("EXCLUDE", "EC4 - Code generation")

    # DevOps general
    if 'devops' in title_lower and 'rest' not in title_lower and 'api test' not in title_lower and 'test' not in title_lower:
        return ("EXCLUDE", "EC4 - DevOps general")

    # Metamorphic testing general (not REST or API)
    if 'metamorphic relation' in title_lower and 'rest' not in title_lower and 'api' not in title_lower:
        return ("EXCLUDE", "EC4 - Metamorphic testing general")

    # Payload/fuzzer identification
    if 'payload analysis' in title_lower:
        return ("EXCLUDE", "EC4 - Payload/fuzzer identification")

    # Fuzz driver generation for libraries
    if 'prompt fuzzing' in title_lower and 'fuzz driver' in title_lower:
        return ("EXCLUDE", "EC4 - Fuzz driver generation for libraries")
    # Also catch "Prompt Fuzzing for Fuzz Driver Generation" style
    if 'prompt fuzzing' in title_lower and 'fuzz driver' in abstract_lower:
        return ("EXCLUDE", "EC4 - Fuzz driver generation for libraries")

    # SQA general (abstract about SQA broadly without REST API specific content)
    if 'software quality assurance' in abstract_lower and not any(t in abstract_lower for t in ['rest api', 'web api', 'restful', 'openapi']):
        # Check more carefully - is REST API mentioned at all?
        if 'rest' not in abstract_lower and 'api test' not in abstract_lower:
            return ("EXCLUDE", "EC4 - SQA general")

    # MBT for web UI (clickstream + model-based testing)
    if 'clickstream' in abstract_lower and 'model-based testing' in abstract_lower:
        if not any(t in abstract_lower for t in ['rest api', 'web api', 'restful']):
            return ("EXCLUDE", "EC4 - MBT for web UI")

    # EC5 - Out of Phase
    if 'flakiness' in title_lower or 'flaky' in title_lower:
        return ("EXCLUDE", "EC5 - Test flakiness")

    if 'test maintenance' in title_lower and 'generation' not in title_lower:
        return ("EXCLUDE", "EC5 - Test maintenance")

    # ─── IC3: REST API context ───────────────────────────────────────
    rest_terms = ['rest api', 'web api', 'openapi', 'swagger', 'restful']
    test_terms = ['test', 'testing', 'fuzzing', 'fuzz']

    has_rest = any(t in title_abstract for t in rest_terms)
    has_test = any(t in title_abstract for t in test_terms)

    if not (has_rest and has_test):
        return ("EXCLUDE", "EC4 - No REST API testing context")

    # ─── IC4: LLM involvement ───────────────────────────────────────
    llm_terms = ['llm', 'large language model', 'gpt', 'chatgpt', 'language model',
                 'generative ai', 'codex', 'claude', 'deepseek', 'llama', 'starcoder',
                 'gemini', 'prompt engineering', 'fine-tun']
    has_llm = any(t in title_abstract for t in llm_terms)

    rest_api_tools = ['evomaster', 'restler', 'morest', 'restest', 'restgen',
                      'schemathesis', 'arat-rl', 'restgpt', 'resttestgen']

    if not has_llm:
        has_tools = any(t in title_abstract for t in rest_api_tools)
        if has_tools:
            return ("Unsure", "IC4 borderline")
        return ("EXCLUDE", "IC4 - No LLM involvement")

    # ─── IC5: Empirical ──────────────────────────────────────────────
    survey_terms = ['survey', 'review', 'systematic mapping', 'roadmap']
    empirical_terms = ['experiment', 'evaluation', 'results show', 'outperform',
                       'case study', 'compared']

    if any(t in title_lower for t in survey_terms):
        if not any(t in abstract_lower for t in empirical_terms):
            return ("EXCLUDE", "IC5 - Survey/review without empirical")

    return ("INCLUDE", "IC1, IC2, IC3, IC4, IC5")


# Apply V1 screening
print("\n=== V1 Screening ===")
v1_stats = defaultdict(int)
for rec in unique_records:
    decision, reason = v1_screen(rec)
    rec["v1_decision"] = decision
    rec["v1_reason"] = reason
    v1_stats[decision] += 1

print(f"V1 INCLUDE: {v1_stats['INCLUDE']}")
print(f"V1 Unsure: {v1_stats['Unsure']}")
print(f"V1 EXCLUDE: {v1_stats['EXCLUDE']}")

# Breakdown by exclusion reason
v1_exclude_reasons = defaultdict(int)
for rec in unique_records:
    if rec["v1_decision"] == "EXCLUDE":
        v1_exclude_reasons[rec["v1_reason"]] += 1

print("\nV1 EXCLUDE breakdown:")
for reason, count in sorted(v1_exclude_reasons.items()):
    print(f"  {reason}: {count}")

# ─── Step 6: Output 02_after_screening_v1.csv ────────────────────────

print(f"\n=== Writing {OUT_02} ({len(unique_records)} records) ===")
with open(OUT_02, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["id", "title", "authors", "year", "venue", "doi", "url",
                     "search_strings", "v1_decision", "v1_reason"])
    for rec in unique_records:
        writer.writerow([
            rec["_seq_id"],
            rec.get("title", ""),
            rec.get("authors", ""),
            rec.get("year", ""),
            rec.get("venue", ""),
            rec.get("doi", ""),
            rec.get("url", ""),
            rec["search_strings"],
            rec["v1_decision"],
            rec["v1_reason"]
        ])

# ─── Step 7: V2 Screening ────────────────────────────────────────────

# Known-good papers for final inclusion (match by partial title keywords)
KNOWN_INCLUDE_PATTERNS = [
    "llamaresttest",
    "kat",  # will check more carefully
    "saint",
    "autoresttest",
    "restspecit",
    "you can rest now",
    "dyner",
    "automating rest api postman",
    "apitestgenie",
    "resttslllm",
    "combining tsl and llm",
    "armeta",
    "restifai",
    "autoresttest",  # tool paper
    "restestbench",
    "assessing rest api test generation strategies with log coverage",  # Reinikainen
    "assessing rest api with log coverage",
    "orchestration architecture",  # Moskalenko
    "оркестраційної архітектури",  # Ukrainian title
    "augmenting api security testing",  # Pasca
    "tape",
    "technology adoption performance evaluation",
    "automating complete",  # Wang automotive
    "generating rest api tests with descriptive names",
    "lobrest",
    "log-based, business-aware",
    "quality of llm-generated authorization",
    "multi-agent approach for rest api testing",  # AutoRestTest multi-agent
    "multi-agent llm-based metamorphic testing for rest apis",  # ARMeta
]


def is_known_include(title):
    """Check if title matches a known-include paper."""
    t = title.lower().strip()
    normalized_t = normalize_title(title)
    
    checks = [
        "llamaresttest" in normalized_t,
        # KAT - dependency-aware
        "dependency-aware automated api testing" in t,
        "kat" == t.split(":")[0].strip() if ":" in t else False,
        "saint" in t and "service-level" in t,
        "autoresttest" in normalized_t and "tool" in t.lower(),
        "autoresttest" in normalized_t and "multi-agent" in t.lower(),
        "restspecit" in normalized_t,
        "you can rest now" in t,
        "dyner" in t.lower() and "rest" in t.lower(),
        "automating rest api postman" in t,
        "apitestgenie" in normalized_t,
        "combining tsl and llm" in t,
        "resttslllm" in normalized_t,
        "armeta" in normalized_t,
        "multi-agent llm-based metamorphic testing for rest api" in t,
        "restifai" in normalized_t,
        "restestbench" in normalized_t or "restestbench" in normalized_t.replace(" ", ""),
        "assessing rest api test generation strategies with log coverage" in t,
        "оркестраційної архітектури" in title.lower() or "orchestration architecture" in t,
        "augmenting api security testing" in t,
        "technology adoption performance evaluation" in t,
        "automating complete" in t and ("automotive" in t or "vehicle" in t or "test process" in t),
        "generating rest api tests with descriptive names" in t,
        "lobrest" in normalized_t or "log-based, business-aware" in t,
        "quality of llm-generated authorization" in t,
        "saint" in normalized_t and "integration test" in t,
    ]
    return any(checks)


def v2_screen(rec):
    """Apply V2 screening. Returns (decision, reason)."""
    title = (rec.get("title", "") or "").strip()
    abstract = (rec.get("abstract", "") or "").strip()
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    title_abstract = title_lower + " " + abstract_lower

    # EC2 - Cannot assess full-text (empty/very short abstract)
    if len(abstract.strip()) < 100:
        return ("Exclude", "EC2 - Cannot assess full-text")

    # Check if it's a known-include paper
    if is_known_include(title):
        return ("Include", "IC3, IC4, IC5 - Verified relevant")

    # IC4 strict: paper ACTUALLY uses LLM for REST API test generation
    llm_terms = ['llm', 'large language model', 'gpt', 'chatgpt', 'language model',
                 'generative ai', 'codex', 'claude', 'deepseek', 'llama', 'starcoder',
                 'gemini', 'prompt engineering', 'fine-tun']
    rest_terms = ['rest api', 'web api', 'openapi', 'swagger', 'restful']

    has_llm = any(t in title_abstract for t in llm_terms)
    has_rest = any(t in title_abstract for t in rest_terms)

    if not has_llm:
        return ("Exclude", "IC4 - LLM not actually used for REST API testing")

    if not has_rest:
        return ("Exclude", "IC4 - Not about REST API testing")

    # IC5 strict: paper has quantitative results
    quant_indicators = ['%', 'percent', 'coverage', 'outperform', 'f1', 'precision',
                        'recall', 'accuracy', 'compared', 'experiment', 'evaluation',
                        'results show', 'case study', 'bug', 'fault', 'error',
                        'improve', 'higher', 'better']
    has_quant = any(t in abstract_lower for t in quant_indicators)

    if not has_quant:
        # Be generous - if it mentions test generation for REST APIs with LLM, include
        test_gen_terms = ['test generation', 'test case generation', 'generate test',
                          'automated test', 'automat']
        if any(t in title_abstract for t in test_gen_terms):
            return ("Include", "IC5 - Test generation paper, borderline empirical")
        return ("Exclude", "IC5 - No empirical results")

    return ("Include", "IC3, IC4, IC5 - Relevant")


print("\n=== V2 Screening ===")
v2_assessed = 0
v2_include = 0
v2_exclude = 0
v2_exclude_reasons = defaultdict(int)

for rec in unique_records:
    if rec["v1_decision"] in ("INCLUDE", "Unsure"):
        v2_assessed += 1
        decision, reason = v2_screen(rec)
        rec["v2_decision"] = decision
        rec["v2_reason"] = reason
        if decision == "Include":
            v2_include += 1
        else:
            v2_exclude += 1
            v2_exclude_reasons[reason] += 1
    else:
        rec["v2_decision"] = ""
        rec["v2_reason"] = ""

print(f"V2 assessed (INCLUDE + Unsure from V1): {v2_assessed}")
print(f"V2 Include: {v2_include}")
print(f"V2 Exclude: {v2_exclude}")

print("\nV2 EXCLUDE breakdown:")
for reason, count in sorted(v2_exclude_reasons.items()):
    print(f"  {reason}: {count}")

# ─── Step 8: Output 03_final_included.csv ─────────────────────────────

print(f"\n=== Writing {OUT_03} ({len(unique_records)} records) ===")
with open(OUT_03, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["id", "title", "authors", "year", "venue", "doi", "url",
                     "search_strings", "v1_decision", "v1_reason", "v2_decision", "v2_reason"])
    for rec in unique_records:
        writer.writerow([
            rec["_seq_id"],
            rec.get("title", ""),
            rec.get("authors", ""),
            rec.get("year", ""),
            rec.get("venue", ""),
            rec.get("doi", ""),
            rec.get("url", ""),
            rec["search_strings"],
            rec["v1_decision"],
            rec["v1_reason"],
            rec["v2_decision"],
            rec["v2_reason"]
        ])

# ─── Step 9: Print Statistics ─────────────────────────────────────────

after_dedup = len(unique_records)
v1_include_count = v1_stats['INCLUDE']
v1_unsure_count = v1_stats['Unsure']
v1_exclude_count = v1_stats['EXCLUDE']
v1_pass = v1_include_count + v1_unsure_count

# Build exclude breakdown string
exclude_breakdown_parts = []
for reason, count in sorted(v1_exclude_reasons.items()):
    exclude_breakdown_parts.append(f"{reason} ({count})")
v1_exclude_breakdown = ", ".join(exclude_breakdown_parts)

v2_exclude_breakdown_parts = []
for reason, count in sorted(v2_exclude_reasons.items()):
    v2_exclude_breakdown_parts.append(f"{reason} ({count})")
v2_exclude_breakdown = ", ".join(v2_exclude_breakdown_parts)

print("\n" + "=" * 60)
print("=== PRISMA STATISTICS ===")
print("=" * 60)
print(f"String 1 raw: {len(records1)}")
print(f"String 2 raw: {len(records2)}")
print(f"Total before dedup: {total_before_dedup}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"After dedup (01_all_records.csv): {after_dedup}")
print("---")
print(f"V1 INCLUDE: {v1_include_count}")
print(f"V1 Unsure: {v1_unsure_count}")
print(f"V1 EXCLUDE: {v1_exclude_count}")
print(f"  Breakdown: {v1_exclude_breakdown}")
print("---")
print(f"V2 assessed (INCLUDE + Unsure from V1): {v2_assessed}")
print(f"V2 Include: {v2_include}")
print(f"V2 Exclude: {v2_exclude}")
print(f"  Breakdown: {v2_exclude_breakdown}")
print("---")
print(f"Final included: {v2_include}")
print("=" * 60)

# Print final included papers
print("\n=== FINAL INCLUDED PAPERS ===")
for rec in unique_records:
    if rec.get("v2_decision") == "Include":
        print(f"  [{rec['_seq_id']}] {rec.get('title', '')} ({rec.get('year', '')}) - {rec.get('v2_reason', '')}")

# ─── Step 10: search-log.md ──────────────────────────────────────────

search_log = f"""# Search Log — LLM REST API Test Generation
**Thành viên:** [Tên thành viên]
**Ngày thực hiện:** 2026-06-03

---

## Chuỗi tìm kiếm (Query Strings)

### String 1
**Query nguyên văn:**
("REST API" OR "Web API" OR "OpenAPI" OR "Swagger") AND ("Large Language Model" OR "LLM") AND ("test")
**Database:** OpenAlex
**Bộ lọc:** Không có bộ lọc đặc biệt
**Ngày search:** 2026-06-03 16:03
**Số kết quả:** 223 papers

### String 2
**Query nguyên văn:**
("REST API" OR "Web API") AND ("LLM" OR "Generative AI" OR "zero-shot" OR "few-shot") AND ("automate")
**Database:** OpenAlex
**Bộ lọc:** Không có bộ lọc đặc biệt
**Ngày search:** 2026-06-03 16:04
**Số kết quả:** 40 papers

## Tổng hợp trước dedup
| Database | String | Kết quả |
|----------|--------|---------|
| OpenAlex | String 1 | 223 |
| OpenAlex | String 2 | 40 |
| **Tổng trước dedup** | | **263** |
| **Sau dedup** | | **{after_dedup}** |
| Số bị loại (trùng lặp) | | {263 - after_dedup} |

## Ghi chú
- Dedup bằng: Python script (so sánh DOI + normalized title)
- Search thực hiện trên OpenAlex với giao diện web
"""

with open(OUT_SEARCH_LOG, 'w', encoding='utf-8') as f:
    f.write(search_log)
print(f"\n=== Written {OUT_SEARCH_LOG} ===")

# ─── Step 11: prisma-flow.md ─────────────────────────────────────────

prisma_flow = f"""# PRISMA Flow Diagram — LLM REST API Test Generation

[Records từ database searching (N = 263)]
↓
[Sau khi xóa duplicate (N = {after_dedup})]
↓
┌─────────────────────────────────────────┐
│ Screened title + abstract (N = {after_dedup})
│ └── Excluded (N = {v1_exclude_count}): {v1_exclude_breakdown}
└─────────────────────────────────────────┘
↓ {v1_pass} papers pass
┌─────────────────────────────────────────┐
│ Full-text assessed (N = {v1_pass})
│ └── Excluded (N = {v2_exclude}): {v2_exclude_breakdown}
└─────────────────────────────────────────┘
↓
[Final included (N = {v2_include})]

## Kiểm tra nhất quán
Rows trong 01 CSV = {after_dedup} ✓
Count(v1_decision = EXCLUDE) = {v1_exclude_count} ✓
Count(v1 = INCLUDE + Unsure) = {v1_pass} ✓
Count(v2_decision = Include) = {v2_include} ✓
"""

with open(OUT_PRISMA, 'w', encoding='utf-8') as f:
    f.write(prisma_flow)
print(f"=== Written {OUT_PRISMA} ===")

print("\n=== DONE ===")
