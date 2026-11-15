"""D595 (locked PREREG_D595_STIFF_GROWTH): D592 background code. AI-assisted."""
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

import numpy as np
p,pd,N=st
sol=solve_ivp(rhsB,[ts,1e14],[p,pd,N],rtol=1e-10,atol=1e-13,dense_output=True,events=lambda t,s:s[2]-(Ne+3),max_step=1.0)
T=sol.t; P,PD,NN=sol.y; rho=0.5*PD**2+np.array([v(x) for x in P])
# smooth over oscillations: average ln rho in bins of N
def wfit(a,b):
    msk=(NN>=Ne+a)&(NN<=Ne+b); c=np.polyfit(NN[msk],np.log(rho[msk]),1)[0]; return -c/3-1
w1=wfit(0.5,1.5); w2=wfit(1.5,3.0)
print(f"effective w: [0.5,1.5] = {w1:.3f}; [1.5,3] = {w2:.3f}  (octic expectation 0.6, matter 0)")
i15=np.argmin(abs(NN-(Ne+1.5))); ie=np.argmin(abs(NN-Ne))
r15=rho[i15]/rho[ie]; target=2.4e-6
dN=np.log(r15/target)/(3*(1+w2)); G=np.exp(3*w2*dN)
print(f"rho(N_end+1.5)/rho_end = {r15:.2e}; e-folds to crossover = {dN:.2f}; growth G = {G:.1f}; requirement f_Y(1.5) <= {4e-11/G:.2e}")
Rs=np.array([10,30,100,200,320]); fs=np.array([6.019e-2,3.319e-5,2.227e-9,2.419e-15,3.185e-17]); req=4e-11/G
lr=np.interp(np.log(req),np.log(fs[::-1]),np.log(Rs[::-1])); print(f"R needed = {np.exp(lr):.0f}")
