#!/usr/bin/env python3
"""
Outcome-based error profile  (Gap-M extension: triggered-vs-missed).

Reads REAL captured traffic (experiment/results/raw/traffic.csv produced by
run_capture.sh + logproxy.py) -- every request each arm actually issued, with the
SUT's actual HTTP status -- and per endpoint computes:

  * how many requests landed in 2xx / 4xx / 5xx   (-> "how many 4xx/5xx caught"),
  * the distinct inputs (paths) that triggered each error  (-> "which boundary"),
  * the error behaviours (op, status>=400) each arm TRIGGERED, and
  * the behaviours each arm MISSED -- present in the union answer key (anything any
    arm, incl. EvoMaster, ever elicited) but not triggered by this arm.

Turns the RQ3 *scenario count* (intent) into an *outcome* measure: which real
error/boundary behaviours each suite reached, and which it missed.

Outputs: experiment/results/raw/error_profile.csv   (per sut,arm,op counts)
         experiment/results/raw/error_missed.csv      (answer-key behaviours + who missed)
         + ASCII report to stdout.
"""
import re, csv, json, os, sys, collections

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../experiment
SPECS = os.path.join(ROOT, 'specs')
OUT   = os.path.join(ROOT, 'results', 'raw')
TRAFFIC = os.path.join(OUT, 'traffic.csv')

SPEC_OF = {'ncs': 'rest-ncs.openapi.json', 'scs': 'rest-scs.openapi.json',
           'features': 'features-service.openapi.json'}

def load_ops(spec_path):
    spec = json.load(open(spec_path, encoding='utf-8'))
    base = (spec.get('basePath') or '').rstrip('/')
    ops = []
    for tmpl, methods in spec.get('paths', {}).items():
        # split on {param}; escape literal parts; join with a single-segment matcher
        seg = '[^/]+'.join(re.escape(p) for p in re.split(r'\{[^}]*\}', tmpl))
        variants = {('^' + seg + r'/?$'), ('^' + re.escape(base) + seg + r'/?$')}
        pats = [re.compile(v) for v in variants]
        for m, o in methods.items():
            if m.lower() in ('get', 'post', 'put', 'delete', 'patch'):
                ops.append((pats, m.lower(), o.get('operationId', m + ':' + tmpl)))
    return ops

def map_op(path, method, ops):
    p = path.split('?')[0]
    for pats, m, opid in ops:
        if m == method.lower() and any(pat.match(p) for pat in pats):
            return opid
    for pats, m, opid in ops:                    # method-agnostic fallback
        if any(pat.match(p) for pat in pats):
            return opid
    return 'UNKNOWN'

def cls(code):
    code = int(code)
    if 200 <= code < 300: return '2xx'
    if 400 <= code < 500: return '4xx'
    if 500 <= code < 600: return '5xx'
    return None

def main():
    if not os.path.exists(TRAFFIC):
        sys.exit('traffic.csv not found -- run experiment/scripts/run_capture.sh first')
    ops_cache = {s: load_ops(os.path.join(SPECS, f)) for s, f in SPEC_OF.items()}

    counts = collections.defaultdict(collections.Counter)            # (sut,arm,op) -> Counter
    behav  = collections.defaultdict(lambda: collections.defaultdict(set))  # (sut,op) -> arm -> {code}
    epaths = collections.defaultdict(set)                            # (sut,op,arm) -> {(method path, code)}
    seen_ops = collections.defaultdict(set)                          # sut -> {op}

    for row in csv.DictReader(open(TRAFFIC, encoding='utf-8')):
        sut, arm = row['tag'].split(':', 1)
        if sut not in ops_cache: continue
        c = cls(row['status'])
        if c is None: continue
        op = map_op(row['path'], row['method'], ops_cache[sut])
        counts[(sut, arm, op)][c] += 1
        seen_ops[sut].add(op)
        if c in ('4xx', '5xx'):
            behav[(sut, op)][arm].add(int(row['status']))
            epaths[(sut, op, arm)].add(('%s %s' % (row['method'], row['path']), int(row['status'])))

    # write per-op counts
    crows = [{'sut': s, 'arm': a, 'op': o, 'n_2xx': c['2xx'], 'n_4xx': c['4xx'], 'n_5xx': c['5xx']}
             for (s, a, o), c in sorted(counts.items())]
    with open(os.path.join(OUT, 'error_profile.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['sut', 'arm', 'op', 'n_2xx', 'n_4xx', 'n_5xx']); w.writeheader(); w.writerows(crows)

    # answer key + who-missed
    mrows = []
    for (sut, op), arms in sorted(behav.items()):
        key = sorted(set().union(*arms.values()))
        for arm in ('llm', 'manual', 'evomaster'):
            got = arms.get(arm, set())
            mrows.append({'sut': sut, 'op': op, 'answer_key_codes': ';'.join(map(str, key)), 'arm': arm,
                          'triggered': ';'.join(map(str, sorted(got))) or '-',
                          'missed': ';'.join(str(k) for k in key if k not in got) or '-'})
    with open(os.path.join(OUT, 'error_missed.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['sut', 'op', 'answer_key_codes', 'arm', 'triggered', 'missed']); w.writeheader(); w.writerows(mrows)

    # ---- report ----
    def g(s, a, o):
        c = counts.get((s, a, o))
        return '%d/%d/%d' % (c['2xx'], c['4xx'], c['5xx']) if c else '  -  '
    print('\n' + '=' * 80)
    print('OUTCOME ERROR PROFILE  (real captured traffic; format = 2xx/4xx/5xx request counts)')
    print('=' * 80)
    grand = collections.Counter()
    for sut in SPEC_OF:
        ops = sorted(o for o in seen_ops.get(sut, ()) if o != 'UNKNOWN') + \
              (['UNKNOWN'] if 'UNKNOWN' in seen_ops.get(sut, ()) else [])
        if not ops: continue
        print('\n### %s   (%d endpoints touched)' % (sut.upper(), len([o for o in ops if o != 'UNKNOWN'])))
        print('  %-34s | %-14s | %-14s | %-14s' % ('endpoint', 'LLM', 'Manual', 'EvoMaster'))
        for op in ops:
            print('  %-34s | %-14s | %-14s | %-14s' % (op[:34], g(sut, 'llm', op), g(sut, 'manual', op), g(sut, 'evomaster', op)))
        # answer key = documented operations only (UNKNOWN = garbage/undocumented paths, reported separately)
        akey = {op: sorted(set().union(*behav[(sut, op)].values())) for op in ops if op != 'UNKNOWN' and (sut, op) in behav}
        total_key = sum(len(v) for v in akey.values())
        print('  -- error behaviours (op,status>=400) in answer key [documented endpoints]: %d' % total_key)
        for arm in ('llm', 'manual', 'evomaster'):
            t = sum(len(behav[(sut, op)].get(arm, set())) for op in akey)
            print('     %-9s triggered %2d / %d   (missed %d)' % (arm, t, total_key, total_key - t))
            if arm in ('llm', 'manual'): grand[arm] += t
        grand['key'] += total_key
        if (sut, 'UNKNOWN') in behav:
            ub = behav[(sut, 'UNKNOWN')]
            sh = lambda a: ','.join(map(str, sorted(ub.get(a, set())))) or '-'
            print('     [undocumented/garbage-path 4xx (UNKNOWN, not in answer key): llm={%s} manual={%s} evo={%s}]'
                  % (sh('llm'), sh('manual'), sh('evomaster')))
        # boundaries LLM caught that Manual missed (the headline contrast)
        ex = []
        for op in ops:
            if op == 'UNKNOWN': continue
            l = behav.get((sut, op), {}).get('llm', set()); m = behav.get((sut, op), {}).get('manual', set())
            for code in sorted(l - m):
                sample = next((p for p, cc in epaths[(sut, op, 'llm')] if cc == code), '')
                ex.append('%s -> %d   e.g. %s' % (op, code, sample))
        if ex:
            print('  -- error behaviours LLM caught but Manual MISSED:')
            for e in ex[:15]: print('       ' + e)
    print('\n' + '-' * 80)
    print('TOTAL across SUTs (vs union answer key %d): LLM triggered %d, Manual triggered %d'
          % (grand['key'], grand['llm'], grand['manual']))
    print('Wrote results/raw/error_profile.csv , results/raw/error_missed.csv')

if __name__ == '__main__':
    main()
