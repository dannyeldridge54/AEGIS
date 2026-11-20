"""Build 'Status update, 20 November 2026' addendum PDFs from <id>_REFEREE.md (section 'Addendum text')."""
import re, glob, html, json, os, subprocess
SUB = [(r'\(new version of (?:doi:)?10\.5281/zenodo\.24289118\)', '(doi:10.5281/zenodo.24396665)'),
       (r'1 pass, 2 tensions?, 1 fail, 1 open', '1 pass, 2 tension, 2 fail, after the quark row was added and open rows stopped counting (atlas deviation D3; the 12.8 GeV row stays open)'),(r'\(new version of doi:10\.5281/zenodo\.24289118\)', '(doi:10.5281/zenodo.24396665)'),
       (r'new version of doi:10\.5281/zenodo\.24289118', 'doi:10.5281/zenodo.24396665'),
       (r'SERAPIS v3\.4 status update \(being published[^)]*\)', 'SERAPIS v3.4 status update (doi:10.5281/zenodo.24396665)')]
QT = r'"?The Quark Thread"?[^(.;]*\((?:DOI pending|this deposit series[^)]*)\)'
WC = r'"?Weave Control and the Evidence Atlas"?[^(.;]*\((?:DOI pending|this deposit series[^)]*)\)'
def fix(t):
    for a, b in SUB: t = re.sub(a, b, t)
    t = re.sub(QT, '"The Quark Thread" (doi:10.5281/zenodo.24399408)', t)
    t = re.sub(WC, '"Weave Control and the Evidence Atlas" (doi:10.5281/zenodo.24399447)', t)
    t = t.replace('this deposit series, 20 Nov 2026', 'doi:10.5281/zenodo.24399408 / 24399447')
    return t
def md(t):
    t = html.escape(t); t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); t = re.sub(r'(?<!\*)\*(?!\s)(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t); return t
out = {}
for f in sorted(glob.glob('*_REFEREE.md')):
    rid = f.split('_')[0]; s = open(f).read()
    h1 = s.splitlines()[0]
    m0 = re.search(r'"([^"]+)"', h1) or re.search(r'— (.+?)(?: \((?:v[\d.]+|software|\d+ Nov)[^)]*\))*$', h1) or re.search(r'record \d+, (.+?) \(20 Nov', h1)
    title = re.sub(r"^record \d+, ", "", m0.group(1).strip())
    m = re.search(r'## Addendum text[^\n]*\n(.+?)(?=\n## |\Z)', s, re.S)
    raw = '\n'.join(re.sub(r'^>\s?', '', ln) for ln in m.group(1).strip().splitlines())
    raw = re.sub(r'\n\s*[*_(]*\(?≈?\s*\d+\s*words\)?[*_)]*\s*$', '', raw.strip())
    body = fix(raw.strip()); rel = re.search(r'## Related works[^\n]*\n(.+?)(?=\n## |\Z)', s, re.S)
    paras = ''.join(f'<p>{md(p.strip())}</p>' for p in body.split('\n\n') if p.strip())
    h = f'''<!doctype html><meta charset="utf-8"><style>@page{{size:A4;margin:22mm 20mm}}body{{font:11pt/1.45 "DejaVu Serif",Georgia,serif;color:#111}}
h1{{font-size:15pt;margin:0 0 4px}}.m{{font:9.5pt "DejaVu Sans",sans-serif;color:#444;margin-bottom:14px}}p{{margin:0 0 9px;text-align:justify}}code{{font-size:9.5pt}}
.f{{margin-top:14px;font:8.5pt "DejaVu Sans",sans-serif;color:#555;border-top:1px solid #bbb;padding-top:6px}}</style>
<h1>Status update, 20 November 2026</h1><div class="m">Addendum to: {html.escape(title)} (Zenodo record {rid}) · Danny Eldridge, independent researcher, Oklahoma City, Oklahoma, USA · dannyeldridge54@gmail.com</div>
{paras}<div class="f">This addendum accompanies the unchanged original PDF in this new version. It was prepared after an independent referee check against the project log (D-notes up to D1746), locked rules and results in https://github.com/dannyeldridge54/AEGIS (branch unify-bg). Errata are listed only where verified. Licence as the original record.</div>'''
    open(f'build/{rid}_addendum.html', 'w').write(h); out[rid] = dict(title=title, words=len(body.split()))
json.dump(out, open('build/index.json', 'w'), indent=1); print(len(out), 'addenda;', max(v['words'] for v in out.values()), 'max words')
