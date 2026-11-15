"""D717 (locked PREREG_D717): sugra rung, K = -(3a/2) ln E(tau,2), constant W0, uplift. AI-assisted."""
import math, numpy as np
from scipy.special import kv, zeta
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.integrate import quad
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,41)]
def E(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    for n in range(1,41): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
Er=E(0.5,math.sqrt(3)/2); print(f"E(rho,2)={Er:.7f} (D689: 5.7833593)")
def model(a):
    K=lambda x,y: -1.5*a*math.log(E(x,y)); h=1e-4
    def parts(y):
        x=0.5; k=K(x,y); ky=(K(x,y+h)-K(x,y-h))/(2*h)
        kxx=(K(x+h,y)-2*k+K(x-h,y))/h**2; kyy=(K(x,y+h)-2*k+K(x,y-h))/h**2
        g=0.25*(kxx+kyy)                       # K_{tau taubar}
        F=(ky*ky/4)/g                          # K^{tt} |K_t|^2  (K_x = 0 on Re tau = 1/2)
        return k,g,F
    ys=np.concatenate([np.linspace(math.sqrt(3)/2+1e-3,3,600),np.linspace(3.005,60,1500)])
    P=[parts(y) for y in ys]
    Vf=np.array([math.exp(k)*(F-3) for k,g,F in P])        # |W0|^2 = 1
    Vup=-Vf[0]*1.0                                           # tune V(rho)=0 (first grid point ~ rho)
    V=Vf+Vup
    gk=np.array([g for k,g,F in P])
    dphi=np.sqrt(np.clip(2*gk,0,None)); phi=np.concatenate([[0],np.cumsum(0.5*(dphi[1:]+dphi[:-1])*np.diff(ys))])
    return ys,phi,V/Vup,np.array([F for k,g,F in P]),gk
def Ehat(y): return E(0.5,y)-Er
def obs(ys,phi,v,C,N):
    vv=v*(1+C*np.array([Ehat(y) for y in ys]))
    S=CubicSpline(phi,vv); d1=S.derivative(1); d2=S.derivative(2); d3=S.derivative(3)
    eps=lambda f: 0.5*(d1(f)/S(f))**2
    grid=np.linspace(phi[5],phi[-5],4000); e=np.array([eps(f) for f in grid])
    idx=np.where((e[:-1]>=1)&(e[1:]<1))[0]
    if not len(idx): return None
    fe=brentq(lambda f: eps(f)-1, grid[idx[-1]], grid[idx[-1]+1])
    Nf=lambda f: quad(lambda w: S(w)/d1(w), fe, f, limit=200)[0]
    try: fs=brentq(lambda f: Nf(f)-N, fe+1e-3, phi[-6])
    except ValueError: return None
    V0=S(fs); ee=eps(fs); eta=d2(fs)/V0; xi=d1(fs)*d3(fs)/V0**2
    ystar=float(np.interp(fs,phi,ys))
    return ystar, 1-6*ee+2*eta, 16*ee, 16*ee*eta-24*ee*ee-2*xi
for a in (1/3,1/2,2/3,0.8,0.9):
    ys,phi,v,F,g=model(a)
    print(f"alpha={a:.3f}: p_pred=sqrt(6a)={math.sqrt(6*a):.3f}; V>=0 on line: {bool((v>-1e-9).all())}; argmin y={ys[int(np.argmin(v))]:.4f} (rho y=0.8660); "
          f"K^tt|K_t|^2 at y=60: {F[-1]:.3f} (asympt 3a={3*a:.2f}); V(60)={v[-1]:.5f}")
    for N in (48.4,49.9):
        row=[]
        for C in (0,1e-7,1e-6,1e-5,3e-5):
            o=obs(ys,phi,v,C,N)
            row.append((C,o))
            if o: print(f"   N*={N} C={C:.0e}: y*={o[0]:.2f} n_s={o[1]:.4f} r={o[2]:.3e} alpha_s={o[3]:.3e}")
            else: print(f"   N*={N} C={C:.0e}: no slow-roll solution on the grid")
        ok=[(C,o) for C,o in row if o]
        for (C1,o1),(C2,o2) in zip(ok,ok[1:]):
            if (o1[1]-0.970)*(o2[1]-0.970)<=0 and C1>0 or ((o1[1]-0.970)*(o2[1]-0.970)<=0 and C1==0):
                t=(0.970-o1[1])/(o2[1]-o1[1]); print(f"   -> n_s=0.970 between C={C1:.0e} and {C2:.0e}: r~{o1[2]+t*(o2[2]-o1[2]):.3e} y*~{o1[0]+t*(o2[0]-o1[0]):.1f} alpha_s~{o1[3]+t*(o2[3]-o1[3]):.2e}")
