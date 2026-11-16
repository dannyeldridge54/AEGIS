import sys, math, numpy as np, mpmath as mp
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.modular import j as jfun
from tools.serapis_calc.ms import Background, spectra
from tools.serapis_calc.landscape import hessian_canonical
s2=math.sqrt(2); yr=math.sqrt(3)/2
def eta_abs(x,y,nmax=80):
    q=mp.e**(2j*mp.pi*mp.mpc(x,y)); e=mp.e**(2j*mp.pi*mp.mpc(x,y)/24)
    for n in range(1,nmax+1): e*=(1-q**n)
    return float(abs(e))
def L(x,y): return -(math.log(2*y)+4*math.log(eta_abs(x,y)))
def Irho(y): a=float(abs(jfun(complex(0.5,y)))); return math.log1p((a/1728)**2)/(4*math.pi) if a<1e150 else 2*(math.log(a)-math.log(1728))/(4*math.pi)
Lr=L(0.5,yr)
ev=hessian_canonical(lambda x,y:L(x,y),0.5,yr)
lines=[f'L(rho) = {Lr:.9f} (old constant 0.340372354, diff {Lr-0.340372354:+.2e}); L Hessian at rho {ev} ratio {ev[0]/ev[1]:.6f}']
ph=np.linspace(math.log(yr)/s2+1e-5,math.log(60)/s2,3000); ys=np.exp(s2*ph)
SI=CubicSpline(ph,[Irho(y) for y in ys]); SL=CubicSpline(ph,[L(0.5,y)-Lr for y in ys]); dI=SI.derivative(); dL=SL.derivative()
eps=6e-5
V=lambda p:(lambda a:a*a/(a*a+1))(float(SI(p)))+eps*float(SL(p))
dV=lambda p:(lambda a,da:2*a*da/(a*a+1)**2)(float(SI(p)),float(dI(p)))+eps*float(dL(p))
bg=Background(V,dV,math.log(40)/s2)
ref={46.09:(0.9691,5.160e-4,-9.87e-4),49.49:(0.9722,4.672e-4,-8.69e-4)}
ok=True
for Ns,(n0,r0,a0) in ref.items():
    r=spectra(bg,Ns)
    good=abs(r['ns']-n0)<=5e-4 and abs(r['r']/r0-1)<=0.02 and abs(r['alpha_s']/a0-1)<=0.10; ok&=good
    lines.append(f"N*={Ns}: ns={r['ns']:.5f} (ref {n0}) r={r['r']:.4e} (ref {r0}) alpha_s={r['alpha_s']:.3e} (ref {a0}) {'ok' if good else 'OFF'}")
lines.append('PASS' if ok else 'FAIL')
open('field_tests/results/repro_rho_d957.txt','w').write('\n'.join(lines)+'\n'); print('\n'.join(lines))
