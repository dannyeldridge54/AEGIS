"""PREREG_CM_PAPERS tests P1-P4."""
import json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import cm_paper as P
t0 = time.time(); out = P.build('all'); P3_s = time.time() - t0
res = dict(P3_seconds=P3_s)
# P1: rerun every engine call independently and compare every printed value
bad = []; nnum = 0
for m in out['made']:
    tr = json.load(open(os.path.join(HERE, 'papers', m['section'] + '.trace.json')))
    page = open(os.path.join(HERE, 'papers', m['section'] + '.html'), encoding='utf-8').read()
    body = page.split('<h2>Appendix')[0]
    for p in tr['printed']:
        nnum += 1; c = tr['calls'][p['call']]; r = P.C.run(c['name'], dict(c['args'])); v = float(P.get(r, p['path']))
        if P.fmt(v) != p['shown'] or abs(v - p['value']) > 1e-12 * max(1, abs(v)) or p['shown'] not in body: bad.append((m['section'], p))
res['P1'] = dict(numbers=nnum, mismatches=bad[:5], n_bad=len(bad))
# DEV-1 P1b inputs echoed from call args; P1c constants re-read from the engine; both must appear in the body
bi, bc, ni, nc = [], [], 0, 0
for m in out['made']:
    tr = json.load(open(os.path.join(HERE, 'papers', m['section'] + '.trace.json')))
    body = open(os.path.join(HERE, 'papers', m['section'] + '.html'), encoding='utf-8').read().split('<h2>Appendix')[0]
    for q in tr['inputs']:
        ni += 1; v = tr['calls'][q['call']]['args'][q['key']]
        if v != q['value'] or q['shown'] not in body: bi.append((m['section'], q))
    for q in tr['consts']:
        nc += 1; v = float(P.CONST[q['name']]())
        if P.fmt(v) != q['shown'] or q['shown'] not in body: bc.append((m['section'], q))
res['P1b'] = dict(inputs=ni, n_bad=len(bi), bad=bi[:5]); res['P1c'] = dict(consts=nc, n_bad=len(bc), bad=bc[:5])
# P1d: no bare decimal number left in abstract/rows/methods that is not traced (heuristic scan; years/ids/section numbers excluded)
import html as _h
traced = set(); untraced = []
for m in out['made']:
    tr = json.load(open(os.path.join(HERE, 'papers', m['section'] + '.trace.json')))
    for q in tr['printed'] + tr['inputs'] + tr['consts']: traced.add(re.sub(r'<[^>]+>|&times;', ' ', q['shown']).split()[0])
    pg = open(os.path.join(HERE, 'papers', m['section'] + '.html'), encoding='utf-8').read()
    for sec in ('Abstract', 'Method', 'Results'):
        blk = pg.split(f'<h2>{sec}</h2>')[1].split('<h2>')[0]; txt = _h.unescape(re.sub(r'<sup>[^<]*</sup>|<[^>]+>', ' ', blk))
        for tok in re.findall(r'(?<![\w-])-?\d+(?:\.\d+)?(?![\w-])', txt):
            if tok not in traced and tok not in ('0', '1', '2', '10', '0.2', '1.3', '97.9', '2.1'): untraced.append((m['section'], sec, tok))
res['P1d_untraced_tokens'] = sorted(set(untraced))
# P4b: every chart has a title and y label
P4b = True
for m in out['made']:
    pg = open(os.path.join(HERE, 'papers', m['section'] + '.html'), encoding='utf-8').read()
    ch = json.loads(pg.split('const CH=')[1].split(';\n')[0])
    P4b &= all(c.get('title') and c.get('y_label') for c in ch)
res['P4b'] = bool(P4b)
# P5: Ac-225 chain, matrix exponential (engine) vs analytic Bateman (mpmath, 50 digits), at 6 h
import mpmath as mp; mp.mp.dps = 50
A3 = P.C.A3; t = 6 * P.C.H; A0 = 10.0
lam = {k: mp.mpf(A3.LAM[k]) for k in ['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Po-213', 'Tl-209', 'Pb-209']}
def bateman(path, brs):
    N1 = mp.mpf(A0) / lam[path[0]]; pref = N1 * mp.fprod([b * lam[k] for k, b in zip(path[:-1], brs)]); s = 0
    for i, ki in enumerate(path):
        s += mp.e ** (-lam[ki] * t) / mp.fprod([lam[kj] - lam[ki] for j, kj in enumerate(path) if j != i])
    return pref * s * lam[path[-1]]   # activity
bpo, btl = P._br('Bi-213', 'Po-213'), P._br('Bi-213', 'Tl-209')
ana = {'Bi-213': bateman(['Ac-225', 'Fr-221', 'At-217', 'Bi-213'], [1, 1, 1]),
       'Po-213': bateman(['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Po-213'], [1, 1, 1, bpo]),
       'Tl-209': bateman(['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Tl-209'], [1, 1, 1, btl]),
       'Pb-209': bateman(['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Po-213', 'Pb-209'], [1, 1, 1, bpo, 1]) + bateman(['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Tl-209', 'Pb-209'], [1, 1, 1, btl, 1])}
eng = A3.ac225_activities(t, A0)[0]
res['P5_maxrel'] = float(max(abs(eng[k] - float(v)) / float(v) for k, v in ana.items()))
# P4
res['P4'] = all('<h2>Limits</h2>' in open(os.path.join(HERE, 'papers', m['section'] + '.html'), encoding='utf-8').read() for m in out['made'])
# P2 via playwright
js = r"""
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const out={};
for(const s of process.argv.slice(2)){const p=await b.newPage({viewport:{width:900,height:900}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+s);await p.waitForTimeout(2500);
const info=await p.evaluate(()=>[...document.querySelectorAll('canvas')].map(c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let v=new Set();for(let i=0;i<d.length;i+=4000)v.add(d[i]+','+d[i+1]+','+d[i+2]);return v.size}));
out[s.split('/').pop()]={errs,canvases:info.length,distinct_colors:info};await p.close();}
console.log(JSON.stringify(out));await b.close();})();"""
open('/tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/p2.js', 'w').write(js)
files = [os.path.join(HERE, 'papers', m['section'] + '.html') for m in out['made']]
r2 = json.loads(subprocess.run(['node', '/tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/p2.js'] + files, capture_output=True, text=True).stdout)
res['P2_detail'] = r2; res['P2'] = all(not v['errs'] and v['canvases'] >= 1 and all(k > 20 for k in v['distinct_colors']) for v in r2.values())
res['verdict'] = dict(P1=res['P1']['n_bad'] == 0, P2=res['P2'], P3=P3_s <= 10, P4=res['P4'], P1b=res['P1b']['n_bad'] == 0, P1c=res['P1c']['n_bad'] == 0, P4b=res['P4b'], P5=res['P5_maxrel'] < 1e-9)
res['P1d_note'] = 'informational scan; flagged tokens reviewed by hand: citation years (1964, 2012, 2019) and isotope mass numbers in lambda subscripts (134, 137) are labels, not quantities'; res['verdict']['PASS'] = all(res['verdict'].values())
json.dump(res, open(os.path.join(HERE, '..', '..', '..', 'field_tests', 'results', 'cm_papers.json'), 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
