"""D592 (locked PREREG_D592_ADIABATIC_Y). AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
def Ljm(y): q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q+21493760*q**3); return lj+math.log(max(abs(1-1728*math.exp(-lj)),1e-300))
def Iy(y): l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y): l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
s2=math.sqrt(2); E=1e-4
def v(phi):
    y=math.exp(s2*abs(phi))
    if y<1+1e-9: return 0.0
    x=Iy(y)**2; return x/(x+1)+E*I1y(y)
def dv(phi,h=1e-6):
    if abs(phi)<2e-6: h=abs(phi)/2+1e-12
    return (v(phi+h)-v(phi-h))/(2*h)
# 1) find end of inflation & start point (3 e-folds before) with exact background from y=40
def rhsB(t,s):
    p,pd,N=s; H=math.sqrt((0.5*pd*pd+v(p))/3); return [pd,-3*H*pd-dv(p),H]
p0=math.log(40)/s2; H0=math.sqrt(v(p0)/3); s0=[p0,-dv(p0)/(3*H0),0]
def endev(t,s): p,pd,N=s; H2=(0.5*pd*pd+v(p))/3; return 0.5*pd*pd/H2-1
endev.terminal=True; endev.direction=1
bg=solve_ivp(rhsB,[0,1e9],s0,events=endev,rtol=1e-10,atol=1e-13,dense_output=True)
te=bg.t_events[0][0]; Ne=bg.y_events[0][0][2]; He=math.sqrt((0.5*bg.y_events[0][0][1]**2+v(bg.y_events[0][0][0]))/3)
from scipy.optimize import brentq
ts=brentq(lambda t:bg.sol(t)[2]-(Ne-3),0,te); st=bg.sol(ts)
print(f"end of inflation: N={Ne:.2f}, H_end={He:.3e}; start at N_end-3")
for R in (10,30,100):
    m=R*He
    def rhs(t,s):
        p,pd,N,Y,Yd=s; vv=v(p); H=math.sqrt((0.5*pd*pd+vv)/3); d=vv/m**2
        return [pd,-3*H*pd-dv(p),H,Yd,-3*H*Yd-m*m*(Y-d)]
    p,pd,N=st; d0=v(p)/m**2; dd0=dv(p)*pd/m**2
    def fin(t,s): return s[2]-(Ne+1.5)
    fin.terminal=True
    sol=solve_ivp(rhs,[ts,1e12],[p,pd,N,d0,dd0],events=fin,rtol=1e-10,atol=1e-22,method='DOP853',max_step=0.05/m)
    p,pd,N,Y,Yd=sol.y[:,-1]; vv=v(p); d=vv/m**2; ddot=dv(p)*pd/m**2
    rho=0.5*pd*pd+vv; EY=0.5*(Yd-ddot)**2+0.5*m*m*(Y-d)**2
    print(f"m/H_end={R}: f_Y={EY/rho:.3e}  f_track={0.5*m*m*d*d/rho:.3e}  (N_final={N:.2f}, steps={sol.t.size})",flush=True)
