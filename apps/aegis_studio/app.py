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
# ---------- link to Claude: file inbox/outbox (Desktop\AEGIS_PCJOBS\janus_link) ----------
LINK = os.path.join(os.path.expanduser('~'), 'Desktop', 'AEGIS_PCJOBS', 'janus_link')
def handle(api, win, req):
    """One request (dict) -> result (dict). Commands: ping | recompute{N, C} | scan{Ns:[..], Cs:[..]} | selftest | wave{node, sign} | knob{name, value} | view{name} | eval{js} (UI only)."""
    import json, time
    c = req.get('cmd'); t0 = time.time()
    if c == 'ping': out = dict(ok=True, app='Janus', engine='live', time=time.strftime('%Y-%m-%d %H:%M:%S'))
    elif c == 'recompute': out = dict(ok=True, **api.recompute(req['N'], req['C']))
    elif c == 'scan': out = dict(ok=True, rows=[dict(N=n, C=cf, **api.recompute(n, cf)) for cf in req['Cs'] for n in req['Ns']])
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
def _link_loop(api, win):
    import json, time
    inbox, outbox = os.path.join(LINK, 'inbox'), os.path.join(LINK, 'outbox'); os.makedirs(inbox, exist_ok=True); os.makedirs(outbox, exist_ok=True)
    open(os.path.join(LINK, 'status.json'), 'w').write(json.dumps(dict(running=True, pid=os.getpid(), since=time.strftime('%H:%M:%S'))))
    while True:
        for f in sorted(os.listdir(inbox)):
            if not f.endswith('.json'): continue
            p = os.path.join(inbox, f)
            try: req = json.load(open(p, encoding='utf-8')); res = handle(api, win, req)
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
