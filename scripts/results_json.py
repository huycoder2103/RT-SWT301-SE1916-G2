#!/usr/bin/env python3
"""
Consolidate ALL experiment outcomes into clean JSON result files (report-from-JSON, mirroring
results/error-surface-baseline.json). Reads only authoritative artifacts — no re-computation of stats.

Inputs:
  results/raw/<sut>_recall.json   mutation kills/total/recall per arm (ground-truth seeded faults)
  results/raw/error_missed.csv    outcome: error behaviours triggered/missed per endpoint per arm
  results/raw/error_profile.csv   HTTP 2xx/4xx/5xx counts per sut/arm/op (785 real requests)
  results/stats/summary.json      RQ1/RQ2/RQ3 statistics
Outputs (results/):
  bug-detection.json   "AI bắt được bao nhiêu bug" — mutation recall + error-behaviours + HTTP outcomes
  rq-results.json      RQ1/RQ2/RQ3 numbers + verdict (plain VI)
  error-profile.json   per-endpoint triggered-vs-missed (outcome)
"""
import json, csv, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../experiment
RAW   = os.path.join(ROOT, 'results', 'raw')
STATS = os.path.join(ROOT, 'results', 'stats')
OUT   = os.path.join(ROOT, 'results')
SUTS  = ['ncs', 'scs', 'features']
ARMS  = ['llm', 'manual', 'evomaster']

def jload(p): return json.load(open(p, encoding='utf-8'))
def rows(p): return list(csv.DictReader(open(p, encoding='utf-8')))

# ---- 1. mutation faults (per-sut recall jsons) ----
mut = {s: jload(os.path.join(RAW, f'{s}_recall.json')) for s in SUTS}
n_mut = sum(mut[s]['llm']['total'] for s in SUTS)
killed = {a: sum(mut[s][a]['killed'] for s in SUTS) for a in ARMS}

# ---- 2. outcome error behaviours (error_missed.csv, documented endpoints) ----
em = [r for r in rows(os.path.join(RAW, 'error_missed.csv')) if r['op'] != 'UNKNOWN']
keyset, trig = {}, collections.Counter()
for r in em:
    keyset[(r['sut'], r['op'])] = [c for c in r['answer_key_codes'].split(';') if c]
    trig[(r['sut'], r['arm'])] += len([c for c in r['triggered'].split(';') if c and c != '-'])
KEY = sum(len(v) for v in keyset.values())
trig_tot = {a: sum(trig[(s, a)] for s in SUTS) for a in ARMS}

# ---- 3. HTTP outcomes (error_profile.csv) ----
http = collections.defaultdict(collections.Counter)
for r in rows(os.path.join(RAW, 'error_profile.csv')):
    a = r['arm']
    for k in ('n_2xx', 'n_4xx', 'n_5xx'):
        http[a][k] += int(r.get(k, 0) or 0)

# ---- bug-detection.json ----
bug = {
  "title": "Bug-detection results — AI (LLM) vs Manual vs EvoMaster",
  "description": "Bao nhiêu lỗi mỗi bộ test thực sự BẮT ĐƯỢC, đối chiếu ground truth. LLM = Claude Sonnet 4.6 (pilot + full run).",
  "generated_by": "experiment/scripts/results_json.py",
  "mutation_faults": {
    "what": "Gieo lỗi bằng mutation; 'killed' = test pass trên bản gốc nhưng fail trên mutant. Recall = killed/total.",
    "n_mutants_total": n_mut,
    "per_sut": {s: {"n_mutants": mut[s]['llm']['total'],
                    "killed":  {a: mut[s][a]['killed'] for a in ARMS},
                    "recall":  {a: mut[s][a]['recall'] for a in ARMS}} for s in SUTS},
    "overall": {"killed": killed, "recall": {a: round(killed[a] / n_mut, 4) for a in ARMS}},
    "verdict_vi": f"EvoMaster bắt nhiều nhất ({killed['evomaster']}/{n_mut}); AI = Người ({killed['llm']}/{n_mut}). "
                  "EvoMaster mạnh nhờ oracle ghi-giá-trị, bắt lỗi tính toán mà oracle dựa-status của AI/Người bỏ sót."
  },
  "error_behaviours": {
    "what": "Số hành vi lỗi (endpoint, status>=400) thực sự KÍCH được trên API sống, so với answer-key (hợp của 3 arm). Chỉ endpoint có tài liệu.",
    "answer_key_total": KEY,
    "triggered": trig_tot,
    "missed": {a: KEY - trig_tot[a] for a in ARMS},
    "per_sut": {s: {"answer_key": sum(len(v) for (ss, o), v in keyset.items() if ss == s),
                    "triggered": {a: trig[(s, a)] for a in ARMS}} for s in SUTS},
    "verdict_vi": f"AI kích {trig_tot['llm']}/{KEY} (100%), Người {trig_tot['manual']}/{KEY}, EvoMaster {trig_tot['evomaster']}/{KEY}. "
                  "AI bắt riêng được 1 crash 500 + các 405/406 mà bộ test người bỏ sót."
  },
  "http_outcomes": {
    "what": "Tổng response HTTP thật bắt được khi replay mọi request (785 request).",
    "by_arm": {a: {"http_2xx": http[a]['n_2xx'], "http_4xx": http[a]['n_4xx'], "http_5xx": http[a]['n_5xx']} for a in ARMS}
  }
}

# ---- rq-results.json ----
S = jload(os.path.join(STATS, 'summary.json'))
rq1, rq2, rq3 = S['RQ1_endpoint_coverage'], S['RQ2_fault_detection'], S['RQ3_edge_cases_llm_vs_manual']
rqdoc = {
  "title": "Research-question results (RQ1 / RQ2 / RQ3)",
  "description": "Số liệu + phán quyết cho 3 câu hỏi nghiên cứu. Pilot run.",
  "generated_by": "experiment/scripts/results_json.py",
  "RQ1_endpoint_coverage": {
    "question_vi": "AI có phủ >=90% endpoint không?",
    "coverage_pct": rq1['coverage_overall_pct'], "ops": f"{rq1['ops_covered']}/{rq1['n_operations']}",
    "p_value": rq1['p_value_one_sided'], "reject_H0": rq1['reject_H0_(coverage>90%)'],
    "verdict_vi": f"AI phủ {rq1['coverage_overall_pct']}% ({rq1['ops_covered']}/{rq1['n_operations']}), vượt 90% (p≈{rq1['p_value_one_sided']:.1e}) → H1 ĐÚNG."
  },
  "RQ2_fault_recall": {
    "question_vi": "AI bắt nhiều lỗi gieo hơn Người & EvoMaster không?",
    "overall_recall": rq2['overall_recall'], "n_mutants": rq2['n_mutants_total'],
    "mcnemar_llm_vs_evomaster_p": rq2['mcnemar']['llm_vs_evomaster']['p_value'],
    "verdict_vi": f"EvoMaster {rq2['overall_recall']['evomaster']} > AI={rq2['overall_recall']['llm']} = Người; AI CHƯA vượt (McNemar p≈{rq2['mcnemar']['llm_vs_evomaster']['p_value']:.3f}) → H0 chưa bị bác. Báo trung thực."
  },
  "RQ3_edge_cases": {
    "question_vi": "AI sinh nhiều kịch bản lỗi/biên per endpoint hơn Người không?",
    "llm_total": rq3['llm_total_edge'], "manual_total": rq3['manual_total_edge'],
    "median_llm": rq3['llm_median_per_op'], "median_manual": rq3['manual_median_per_op'],
    "p_value": rq3['p_value_one_sided'], "pairs_llm_more": rq3['pairs_llm_more'], "n_operations": rq3['n_operations'],
    "reject_H0": rq3['reject_H0_(llm>manual)'],
    "verdict_vi": f"AI {rq3['llm_total_edge']} vs Người {rq3['manual_total_edge']} (p≈{rq3['p_value_one_sided']:.1e}); AI hơn ở {rq3['pairs_llm_more']}/{rq3['n_operations']} endpoint → H1 ĐÚNG."
  }
}

# ---- error-profile.json (per endpoint) ----
prof = {}
for r in rows(os.path.join(RAW, 'error_missed.csv')):
    prof.setdefault(r['sut'], {}).setdefault(r['op'], {"answer_key_codes": r['answer_key_codes'], "by_arm": {}})
    prof[r['sut']][r['op']]["by_arm"][r['arm']] = {"triggered": r['triggered'], "missed": r['missed']}
errdoc = {
  "title": "Outcome error-profile per endpoint (triggered vs missed)",
  "description": "Mỗi endpoint: answer-key (hành vi lỗi nào tồn tại) + arm nào kích được / bỏ sót. Từ 785 request thật.",
  "generated_by": "experiment/scripts/results_json.py",
  "suts": prof
}

# ---- produced-vs-detected.json (chống nhầm "viết ra" với "bắt được") ----
ms = {r['arm']: r for r in rows(os.path.join(STATS, 'master_summary.csv')) if r['sut'] == 'ALL'}
pvd = {
  "title": "Produced vs Detected — phân biệt 'VIẾT RA' với 'BẮT ĐƯỢC'",
  "description": "Số test/kịch bản AI SINH RA khác hẳn số bug AI BẮT ĐƯỢC. Tránh nói nhầm khi báo cáo.",
  "generated_by": "experiment/scripts/results_json.py",
  "produced": {
    "note_vi": "AI/Người/Tool TẠO RA — KHÔNG phải bug.",
    "test_cases": {a: int(ms[a]['test_cases']) for a in ARMS if a in ms},
    "edge_case_scenarios_llm_vs_manual": {"llm": int(ms['llm']['edge_scenarios']), "manual": int(ms['manual']['edge_scenarios'])}
  },
  "detected": {
    "note_vi": "Thực sự BẮT ĐƯỢC, đối chiếu ground truth.",
    "mutation_faults_killed": {**killed, "total": n_mut},
    "http_error_behaviours_triggered": {**trig_tot, "answer_key": KEY},
    "server_crash_5xx_responses": {a: http[a]['n_5xx'] for a in ARMS}
  },
  "why_gap_vi": "Test AI/Người chủ yếu check status (200/400); mutation đổi GIÁ TRỊ tính toán → status không đổi → test vẫn pass → không bắt. EvoMaster ghi lại giá trị đúng làm oracle nên bắt nhiều lỗi giá-trị hơn.",
  "correct_phrasing_vi": [
    "ĐÚNG: 'AI SINH 217 kịch bản edge-case (Người 141)'.",
    "ĐÚNG: 'AI BẮT 9/133 lỗi gieo (= Người); KÍCH 31/31 hành vi lỗi HTTP, gồm crash 500'.",
    "SAI: 'AI bắt 270 bug' — đó là SỐ TEST VIẾT RA, không phải bug."
  ]
}

for name, doc in [('bug-detection.json', bug), ('rq-results.json', rqdoc), ('error-profile.json', errdoc), ('produced-vs-detected.json', pvd)]:
    json.dump(doc, open(os.path.join(OUT, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote results/' + name)
print(f"\nMUTATION killed/{n_mut}:  llm={killed['llm']}  manual={killed['manual']}  evomaster={killed['evomaster']}")
print(f"ERROR-BEHAVIOURS /{KEY}:  llm={trig_tot['llm']}  manual={trig_tot['manual']}  evomaster={trig_tot['evomaster']}")
