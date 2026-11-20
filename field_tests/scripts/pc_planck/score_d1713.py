"""Score PREREG_PLANCK_CLASS (D1713) from results/cls_*.json. Rules exactly as locked."""
import json, os, sys, math
R=sys.argv[1] if len(sys.argv)>1 else 'results'
CAMB={'':2433.52,'_desy5':2677.37,'_union3':1056.28}
W0WA={'':-9.11,'_desy5':-19.72,'_union3':-15.02}
def get(m,s):
    p=os.path.join(R,f'cls_{m}{s}.json')
    return json.load(open(p))['minimum'] if os.path.exists(p) else None
rows={}; gate=True
for s in CAMB:
    L,T,C=get('lcdm',s),get('thread',s),get('coupled',s)
    if L is None: print(s or 'pantheon+','lcdm missing'); gate=False; continue
    g=abs(L['chi2']-CAMB[s])<=2.0; gate&=g
    rows[s]=dict(lcdm=L['chi2'],gate_diff=L['chi2']-CAMB[s],
        thread=None if T is None else T['chi2']-L['chi2'],
        coupled=None if C is None else C['chi2']-L['chi2'],
        b=None if C is None else C.get('rt_bc'), amp=None if C is None else C.get('rt_ui'),
        Om=None if C is None else C.get('Omega_m'), s8=None if C is None else C.get('sigma8'))
print(json.dumps(rows,indent=1)); print('GATE', 'PASS' if gate else 'FAIL/INCOMPLETE')
if gate and all(r['thread'] is not None and r['coupled'] is not None for r in rows.values()):
    a=sum(r['coupled']<=-6 and r['coupled']-r['thread']<=-4 for r in rows.values())
    b=sum(r['coupled']-r['thread']<=-2 for r in rows.values())
    v='fix_confirmed' if a>=2 else ('fix_partial' if b>=2 else 'fix_fails')
    print('VERDICT',v)
    for s,r in rows.items():
        bb=abs(r['b']); zd=(0.70/(0.25*(math.exp(bb*0.64)-1)))**(1/3)-1 if bb>0 else float('inf')
        print(s or 'pantheon+','b=%.4f'%r['b'],'z_dagger(closed form, Ω≈0.70/0.25, Δφ≈0.64)=%.2f'%zd,'w0wa(CAMB, context)',W0WA[s])
