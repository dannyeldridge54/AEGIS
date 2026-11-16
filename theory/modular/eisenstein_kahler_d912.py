"""D912 (locked PREREG_D912): plateau from K = -k ln(2y) - c ln E(tau,2). MS solver = running_d632.py lines 12-41 verbatim. AI-assisted."""
import math, numpy as np
from scipy.special import kv, zeta
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
src=open(__file__.replace('eisenstein_kahler_d912','running_d632')).read().split('\n')
s2=math.sqrt(2)
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,31)]
def Ese(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    for n in range(1,31): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
def lneta4(x,y):
    q=complex(math.exp(-2*math.pi*y)*math.cos(2*math.pi*x),math.exp(-2*math.pi*y)*math.sin(2*math.pi*x))
    return -math.pi*y/3+4*sum(math.log(abs(1-q**n)) for n in range(1,31))
yr=math.sqrt(3)/2
def G(x,y,k,c): return -k*(math.log(2*y)+lneta4(x,y))-c*math.log(Ese(x,y))
def derivs(x,y,k,c,h=1e-4):
    g0=G(x,y,k,c); gx=(G(x+h,y,k,c)-G(x-h,y,k,c))/(2*h); gy=(G(x,y+h,k,c)-G(x,y-h,k,c))/(2*h)
    gxx=(G(x+h,y,k,c)-2*g0+G(x-h,y,k,c))/h**2; gyy=(G(x,y+h,k,c)-2*g0+G(x,y-h,k,c))/h**2
    return g0,gx,gy,gxx,gyy
def VF(y,k,c):
    g0,gx,gy,gxx,gyy=derivs(0.5,y,k,c); return math.exp(g0)*((gx*gx+gy*gy)/(gxx+gyy)-3)
res=[]
for w in (2.0,2.5,2.9,3.5):
    k,c=0.75*w,0.125*w
    # (1) positivity
    mn=1e9
    for x in np.linspace(-0.5,0.5,21):
        for y in np.linspace(math.sqrt(max(1-x*x,0))+0.02,6,25):
            d=derivs(x,y,k,c); mn=min(mn,(d[3]+d[4])*4*y*y)
    for y in np.linspace(1,40,60):
        d=derivs(0.5,y,k,c); mn=min(mn,(d[3]+d[4])*4*y*y)
    V0=-VF(yr+1e-6,k,c)
    Vy=lambda y:VF(y,k,c)+V0
    # (2) vacuum: V near rho
    vn=[Vy(yr+d) for d in (0.01,0.03,0.1)]
    # (3) plateau side
    side=Vy(40)-V0
    line=f"w={w} k={k:.3f} c={c:.3f}: min 4y^2*g={mn:.4f}; V(rho+0.01,0.03,0.1)/V0={[f'{v/V0:.3e}' for v in vn]}; V(40)-V0={side/V0:+.3e} V0"
    print(line,flush=True)
    ok=mn>0 and all(v>0 for v in vn) and side<0
    if not ok: print(f"  -> fails checks (positivity {mn>0}, vacuum {all(v>0 for v in vn)}, plateau-from-below {side<0}); no spectra",flush=True); continue
    # canonical phi(y) along x=1/2 from rho
    ys=np.concatenate([np.linspace(yr+1e-3,3,300),np.geomspace(3.01,60,600)])
    gs=np.array([ (lambda d:(d[3]+d[4])/4)(derivs(0.5,y,k,c)) for y in ys])
    dphi=np.sqrt(2*gs); ph=np.concatenate([[0],np.cumsum(0.5*(dphi[1:]+dphi[:-1])*np.diff(ys))])
    y_of=CubicSpline(ph,ys); Vs=np.array([Vy(y) for y in ys]); Vphi=CubicSpline(ph,Vs)
    phi_of_y=CubicSpline(ys,ph)
    for C in (0.0,1e-6):
        Er=Ese(0.5,yr)
        def V(phi,e,C=C): y=float(y_of(phi)); return float(Vphi(phi))*(1+C*(Ese(0.5,y)-Er))
        def dlnV(phi,e,h=1e-5): return (math.log(V(phi+h,e))-math.log(V(phi-h,e)))/(2*h)
        code='\n'.join(src[11:41]).replace('phi0=math.log(40)/s2','phi0=float(phi_of_y(25.0))')
        code=code.replace('def V(phi,e):','def _unusedV(phi,e):').replace('def dlnV(phi,e,h=1e-5):','def _unused(phi,e,h=1e-5):')
        g={}; g.update(globals()); g['V']=V; g['dlnV']=dlnV; g['phi_of_y']=phi_of_y
        exec(code,g)
        B=g['background'](None)
        for Ns in (48.4,49.9):
            S=[-0.05,0,0.05]; out=[g['spectra'](B,Ns,math.exp(x)) for x in S]
            lp=[math.log(o[0]) for o in out]; ns=1+(lp[2]-lp[0])/0.1; r=out[1][1]/out[1][0]
            yst=float(y_of(B['phiS'](B['Ne']-Ns)))
            print(f"  C={C:.0e} N*={Ns}: n_s={ns:.4f} r={r:.3e} y*={yst:.2f}",flush=True)
            res.append((w,C,Ns,ns,r))
band=[x for x in res if 0.970<=x[3]<=0.975 and 4.55e-4<=x[4]<=5.12e-4]
print("VERDICT:", "REPRODUCES" if band else "FAILS for the frozen band", band if band else "")
