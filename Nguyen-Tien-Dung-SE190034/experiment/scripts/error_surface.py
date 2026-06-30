#!/usr/bin/env python3
"""
CODE-DERIVED ERROR-SURFACE BASELINE  (pure, per-endpoint, JSON output).

For each SUT it (1) reads the OpenAPI spec to list the operations, then (2) derives — purely from the
SOURCE CODE — every way each endpoint can produce a non-2xx response. It is a standalone ground-truth
baseline: "what can each endpoint do / where can it fail." It contains NO test-tool statistics
(no LLM / Manual / EvoMaster).

Provenance of each error point:
  declared   : explicit `ResponseEntity.status(4xx/5xx)` / `.badRequest()` in the controller (file:line + source line).
  framework  : a typed numeric @PathVariable -> Spring returns 400 automatically on a type mismatch.
  potential  : a source line that can throw an UNCAUGHT runtime exception -> HTTP 500, or a checked
               exception the controller turns into a 4xx (identified by source review; file:line + reason).

Output: experiment/results/error-surface-baseline.json   (JSON only — no HTML, no CSV, no Markdown).
"""
import re, os, json, glob, collections

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../experiment
EMB   = os.path.join(ROOT, 'EMB', 'jdk_8_maven', 'cs', 'rest')
SPECS = os.path.join(ROOT, 'specs')
OUT   = os.path.join(ROOT, 'results', 'error-surface-baseline.json')

SUTS = {
  'ncs': {'spec': 'rest-ncs.openapi.json', 'base': '/api',
          'ctrl': [EMB + '/artificial/ncs/src/main/java/org/restncs/NcsRest.java']},
  'scs': {'spec': 'rest-scs.openapi.json', 'base': '/api',
          'ctrl': [EMB + '/artificial/scs/src/main/java/org/restscs/ScsRest.java']},
  'features': {'spec': 'features-service.openapi.json', 'base': '',
          'ctrl': glob.glob(EMB + '/original/features-service/src/main/java/org/javiermf/features/services/rest/*.java')},
}

# Crash / exception points identified by SOURCE REVIEW (regex cannot infer "NPE if entity absent").
# Keyed by operation short-name (ncs/scs) or operationId (features). status = the HTTP code it surfaces as.
CURATED = {
  'ncs': {
    'bessj':     [(500, 'potential', 'imp/Bessj.java', 61, 'series divide-by-zero if internal sum==0 (uncaught -> 500)')],
    'expint':    [(400, 'potential', 'imp/Expint.java', 16, 'n<0 || x<0 || (x==0 && (n==0||n==1)) -> RuntimeException, caught -> 400')],
    'fisher':    [(500, 'potential', 'imp/Fisher.java', 44, 'divide-by-zero when denominator w==0 (uncaught -> 500)')],
    'gammq':     [(400, 'potential', 'imp/Gammq.java', 80, 'x<0 || a<=0 -> RuntimeException, caught -> 400')],
    'remainder': [(500, 'potential', 'imp/Remainder.java', 34, 'b==0 reaches an unguarded division/loop path (uncaught -> 500)')],
  },
  'scs': {
    'calc':       [(500, 'potential', 'imp/Calc.java', 55, 'divide-by-zero when arg2==0 (uncaught -> 500)')],
    'cookie':     [(500, 'potential', 'imp/Cookie.java', 27, 'substring() StringIndexOutOfBounds if val.length()<=3 (uncaught -> 500)')],
    'filesuffix': [(500, 'potential', 'imp/FileSuffix.java', 29, "split('.') edge yields empty array -> ArrayIndexOutOfBounds (uncaught -> 500)")],
    'pat':        [(500, 'potential', 'imp/Pat.java', 54, 'charAt()/substring() out-of-bounds when pattern longer than text (uncaught -> 500)')],
    'regex':      [(500, 'potential', 'imp/Regex.java', 45, 'PatternSyntaxException on an invalid regex argument (uncaught -> 500)')],
  },
  'features': {
    'getProductByName':                  [(500, 'potential', 'services/ProductsDAO.java', 39, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
    'deleteProductByName':               [(500, 'potential', 'services/ProductsDAO.java', 39, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
    'addProduct':                        [(500, 'potential', 'services/ProductsService.java', 53, 'DuplicatedObjectException / constraint violation when product already exists (uncaught -> 500)')],
    'getConfigurationWithNameForProduct':[(500, 'potential', 'services/ProductsConfigurationsDAO.java', 43, 'singleResult returns null -> NPE on getActivedFeatures() (uncaught -> 500)')],
    'addConfiguration':                  [(500, 'potential', 'services/ProductsService.java', 54, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
    'deleteConfiguration':               [(500, 'potential', 'services/ProductsConfigurationsDAO.java', 70, 'findByNameAndProductName null -> NPE on entityManager.remove() (uncaught -> 500)')],
    'getFeaturesForProduct':             [(500, 'potential', 'services/ProductsDAO.java', 39, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
    'addFeatureToProduct':               [(500, 'potential', 'services/ProductsService.java', 62, 'findByName ObjectNotFoundException when product absent; DuplicatedObjectException if feature exists (uncaught -> 500)')],
    'deleteFeature':                     [(500, 'potential', 'model/Product.java', 75, 'findProductFeatureByName throws ObjectNotFoundException when feature absent (uncaught -> 500)')],
    'getConfigurationActivedFeatures':   [(500, 'potential', 'services/ProductsConfigurationsDAO.java', 43, 'singleResult null -> NPE on getActivedFeatures() (uncaught -> 500)')],
    'addFeatureToConfiguration':         [(500, 'potential', 'services/ProductsConfigurationsDAO.java', 43, 'config null -> NPE; WrongProductConfigurationException for invalid config (uncaught -> 500)')],
    'deleteFeatureOfProduct':            [(500, 'potential', 'model/Product.java', 75, 'findByName / findProductFeatureByName ObjectNotFoundException when product/feature absent (uncaught -> 500)')],
    'updateFeatureOfProduct':            [(500, 'potential', 'model/Product.java', 75, 'findByName / findProductFeatureByName ObjectNotFoundException when product/feature absent (uncaught -> 500)')],
    'addRequiresConstraintToProduct':    [(500, 'potential', 'services/ProductsDAO.java', 39, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
    'addExcludesConstraintToProduct':    [(500, 'potential', 'services/ProductsDAO.java', 39, 'findByName throws ObjectNotFoundException when product absent (uncaught -> 500)')],
  },
}

STATUS_RE = re.compile(r'ResponseEntity\.status\(\s*(\d{3})\s*\)')
BADREQ_RE = re.compile(r'\.badRequest\(\)')
MAP_MULTI = re.compile(r'@(Get|Post|Put|Delete|Patch)Mapping\s*\(([\s\S]*?)\)')
PATHSTR   = re.compile(r'"([^"]+)"')

def load_ops(sut):
    d = json.load(open(os.path.join(SPECS, SUTS[sut]['spec']), encoding='utf-8'))
    base = (d.get('basePath') or '').rstrip('/')
    ops = []
    for tmpl, methods in d.get('paths', {}).items():
        seg = '[^/]+'.join(re.escape(p) for p in re.split(r'\{[^}]*\}', tmpl))
        pats = [re.compile('^' + v + r'/?$') for v in {seg, re.escape(base) + seg}]
        for m, o in methods.items():
            if m.lower() in ('get', 'post', 'put', 'delete', 'patch'):
                opId = o.get('operationId', m + ':' + tmpl)
                ops.append({'pats': pats, 'method': m.upper(), 'opId': opId, 'tmpl': tmpl,
                            'short': re.sub(r'Using(GET|POST|PUT|DELETE|PATCH)$', '', opId, flags=re.I)})
    return ops

def map_path(path, method, ops):
    p = path.split('?')[0]
    for o in ops:
        if o['method'] == method.upper() and any(r.match(p) for r in o['pats']): return o['opId']
    for o in ops:
        if any(r.match(p) for r in o['pats']): return o['opId']
    return None

def scan_declared(sut, ops):
    """Static scan: declared status()/badRequest + framework-400. Returns opId -> [points]."""
    pts = collections.defaultdict(list)
    base = SUTS[sut]['base']
    for fp in SUTS[sut]['ctrl']:
        if not os.path.exists(fp): continue
        text = open(fp, encoding='utf-8', errors='replace').read()
        lines = text.splitlines()
        fname = os.path.basename(fp)
        maps = []
        for m in MAP_MULTI.finditer(text):
            ps = PATHSTR.search(m.group(2))
            opId = map_path(base + (ps.group(1) if ps else ''), m.group(1), ops)
            maps.append({'line': text.count('\n', 0, m.start()) + 1, 'opId': opId})
        for k, mp in enumerate(maps):
            if not mp['opId']: continue
            start = mp['line']; end = maps[k + 1]['line'] - 1 if k + 1 < len(maps) else len(lines)
            block = lines[start - 1:end]; opId = mp['opId']
            for j, bl in enumerate(block):
                for sm in STATUS_RE.finditer(bl):
                    pts[opId].append({'status': int(sm.group(1)), 'provenance': 'declared', 'file': fname, 'line': start + j, 'detail': bl.strip()})
                if BADREQ_RE.search(bl):
                    pts[opId].append({'status': 400, 'provenance': 'declared', 'file': fname, 'line': start + j, 'detail': bl.strip()})
            if re.search(r'@PathVariable[\s\S]{0,60}?\b(Integer|Long|Double|int|double|Short|Float)\b', '\n'.join(block)):
                pts[opId].append({'status': 400, 'provenance': 'framework', 'file': fname, 'line': start,
                                  'detail': 'typed @PathVariable -> Spring auto-400 on type mismatch'})
    return pts

def main():
    suts_out = {}
    n_ep = n_pt = n_guard = n_crash = 0
    for sut in SUTS:
        ops = load_ops(sut)
        declared = scan_declared(sut, ops)
        eps = []
        for o in ops:
            pts = list(declared.get(o['opId'], []))
            for (st, kind, f, ln, cond) in CURATED.get(sut, {}).get(o['short'], []) + CURATED.get(sut, {}).get(o['opId'], []):
                pts.append({'status': st, 'provenance': kind, 'file': f, 'line': ln, 'detail': cond})
            seen, dedup = set(), []
            for p in pts:
                key = (p['status'], p['provenance'], p['file'], p['line'])
                if key in seen: continue
                seen.add(key); dedup.append(p)
            dedup.sort(key=lambda p: (p['status'], p['provenance']))
            eps.append({'operationId': o['opId'], 'method': o['method'], 'path': o['tmpl'], 'error_surface': dedup})
            n_ep += 1; n_pt += len(dedup)
            if any(p['provenance'] == 'declared' for p in dedup): n_guard += 1
            if any(p['provenance'] == 'potential' and p['status'] >= 500 for p in dedup): n_crash += 1
        suts_out[sut] = {'base_path': SUTS[sut]['base'], 'n_endpoints': len(eps), 'endpoints': eps}

    doc = {
        'title': 'Error-Surface Baseline (code-derived, per endpoint)',
        'description': "Per-endpoint error surface derived purely from source code: where each endpoint can "
                       "return a non-2xx response. Ground-truth baseline, independent of any test tool "
                       "(no LLM / Manual / EvoMaster statistics).",
        'generated_by': 'experiment/scripts/error_surface.py',
        'provenance_legend': {
            'declared':  'explicit ResponseEntity.status(4xx/5xx) / .badRequest() in the controller (file:line shown)',
            'framework': 'typed numeric @PathVariable -> Spring returns 400 automatically on a type mismatch',
            'potential': 'a source line that can throw: uncaught -> HTTP 500, or caught by the controller -> 4xx (source review)',
        },
        'summary': {
            'total_endpoints': n_ep,
            'total_error_points': n_pt,
            'endpoints_with_explicit_4xx_guard': n_guard,
            'endpoints_with_potential_5xx_crash': n_crash,
        },
        'suts': suts_out,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), indent=2)
    print('wrote %s' % os.path.relpath(OUT, ROOT))
    print('endpoints=%d  error-points=%d  guarded=%d  potential-5xx=%d' % (n_ep, n_pt, n_guard, n_crash))

if __name__ == '__main__':
    main()
