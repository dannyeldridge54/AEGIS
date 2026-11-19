import math, json
import numpy as np
def delta(me,mm,mt):
    s=np.sqrt([me,mm,mt]); mu=s.mean(); c=(2/3)*sum((s[k]/mu-1)*np.exp(-2j*np.pi*k/3) for k in range(3))
    A=abs(c); d=math.atan2(c.imag,c.real)
    # convention: sqrt m_k = mu(1+A cos(d + 2pi k/3)); we want delta in (0, 2pi/3) small branch -> report d mod 2pi/3
    return A, d % (2*math.pi/3)
out={}
for lab,(mt,st) in {'PDG2024':(1776.93,0.09),'BelleII':(1777.09,0.14)}.items():
    me,se=0.51099895000,0.00000000015; mm,sm=105.6583755,0.0000023
    A,d=delta(me,mm,mt)
    var=0
    for i,(x,s) in enumerate([(me,se),(mm,sm),(mt,st)]):
        h=s*1e-2 if s>0 else 1e-9; v=[me,mm,mt]; v[i]+=h; var+=((delta(*v)[1]-d)/h*s)**2
    sig=math.sqrt(var); out[lab]=dict(A=A,delta=d,sigma=sig,dev_sigma=(d-2/9)/sig,excluded=abs(d-2/9)>3*sig)
    # sigma without m_tau error (to test the preprint's claim)
    v=0
    for i,(x,s) in enumerate([(me,se),(mm,sm)]):
        h=s*1e-2; vv=[me,mm,mt]; vv[i]+=h; v+=((delta(*vv)[1]-d)/h*s)**2
    out[lab]['sigma_no_mtau']=math.sqrt(v); out[lab]['dev_no_mtau']=(d-2/9)/math.sqrt(v)
print(json.dumps(out,indent=1)); json.dump(out,open('field_tests/results/rb2_delta.json','w'),indent=1)
