#!/usr/bin/env python3
"""
Master baseline aggregator.

Pulls EVERY metric produced by the experiment into ONE place so a reviewer can see,
per (SUT x arm): number of test cases, requests issued, real 2xx/4xx/5xx outcomes,
endpoint coverage, edge-case scenarios, mutation fault-recall, and triggered error
behaviours -- with the two BASELINES (human Manual, tool EvoMaster) shown next to the
proposed LLM arm.

Outputs:
  results/stats/master_summary.csv   (machine-readable, one row per SUT x arm + TOTAL)
  BASELINE-SUMMARY.md                 (reviewer-facing document)
Reads: harness *.java (@Test counts), results/raw/{traffic,coverage,scenarios,error_missed}.csv,
       results/stats/summary.json
"""
import csv, json, os, re, collections

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../experiment
HARNESS = os.path.join(ROOT, 'harness', 'src', 'test', 'java')
RAW     = os.path.join(ROOT, 'results', 'raw')
STATS   = os.path.join(ROOT, 'results', 'stats')

SUTS = ['ncs', 'scs', 'features']
ARMS = ['llm', 'manual', 'evomaster']
ROLE = {'llm': 'Proposed — LLM (Claude Sonnet 4.6)',
        'manual': 'Baseline 1 — Human (black-box, EP+BVA)',
        'evomaster': 'Baseline 2 — Tool (EvoMaster 6.0, SOTA white-box fuzzer)'}
FILES = {
  'llm':       {'ncs': ['llm/NcsLlmTests.java'], 'scs': ['llm/ScsLlmTests.java'], 'features': ['llm/FeaturesLlmTests.java']},
  'manual':    {'ncs': ['manual/NcsManualTests.java'], 'scs': ['manual/ScsManualTests.java'], 'features': ['manual/FeaturesManualTests.java']},
  'evomaster': {'ncs': ['evomaster/NcsEvoSuccessesTests.java', 'evomaster/NcsEvoOthersTests.java'],
                'scs': ['evomaster/ScsEvoSuccessesTests.java', 'evomaster/ScsEvoFaultsTests.java'],
                'features': ['evomaster/FeaturesEvoSuccessesTests.java', 'evomaster/FeaturesEvoFaultsTests.java']},
}

def count_tests(files):
    n = 0
    for rel in files:
        p = os.path.join(HARNESS, rel)
        if os.path.exists(p):
            n += len(re.findall(r'@Test\b', open(p, encoding='utf-8', errors='replace').read()))
    return n

def load_csv(path):
    return list(csv.DictReader(open(path, encoding='utf-8'))) if os.path.exists(path) else []

# --- gather ---
tests = {(a, s): count_tests(FILES[a][s]) for a in ARMS for s in SUTS}

SPEC_OF = {'ncs': 'rest-ncs.openapi.json', 'scs': 'rest-scs.openapi.json', 'features': 'features-service.openapi.json'}
def _spec_paths(sut):
    p = os.path.join(ROOT, 'specs', SPEC_OF[sut])
    return json.load(open(p, encoding='utf-8')).get('paths', {}) if os.path.exists(p) else {}
endpoints = {s: sum(1 for _, ms in _spec_paths(s).items() for m in ms if m.lower() in ('get', 'post', 'put', 'delete', 'patch')) for s in SUTS}
npaths = {s: len(_spec_paths(s)) for s in SUTS}

traffic = collections.defaultdict(lambda: collections.Counter())   # (sut,arm) -> 2xx/4xx/5xx/req
for r in load_csv(os.path.join(RAW, 'traffic.csv')):
    sut, arm = r['tag'].split(':', 1); code = int(r['status'])
    traffic[(sut, arm)]['req'] += 1
    k = '2xx' if code < 300 else '4xx' if code < 500 else '5xx' if code < 600 else 'oth'
    traffic[(sut, arm)][k] += 1

cov = {(r['sut'], r['arm']): r.get('coverage_pct', '') for r in load_csv(os.path.join(RAW, 'coverage.csv'))}

edge = collections.Counter()                                       # (sut,arm) -> neg+bnd+err
for r in load_csv(os.path.join(RAW, 'scenarios.csv')):
    if r['type'] in ('negative', 'boundary', 'errorcode'):
        edge[(r['sut'], r['arm'])] += int(r['count'])

# error behaviours triggered (documented; from error_missed.csv) + answer-key per sut
em = [r for r in load_csv(os.path.join(RAW, 'error_missed.csv')) if r['op'] != 'UNKNOWN']
trig = {(r['sut'], r['arm']): len([c for c in r['triggered'].split(';') if c and c != '-'])
        for r in em}
trig = collections.Counter()
keyset = collections.defaultdict(dict)
for r in em:
    trig[(r['sut'], r['arm'])] += len([c for c in r['triggered'].split(';') if c and c != '-'])
    keyset[r['sut']][r['op']] = [c for c in r['answer_key_codes'].split(';') if c]
errkey = {s: sum(len(v) for v in keyset[s].values()) for s in SUTS}

summary = json.load(open(os.path.join(STATS, 'summary.json'), encoding='utf-8')) if os.path.exists(os.path.join(STATS, 'summary.json')) else {}
recall = summary.get('RQ2_fault_detection', {}).get('per_sut_recall', {})

# --- master rows ---
COLS = ['sut', 'arm', 'role', 'endpoints', 'test_cases', 'requests', 'http_2xx', 'http_4xx', 'http_5xx',
        'endpoint_coverage_pct', 'edge_scenarios', 'fault_recall', 'err_behaviours_triggered', 'err_behaviours_in_key']
rows = []
for s in SUTS:
    for a in ARMS:
        t = traffic[(s, a)]
        rows.append({'sut': s, 'arm': a, 'role': ROLE[a], 'endpoints': endpoints[s], 'test_cases': tests[(a, s)],
                     'requests': t['req'], 'http_2xx': t['2xx'], 'http_4xx': t['4xx'], 'http_5xx': t['5xx'],
                     'endpoint_coverage_pct': cov.get((s, a), ''), 'edge_scenarios': edge[(s, a)],
                     'fault_recall': recall.get(s, {}).get(a, ''),
                     'err_behaviours_triggered': trig[(s, a)], 'err_behaviours_in_key': errkey[s]})
# TOTAL per arm
for a in ARMS:
    agg = {'sut': 'ALL', 'arm': a, 'role': ROLE[a], 'endpoints': sum(endpoints.values()),
           'test_cases': sum(tests[(a, s)] for s in SUTS),
           'requests': sum(traffic[(s, a)]['req'] for s in SUTS),
           'http_2xx': sum(traffic[(s, a)]['2xx'] for s in SUTS),
           'http_4xx': sum(traffic[(s, a)]['4xx'] for s in SUTS),
           'http_5xx': sum(traffic[(s, a)]['5xx'] for s in SUTS),
           'endpoint_coverage_pct': '', 'edge_scenarios': sum(edge[(s, a)] for s in SUTS),
           'fault_recall': summary.get('RQ2_fault_detection', {}).get('overall_recall', {}).get(a, ''),
           'err_behaviours_triggered': sum(trig[(s, a)] for s in SUTS),
           'err_behaviours_in_key': sum(errkey[s] for s in SUTS)}
    rows.append(agg)

os.makedirs(STATS, exist_ok=True)
with open(os.path.join(STATS, 'master_summary.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)

# --- reviewer document ---
def tot(a, k): return next(r for r in rows if r['sut'] == 'ALL' and r['arm'] == a)[k]
rq1 = summary.get('RQ1_endpoint_coverage', {}); rq3 = summary.get('RQ3_edge_cases_llm_vs_manual', {})
rq2 = summary.get('RQ2_fault_detection', {})
md = []
md.append('# Baseline & Consolidated Metrics — Gap-M Experiment\n')
md.append('**Member:** Nguyen Tien Dung (SE190034) · **Generated by:** `experiment/scripts/baseline_summary.py` · auto-aggregated, do not hand-edit.\n')
md.append('## 1. Baselines used (what we compare against, and why)\n')
md.append('| Arm | Role | What it is |')
md.append('|-----|------|-----------|')
md.append('| **LLM** | *Proposed method* | Claude Sonnet 4.6, blind black-box (spec-only). |')
md.append('| **Manual** | **Baseline 1 (human)** | Human black-box suite via Equivalence Partitioning + Boundary-Value Analysis — the conventional practice every QA course teaches. |')
md.append('| **EvoMaster 6.0** | **Baseline 2 (tool, SOTA)** | The de-facto state-of-the-art automated REST test generator; the fuzzer the EMB/WFD benchmark was built for. Standard baseline in REST-API-testing papers. |')
md.append('\nEMB/WFD ships **no pre-computed numbers** (targets + JaCoCo/driver tooling only); every figure below is generated by running these three arms on the same SUTs.\n')
md.append('\n**Scope under test: %d endpoints (operations)** = ncs %s + scs %s + features %s, over %d URL paths, 3 SUTs.\n' % (
    sum(endpoints.values()), endpoints['ncs'], endpoints['scs'], endpoints['features'], sum(npaths.values())))
md.append('## 2. Consolidated totals (all 3 SUTs)\n')
md.append('| Metric | LLM (proposed) | Manual (baseline) | EvoMaster (baseline) |')
md.append('|--------|---------------:|------------------:|---------------------:|')
md.append('| **Test cases authored** | %s | %s | %s |' % (tot('llm','test_cases'), tot('manual','test_cases'), tot('evomaster','test_cases')))
md.append('| Requests issued (live) | %s | %s | %s |' % (tot('llm','requests'), tot('manual','requests'), tot('evomaster','requests')))
md.append('| HTTP 2xx | %s | %s | %s |' % (tot('llm','http_2xx'), tot('manual','http_2xx'), tot('evomaster','http_2xx')))
md.append('| **HTTP 4xx (client errors hit)** | %s | %s | %s |' % (tot('llm','http_4xx'), tot('manual','http_4xx'), tot('evomaster','http_4xx')))
md.append('| **HTTP 5xx (server crashes hit)** | %s | %s | %s |' % (tot('llm','http_5xx'), tot('manual','http_5xx'), tot('evomaster','http_5xx')))
md.append('| Edge-case scenarios (neg+bnd+err) | %s | %s | %s |' % (tot('llm','edge_scenarios'), tot('manual','edge_scenarios'), tot('evomaster','edge_scenarios')))
md.append('| Mutation fault-recall (overall) | %s | %s | %s |' % (tot('llm','fault_recall'), tot('manual','fault_recall'), tot('evomaster','fault_recall')))
md.append('| Error behaviours triggered / %d | %s | %s | %s |' % (tot('llm','err_behaviours_in_key'), tot('llm','err_behaviours_triggered'), tot('manual','err_behaviours_triggered'), tot('evomaster','err_behaviours_triggered')))
md.append('\n## 3. Statistical verdicts (from results/stats/summary.json)\n')
md.append('- **RQ1 endpoint coverage:** LLM %.1f%% over %s operations (H0 coverage>90%% %s, p=%s).' % (
    rq1.get('coverage_overall_pct', 0), rq1.get('n_operations', '?'),
    'rejected→PASS' if rq1.get('reject_H0_(coverage>90%)') else 'not rejected', rq1.get('p_value_one_sided', '?')))
md.append('- **RQ3 edge-case scenarios:** LLM %s vs Manual %s (median/op %s vs %s), Wilcoxon p=%s; LLM>Manual on %s/%s operations.' % (
    rq3.get('llm_total_edge'), rq3.get('manual_total_edge'), rq3.get('llm_median_per_op'), rq3.get('manual_median_per_op'),
    rq3.get('p_value_one_sided'), rq3.get('pairs_llm_more'), rq3.get('n_operations')))
md.append('- **RQ2 fault-detection (mutation recall, %s mutants):** EvoMaster %s > LLM %s = Manual %s; Friedman p=%s.' % (
    rq2.get('n_mutants_total'), rq2.get('overall_recall', {}).get('evomaster'), rq2.get('overall_recall', {}).get('llm'),
    rq2.get('overall_recall', {}).get('manual'), rq2.get('friedman_p')))
md.append('- **Outcome error-profile (documented behaviours, see REPORT-error-profile.md):** LLM %s/%s, Manual %s/%s, EvoMaster %s/%s.' % (
    tot('llm','err_behaviours_triggered'), tot('llm','err_behaviours_in_key'),
    tot('manual','err_behaviours_triggered'), tot('manual','err_behaviours_in_key'),
    tot('evomaster','err_behaviours_triggered'), tot('evomaster','err_behaviours_in_key')))
md.append('\n## 4. Per-SUT × arm breakdown — full table in `results/stats/master_summary.csv`\n')
md.append('| SUT | Arm | Endpoints | Tests | Req | 2xx | 4xx | 5xx | Cov% | Edge | Recall | ErrTrig |')
md.append('|-----|-----|----------:|------:|----:|----:|----:|----:|-----:|-----:|-------:|--------:|')
for r in rows:
    if r['sut'] == 'ALL': continue
    md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s/%s |' % (
        r['sut'], r['arm'], r['endpoints'], r['test_cases'], r['requests'], r['http_2xx'], r['http_4xx'], r['http_5xx'],
        r['endpoint_coverage_pct'], r['edge_scenarios'], r['fault_recall'], r['err_behaviours_triggered'], r['err_behaviours_in_key']))
md.append('\n## 5. Regenerate\n```bash\npython experiment/scripts/baseline_summary.py   # rebuilds master_summary.csv + this file\n```\n')
open(os.path.join(ROOT, 'BASELINE-SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(md))

print('Wrote results/stats/master_summary.csv  and  experiment/BASELINE-SUMMARY.md')
print('\nTOTALS  (test cases | requests | 4xx | 5xx | edge | recall | err-behav)')
for a in ARMS:
    print('  %-9s  %4s | %4s | %3s | %3s | %3s | %-7s | %s/%s' % (
        a, tot(a,'test_cases'), tot(a,'requests'), tot(a,'http_4xx'), tot(a,'http_5xx'),
        tot(a,'edge_scenarios'), tot(a,'fault_recall'), tot(a,'err_behaviours_triggered'), tot(a,'err_behaviours_in_key')))
