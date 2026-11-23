"""D2226 (PREREG_D2226_UFE_PASS): ring-engine pulse + stage map for the baseline and every stable tau = i pair from D2225."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'rings'))
N25 = json.load(open(os.path.join(ROOT, 'field_tests', 'results', 'd2225_negspace.json')))
cases = [('baseline', 0.11446, 0)] + [(f"tau_i_db{r['db32']}_{r['db12']}", r['alpha_s'], 2) for r in N25['tau_i']['stable']]
out = {}
for name, a, extra in cases:
    os.environ['AEGIS_AS_ENGINE'] = repr(a)
    code = ("import json,sys,math; sys.path.insert(0,'tools/rings'); import hex as H, bandmap1 as BM; B=H.B\n"
            "cur, hist, rnds = H.loop(log=lambda *a: None)\n"
            "k_fit = sum(k['n'] for k in B.D['fitted_knobs']); moved = sum(1 for k in cur['knobs'] if cur['knobs'][k] != H.ADOPTED[k])\n"
            f"t0 = B.target(cur['terms'], k_fit, moved); t2 = B.target(cur['terms'], k_fit, moved + {extra})\n"
            "m = BM.marks(cur); print(json.dumps(dict(knobs=cur['knobs'], rounds=rnds, accepted=[h for h in hist if h.get('decision')=='ACCEPT'], lnL=t0[0], target_k0=t0[1], target_k2=t2[1], k0=t0[3], k2=t2[3], marks=m), default=str))")
    r = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ))
    ring = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else dict(error=r.stderr[-400:])
    sm = subprocess.run([sys.executable, 'tools/stagemap.py', f'ufe_{name}'], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ))
    cnt = json.load(open(os.path.join(ROOT, 'field_tests', 'results', f'stagemap_ufe_{name}.json')))['counts'] if sm.returncode == 0 else sm.stderr[-300:]
    out[name] = dict(alpha_s=a, ring=ring, stagemap_counts=cnt)
    mk = ring.get('marks', {}); print(name, a, 'lnL', ring.get('lnL'), 'tgt k+0/k+2', ring.get('target_k0'), ring.get('target_k2'), 'alpha_s', mk.get('alpha_s'), 'Hoyle', mk.get('Hoyle'), 'map', cnt)
json.dump(out, open(os.path.join(ROOT, 'field_tests', 'results', 'd2226_ufe_pass.json'), 'w'), indent=1, default=str)
