"""Snapshot docs/web/*.json into data.js for AEGIS Studio (run before building the .exe)."""
import json, pathlib, re
R = pathlib.Path(__file__).resolve().parents[2]; W = R / 'docs/web'
def j(n):
    p = W / n; return json.load(open(p, encoding='utf-8')) if p.exists() else None
waves = j('waves.json'); waves and waves.pop('reach', None)
D = dict(web=j('web.json'), waves=waves, modes=j('modes.json'), landscape=j('landscape.json'), grid=j('knob_grid.json'), shapes=j('shapes.json'), strings=j('string_geom.json'),
         particles=json.load(open(R / 'tools/web/particles.json', encoding='utf-8')))
# PW6 inverse string meter table (D1268) for the Strings measurement lens
_m = []
_f = R / 'field_tests/results/pw6_inverse_meter.txt'
if _f.exists():
    for l in open(_f, encoding='utf-8'):
        mm = re.match(r"n_s ([0-9.]+): P_lin ([0-9.]+) \| exact C ([0-9.e+-]+) P ([0-9.]+) .*N\* ([0-9.]+) n_s [0-9.]+ r ([0-9.e+-]+) α_s ([0-9.e+-]+)", l)
        if mm: a = mm.groups(); _m.append(dict(ns=float(a[0]), Plin=float(a[1]), C=float(a[2]), P=float(a[3]), Nstar=float(a[4]), r=float(a[5]), alpha_s=float(a[6])))
if D['strings'] is not None: D['strings']['meter'] = _m
# CubeMind memory stars (public D-note titles only; NO private memory text). Each D-note = a star: pos from a hash, tier EVIDENCE.
import hashlib
_stars = []
_log = R / 'theory/derivations/DERIVATION_LOG.md'
if _log.exists():
    for l in open(_log, encoding='utf-8'):
        m = re.match(r'^## (D\d+[a-z]?):\s*(.+)', l.strip())
        if not m: continue
        did, title = m.group(1), m.group(2)[:80]
        h = hashlib.sha1(did.encode()).digest()
        x = (h[0]/255-0.5)*2; y = (h[1]/255-0.5)*2; z = (h[2]/255-0.5)*2
        low = title.lower()
        topic = ('killed' if 'kill' in low else 'pass' if ('pass' in low or 'adopt' in low) else 'note')
        _stars.append(dict(id=did, title=title, pos=[round(x,3), round(y,3), round(z,3)], topic=topic))
D['memstars'] = _stars
web = D['web']; import yaml
mp = yaml.safe_load(open(R / 'theory/map/map.yaml', encoding='utf-8')); lay = {n['id']: n.get('layer', 1) for n in mp['nodes']}
for n in web['nodes']: n['layer'] = lay.get(n['id'], 1)
# Janus auto-feeder seed: pulses to animate along edges (wiring lane + edges touching the newest nodes). Live pulses come from janus_feed.jsonl via the app.
_pulses = []
_w = D['web']
if _w:
    _edges = _w.get('edges', [])
    # wiring edges (kind 'wire') always pulse
    for e in _edges:
        if e.get('kind') == 'wire': _pulses.append(dict(s=e['s'], t=e['t'], w=1.0))
    # newest nodes (highest D-number in refs) -> pulse their edges
    def _lastd(n):
        import re as _re; m=_re.findall(r'D(\d{3,4})', str(n.get('refs',''))); return max((int(x) for x in m), default=0)
    _newest = sorted(_w.get('nodes', []), key=_lastd, reverse=True)[:6]
    _nid = {n['id'] for n in _newest}
    for e in _edges:
        if e['s'] in _nid or e['t'] in _nid: _pulses.append(dict(s=e['s'], t=e['t'], w=0.8))
    # live feed (if present after a run)
    _ff = R / 'docs/web/janus_feed.jsonl'
    if _ff.exists():
        for l in open(_ff, encoding='utf-8'):
            try: r=json.loads(l)
            except Exception: continue
            if r.get('k')=='pulse': _pulses.append(dict(s=r['s'], t=r['t'], w=r.get('w',1.0), why=r.get('why','')))
D['pulses'] = _pulses[-120:]
(pathlib.Path(__file__).parent / 'data.js').write_text('window.AEGIS = ' + json.dumps(D, ensure_ascii=False) + ';\n', encoding='utf-8')
(pathlib.Path(__file__).parent / 'classic.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'
    + open(W / 'aegis_web.html', encoding='utf-8').read() + '</body></html>', encoding='utf-8')
print('data.js', (pathlib.Path(__file__).parent / 'data.js').stat().st_size, 'bytes')
