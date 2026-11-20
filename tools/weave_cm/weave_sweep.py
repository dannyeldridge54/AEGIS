"""CubeMind data builder for the Weave (Danny 20 Nov 09:08: "give it most of what's left in storage to build up the data and sift").
Each call runs a time-boxed batch of systematic scans and appends rows to weave_data/*.jsonl; a disk guard stops writing when
free space falls below WEAVE_MIN_FREE_GB (default 80) or the data folder exceeds WEAVE_MAX_GB (default 200).
Scans (all deterministic tools from weave_tools; every row carries its label):
  ckm   - random O(1) couplings for down rung 1 x up rung u (2..16), both models -> score + all 8 observables
  rungs - occupancy of supplied/known families on the ladder
  prop  - how a rung change of the up/down sector would move m_p and molecular scales (standard physics propagation)
Summaries (best points per rung/model, counts) go to weave_data/summary.json for the learn loop to ingest."""
import json, math, os, pathlib, random, shutil, time
import numpy as np
import weave_tools as W

T = dict(ms_mb=0.0199, md_mb=1.00e-3, mc_mt=3.72e-3, mu_mt=7.6e-6, Vus=0.2250, Vcb=0.0418, Vub=0.00369, J=3.08e-5)
TOL = dict(ms_mb=1.5, md_mb=1.5, mc_mt=1.5, mu_mt=1.5, Vus=1.1, Vcb=1.2, Vub=1.3, J=1.5)
RUNG_TAUS = None


def _guard(d):
    free = shutil.disk_usage(str(d)).free / 1e9
    used = sum(f.stat().st_size for f in d.glob('*.jsonl')) / 1e9
    return free > float(os.environ.get('WEAVE_MIN_FREE_GB', '80')) and used < float(os.environ.get('WEAVE_MAX_GB', '200')), free, used


def _score(o):
    return sum((math.log(max(o[k], 1e-30) / T[k]) / math.log(TOL[k])) ** 2 for k in T)


def _tau_for(m):
    """Use computed minima where available; otherwise the ladder formula at arg 50 deg (label E beyond m=32)."""
    if m in W._TAU: return W._TAU[m]
    rho = complex(-0.5, math.sqrt(3) / 2); e = W.C_RUNG / (m + 1 / 16)
    return rho + e * complex(math.cos(math.radians(50)), math.sin(math.radians(50)))


def batch_ckm(out, rng, seconds):
    t0 = time.time(); n = 0; best = {}
    while time.time() - t0 < seconds:
        model = rng.choice(['w642', 'w864']); mu = rng.randint(2, 16)
        W._TAU.setdefault(mu, _tau_for(mu))
        p = lambda: {'r1': math.exp(rng.uniform(math.log(1/3), math.log(3))), 'r2': math.exp(rng.uniform(math.log(1/3), math.log(3))),
                     'g_abs': math.exp(rng.uniform(math.log(1/3), math.log(3))), 'g_arg': rng.uniform(-math.pi, math.pi),
                     'f_abs': math.exp(rng.uniform(math.log(1/3), math.log(3))), 'f_arg': rng.uniform(-math.pi, math.pi)}
        a = {'model': model, 'rung_d': 1, 'rung_u': mu, 'down': p(), 'up': p()}
        try: o = W.weave_ckm(a)
        except Exception as e: continue
        s = _score(o); row = dict(scan='ckm', model=model, rung_u=mu, score=s, obs={k: o[k] for k in T}, args=a, label='A (hosted fit scan)',
                                  tau_u_source='computed' if mu in (1, 8, 9, 10, 13) else 'formula (E)')
        out.write(json.dumps(row) + '\n'); n += 1
        k = f'{model}:{mu}'
        if k not in best or s < best[k]['score']: best[k] = row
    return n, best


def polish(row, seconds=15):
    """Nelder-Mead polish of a scan point inside the O(1) box (same box/tolerances as PREREG_Q8/Q12)."""
    from scipy.optimize import minimize
    keys = ['r1', 'r2', 'g_abs', 'g_arg', 'f_abs', 'f_arg']; a = row['args']
    lo = np.array([1/3, 1/3, 1/3, -math.pi, 1/3, -math.pi] * 2); hi = np.array([3, 3, 3, math.pi, 3, math.pi] * 2)
    x0 = np.array([a['down'][k] for k in keys] + [a['up'][k] for k in keys]); t0 = time.time()
    def f(x):
        if time.time() - t0 > seconds: raise TimeoutError
        x = np.clip(x, lo, hi); b = dict(a, down=dict(zip(keys, x[:6])), up=dict(zip(keys, x[6:])))
        return _score(W.weave_ckm(b))
    best = [row['score'], x0]
    try:
        r = minimize(lambda x: (lambda v: (best.__setitem__(slice(0, 2), [v, x]) if v < best[0] else None, v)[1])(f(x)), x0, method='Nelder-Mead', options=dict(maxiter=3000))
    except TimeoutError:
        pass
    x = np.clip(best[1], lo, hi); b = dict(a, down=dict(zip(keys, x[:6])), up=dict(zip(keys, x[6:]))); o = W.weave_ckm(b)
    return dict(row, scan='ckm_polished', score=_score(o), obs={k: o[k] for k in T}, args=b,
                fails=[k for k in T if not (1/TOL[k] <= o[k]/T[k] <= TOL[k])])


def batch_props(out):
    rows = []
    for du in (-1, 1):     # up-quark rung moves by one step around 8
        for base in (8, 9):
            ratio = (base + 1 / 16) / (base + du + 1 / 16)        # eps ratio -> hierarchy ratio scale (equal-coefficient)
            rows.append(dict(scan='prop', what=f'up rung {base}->{base+du}', eps_ratio=ratio,
                             proton=W.weave_proton({'dmhat_over_mhat': 0.0, 'dms_over_ms': 0.0}),
                             note='light-quark masses are set by the rung only through the hierarchy; m_u,m_d absolute scale needs the coupling: not predicted', label='E'))
    rows.append(dict(scan='prop', what='m_e -1e-5 (Koide-scale slip)', atomic=W.weave_atomic({'m_e_MeV': W.LEPTONS['e'] * (1 - 1e-5)}), label='S'))
    for r in rows: out.write(json.dumps(r) + '\n')
    return len(rows)


KNOBS = dict(Nstar=(45, 60), omega_b=(0.0218, 0.0229), dark_sector=['none', 'brane_split', 'minimal_equal_sharing', 'mirror_at_bound'],
             b_A=(-0.12, 0.02), dphi=(0.3, 1.0), wino_mass_GeV=(500, 3000), run=['run2', 'run3', 'run2+3', 'hl-lhc', 'hl-lhc-ult', 'he-lhc', 'fcc-hh'], halo=['Einasto', 'NFW', 'Burkert'],
             rho_sun=(0.3, 0.5), eos=['SLy', 'AP4'], sugra_m=(1, 16), tauq_mass_GeV=(1e8, 5e12), tauq_phi0=(0.1, 1.0),
             inflation_model=['serapis_10d', 'serapis_6d'])


def batch_engine(out, rng, seconds, cur):
    """Whole-Weave scan: random knob values across EVERY level of the Weave Control engine (inflation, flavour, quarks, BBN,
    late universe, colliders, galaxy, stars, sky); each row = one consistent universe with every level's status and outputs."""
    import sys as _s
    if cur not in _s.path: _s.path.insert(0, cur)
    from tools.weave_control import engine as E
    kn = {k['key'] for lv in E.knobs().values() for k in lv}; t0 = time.time(); n = 0; allp = 0
    while time.time() - t0 < seconds:
        p = {}
        for k, v in KNOBS.items():
            if k not in kn and k not in E.DEFAULTS: continue
            if isinstance(v, list): p[k] = rng.choice(v)
            elif k in ('tauq_mass_GeV',): p[k] = 10 ** rng.uniform(math.log10(v[0]), math.log10(v[1]))
            elif k == 'sugra_m': p[k] = rng.randint(*v)
            else: p[k] = rng.uniform(*v)
        try: r = E.run(p)
        except Exception as e:
            out.write(json.dumps(dict(scan='engine', params=p, error=str(e)[:200])) + '\n'); continue
        lv = {l['id']: dict(status=l['status'], outputs={k: v for k, v in l['outputs'].items() if isinstance(v, (int, float, str, bool))}) for l in r['levels']}
        ok = all(v['status'] in ('pass', 'open') for k, v in lv.items() if k != 'quarks')
        allp += ok
        jt = next((l.get('joint_tauq') for l in r['levels'] if l.get('joint_tauq')), None)   # PREREG_J1 joint (tau_q -> N* -> r)
        out.write(json.dumps(dict(scan='engine', params=p, levels=lv, joint_tauq=jt, all_pass_except_quarks=ok, label='mixed: per-level labels in the engine')) + '\n'); n += 1
    return n, allp


def run(data_dir, seconds=60, seed=None):
    d = pathlib.Path(data_dir); d.mkdir(parents=True, exist_ok=True)
    ok, free, used = _guard(d)
    if not ok: return {'weave_sweep': 'paused by disk guard', 'free_GB': round(free, 1), 'used_GB': round(used, 3)}
    rng = random.Random(seed if seed is not None else time.time_ns())
    with open(d / 'ckm_scan.jsonl', 'a', encoding='utf-8') as f: n, best = batch_ckm(f, rng, seconds)
    if best:
        top = min(best.values(), key=lambda r: r['score']); pr = polish(top, seconds=max(5, seconds // 4))
        with open(d / 'ckm_scan.jsonl', 'a', encoding='utf-8') as f: f.write(json.dumps(pr) + '\n')
        best[f"{pr['model']}:{pr['rung_u']}"] = pr if pr['score'] < top['score'] else top
    with open(d / 'propagation.jsonl', 'a', encoding='utf-8') as f: npr = batch_props(f)
    ne = na = 0
    cur = os.environ.get('WEAVE_CURRENT') or str(pathlib.Path(__file__).resolve().parents[3] / 'aegis_current')
    if pathlib.Path(cur).is_dir():
        try:
            with open(d / 'engine_scan.jsonl', 'a', encoding='utf-8') as f: ne, na = batch_engine(f, rng, max(20, seconds // 3), cur)
        except Exception as e:
            ne = 'error: ' + str(e)[:120]
    sp = d / 'summary.json'; S = json.loads(sp.read_text()) if sp.exists() else {'rows': 0, 'best': {}}
    S['rows'] += n
    for k, r in best.items():
        if k not in S['best'] or r['score'] < S['best'][k]['score']: S['best'][k] = r
    S['top'] = sorted(S['best'].values(), key=lambda r: r['score'])[:5]
    sp.write_text(json.dumps(S, indent=1))
    S['engine_rows'] = S.get('engine_rows', 0) + (ne if isinstance(ne, int) else 0); S['engine_all_pass'] = S.get('engine_all_pass', 0) + na
    sp.write_text(json.dumps(S, indent=1))
    return {'weave_sweep': n, 'prop_rows': npr, 'engine_rows': ne, 'engine_all_pass': na, 'best_score': round(S['top'][0]['score'], 2) if S['top'] else None,
            'best_at': f"{S['top'][0]['model']} up rung {S['top'][0]['rung_u']}" if S['top'] else None, 'free_GB': round(free, 1)}


if __name__ == '__main__':
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'weave_data', int(sys.argv[2]) if len(sys.argv) > 2 else 20, seed=1)))
