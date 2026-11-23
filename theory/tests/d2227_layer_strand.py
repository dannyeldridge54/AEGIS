"""D2227 (PREREG_D2227_LAYER_STRAND): flux/twist/condensate strand -> m3/2, T_R -> UFE ring pulse at every point."""
import itertools, json, math, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(ROOT)
src = open('tools/weave_knobs.py').read().split('O0 = chain(base)')[0]; ns = {}; exec(src, ns); chain, base = ns['chain'], ns['base']
ReS0 = math.sqrt(3) / 2; ReT0 = 28 - 9 * ReS0; x0 = 9 * ReS0 / 28; M0 = 257945.66231349262
pts = []
for ReS, g, N in itertools.product((ReS0, 1.0), (2, 3, 4), (4, 5, 6, 7, 8)):
    ReT = 28 - g * g * ReS
    if ReT <= 1: pts.append(dict(ReS=ReS, g=g, N=N, void=True)); continue
    k = dict(base, g_s=1 / ReS, sigma=20.15 + (ReT - ReT0)); xx = 2 * math.pi * k['sigma'] / N; W0 = k['A'] * math.exp(-xx) * (1 + 2 * xx / 3)
    m32 = math.sqrt(k['g_s'] / 2) / k['Vol'] * W0 * ns['MP']   # DEV-0: chain's m3/2 lines only
    pts.append(dict(ReS=round(ReS, 4), g=g, N=N, ReT=ReT, m32=m32, s_m32=m32 / M0, T_R=8.94e8 * (g * g * ReS / 28) / x0))
code = r'''
import json, sys; sys.path.insert(0, 'tools/rings'); import hex as H, bandmap1 as BM
p = json.loads(sys.argv[1]); H.ADOPTED = dict(C=1.25e-06, T_R=p['T_R'], s_m32=p['s_m32'])
cur, hist, rnds = H.loop(log=lambda *a: None); m = BM.marks(cur)
print(json.dumps(dict(knobs=cur['knobs'], lnL=cur['lnL'], target=cur['target'], rounds=rnds, marks=m)))
'''
out = []
for p in pts:
    if p.get('void'): out.append(p); continue
    for lab, a in (('official', 0.11446), ('threshold_m3_0', 0.117953)):
        env = dict(os.environ, AEGIS_AS_ENGINE=repr(a))
        r = subprocess.run([sys.executable, '-c', code, json.dumps(p)], capture_output=True, text=True, env=env)
        res = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else dict(error=r.stderr[-300:])
        mk = res.get('marks', {}); bad = sorted(k for k, v in mk.items() if v[0] == 'OUT' and k != 'DH')
        stable = bool(mk) and not bad and mk.get('genesis', ['OUT'])[0] == 'IN'
        p[lab] = dict(lnL=res.get('lnL'), target=res.get('target'), C=res.get('knobs', {}).get('C'), out_marks=bad, stable=stable, err=res.get('error'))
    out.append(p); print(p['ReS'], p['g'], p['N'], f"m32 {p['m32']:.3g} T_R {p['T_R']:.3g}", 'off', p['official']['stable'], p['official']['out_marks'], 'thr', p['threshold_m3_0']['stable'], p['threshold_m3_0']['out_marks'], flush=True)
live = [p for p in out if not p.get('void')]
summ = {lab: dict(n_stable=sum(p[lab]['stable'] for p in live), n=len(live), model_point_stable=[p[lab]['stable'] for p in live if p['g'] == 3 and p['N'] == 6 and abs(p['ReS'] - 0.866) < 1e-3][0],
                  stable=[(p['ReS'], p['g'], p['N']) for p in live if p[lab]['stable']]) for lab in ('official', 'threshold_m3_0')}
json.dump(dict(summary=summ, points=out), open('field_tests/results/d2227_layer_strand.json', 'w'), indent=1, default=str); print(json.dumps(summ, indent=1))
