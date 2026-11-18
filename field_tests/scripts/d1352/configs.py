import json, numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
CFG = [('A2',2),('D4',4),('E6',6),('E8',8),('BW16',16),('Leech',24)]
def V(p,a): return np.tanh(p/np.sqrt(6*a))**2
def dV(p,a,h=1e-5): return (V(p+h,a)-V(p-h,a))/(2*h)
def d2V(p,a,h=1e-4): return (V(p+h,a)-2*V(p,a)+V(p-h,a))/h**2
eps=lambda p,a: 0.5*(dV(p,a)/V(p,a))**2
eta=lambda p,a: d2V(p,a)/V(p,a)
def obs(a,N):
    pe=brentq(lambda p: eps(p,a)-1, 1e-3, 50)
    Nf=lambda p: quad(lambda x: V(x,a)/dV(x,a), pe, p, limit=200)[0]
    ps=brentq(lambda p: Nf(p)-N, pe+1e-6, 200)
    e,h=eps(ps,a),eta(ps,a)
    return 1-6*e+2*h, 16*e
out=[]
for L,d in CFG:
    a=d/6
    for N in (50.7,55):
        ns,r=obs(a,N)
        p1=(ns-0.9684)/0.0030; p2=(ns-0.9728)/0.0027
        alive=(min(abs(p1),abs(p2))<2) and r<0.036
        out.append(dict(lattice=L,d=d,three_alpha=d/2,N=N,ns=round(ns,5),r=float('%.4g'%r),pull_SPA=round(p1,2),pull_SPA_DESI=round(p2,2),alive=bool(alive)))
ns,r=obs(1/3,55); chk=abs(r-12*(1/3)/55**2)/(12*(1/3)/55**2)
print('check 3a=1 N=55: ns',round(ns,5),'vs',round(1-2/55,5),' r rel diff',round(chk,4))
for o in out: print(o)
json.dump(dict(check_r_rel=chk,configs=out),open('field_tests/results/D1352_lattice_configs.json','w'),indent=1)
