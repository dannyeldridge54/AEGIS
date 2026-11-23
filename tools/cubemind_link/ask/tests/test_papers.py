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
res['verdict'] = dict(P1=res['P1']['n_bad'] == 0, P2=res['P2'], P3=P3_s <= 10, P4=res['P4']); res['verdict']['PASS'] = all(res['verdict'].values())
json.dump(res, open(os.path.join(HERE, '..', '..', '..', 'field_tests', 'results', 'cm_papers.json'), 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
