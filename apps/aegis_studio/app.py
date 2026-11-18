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
    def testable_nodes(self): return sorted(NODE_TESTS)
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
    to_cubemind(f"Janus sweep {node}: {name} over {key} {vals[0]}..{vals[-1]} -> {txt} (table {os.path.basename(path)})", name, importance=2)
    return meta
_LANE_ORDER = ['theory', 'centre', 'left', 'right', 'lhc', 'janus', 'strings', 'lattice', 'wiring']
def test_node(node):
    import time
    t = NODE_TESTS.get(node)
    if not t: return dict(node=node, ok=None, text='no runnable test for this node yet', seconds=0.0)
    name, args, chk = t; t0 = time.time()
    try:
        r = run_tool(name, args); ok, txt = (False, 'tool error: ' + str(r.get('error'))[:160]) if 'error' in r else chk(r)
    except Exception as e: ok, txt = False, f'{type(e).__name__}: {e}'
    return dict(node=node, tool=name, ok=bool(ok), text=txt, seconds=round(time.time() - t0, 2))
class Weave:
    """Derive-the-weave switch: walks every testable node (lane order), test-runs it, pulses it on the weave, feeds the result."""
    def __init__(self): self.on = False; self.th = None; self.win = None; self.last = []; self.sweep = False
    def start(self, win, order):
        if self.on: return dict(on=True, note='already deriving')
        self.on, self.win = True, win
        nodes = [n for n in order if n in NODE_TESTS] + [n for n in NODE_TESTS if n not in order]
        self.th = threading.Thread(target=self._run, args=(nodes,), daemon=True); self.th.start(); return dict(on=True, nodes=len(nodes))
    def stop(self): self.on = False; return dict(on=False)
    def _run(self, nodes):
        import json
        ok = fail = 0; push(self.win, 'calc', 'Deriving the weave', f'{len(nodes)} testable nodes')
        for n in nodes:
            if not self.on: break
            res = test_node(n); self.last.append(res); ok += res['ok'] is True; fail += res['ok'] is False
            if self.win is not None:
                try: self.win.evaluate_js(f"weaveResult({json.dumps(res)})")
                except Exception: pass
            push(self.win, 'calc', f"{'PASS' if res['ok'] else 'FAIL'} · {n}", f"{res['tool']}: {res['text']} ({res['seconds']} s)")
            if self.sweep and res['ok'] and n in NODE_SWEEPS and self.on:
                sw = sweep_node(n); push(self.win, 'calc', f"{'SWEEP OK' if sw['ok'] else 'SWEEP CHECK'} · {n}", f"{sw['text']} → {os.path.basename(sw.get('path', ''))}")
        self.on = False; push(self.win, 'calc', 'Weave derived', f'{ok} pass, {fail} fail of {ok + fail} nodes')
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
