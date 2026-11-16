import sys, math, numpy as np
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.modular import I_inv
from tools.serapis_calc.ms import Background, spectra
s2=math.sqrt(2); L=[]
ph=np.linspace(np.log(RHO_Y)/s2+1e-4,np.log(3000)/s2,4000)
Eg=np.maximum(2*1.0823232337111382*np.array([Ehat(np.exp(s2*p)) for p in ph]),1e-14)
S=CubicSpline(ph,Eg); dS=S.derivative(); C=1.0e-6
V=lambda p:(lambda e:e/(e+1)*(1+C*e))(float(S(p))); dV=lambda p:(lambda e,de:de*((1+C*e)/(e+1)**2+C*e/(e+1)))(float(S(p)),float(dS(p)))
bgE=Background(V,dV,ph[np.searchsorted(Eg,600)])
ph2=np.linspace(1e-4,math.log(60)/s2,3000); ys=np.exp(s2*ph2)
S2=CubicSpline(ph2,[I_inv(1j*y,2) for y in ys]); S1=CubicSpline(ph2,[I_inv(1j*y,1) for y in ys]); d2=S2.derivative(); d1=S1.derivative(); eps=1.3e-4
V2=lambda p:(lambda a:a*a/(a*a+1))(float(S2(p)))+eps*float(S1(p)); dV2=lambda p:(lambda a,da:2*a*da/(a*a+1)**2)(float(S2(p)),float(d2(p)))+eps*float(d1(p))
bgC=Background(V2,dV2,math.log(45)/s2)
for name,bg,Ns,band in (('SERAPIS-E C=1e-6',bgE,48.4,(-10.6e-4,-9.4e-4)),('Chronos eps=1.3e-4',bgC,46.0,(-10.2e-4,-8.8e-4))):
    a={}
    for bd in (200.0,1000.0,5000.0):
        r=spectra(bg,Ns,bd=bd,ic='ds'); a[bd]=r['alpha_s']; L.append(f"{name} N*={Ns} bd={bd:.0f}: ns={r['ns']:.6f} r={r['r']:.4e} alpha_s={r['alpha_s']:.4e}")
    conv=abs(a[5000.0]/a[1000.0]-1)<=0.02 and abs(a[1000.0]/a[200.0]-1)<=0.02
    inb=band[0]<=a[5000.0]<=band[1] or min(abs(a[5000.0]/band[0]-1),abs(a[5000.0]/band[1]-1))<=0.05
    L.append(f"{name}: converged={conv} alpha_s(5000)={a[5000.0]:.4e} published band {band} -> {'published alpha_s stands' if conv and inb else ('CORRECTION NOTE' if conv else 'NOT CONVERGED')}")
open('field_tests/results/alpha_ds_d975.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
