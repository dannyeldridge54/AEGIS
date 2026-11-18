"""Build docs/web/aegis_web.html from web.json + waves.json (rerun after build_web.py and waves.py)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
t = open(R / 'tools/web/page_template.html', encoding='utf-8').read()
w = json.load(open(R / 'docs/web/web.json', encoding='utf-8')); v = json.load(open(R / 'docs/web/waves.json', encoding='utf-8')); v.pop('reach', None)
out = t.replace('__WEB__', json.dumps(w, ensure_ascii=False)).replace('__WAVES__', json.dumps(v, ensure_ascii=False))
open(R / 'docs/web/aegis_web.html', 'w', encoding='utf-8').write(out); print(len(out), 'bytes')
