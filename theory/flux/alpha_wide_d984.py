import sys, math, numpy as np, mpmath as mp
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.modular import j as jfun
from tools.serapis_calc.ms import Background, spectra
from tools.serapis_calc.modular import I_inv
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
_lines=[f'L(rho) = {Lr:.9f} (old constant 0.340372354, diff {Lr-0.340372354:+.2e}); L Hessian at rho {ev} ratio {ev[0]/ev[1]:.6f}']
ph=np.linspace(math.log(yr)/s2+1e-5,math.log(60)/s2,3000); ys=np.exp(s2*ph)
SI=CubicSpline(ph,[Irho(y) for y in ys]); SL=CubicSpline(ph,[L(0.5,y)-Lr for y in ys]); dI=SI.derivative(); dL=SL.derivative()
eps=6e-5
V=lambda p:(lambda a:a*a/(a*a+1))(float(SI(p)))+eps*float(SL(p))
dV=lambda p:(lambda a,da:2*a*da/(a*a+1)**2)(float(SI(p)),float(dI(p)))+eps*float(dL(p))
bg=Background(V,dV,math.log(40)/s2)
bgR=bg
ph2=np.linspace(1e-4,math.log(60)/s2,3000); ys=np.exp(s2*ph2)
S2=CubicSpline(ph2,[I_inv(1j*y,2) for y in ys]); S1=CubicSpline(ph2,[I_inv(1j*y,1) for y in ys]); d2=S2.derivative(); d1=S1.derivative(); epsK=0.0
V2=lambda p:(lambda a:a*a/(a*a+1))(float(S2(p)))+epsK*float(S1(p)); dV2=lambda p:(lambda a,da:2*a*da/(a*a+1)**2)(float(S2(p)),float(d2(p)))+epsK*float(d1(p))
bgK=Background(V2,dV2,math.log(45)/s2)
W=tuple(np.round(np.linspace(-0.8,0.8,9),10)); M=tuple(np.round(np.linspace(-0.4,0.4,9),10)); L=[]
for name,b,Ns_list,band in (('SERAPIS-rho eps=6e-5',bgR,(46.09,49.49),(-9.5e-4,-8.5e-4)),('Kairos eps=0',bgK,(46.08,49.21),None)):
    for Ns in Ns_list:
        a={}
        for bd in (200.0,1000.0,5000.0):
            r=spectra(b,Ns,dlnk=W,bd=bd,ic='ds'); a[bd]=r['alpha_s']; L.append(f"{name} N*={Ns} grid W bd={bd:.0f}: ns={r['ns']:.6f} r={r['r']:.4e} alpha_s={r['alpha_s']:.4e}"); print(L[-1],flush=True)
        rm=spectra(b,Ns,dlnk=M,bd=1000.0,ic='ds'); L.append(f"{name} N*={Ns} grid M bd=1000: alpha_s={rm['alpha_s']:.4e}"); print(L[-1],flush=True)
        conv=abs(a[5000.0]/a[1000.0]-1)<=0.02 and abs(a[1000.0]/a[200.0]-1)<=0.02; bias=abs(a[1000.0]/rm['alpha_s']-1)<=0.03
        if band:
            inb=band[0]<=a[5000.0]<=band[1] or min(abs(a[5000.0]/band[0]-1),abs(a[5000.0]/band[1]-1))<=0.05
            v='NOT CONVERGED' if not conv else ('BIASED' if not bias else ('published rho alpha_s stands' if inb else 'CORRECTION NOTE'))
        else:
            v=f"reference: alpha_s/(-2/N*^2) = {a[5000.0]/(-2/Ns**2):.3f}" + ('' if conv and bias else ' (NOT CONVERGED/BIASED)')
        L.append(f"{name} N*={Ns}: converged={conv} bias_ok={bias} alpha_W(5000)={a[5000.0]:.4e} -> {v}")
open('field_tests/results/alpha_wide_d984.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
