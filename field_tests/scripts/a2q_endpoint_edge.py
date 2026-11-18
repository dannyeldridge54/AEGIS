# A2q: rescale A2o f_max by 1/R (A2p, Delta=0.10) and reclassify. Same verdict rule as A2o.
import re
R={'1.0':1.1174,'1.25':1.1415,'1.5':1.1622}
txt=open('field_tests/results/a2o_upper_edge.txt').read().splitlines()
M=None
for l in txt:
    m=re.match(r'M=([\d.]+) TeV:.*f_pred=\[([\d.]+),([\d.]+)\]',l)
    if m: M,lo,hi=m.group(1),float(m.group(2)),float(m.group(3)); print(f'M={M} TeV f_pred=[{lo},{hi}] R={R[M]}'); continue
    m=re.match(r'\s+(.+?): J/Jb=([\d.]+); LO \[([\d.]+),([\d.]+)\] \S+; NLO \[([\d.]+),([\d.]+)\] \S+',l)
    if m and M:
        out=[]
        for a,b in((3,4),(5,6)):
            x,y=float(m.group(a))/R[M],float(m.group(b))/R[M]
            v='PASS' if x>=hi else ('FAIL' if y<lo else 'BAND-DEP')
            out.append(f'[{x:.3f},{y:.3f}] {v}')
        print(f'  {m.group(1)}: LO {out[0]}; NLO {out[1]}')
