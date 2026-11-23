import json, os, pathlib, subprocess, sys, tempfile
AEGIS = os.environ.get('AEGIS_DIR') or next((p for p in (os.path.join(os.path.dirname(__file__), 'aegis_bundle'), os.path.expanduser('~/aegis'), '/home/claude/aegis') if os.path.isdir(p)), None)
TOOLS = {
 'weave_verdict': ('{"chi2_W": 7217.7, "chi2_L": 7215.3}', 90),
 'weave_wtoday': ('{"ui": 0.157}', 120),
 'weave_engine': ('{"mode": "background", "ui": 0.13}', 180),
 'weave_basic': ('{"q": "Omega_nu_h2", "sum_mnu_eV": 0.0587}', 5),
 'weave_mbb': ('{"s12": 0.3184}', 5),
 'weave_magd7': ('{"alpha_inv": 40}', 5),
 'weave_sidm': ('{"alpha_D": 4.7e-4, "m_A_GeV": 0.3, "v_kms": 1000}', 5),
 'weave_wino': ('{"T_R_GeV": 2.61e8}', 5),
 'weave_genesis': ('{"T_R_GeV": 4.3e8}', 5),
 'weave_axion_relic': ('{"f_GeV": 1e17, "theta": 0.02, "D": 67}', 5),
 'weave_W0': ('{"volume": 1e5, "m32_GeV": 5e5}', 5),
 'weave_rinv': ('{"x": 0.32, "D0": 67.2}', 5),
 'weave_control': ('{"params": {"wino_mass_GeV": 900, "dark_sector": "brane_split", "sugra_m": 1}}', 120),
 'evidence_atlas': ('{}', 120),
 'hyperion_bbn': ('{"omega_b": 0.0224, "dNeff": 0.1}', 30),
 'weave_paths': ('{"from": "m_tauq", "to": "m_X"}', 5),
 'weave_arc': ('{"m": 2, "n": 1}', 60),
 'weave_rladder': ('{"D": 6}', 5),
 'weave_negspace': ('{"b": 0.05, "dphi": 0.64}', 5),
 'weave_rung': ('{"m": 9}', 5),
 'weave_rung_of': ('{"masses": [0.0028, 0.0557, 2.794]}', 5),
 'weave_koide': ('{"masses": [1.29e-3, 0.629, 169]}', 5),
 'weave_koide_slip': ('{"eps": 1e-4}', 30),
 'weave_tauq': ('{"mass_GeV": 3e10, "phi0": 1}', 5),
 'weave_ckm': ('{"model": "w864", "rung_d": 1, "rung_u": 9, "down": {"r1": 1.8, "r2": 0.7, "g_abs": 0.8, "g_arg": 2.9, "f_abs": 2.2, "f_arg": 3.1}, "up": {"r1": 2.6, "r2": 0.33, "g_abs": 0.4, "g_arg": -3.1, "f_abs": 1.7, "f_arg": -3.1}}', 60),
 'weave_proton': ('{"dmhat_over_mhat": 0.01, "dms_over_ms": 0.0}', 5),
 'weave_atomic': ('{"m_e_MeV": 0.511, "alpha": 0.0072973525, "m_p_MeV": 938.272}', 5),
 'janus_single': ('{"V": "phi**2", "Nstar": 55}', 25),
 'janus_mf': ('{"m2": [1e-11, 9e-11], "phi_init": [12, 12], "Nstar": 55}', 120),
 'janus_lt': ('{"h": 0.6736, "ombh2": 0.02237, "omch2": 0.12, "w0": -1, "wa": 0, "z": [0.5, 1.0], "sigma8": 0.811}', 60),
 'kaluza_tensor': ('{"D": 6, "gamma": 2, "n": [1, 2], "eps": 1e-4}', 600),
 'kaluza_stable': ('{"D": 6, "gamma": 2}', 120),
 'lock_lint': ('{"lock_text": "```claims\\n- {id: C1, quantity: x, op: \\"<=\\", value: 1}\\n```"}', 20),
 'lock_verdict': ('{"lock_text": "...", "results": {"x": 0.5}}', 20),
 'serapis_point': ('{"C": 1.25e-6, "T_R": 8.94e8}', 120),
 'serapis_spectra': ('{"C": 1.15e-6, "Nstar": 50.7}', 60),
 'serapis_ms': ('{"C": 1.15e-6, "Nstar": 50.7}', 120),
 'janus_relation': ('{"ns": 0.9745, "r": 4.8e-4, "p": 2.8284, "kappa": 1}', 10),
 'nstar_match': ('{"r": 4.8e-4, "V_ratio": 2.2674, "T_R": 8.94e8}', 10),
 'string_meter': ('{"ns": 0.9744, "ns_sigma": 0.0016}', 60),
 'serapis_emulator': ('{"C": 1.15e-6}', 30),
 'lattice_lab': ('{"cmd": "flip", "args": ["E6"]}', 120),
 'lhc_xsec': ('{"m": 1000, "sqrts": "13.6"}', 20),
 'lhc_ul': ('{"b": 3.0, "n": 3}', 60),
 'lhc_lifetime': ('{"m": 1000}', 10),
 'lhc_dt_limit': ('{"lumi": 136, "sqrts": "13", "search": "ATLAS_136|ATLAS_36", "boost": "fixed|kinematic", "band": false}', 300),
 'lhc_panel': ('{}', 30),
 'lhc_selftest': ('{}', 30),
 'lhc_future': ('{}', 120),
 # Chronos nuclear rung (CM-NUCLEAR, 2026-11-23): decay, isotopes, release clocks, waste, fusion fuel, supernovae, stars
 'chronos_half_life': ('{"nuclide": "Tc-99m"}', 60),
 'chronos_activity_after': ('{"nuclide": "I-131", "A0": 100, "hours": 24}', 60),
 'chronos_make_now': ('{"nuclide": "F-18", "A_needed": 370, "hours": 2.5}', 60),
 'chronos_generator': ('{"parent": "Mo-99", "parent_GBq": 10, "hours": 23}', 60),
 'chronos_release_age': ('{"pair": "Cs-134/Cs-137", "ratio_now": 0.05, "ratio_at_release": 1}', 60),
 'chronos_ac225': ('{"Ac225_MBq_at_purification": 10, "hours": 6, "ac227_ratio_eob": 0.0015, "days_stored": 10}', 60),
 'chronos_pu_age': ('{"am_over_pu_activity": 0.02}', 60),
 'chronos_tritium': ('{"grams": 1000, "years": 1}', 60),
 'chronos_decay_heat': ('{"days_operated": 365, "hours_after_shutdown": 24}', 60),
 'chronos_supernova': ('{"M_Ni_Msun": 0.6, "days": 18, "t0_days": 35}', 60),
 'chronos_nickel_mass': ('{"L_erg_s": 1e41, "days": 200, "mode": "tail", "t0_days": 40}', 60),
 'chronos_wd_merger': ('{"period_s": 765, "m1": 0.26, "m2": 0.50}', 60),
 'chronos_kilonova': ('{"M_ej_Msun": 0.05, "days": 1}', 60),
 'chronos_star_age': ('{"pair": "Th/Eu", "log_eps_observed": -0.52, "production_ratio": 0.45}', 60),
}
TOOL_INTRO = ('You can call validated physics tools. Write one line per call:\nTOOL: <name> <JSON args>\nAvailable: ' +
              '; '.join(f'{k} {v[0]}' for k, v in TOOLS.items()) + '\nI will reply with RESULT lines (JSON).\n')
WORKER = r'''
import json, sys, os, math, tempfile
sys.path.insert(0, os.environ['AEGIS_DIR']); os.chdir(os.environ['AEGIS_DIR'])
name, a = sys.argv[1], json.loads(sys.argv[2]); out = None
if name == 'janus_single':
    import sympy as sp
    from tools.janus_calc.core import Model, spectra3
    x = sp.symbols('phi'); e = sp.sympify(a['V'], locals={'phi': x}); V = sp.lambdify(x, e, 'math'); dV = sp.lambdify(x, sp.diff(e, x), 'math')
    N = float(a.get('Nstar', 55)); y0 = None
    for y in [float(v) for v in a.get('starts', [5, 10, 15, 20, 30, 40, 60])]:
        try:
            m = Model(V, dV, y, Nmax=4000)
            if m.Nend >= N + 15: y0 = y; break
        except Exception: pass
    if y0 is None: raise RuntimeError('no start with enough e-folds; pass "starts"')
    s = spectra3(m, N); out = dict(ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']), beta_s=float(s['beta_s']), start=y0)
elif name == 'janus_mf':
    import numpy as np
    from tools.janus_calc.mfms import spectra_mf
    m2 = np.array(a['m2'], float); s = spectra_mf(lambda f: 0.5*float(m2 @ (f*f)), lambda f: m2*f, lambda f: np.diag(m2), list(map(float, a['phi_init'])), Nstar=float(a.get('Nstar', 55)))
    out = dict(ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']))
elif name == 'janus_lt':
    from tools.janus_lt.background import Cosmo
    from tools.janus_lt.growth import growth
    c = Cosmo(100*a['h'], a['ombh2'], a['omch2'], a.get('w0', -1), a.get('wa', 0)); zs = [float(z) for z in a['z']]; g = growth(c, zs); s8 = a.get('sigma8')
    out = {str(z): dict(DM_Mpc=c.DM(z), H_kms_Mpc=c.H(z), D=g[z][0], f=g[z][1], fsigma8=(g[z][1]*g[z][0]*s8 if s8 else None)) for z in zs}
elif name in ('kaluza_tensor', 'kaluza_stable'):
    import sympy as sp
    from tools.kaluza.background import vacuum
    bg = vacuum(int(a['D']), sp.nsimplify(a['gamma']))
    if name == 'kaluza_stable':
        from tools.kaluza.stability import scalar_condition; out = scalar_condition(bg)
    else:
        from tools.kaluza.spectra import tensor_pw; from tools.kaluza.solvers import pruefer_SL
        p, w = tensor_pw(bg); ye = float(bg['y_end']); e = float(a.get('eps', 1e-4))
        out = {f'm2_{n}': pruefer_SL(int(n), p, w, e*ye, (1 - e)*ye) for n in a.get('n', [1])}; out['note'] = 'units of the 5D scale; cutoff eps (D1036: converges as eps^0.84)'
elif name in ('serapis_point', 'serapis_spectra', 'serapis_ms'):
    from tools.serapis_calc.pipeline import build
    from tools.janus_calc.core import Model, spectra3
    C = float(a.get('C', 1.15e-6)); m, V, dV, p0 = build('serapis_e', C); M = Model(V, dV, p0, Nmax=4000)
    if name == 'serapis_point':
        from tools.serapis_calc.nstar import Nstar
        Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
        for _ in range(40):
            s = spectra3(M, N); ra = V(M.sol.sol(M.Nend - N)[0])/Ve; N2 = Nstar(s['r'], ra, float(a['T_R']))
            if abs(N2 - N) < 1e-3: break
            N = N2
        s = spectra3(M, N2); out = dict(Nstar=N2, ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']), V_ratio=ra, engine='janus core spectra3 + nstar (exact end)')
    elif name == 'serapis_spectra':
        s = spectra3(M, float(a['Nstar'])); out = dict(ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']), engine='janus core spectra3')
    else:   # U1b (D1255): compiled, ripple-free exact MS (bd 4000, 9-point fit)
        import numpy as np
        from tools.serapis_calc.ms_jit import build_spline, spectra_msjit
        mj, q0 = build_spline('serapis_e', C); s = spectra_msjit(mj, q0, float(a['Nstar']), dlnk=tuple(np.linspace(-0.1, 0.1, 9)), bd=4000.0)
        out = dict(ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']), engine='exact Mukhanov-Sasaki (compiled, U1b)')
elif name == 'lhc_xsec':
    from tools.lhc import xsec as X
    out = X.total(float(a['m']), a.get('sqrts', '13.6')); out['unit'] = 'fb'; out['source'] = 'Resummino tables (arXiv:2304.11915) via ln-ln spline, LOO max 0.3%'
elif name == 'lhc_ul':
    from tools.lhc import stats as St
    out = dict(ul_exact=St.ul_poisson(float(a['b']), int(a['n'])), ul_pyhf=St.ul_pyhf(float(a['b']), int(a['n']), float(a.get('sigma_b', 0.0))), note='95% CLs on signal events; exact Poisson preferred at low counts')
elif name == 'lhc_lifetime':
    from tools.lhc import lifetime as Lt
    out = Lt.widths(float(a['m']))
elif name == 'lhc_dt_limit':
    from tools.lhc import recast_dt as Rd
    if float(a.get('lumi', 136)) > 136: out = Rd.hl_lhc(float(a['lumi']), sqrts=float(a.get('sqrts', 14.0)))
    elif a.get('search') and a.get('band'):
        from tools.lhc import theory_band as Tb
        out = Tb.band(a['search']); out['note'] = 'kinematic boost; band = Resummino scale+PDF (2304.11915 Tab. 6) and dm +-0.4 MeV (D1309)'
    elif a.get('search') and a.get('boost') == 'kinematic':
        from tools.lhc import kinematics as Kn
        out = dict(m_limit_GeV=Kn.limit_search(a['search']), published_GeV=Rd.SEARCHES[a['search']]['published'], ref=Rd.SEARCHES[a['search']]['ref'], boost='computed distribution (D1307)')
    elif a.get('search'): out = dict(m_limit_GeV=Rd.limit_search(a['search']), published_GeV=Rd.SEARCHES[a['search']]['published'], ref=Rd.SEARCHES[a['search']]['ref'])
    else: out = dict(m_limit_GeV=Rd.limit(), N95=Rd.N95_OBS, note='ATLAS 2201.02472 recast; ATLAS quotes 660 GeV')
elif name == 'lhc_future':
    from tools.lhc import future as Fu
    out = Fu.table(); out['note'] = 'TeV; beyond 13.6 TeV the cross sections are a rough Drell-Yan extrapolation (FCC-hh 17-36% below the published study)'
elif name == 'lhc_selftest':
    from tools.lhc import selftest as Sf
    out = Sf.run()
elif name == 'lhc_panel':
    from tools.lhc import panel as Pn
    out = Pn.panel()
elif name == 'lattice_lab':
    from tools.lattice import lattice_lab as LL
    out = LL.CMDS[a['cmd']](*a.get('args', []))
elif name == 'janus_relation':
    from tools.serapis_calc.relation import alpha_s
    out = dict(alpha_s=alpha_s(float(a['ns']), float(a['r']), float(a.get('p', 2*2**0.5)), float(a.get('kappa', 1))))
elif name == 'nstar_match':
    from tools.serapis_calc.nstar import Nstar
    out = dict(Nstar=Nstar(float(a['r']), float(a['V_ratio']), float(a['T_R']), g=float(a.get('g', 106.75))))
elif name == 'serapis_emulator':   # PT1 (fast surrogate at the leptogenesis T_R)
    from tools.serapis_calc.emulator import emulate
    out = emulate(float(a['C']))
elif name == 'string_meter':   # T1 (inverse string meter, PW6 D1268)
    from tools.serapis_calc.meter import meter
    out = meter(float(a['ns']), a.get('ns_sigma'), float(a.get('T_R', 7.389e8)), bool(a.get('exact', False)))
elif name in ('lock_lint', 'lock_verdict'):
    d = tempfile.mkdtemp(); p = os.path.join(d, 'L.md'); open(p, 'w').write(a['lock_text'])
    if name == 'lock_lint':
        from tools.lockbench.lint import lint; out = dict(problems=lint(p))
    else:
        from tools.lockbench.claims import evaluate; out = evaluate(p, a['results'])
elif name in ('weave_control', 'evidence_atlas', 'hyperion_bbn'):   # current AEGIS toolkits (20 Nov 2026)
    _cur = os.path.join(os.path.dirname(os.environ['AEGIS_DIR']), 'aegis_current'); sys.path.insert(0, _cur); os.chdir(_cur)
    for _m in [k for k in list(sys.modules) if k == 'tools' or k.startswith('tools.')]: del sys.modules[_m]
    import cm_bridge as _B; out = _B.TOOLS[name](a)
elif name.startswith('chronos_'):   # CM-NUCLEAR (23 Nov 2026): referee-cleared Chronos engine (D2189), returns numbers + chart specs
    sys.path.insert(0, os.path.join(os.environ['AEGIS_DIR'], 'tools', 'gifts', 'chronos')); import chronos_cm as _C; out = _C.run(name, a)
elif name.startswith('weave_'):   # Weave derivation track (20 Nov 2026)
    sys.path.insert(0, os.path.join(os.environ['AEGIS_DIR'], 'tools', 'weave_cm')); import weave_tools as _W; out = _W.TOOLS[name](a)
print(json.dumps(out, default=str))
'''
def env_threads():
    import os as _os
    return str(max(1, (_os.cpu_count() or 4) - 1))

# AF (2026-11-18): every tool run lights its wire in Janus. Map each tool -> the web node it feeds.
TOOL_NODE = {
    'janus_single': ('janus_core', 'janus_core'), 'janus_mf': ('janus_core', 'janus_core'),
    'janus_lt': ('janus_lt', 'janus_lt'), 'kaluza_tensor': ('kaluza', 'kaluza'), 'kaluza_stable': ('kaluza', 'kaluza'),
    'serapis_point': ('serapis_e', 'serapis_point'), 'serapis_spectra': ('serapis_e', 'serapis_point'),
    'serapis_ms': ('serapis_e', 'ms_jit'), 'serapis_emulator': ('serapis_e', 'serapis_point'),
    'string_meter': ('serapis_point', 'string_meter'), 'janus_relation': ('serapis_point', 'serapis_point'),
    'nstar_match': ('serapis_point', 'serapis_point'), 'lock_lint': ('lockbench', 'lockbench'), 'lock_verdict': ('lockbench', 'lockbench'),
    'lattice_lab': ('X_rule', 'X_rule'), 'lhc_xsec': ('tests_lhc', 'tests_lhc'), 'lhc_ul': ('tests_lhc', 'tests_lhc'), 'lhc_lifetime': ('tests_lhc', 'tests_lhc'), 'lhc_dt_limit': ('tests_lhc', 'tests_lhc'), 'lhc_panel': ('tests_lhc', 'tests_lhc'), 'lhc_selftest': ('tests_lhc', 'tests_lhc'), 'lhc_future': ('tests_lhc', 'tests_lhc'),
}
def _pulse(name, ok):
    """Append a Janus activity pulse for this tool run. Never raises (feed is best-effort)."""
    try:
        if AEGIS is None: return
        import importlib.util as _u
        fp = os.path.join(AEGIS, 'tools', 'web', 'janus_feed.py')
        if not os.path.isfile(fp): return
        sp = _u.spec_from_file_location('_janus_feed', fp); m = _u.module_from_spec(sp); sp.loader.exec_module(m)
        s, t = TOOL_NODE.get(name, ('toolkits', 'toolkits'))
        m.pulse(s, t, 1.0 if ok else 0.4, ('tool ' + name + (' ok' if ok else ' err')))
    except Exception:
        pass
_CODE_STAMP = None
def _code_stamp():
    """Fingerprint of the toolkit code: any edit to a .py under AEGIS/tools invalidates cached results."""
    global _CODE_STAMP
    if _CODE_STAMP is None:
        import hashlib
        h = hashlib.md5()
        for f in sorted((pathlib.Path(AEGIS) / 'tools').rglob('*.py')):
            try: st = f.stat(); h.update(f'{f}:{st.st_mtime_ns}:{st.st_size}'.encode())
            except OSError: pass
        _CODE_STAMP = h.hexdigest()[:12]
    return _CODE_STAMP
def _cache_path(name, args):
    import hashlib
    key = hashlib.md5((name + json.dumps(args, sort_keys=True) + _code_stamp()).encode()).hexdigest()
    d = pathlib.Path(os.environ.get('AEGIS_CACHE', pathlib.Path.home() / '.cache' / 'aegis')) / 'results'
    return d / f'{name}_{key}.json'
def call(name, args):
    """Run a toolkit call. Speed pass 2026-11-18: deterministic tools are memoised on disk (same name + args + same code =
    instant answer); set AEGIS_NOCACHE=1 to force a fresh run. Errors are never cached."""
    if name not in TOOLS: return {'error': f'unknown tool {name}'}
    if AEGIS is None: return {'error': 'AEGIS toolkits not found (set AEGIS_DIR)'}
    cp = None
    if not os.environ.get('AEGIS_NOCACHE') and name not in ('lock_lint', 'lock_verdict'):
        try:
            cp = _cache_path(name, args)
            if cp.exists():
                out = json.loads(cp.read_text()); out['_cached'] = True; _pulse(name, True); return out
        except Exception:
            cp = None
    out = _call_fresh(name, args)
    if cp is not None and 'error' not in out:
        try: cp.parent.mkdir(parents=True, exist_ok=True); cp.write_text(json.dumps(out))
        except Exception: pass
    return out
def _call_fresh(name, args):
    # Danny 2026-11-18: tools run on CPU only (keep the GPU for the models, which stay RAM/VRAM-resident).
    env = dict(os.environ, AEGIS_DIR=AEGIS, CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS=env_threads(), MKL_NUM_THREADS=env_threads(), OPENBLAS_NUM_THREADS=env_threads())
    try:
        r = subprocess.run([sys.executable, '-c', WORKER, name, json.dumps(args)], capture_output=True, text=True, timeout=TOOLS[name][1], env=env)
        out = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {'error': (r.stderr or 'failed').strip().splitlines()[-1][:200]}
        _pulse(name, 'error' not in out); return out
    except subprocess.TimeoutExpired: _pulse(name, False); return {'error': f'timeout {TOOLS[name][1]} s'}
    except Exception as e: _pulse(name, False); return {'error': f'{type(e).__name__}: {e}'[:200]}
