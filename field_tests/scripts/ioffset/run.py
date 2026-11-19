import sys, math, cmath, json, os; sys.path.insert(0,'.')
import numpy as np
from scipy.optimize import minimize
from tools.serapis_calc.shapes import E, log_eta
Ef=lambda x,y:float(E(complex(x,y),1.5).real)
def V0(x,y,h=1e-6):
    L=lambda a,b:math.log(Ef(a,b)); dx=(L(x+h,y)-L(x-h,y))/(2*h); dy=(L(x,y+h)-L(x,y-h))/(2*h); return (4/9)*y*y*(dx*dx+dy*dy)
def Fraw(x,y): t=complex(x,y); return math.sqrt(y)*math.exp(2*log_eta(t).real)
F0=Fraw(0,1); F=lambda x,y:Fraw(x,y)/F0
def hess(f,x,y,h=1e-4):
    fxx=(f(x+h,y)-2*f(x,y)+f(x-h,y))/h**2; fyy=(f(x,y+h)-2*f(x,y)+f(x,y-h))/h**2
    fxy=(f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4*h*h); return np.array([[fxx,fxy],[fxy,fyy]])
H0=hess(V0,0,1); HF=hess(F,0,1)
g=lambda f:((f(1e-4,1)-f(-1e-4,1))/2e-4,(f(0,1+1e-4)-f(0,1-1e-4))/2e-4)
out={'grad_V0_at_i':g(V0),'grad_F_at_i':g(F),'H_V0':H0.tolist(),'H_F':HF.tolist()}
# kappa_c: smallest eig of H0 - k HF crosses 0
ks=np.linspace(0,1e3,200001)
def mineig(k): return np.linalg.eigvalsh(H0-k*HF).min()
kc=None
if np.linalg.eigvalsh(HF).max()>0:
    lo,hi=0.0,1.0
    while mineig(hi)>0 and hi<1e9: hi*=2
    if mineig(hi)<=0:
        for _ in range(80):
            m=(lo+hi)/2
            if mineig(m)>0: lo=m
            else: hi=m
        kc=(lo+hi)/2
out['kappa_c']=kc; out['runs']={}
if kc:
    for r in (1.01,1.1,1.5,2,4):
        k=r*kc; f=lambda p:V0(p[0],p[1])-k*F(p[0],p[1])
        res=minimize(f,[0.01,1.01],method='Nelder-Mead',options=dict(xatol=1e-9,fatol=1e-14,maxiter=4000))
        x,y=res.x; t=complex(x,y); u=abs((t-1j)/(t+1j))
        out['runs'][str(r)]=dict(x=float(x),y=float(y),abs_u=float(u),on_CP_line=bool(abs(x)<1e-5 or abs(abs(t)-1)<1e-5),V=float(res.fun))
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/IOFFSET',exist_ok=True); json.dump(out,open('field_tests/results/IOFFSET/out.json','w'),indent=1)
