"""AEGIS Studio desktop app (pywebview → Windows Edge WebView2). Serves index.html + vendor three.js from the bundle (offline);
exposes the live Python engine to the page: recompute(N*, C-factor) runs Janus core on SERAPIS-E; open_classic() opens the classic views.
Build: see build_studio.bat."""
import os, sys, math, threading, webview
BASE = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'engine'))
class Api:
    def __init__(self): self._cache = {}; self._lock = threading.Lock()
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
# ---------- link to Claude: file inbox/outbox (Desktop\AEGIS_PCJOBS\janus_link) ----------
LINK = os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'janus_link')
def handle(api, win, req):
    """One request (dict) -> result (dict). Commands: ping | recompute{N, C} | scan{Ns:[..], Cs:[..]} | tool{name, args} (any AEGIS toolkit via the shared registry; 'list' lists them) | selftest | wave{node, sign} | knob{name, value} | view{name} | eval{js} (UI only).
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
    threading.Thread(target=link_loop, args=(api, win), daemon=True).start()   # start the link before the GUI loop
    webview.start(http_server=True)
