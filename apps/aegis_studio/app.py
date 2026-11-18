"""AEGIS Studio desktop app (pywebview → Windows Edge WebView2). Serves index.html + vendor three.js from the bundle (offline);
exposes the live Python engine to the page: recompute(N*, C-factor) runs Janus core on SERAPIS-E; open_classic() opens the classic views.
Build: see build_studio.bat."""
import os, sys, math, threading, webview
BASE = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'engine'))
class Api:
    def __init__(self): self._cache = {}; self._lock = threading.Lock(); self._win = None
    def recompute(self, nstar, cfac):
        from tools.serapis_calc.pipeline import build
        from tools.janus_calc.core import Model, spectra3
        key = round(float(cfac), 4)
        with self._lock:
            if key not in self._cache:
                m, V, dV, p0 = build('serapis_e', max(key, 1e-6)*1.15e-6); self._cache[key] = Model(V, dV, p0, Nmax=4000)
            out = spectra3(self._cache[key], float(nstar))
        return dict(ns=float(out['ns']), r=float(out['r']), alpha_s=float(out['alpha_s']))
    def tool(self, name, args):
        return run_tool(name, args)
    def collector_points(self):
        """Live collector points (data/collect/serapis_grid.csv on the Desktop) for the Data overlay."""
        import csv
        p = os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'data', 'collect', 'serapis_grid.csv')
        try: return [dict(C=float(r['C']), T=float(r['T_R']), ns=float(r['ns']), r=float(r['r'])) for r in csv.DictReader(open(p))]
        except Exception: return []
    def test_node(self, node): return test_node(node)
    def derive_weave(self, on, order=None):
        return WEAVE.start(self._win, order or []) if on else WEAVE.stop()
    def testable_nodes(self): return sorted(x['id'] for x in _web())
    def test_particle(self, pid): return test_particle(pid)
    def run_chain(self, name): return run_chain(name)
    def chains(self): return sorted(CHAINS)
    def run_circuit(self): return run_circuit()
    def sweep_node(self, node): return sweep_node(node)
    def set_weave_sweep(self, on): WEAVE.sweep = bool(on); return dict(sweep=WEAVE.sweep)
    def open_classic(self):
        webview.create_window('Janus · classic views', url=os.path.join(BASE, 'classic.html'), width=1500, height=950, background_color='#05020D'); return True
def selftest():
    """Janus.exe --selftest: run the bundled engine at grid nodes and compare with the cloud-computed knob grid (data.js). Writes janus_selftest.txt next to the exe."""
    import json, time
    txt = open(os.path.join(BASE, 'data.js'), encoding='utf-8').read(); D = json.loads(txt[txt.index('=') + 1:].rstrip().rstrip(';')); G = D['grid']
    api = Api(); L = []; ok = True
    for cf in (0.5, 1.0, 1.5):
        i = G['Cfac'].index(cf)
        for N in (50.0, 60.0):
            j = G['Nstar'].index(N); t = time.time(); r = api.recompute(N, cf); dt = time.time() - t
            d = (abs(r['ns'] - G['ns'][i][j]), abs(r['r']/G['r'][i][j] - 1), abs(r['alpha_s'] - G['alpha_s'][i][j])); o = d[0] <= 1e-7 and d[1] <= 1e-6 and d[2] <= 1e-7; ok &= o
            L.append(f"C x{cf} N*={N:.0f}: exe n_s {r['ns']:.9f} vs cloud {G['ns'][i][j]:.9f} |dn_s| {d[0]:.1e} |dr/r| {d[1]:.1e} |da| {d[2]:.1e} ({dt:.1f} s) {'PASS' if o else 'FAIL'}")
    L.append('JANUS EXE SELFTEST: ' + ('PASS' if ok else 'FAIL'))
    out = os.path.join(os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)), 'janus_selftest.txt')
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n'); return ok
# ---------- the wiring: shared toolkit registry (CubeMind aegis_tools) + CubeMind memory feed ----------
CM_DIR = os.environ.get('CUBEMIND_DIR', os.path.join(os.path.expanduser('~'), 'CubeMind_janus'))
CM_MEM = os.environ.get('CUBEMIND_MEM', os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'cubemind_code', 'cubemind_memory.jsonl'))
def to_cubemind(text, model, importance=3):
    """Every Janus computation becomes a CubeMind memory record (tier EVIDENCE, topic serapis). Returns True if written."""
    try:
        if CM_DIR not in sys.path: sys.path.insert(0, CM_DIR)
        from mindmem.store import Store
        Store(CM_MEM).add(text=text, source='janus_app', kind='result', tier='EVIDENCE', topic='serapis', importance=importance, model=model); return True
    except Exception: return False
def run_tool(name, args):
    """Run any AEGIS toolkit through the SAME registry CubeMind's +aegis arm uses (aegis_tools.call)."""
    import json
    if CM_DIR not in sys.path: sys.path.insert(0, CM_DIR)
    from aegis_tools import call, TOOLS
    if name == 'list': return dict(tools=sorted(TOOLS))
    res = call(name, args); res['cubemind'] = to_cubemind(f'Janus app ran {name} {json.dumps(args)} -> {json.dumps(res, default=str)[:600]}', name)
    return res

# ---------- Derive the weave / test-run a node (Danny 2026-11-18) ----------
# node id -> (tool, args, check). check(result) -> (ok, short text); a tool error is always a FAIL. Expected values are
# published or locked numbers (D-notes / CERN+1 / smoke test); nodes without an entry have no runnable test yet.
def _num(r, *keys):
    for k in keys:
        v = r.get(k) if isinstance(r, dict) else None
        if isinstance(v, (int, float)): return float(v)
    return None
def _band(key, lo, hi, label):
    def chk(r):
        v = _num(r, *key) if isinstance(key, tuple) else _num(r, key)
        if v is None: return ('error' not in r, 'ran (no ' + label + ' in result)')
        return (lo <= v <= hi, f'{label} = {v:.6g} (expect {lo:g}-{hi:g})')
    return chk
_SER = ('serapis_emulator', {'C': 1.15e-6}, _band(('ns',), 0.970, 0.976, 'n_s'))
NODE_TESTS = {
    'serapis_e': _SER, 'serapis_point': ('serapis_point', {'C': 1.25e-6, 'T_R': 8.94e8}, _band(('ns',), 0.970, 0.976, 'n_s')),
    'band_e_audited': _SER, 'nstar_e': _SER, 'C_nstar': _SER,
    'janus': ('janus_single', {'V': 'phi**2', 'Nstar': 55}, _band(('ns',), 1 - 2/55.5 - 2e-3, 1 - 2/55.5 + 2e-3, 'phi^2 n_s')),
    'J_core': ('janus_single', {'V': 'phi**2', 'Nstar': 55}, _band(('ns',), 1 - 2/55.5 - 2e-3, 1 - 2/55.5 + 2e-3, 'phi^2 n_s')),
    'J_mf': ('janus_mf', {'m2': [1e-11, 9e-11], 'phi_init': [12, 12], 'Nstar': 55}, _band(('ns',), 0.94, 0.98, 'n_s')),
    'string_meter': ('string_meter', {'ns': 0.9744, 'ns_sigma': 0.0016}, _band(('C',), 1.0e-6, 1.6e-6, 'C')),
    'inverse_meter': ('string_meter', {'ns': 0.9728, 'ns_sigma': 0.0027}, _band(('C',), 1.0e-6, 1.6e-6, 'C')),
    'tests_lhc': ('lhc_selftest', {}, lambda r: ('error' not in r and 'FAIL' not in str(r), 'CERN+1 self-test')),
    'wino_window': ('lhc_dt_limit', {'lumi': 136, 'sqrts': '13', 'search': 'ATLAS_136', 'boost': 'fixed', 'band': False}, _band(('m_limit_GeV',), 666.1, 667.1, 'ATLAS 136/fb limit GeV (CERN+1 666.6)')),
    'J_lt': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -1, 'wa': 0, 'z': [0.5, 1.0], 'sigma8': 0.811}, lambda r: ('error' not in r, 'late-universe run')),
    'R_desi': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -1, 'wa': 0, 'z': [0.5, 1.0], 'sigma8': 0.811}, lambda r: ('error' not in r, 'late-universe run')),
    'R_w0wa': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -0.75, 'wa': -0.86, 'z': [0.5, 1.0], 'sigma8': 0.811}, lambda r: ('error' not in r, 'w0-wa run')),
    'S_stab': ('kaluza_stable', {'D': 6, 'gamma': 2}, lambda r: ('error' not in r and 'False' not in str(r.get('stable', '')), 'scalar stability (D1140)')),
    'S_6d': ('kaluza_stable', {'D': 6, 'gamma': 2}, lambda r: ('error' not in r, '6D vacuum')),
    'X_rule': ('lattice_lab', {'cmd': 'flip', 'args': ['E6']}, lambda r: ('error' not in r, 'E6 duality flip')),
}

# ---------- Sweep a node: its tool over a grid -> a table (CSV) the loop checks afterwards (Danny 2026-11-18) ----------
# node -> (tool, base args, swept arg, values, expected trend of key result: +1 rising, -1 falling, 0 none)
NODE_SWEEPS = {
    'serapis_e': ('serapis_emulator', {}, 'C', [1.0e-6, 1.1e-6, 1.2e-6, 1.3e-6, 1.4e-6, 1.5e-6, 1.6e-6], ('ns', +1)),
    'serapis_point': ('serapis_emulator', {}, 'C', [1.0e-6, 1.15e-6, 1.3e-6, 1.45e-6, 1.6e-6], ('ns', +1)),
    'band_e_audited': ('serapis_emulator', {}, 'C', [1.0e-6, 1.15e-6, 1.3e-6], ('r', +1)),
    'janus': ('janus_single', {'V': 'phi**2'}, 'Nstar', [45, 50, 55, 60, 65], ('ns', +1)),
    'J_core': ('janus_single', {'V': 'phi**2'}, 'Nstar', [45, 50, 55, 60, 65], ('ns', +1)),
    'string_meter': ('string_meter', {'ns_sigma': 0.0016}, 'ns', [0.970, 0.972, 0.974, 0.976], ('C', +1)),
    'inverse_meter': ('string_meter', {'ns_sigma': 0.0027}, 'ns', [0.970, 0.972, 0.974, 0.976], ('C', +1)),
    'tests_lhc': ('lhc_lifetime', {}, 'm', [300, 500, 700, 1000, 1500, 2000], ('ctau_cm', -1)),
    'wino_window': ('lhc_xsec', {'sqrts': '13.6'}, 'm', [600, 800, 1000, 1250, 1500], ('sum', -1)),
    'J_lt': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'wa': 0, 'z': [0.5, 1.0], 'sigma8': 0.811}, 'w0', [-1.1, -1.0, -0.9, -0.8], (None, 0)),
}
SWEEP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'janus_link', 'sweeps')
def _flat(d, pre=''):
    out = {}
    for k, v in (d or {}).items():
        if isinstance(v, (int, float)) and not isinstance(v, bool): out[pre + k] = float(v)
        elif isinstance(v, dict): out.update(_flat(v, pre + k + '.'))
    return out
def sweep_node(node):
    """Run the node's tool over its grid (registry call, cached), write sweeps/<node>_<time>.csv, check the expected trend."""
    import csv, time, json
    sw = NODE_SWEEPS.get(node)
    if not sw: return dict(node=node, ok=None, text='no sweep defined for this node yet')
    name, base, key, vals, (rk, trend) = sw; t0 = time.time()
    if CM_DIR not in sys.path: sys.path.insert(0, CM_DIR)
    from aegis_tools import call
    rows = []
    for v in vals:
        r = call(name, dict(base, **{key: v})); f = _flat(r); f[key] = float(v); f['error'] = r.get('error', ''); rows.append(f)
    cols = [key] + sorted({c for r in rows for c in r if c not in (key, 'error')}) + ['error']
    os.makedirs(SWEEP_DIR, exist_ok=True); stamp = time.strftime('%Y%m%d_%H%M%S')
    path = os.path.join(SWEEP_DIR, f'{node}_{stamp}.csv')
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); [w.writerow({c: r.get(c, '') for c in cols}) for r in rows]
    errs = sum(1 for r in rows if r['error']); ys = [r.get(rk) for r in rows] if rk else []
    if errs: ok, txt = False, f'{errs}/{len(rows)} points errored'
    elif rk and None not in ys and trend:
        d = [b - a for a, b in zip(ys, ys[1:])]; ok = all(x*trend > 0 for x in d)
        txt = f"{rk} {'rises' if trend > 0 else 'falls'} with {key}: {'yes' if ok else 'NO'} ({ys[0]:.5g} -> {ys[-1]:.5g})"
    else: ok, txt = True, f'{len(rows)} points, no trend check'
    meta = dict(node=node, tool=name, swept=key, n=len(rows), ok=ok, text=txt, path=path, seconds=round(time.time() - t0, 2))
    open(path[:-4] + '.json', 'w', encoding='utf-8').write(json.dumps(meta))
    _link_log(dict(node=node + ' sweep', tool=name, ok=ok, text=txt))
    to_cubemind(f"Janus sweep {node}: {name} over {key} {vals[0]}..{vals[-1]} -> {txt} (table {os.path.basename(path)})", name, importance=2)
    return meta

# ---- full weave coverage (Danny 2026-11-18 "full mapping and testing all"; "remember the lattices") ----
def _get(r, path):
    for k in path.split('.'):
        if not isinstance(r, dict) or k not in r: return None
        r = r[k]
    return r
def _approx(path, val, tol, label):
    def chk(r):
        v = _get(r, path)
        if not isinstance(v, (int, float)) or isinstance(v, bool): return (False, f'{label}: no {path} in result')
        return (abs(v - val) <= tol, f'{label} = {v:.6g} (expect {val:g} ± {tol:g})')
    return chk
def _is(path, want, label):
    return lambda r: (_get(r, path) == want, f'{label} = {_get(r, path)} (expect {want})')
_ran = lambda label: (lambda r: ('error' not in r, label))
_LL = lambda cmd, *a: ('lattice_lab', {'cmd': cmd, 'args': list(a)})
_DT = lambda lumi, srch: ('lhc_dt_limit', {'lumi': lumi, 'sqrts': '13', 'search': srch, 'boost': 'fixed', 'band': False})
NODE_TESTS.update({
    # lattice lane — published/locked lattice facts (SPLAG; D1277-D1298)
    'X_rule': (*_LL('flip', 'E6'), _is('flips', True, 'E6 hands over to its dual at alpha=1')),
    'X_tool': (*_LL('flip', 'E8'), _is('flips', False, 'E8 is self-dual: never flips')),
    'X_d2': (*_LL('epstein', 'A2', '2'), _approx('epstein', 5.7833593, 2e-6, 'A2 Epstein E(rho,2)')),
    'X_epstein': (*_LL('epstein', 'A2', '2'), _approx('epstein', 5.7833593, 2e-6, 'A2 Epstein E(rho,2)')),
    'X_mellin': (*_LL('epstein', 'A2', '1.5'), _ran('A2 Epstein at s=1.5 (Mellin continuation)')),
    'X_d3': (*_LL('champion', '3'), _ran('d=3 champions (FCC/BCC)')), 'X_flow3': (*_LL('champion', '3'), _ran('d=3 flow FCC <-> BCC')),
    'X_d4': (*_LL('squares', 'D4'), _approx('square_planes', 18, 0, 'D4 square planes')),
    'X_nest': (*_LL('hexagons', 'D4'), _approx('hexagonal_planes', 16, 0, 'hexagons inside D4')),
    'X_d5': (*_LL('flip', 'D5'), _is('flips', True, 'D5 flips with its dual')),
    'X_d6': (*_LL('flip', 'E6'), _is('flips', True, 'E6 flips with its dual')),
    'X_hexin': (*_LL('hexagons', 'E6'), _approx('hexagonal_planes', 120, 0, 'hexagons inside E6')),
    'X_sqin': (*_LL('squares', 'E6'), _approx('square_planes', 270, 0, 'squares inside E6')),
    'X_d7': (*_LL('flip', 'E7'), _is('flips', True, 'E7 flips with its dual')),
    'X_d8': (*_LL('hexagons', 'E8'), _approx('hexagonal_planes', 1120, 0, 'E8 hexagonal planes')),
    'X_mod': (*_LL('modular', 'E8'), _is('match', True, 'theta_E8 = E4')),
    'X_d24': (*_LL('modular', 'Leech'), _is('match', True, 'theta_Leech = E4^3 - 720 Delta')),
    'X_d16': (*_LL('champion', '16'), _ran('d=16 champions (E8+E8 = D16+, BW16)')),
    'X_bw16': (*_LL('flip', 'BW16'), _ran('BW16 vs its dual')),
    'X_crit': (*_LL('critical'), _ran('2D critical points: tau=i saddle, tau=rho minimum')),
    # LHC lane — CERN+1 values pinned in the smoke test
    'Q_xsec': ('lhc_xsec', {'m': 1000, 'sqrts': '13.6'}, _approx('sum', 2.3793, 0.03, 'wino pair sigma(1 TeV, 13.6 TeV) fb')),
    'Q_resummino': ('lhc_xsec', {'m': 1000, 'sqrts': '13.6'}, _approx('sum', 2.3793, 0.03, 'Resummino-table sigma fb')),
    'Q_life': ('lhc_lifetime', {'m': 1000}, _approx('dm_MeV', 164.11, 0.05, 'chargino-neutralino dm MeV')),
    'Q_stats': ('lhc_ul', {'b': 3.0, 'n': 3}, _approx('ul_exact', 5.395, 0.01, 'exact Poisson N95')),
    'Q_dt': (*_DT(136, 'ATLAS_136'), _approx('m_limit_GeV', 666.6, 0.5, 'ATLAS 136/fb limit GeV')),
    'Q_atlas': (*_DT(136, 'ATLAS_136'), _approx('m_limit_GeV', 666.6, 0.5, 'ATLAS 136/fb limit GeV')),
    'Q_dt36': (*_DT(36, 'ATLAS_36'), _approx('m_limit_GeV', 447.8, 0.5, 'ATLAS 36/fb limit GeV')),
    'Q_panel': ('lhc_panel', {}, _approx('run2_limit_GeV', 666.6, 0.5, 'panel Run-2 floor GeV')),
    'Q_future': ('lhc_future', {}, _approx('HL-LHC.low_bkg_TeV', 0.974, 0.01, 'HL-LHC reach TeV')),
    'Q_fccref': ('lhc_future', {}, _ran('FCC-hh reach (17-36% short of the study, D1306)')),
    # janus / theory / sides / wiring
    'T_chronos': ('janus_single', {'V': 'phi**2', 'Nstar': 55}, _approx('ns', 1 - 2/55.5, 2e-3, 'phi^2 n_s')),
    'X_ms': ('serapis_ms', {'C': 1.15e-6, 'Nstar': 50.7}, _band(('ns',), 0.970, 0.976, 'exact-MS n_s')),
    'eps_tilt': _SER, 'C_lepto': _SER,
    'band_e': ('serapis_emulator', {'C': 1.15e-6}, _band(('ns',), 0.970, 0.975, 'n_s in the frozen band')),
    'caps': ('serapis_emulator', {'C': 1.6e-6}, _band(('ns',), 0.95, 0.985, 'n_s under the cap 0.985')),
    'L_cmb': ('string_meter', {'ns': 0.9744, 'ns_sigma': 0.0016}, _band(('C',), 1.0e-6, 1.6e-6, 'C from n_s')),
    'L_nstar': ('nstar_match', {'r': 4.8e-4, 'V_ratio': 2.2674, 'T_R': 8.94e8}, _ran('N* matching')),
    'L_bridge': ('janus_relation', {'ns': 0.9745, 'r': 4.8e-4, 'p': 2.8284, 'kappa': 1}, _ran('Janus relation alpha_s(n_s, r)')),
    'R_growth': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -1, 'wa': 0, 'z': [0.5, 1.0], 'sigma8': 0.811}, _ran('growth run')),
    'S_kk6': ('kaluza_tensor', {'D': 6, 'gamma': 2, 'n': [1], 'eps': 1e-2}, _ran('6D KK first tensor mode (quick cutoff eps=1e-2)')),
    'W_registry': ('lhc_selftest', {}, _ran('toolkit registry answers')),
})
NODE_SWEEPS.update({
    'Q_xsec': ('lhc_xsec', {'sqrts': '13.6'}, 'm', [600, 800, 1000, 1250, 1500], ('sum', -1)),
    'Q_resummino': ('lhc_xsec', {'sqrts': '13.6'}, 'm', [600, 800, 1000, 1250, 1500], ('sum', -1)),
    'Q_stats': ('lhc_ul', {'b': 3.0}, 'n', [0, 2, 4, 6, 8], ('ul_exact', +1)),
    'Q_life': ('lhc_lifetime', {}, 'm', [600, 800, 1000, 1250, 1500], ('dm_MeV', 0)),
    'L_cmb': ('string_meter', {'ns_sigma': 0.0016}, 'ns', [0.970, 0.972, 0.974, 0.976], ('C', +1)),
    'X_ms': ('serapis_ms', {'Nstar': 50.7}, 'C', [1.0e-6, 1.15e-6, 1.3e-6], ('ns', +1)),
})

# ---- every node gets a test (Danny 16:27 "test for all node configs particles discoveries") ----
# 1) LOCAL_TESTS: exact checks computed here (no registry). 2) registry tests (NODE_TESTS). 3) RECORD check for the rest:
#    the node's status agrees with the ladder map and every D-note it cites exists — a consistency test, labelled as such.
def _web():
    import json
    if not hasattr(_web, 'd'):
        t = open(os.path.join(BASE, 'data.js'), encoding='utf-8').read(); D = json.loads(t[t.index('=') + 1:].rstrip().rstrip(';'))
        _web.d = D['web']['nodes']; _web.p = D.get('particles', [])
    return _web.d
def _link_file(name, repo_rel):
    for p in (os.path.join(CM_DIR, 'aegis_link', name), os.path.join(os.environ.get('AEGIS_DIR', ''), repo_rel)):
        if p and os.path.isfile(p): return p
    return None
def _record_check(node):
    import re
    n = next((x for x in _web() if x['id'] == node), None)
    if not n: return False, 'not on the web'
    out, ok = [], True
    mp = _link_file('map.yaml', 'theory/map/map.yaml')
    if mp:
        import yaml
        m = yaml.safe_load(open(mp, encoding='utf-8')); m = m['nodes'] if isinstance(m, dict) else m
        x = next((y for y in m if y['id'] == node), None)
        if x:
            same = x.get('status') == n.get('status'); ok &= same
            out.append(f"map status {x.get('status')} {'=' if same else '≠'} web {n.get('status')}")
    refs = sorted(set(re.findall(r'D\d{3,4}[a-z]?', n.get('refs', '') + ' ' + n.get('label', ''))))
    ix = _link_file('dnotes_index.txt', '')
    if refs and ix:
        have = set(open(ix, encoding='utf-8').read().split()); miss = [r for r in refs if r not in have]
        ok &= not miss; out.append(f"{len(refs) - len(miss)}/{len(refs)} cited D-notes exist" + (f" (missing {', '.join(miss[:4])})" if miss else ''))
    elif refs: out.append(f'{len(refs)} D-refs (no index here to check them)')
    else: out.append('literature/source ref: ' + n.get('refs', '')[:60])
    return ok, 'record check (no calculation): ' + '; '.join(out)
def _g_cfg(d, r_expect):
    """D1352 lattice-disk config: exact T-model closed form at N* = 50.7; must reproduce the locked result."""
    def f():
        a = d / 6; N = 50.7; ye = math.asinh(math.sqrt(4/(3*a))); y = math.acosh(math.cosh(ye) + 4*N/(3*a)); r = 64/(3*a*math.sinh(y)**2)
        return abs(r - r_expect)/r_expect < 2e-3, f'3α = {d/2:g}: r = {r:.4g} at N* = 50.7 (D1352: {r_expect:.4g}); n_s ≈ 0.9609 for every lattice'
    return f
def _moduli():
    v = [d*(d+1)//2 - 1 for d in (1, 2, 3, 4, 5, 8, 24)]
    return v == [0, 2, 5, 9, 14, 35, 299], f'shape moduli d(d+1)/2−1 for d = 1,2,3,4,5,8,24 → {v}'
def _cm_mem():
    p = os.path.join(CM_DIR, 'cubemind_memory.jsonl')
    if not os.path.isfile(p): return False, 'no CubeMind memory file found'
    n = sum(1 for _ in open(p, encoding='utf-8')); return n > 100, f'CubeMind memory holds {n} records'
def _cm_eval():
    import json
    p = os.path.join(CM_DIR, 'mindmem', 'qa1_score.json')
    if not os.path.isfile(p): return False, 'no QA1 score file'
    j = json.load(open(p)); s = j.get('pc_ollama') or next(iter(j.values()))
    return s['similarity_only'] >= 0.6, f"QA1 hit@5: similarity-only {s['similarity_only']} (adopted), default {s['default']} — locked bar 0.6"
def _w_app():
    n = len(_web()); t = sum(1 for x in _web() if x['id'] in NODE_TESTS or x['id'] in LOCAL_TESTS)
    return n > 100, f'Janus answers: {n} web nodes, {t} with a calculation test, the rest record-checked'
LOCAL_TESTS = {
    'G_A2': _g_cfg(2, 1.522e-3), 'G_D4': _g_cfg(4, 3.009e-3), 'G_E6': _g_cfg(6, 4.465e-3),
    'G_E8': _g_cfg(8, 5.893e-3), 'G_BW16': _g_cfg(16, 1.134e-2), 'G_Leech': _g_cfg(24, 1.641e-2),
    'X_moduli': _moduli, 'CM_mem': _cm_mem, 'CM_eval': _cm_eval, 'W_app': _w_app,
}
NODE_TESTS.update({
    'X_rings': (*_LL('automorphisms', 'Z2'), _approx('automorphisms', 8, 0, 'Z[i] square lattice symmetries')),
    'X_su3': (*_LL('hexagons', 'A2'), _approx('hexagonal_planes', 1, 0, 'A2 (SU(3) root lattice) is one hexagon')),
    'X_narain': (*_LL('flip', 'E8'), _is('self_dual', True, 'E8 (even self-dual, Narain-type) is self-dual')),
    'Q_sym': ('lhc_selftest', {}, _ran('CERN+1 symmetry self-tests')),
    'Q_band': (*_DT(136, 'ATLAS_136'), _approx('m_limit_GeV', 666.6, 10.0, '136/fb limit inside the D1309 band 661.5 ± 10 GeV')),
    'L_reheat': ('nstar_match', {'r': 4.8e-4, 'V_ratio': 2.2674, 'T_R': 8.94e8}, _ran('N* with the reheating/kination history')),
    'T_hyperion': ('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -1, 'wa': 0, 'z': [0.5, 1.0]}, _ran('Hyperion late-universe engine')),
    'tests_cmb': ('serapis_point', {'C': 1.25e-6, 'T_R': 8.94e8}, _band(('r',), 4.0e-4, 6.0e-4, 'SERAPIS r for LiteBIRD (σ ≈ 1e-3 → needs CMB-S4-class)')),
    'band_i': ('serapis_emulator', {'C': 1.15e-6}, _band(('ns',), 0.970, 0.975, 'n_s inside the frozen band')),
})

# ---- Tool chains (Danny 16:35 "wire up tools with our serapis pattern as well as each other") ----
# Each step feeds the next tool the previous tool's OUTPUT and checks the hand-off against an independent route.
# Tolerances fixed before the first run (2026-11-18 22:36 UTC); a failed hand-off is a real inconsistency to investigate.
def _chain_serapis(ns_obs=0.9744):
    st = []; add = lambda node, tool, ok, txt: st.append(dict(node=node, tool=tool, ok=bool(ok), text=txt))
    m = run_tool('string_meter', {'ns': ns_obs, 'ns_sigma': 0.0016}); C, Nm, rm, Tm = m.get('C'), m.get('Nstar'), m.get('r'), m.get('T_R')
    add('string_meter', 'string_meter', C is not None, f'n_s {ns_obs} → C = {C:.4g}, N* = {Nm}, T_R = {Tm:.3g}')
    e = run_tool('serapis_emulator', {'C': C}); d = abs(e['ns'] - ns_obs)
    add('serapis_e', 'serapis_emulator', d < 1e-4, f'round trip C → n_s = {e["ns"]:.5f} (|Δ| = {d:.1e}, tol 1e-4)')
    dr = abs(e['r'] - rm)/rm; add('serapis_e', 'serapis_emulator', dr < 0.01, f'r: meter {rm:.4g} vs emulator {e["r"]:.4g} (rel {dr:.1e}, tol 1%)')
    j = run_tool('janus_relation', {'ns': e['ns'], 'r': e['r'], 'p': 2.8284, 'kappa': 1}); dj = abs(j['alpha_s'] - e['alpha_s'])/abs(e['alpha_s'])
    add('L_bridge', 'janus_relation', dj < 0.06, f'α_s: Janus relation {j["alpha_s"]:.4g} vs emulator {e["alpha_s"]:.4g} (rel {dj:.1%}, D1234 tol 6%)')
    pt = run_tool('serapis_point', {'C': C, 'T_R': Tm}); dn = abs(pt['ns'] - e['ns']); dr2 = abs(pt['r'] - e['r'])/e['r']
    add('serapis_point', 'serapis_point', dn < 3e-4 and dr2 < 0.02, f'exact point n_s {pt["ns"]:.5f}, r {pt["r"]:.4g} vs emulator (|Δn_s| {dn:.1e} tol 3e-4; r rel {dr2:.1e} tol 2%)')
    nm = run_tool('nstar_match', {'r': pt['r'], 'V_ratio': pt['V_ratio'], 'T_R': Tm}); dN = abs(nm['Nstar'] - pt['Nstar'])
    add('L_nstar', 'nstar_match', dN < 0.2, f'N* from r: {nm["Nstar"]:.3f} vs exact point {pt["Nstar"]:.3f} (|Δ| {dN:.2g}, tol 0.2)')
    ms = run_tool('serapis_ms', {'C': C, 'Nstar': pt['Nstar']}); dm = abs(ms['ns'] - pt['ns'])
    add('X_ms', 'serapis_ms', dm < 1e-3, f'exact Mukhanov–Sasaki n_s {ms["ns"]:.5f} vs slow-roll point {pt["ns"]:.5f} (|Δ| {dm:.1e}, tol 1e-3)')
    return st
def _chain_lhc(m_gev=1000):
    st = []; add = lambda node, tool, ok, txt: st.append(dict(node=node, tool=tool, ok=bool(ok), text=txt))
    lf = run_tool('lhc_lifetime', {'m': m_gev}); add('Q_life', 'lhc_lifetime', 150 < lf['dm_MeV'] < 175, f"m = {m_gev} GeV → Δm = {lf['dm_MeV']:.2f} MeV, cτ = {lf['ctau_cm']:.3g} cm (two-loop band 150–175 MeV)")
    xs = run_tool('lhc_xsec', {'m': m_gev, 'sqrts': '13'}); xs6 = run_tool('lhc_xsec', {'m': m_gev, 'sqrts': '13.6'})
    k = xs6['sum']/xs['sum']; add('Q_xsec', 'lhc_xsec', 1.05 < k < 1.25, f"σ(13.6)/σ(13) = {k:.3f} at {m_gev} GeV (energy scaling, expect 1.05–1.25)")
    dt = run_tool('lhc_dt_limit', {'lumi': 136, 'sqrts': '13', 'search': 'ATLAS_136', 'boost': 'fixed', 'band': False})
    add('Q_dt', 'lhc_dt_limit', abs(dt['m_limit_GeV'] - 660) < 15, f"recast limit {dt['m_limit_GeV']:.1f} GeV vs ATLAS published 660 (tol 15)")
    fu = run_tool('lhc_future', {}); pa = run_tool('lhc_panel', {}); hl = fu['HL-LHC']['low_bkg_TeV']*1000
    add('Q_panel', 'lhc_panel', abs(pa['hl_lhc_reach_GeV'] - hl) < 5, f"panel HL-LHC reach {pa['hl_lhc_reach_GeV']:.1f} GeV = future-collider tool {hl:.1f} GeV (tol 5)")
    add('wino_window', 'lhc_panel', abs(pa['run2_limit_GeV'] - dt['m_limit_GeV']) < 1, f"window floor {pa['run2_limit_GeV']:.1f} GeV = recast limit {dt['m_limit_GeV']:.1f} GeV")
    return st
def _chain_lattice():
    st = []; add = lambda node, tool, ok, txt: st.append(dict(node=node, tool=tool, ok=bool(ok), text=txt))
    h = run_tool('lattice_lab', {'cmd': 'hexagons', 'args': ['E8']}); q = run_tool('lattice_lab', {'cmd': 'squares', 'args': ['E8']}); md = run_tool('lattice_lab', {'cmd': 'modular', 'args': ['E8']})
    add('X_hexin', 'lattice_lab', h.get('hexagonal_planes') == 1120, f"E8: {h.get('hexagonal_planes')} hexagons, {q.get('square_planes')} squares (D1294/D1296: 1120, 3780)")
    add('X_sqin', 'lattice_lab', q.get('square_planes') == 3780, f"squares/hexagons in E8 = {q.get('square_planes', 0)/max(h.get('hexagonal_planes', 1), 1):.3f}")
    fl = run_tool('lattice_lab', {'cmd': 'flip', 'args': ['E8']})
    add('X_mod', 'lattice_lab', md.get('match') is True and fl.get('flips') is False, f"θ_E8 = E4 ({md.get('match')}) ⇔ E8 never flips ({not fl.get('flips')}): modularity ↔ flip rule (D1291)")
    ep = run_tool('lattice_lab', {'cmd': 'epstein', 'args': ['A2', '2']}); em = run_tool('serapis_emulator', {'C': 1.15e-6})
    add('X_mellin', 'lattice_lab', abs(ep.get('epstein', 0) - 5.7833593) < 2e-6 and 0.970 < em['ns'] < 0.976,
        f"A2 Epstein E(ρ,2) = {ep.get('epstein', 0):.7f} is the SERAPIS-E vacuum energy scale; same potential gives n_s = {em['ns']:.4f} in band")
    return st

def run_circuit():
    """The SERAPIS circuit (circuit.py): every component fires in order, wires carry the quantities, laws are checked.
    Each run is appended to CubeMind's aegis_link/circuit_runs.jsonl (drift vs the last run); each law goes to janus_tests."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('serapis_circuit', os.path.join(BASE, 'circuit.py')); C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
    d = os.path.join(CM_DIR, 'aegis_link'); os.makedirs(d, exist_ok=True)
    res = C.run(run_tool, log_path=os.path.join(d, 'circuit_runs.jsonl'))
    for c in res['comps']:
        for l in c['laws']: _link_log(dict(node=f"circuit:{c['node']}:{l['law']}", tool=c['tool'], ok=l['ok'], text=l['text']))
    to_cubemind(f"SERAPIS circuit: {res['closed']}/{res['n_laws']} laws closed (health {res['health']}); open: " +
                ('; '.join(f"{o['layer']} {'/'.join(o['nodes'])} {o['law']}" for o in res['open']) or 'none'), 'circuit', importance=4)
    return res
CHAINS = {'serapis': _chain_serapis, 'lhc': _chain_lhc, 'lattice': _chain_lattice}
def run_chain(name):
    import time
    t0 = time.time()
    try: steps = CHAINS[name]()
    except Exception as e: steps = [dict(node=name, tool='chain', ok=False, text=f'{type(e).__name__}: {e}')]
    for s_ in steps: s_['chain'] = name; _link_log(dict(s_, node=f"chain:{name}:{s_['node']}"))
    return dict(chain=name, ok=all(s_['ok'] for s_ in steps), steps=steps, seconds=round(time.time() - t0, 2))
_LANE_ORDER = ['theory', 'centre', 'left', 'right', 'lhc', 'janus', 'strings', 'lattice', 'wiring']
def _link_log(rec):
    """Every node test / sweep result also goes to CubeMind's aegis_link/janus_tests.jsonl, which its learn loop ingests (tiered)."""
    import json
    try:
        d = os.path.join(CM_DIR, 'aegis_link'); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'janus_tests.jsonl'), 'a', encoding='utf-8') as fh: fh.write(json.dumps(rec, default=str) + '\n')
    except Exception: pass
    return rec
def test_node(node, pre=None):
    """pre: a tool result already computed for this node's (tool, args) — shared wire, no second run."""
    import time
    t0 = time.time()
    if node in LOCAL_TESTS or node not in NODE_TESTS:
        kind = 'local' if node in LOCAL_TESTS else 'record'
        try: ok, txt = (LOCAL_TESTS[node] if kind == 'local' else (lambda: _record_check(node)))()
        except Exception as e: ok, txt = False, f'{type(e).__name__}: {e}'
        return _link_log(dict(node=node, tool=kind, ok=bool(ok), text=txt, seconds=round(time.time() - t0, 2)))
    name, args, chk = NODE_TESTS[node]
    try:
        r = pre if pre is not None else run_tool(name, args); ok, txt = (False, 'tool error: ' + str(r.get('error'))[:160]) if 'error' in r else chk(r)
    except Exception as e: ok, txt = False, f'{type(e).__name__}: {e}'
    return _link_log(dict(node=node, tool=name, ok=bool(ok), text=txt, seconds=round(time.time() - t0, 2), shared=pre is not None))
def test_particle(pid):
    """A particle is tested through the node that carries it (particles list in data.js)."""
    _web(); p = next((x for x in _web.p if x['id'] == pid), None)
    if not p: return dict(particle=pid, ok=False, text='unknown particle')
    r = test_node(p['node']); return dict(r, particle=pid, state=p.get('state'), text=f"{p.get('name')} ({p.get('state')}) via {p['node']}: {r['text']}")
class Weave:
    """Derive-the-weave switch: walks every testable node (lane order), test-runs it, pulses it on the weave, feeds the result."""
    def __init__(self): self.on = False; self.th = None; self.win = None; self.last = []; self.sweep = False
    def start(self, win, order):
        if self.on: return dict(on=True, note='already deriving')
        self.on, self.win = True, win
        ids = [x['id'] for x in _web()]; nodes = [n for n in order if n in ids] + [n for n in ids if n not in order]
        self.th = threading.Thread(target=self._run, args=(nodes,), daemon=True); self.th.start(); return dict(on=True, nodes=len(nodes))
    def stop(self): self.on = False; return dict(on=False)
    def _emit(self, res):
        import json
        with self.lock:
            self.last.append(res)
            if self.win is not None:
                try: self.win.evaluate_js(f"weaveResult({json.dumps(res)})")
                except Exception: pass
            push(self.win, 'calc', f"{'PASS' if res['ok'] else 'FAIL'} · {res['node']}", f"{res['tool']}: {res['text']} ({res['seconds']} s{', shared wire' if res.get('shared') else ''})")
    def _one(self, group):
        """One wire = every node that asks the same (tool, args): run the tool ONCE, then check each node against that answer."""
        if not self.on: return []
        out = []
        if len(group) == 1:
            r = test_node(group[0]); self._emit(r); out.append(r)
        else:
            name, args, _ = NODE_TESTS[group[0]]
            try: shared = run_tool(name, args)
            except Exception as e: shared = {'error': f'{type(e).__name__}: {e}'}
            for n in group:
                if not self.on: break
                r = test_node(n, pre=shared); self._emit(r); out.append(r)
            with self.lock: push(self.win, 'calc', f'Shared wire · {name}', f"{len(group)} nodes from one run: {', '.join(group)}")
        for n in group:
            if self.sweep and n in NODE_SWEEPS and self.on and any(r['node'] == n and r['ok'] for r in out):
                sw = sweep_node(n)
                with self.lock: push(self.win, 'calc', f"{'SWEEP OK' if sw['ok'] else 'SWEEP CHECK'} · {n}", f"{sw['text']} → {os.path.basename(sw.get('path', ''))}")
        return out
    def _run(self, nodes):
        """Parallel pass (Danny 16:15 "Janus node loop as fast as possible"): tools run as separate processes, so threads
        overlap them. The slow nodes start first so they never hold up the tail. JANUS_WORKERS overrides the pool size."""
        from concurrent.futures import ThreadPoolExecutor
        import time
        self.lock = threading.Lock(); t0 = time.time()
        workers = int(os.environ.get('JANUS_WORKERS', '0')) or max(2, min(8, (os.cpu_count() or 4) // 2))
        slow = ('S_kk6', 'J_mf', 'X_ms', 'S_6d', 'Q_dt36')
        nodes = [n for n in nodes if n in slow] + [n for n in nodes if n not in slow]
        push(self.win, 'calc', 'Deriving the weave', f'{len(nodes)} testable nodes, {workers} at once')
        import json as _j
        groups, seen = [], {}
        for n in nodes:
            if n in NODE_TESTS and n not in LOCAL_TESTS:
                k = (NODE_TESTS[n][0], _j.dumps(NODE_TESTS[n][1], sort_keys=True))
                if k in seen: seen[k].append(n); continue
                seen[k] = [n]; groups.append(seen[k])
            else: groups.append([n])
        push(self.win, 'calc', 'Shared wires', f'{len(nodes)} nodes → {len(groups)} runs ({sum(len(g) > 1 for g in groups)} shared wires)')
        with ThreadPoolExecutor(max_workers=workers) as ex: out = [r for rs in ex.map(self._one, groups) for r in rs]
        if self.on:   # the SERAPIS circuit after the node pass: every component fires, wires carry values, laws checked
            cr = run_circuit()
            for c in cr['comps']:
                self._emit(dict(node=c['node'], tool='circuit', ok=c['ok'], text='; '.join(f"{'✓' if l['ok'] else '✗'} {l['law']}: {l['text']}" for l in c['laws']), seconds=c['seconds'], shared=True))
            with self.lock: push(self.win, 'calc', f"SERAPIS circuit · health {cr['health']:.0%}", f"{cr['closed']}/{cr['n_laws']} laws closed" + (f"; OPEN: {', '.join(o['layer'] + ' ' + '/'.join(o['nodes']) + ' (' + o['law'] + ')' for o in cr['open'])}" if cr['open'] else '; all closed'))
        ok = sum(r['ok'] is True for r in out); fail = sum(r['ok'] is False for r in out)
        self.on = False; push(self.win, 'calc', 'Weave derived', f'{ok} pass, {fail} fail of {ok + fail} nodes in {time.time() - t0:.0f} s')
        if self.win is not None:
            try: self.win.evaluate_js("weaveDone()")
            except Exception: pass
WEAVE = Weave()
# ---------- link to Claude: file inbox/outbox (Desktop\AEGIS_PCJOBS\janus_link) ----------
LINK = os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'janus_link')
def handle(api, win, req):
    """One request (dict) -> result (dict). Commands: ping | test_node{node} | derive_weave{on} | recompute{N, C} | scan{Ns:[..], Cs:[..]} | tool{name, args} (any AEGIS toolkit via the shared registry; 'list' lists them) | selftest | wave{node, sign} | knob{name, value} | view{name} | eval{js} (UI only).
    scan and tool results are also written to CubeMind's memory (to_cubemind)."""
    import json, time
    c = req.get('cmd'); t0 = time.time()
    if c == 'ping': out = dict(ok=True, app='Janus', engine='live', time=time.strftime('%Y-%m-%d %H:%M:%S'))
    elif c == 'recompute': out = dict(ok=True, **api.recompute(req['N'], req['C']))
    elif c == 'scan':
        out = dict(ok=True, rows=[dict(N=n, C=cf, **api.recompute(n, cf)) for cf in req['Cs'] for n in req['Ns']])
        out['cubemind'] = to_cubemind('Janus app scan (SERAPIS-E, Janus core): ' + '; '.join(f"C {1.15e-6*r['C']:.3g} N* {r['N']}: n_s {r['ns']:.5f} r {r['r']:.4g} a_s {r['alpha_s']:.3g}" for r in out['rows'])[:1500], 'janus_core_scan')
    elif c == 'tool': out = dict(ok=True, **run_tool(req['name'], req.get('args', {})))
    elif c == 'selftest': out = dict(ok=bool(selftest()))
    elif c == 'test_node': out = dict(ok=True, **test_node(req['node']))
    elif c == 'sweep_node': out = dict(ok=True, **sweep_node(req['node']))
    elif c == 'derive_weave': out = dict(ok=True, **(WEAVE.start(win, req.get('order', [])) if req.get('on', True) else WEAVE.stop()))
    elif c in ('wave', 'knob', 'view', 'eval') and win is not None:
        js = {'wave': lambda: f"select({json.dumps(req['node'])}); sendWave({int(req.get('sign', 1))}); 'ok'",
              'knob': lambda: f"K[{json.dumps(req['name'])}].set({float(req['value'])}); 'ok'",
              'view': lambda: f"setView({json.dumps(req['name'])}); 'ok'", 'eval': lambda: req['js']}[c]()
        out = dict(ok=True, js_result=win.evaluate_js(js))
    else: out = dict(ok=False, error=f'unknown or unavailable command: {c}')
    out['seconds'] = round(time.time() - t0, 3); out['id'] = req.get('id'); return out
def link_loop(api, win):
    try: _link_loop(api, win)
    except Exception as e:
        import traceback; os.makedirs(LINK, exist_ok=True); open(os.path.join(LINK, 'link_error.txt'), 'w').write(traceback.format_exc())
def push(win, kind, title, text):
    import json
    if win is None: return
    try: win.evaluate_js(f"feed({json.dumps(dict(kind=kind, title=title, text=text))})")
    except Exception: pass
def _link_loop(api, win):
    import json, time, glob
    inbox, outbox = os.path.join(LINK, 'inbox'), os.path.join(LINK, 'outbox'); os.makedirs(inbox, exist_ok=True); os.makedirs(outbox, exist_ok=True)
    open(os.path.join(LINK, 'status.json'), 'w').write(json.dumps(dict(running=True, pid=os.getpid(), since=time.strftime('%H:%M:%S'))))
    time.sleep(4); push(win, 'link', 'Link to Claude open', 'watching janus_link/inbox; cloud calculations appear here as they run')
    feedf = os.path.join(LINK, 'feed.jsonl'); fpos = os.path.getsize(feedf) if os.path.exists(feedf) else 0
    qlogs = os.path.join(os.path.dirname(LINK), 'queue', 'logs'); seen = {}
    for st in glob.glob(os.path.join(qlogs, '*.status')):
        try: seen[st] = open(st).read().strip()
        except OSError: pass
    while True:
        if os.path.exists(feedf) and os.path.getsize(feedf) > fpos:          # cloud calculations streamed by Claude
            with open(feedf, encoding='utf-8') as fh:
                fh.seek(fpos); lines = fh.read().splitlines(); fpos = fh.tell()
            for ln in lines:
                try: ev = json.loads(ln); push(win, ev.get('kind', 'calc'), ev.get('title', 'calc'), ev.get('text', ''))
                except Exception: pass
        for st in glob.glob(os.path.join(qlogs, '*.status')):                 # PC job starts / finishes
            try: v = open(st).read().strip()
            except OSError: continue
            if seen.get(st) != v:
                seen[st] = v; push(win, 'job', 'PC job ' + os.path.basename(st)[:-7], v)
        for f in sorted(os.listdir(inbox)):
            if not f.endswith('.json'): continue
            p = os.path.join(inbox, f)
            try:
                req = json.load(open(p, encoding='utf-8')); push(win, 'link', 'From Claude: ' + str(req.get('cmd')), json.dumps({k: v for k, v in req.items() if k not in ('cmd', 'id')}))
                res = handle(api, win, req); push(win, 'calc', 'Result: ' + str(req.get('cmd')) + (' · ' + str(req.get('name')) if req.get('cmd') == 'tool' else ''), json.dumps({k: v for k, v in res.items() if k not in ('rows', 'cubemind')}, default=str)[:300] + (f" · {len(res['rows'])} rows" if 'rows' in res else ''))
                if res.get('cubemind'): push(win, 'link', '→ CubeMind memory', 'result stored as an EVIDENCE record (topic serapis)')
            except Exception as e: res = dict(ok=False, error=repr(e), file=f)
            tmp = os.path.join(outbox, f + '.tmp'); open(tmp, 'w', encoding='utf-8').write(json.dumps(res)); os.replace(tmp, os.path.join(outbox, f))
            try: os.replace(p, os.path.join(inbox, f + '.done'))
            except OSError: pass
        time.sleep(0.5)
if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    api = Api()
    if '--headless' in sys.argv:              # no window: just the link (for batch runs)
        link_loop(api, None)
    win = webview.create_window('Janus', url=os.path.join(BASE, 'index.html'), js_api=api, width=1680, height=1000, min_size=(1100, 680), background_color='#04020B')
    api._win = win
    threading.Thread(target=link_loop, args=(api, win), daemon=True).start()   # start the link before the GUI loop
    webview.start(http_server=True)
