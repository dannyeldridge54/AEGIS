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
web = D['web']; import yaml
mp = yaml.safe_load(open(R / 'theory/map/map.yaml', encoding='utf-8')); lay = {n['id']: n.get('layer', 1) for n in mp['nodes']}
for n in web['nodes']: n['layer'] = lay.get(n['id'], 1)
(pathlib.Path(__file__).parent / 'data.js').write_text('window.AEGIS = ' + json.dumps(D, ensure_ascii=False) + ';\n', encoding='utf-8')
(pathlib.Path(__file__).parent / 'classic.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'
    + open(W / 'aegis_web.html', encoding='utf-8').read() + '</body></html>', encoding='utf-8')
print('data.js', (pathlib.Path(__file__).parent / 'data.js').stat().st_size, 'bytes')
