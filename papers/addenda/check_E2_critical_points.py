import numpy as np
from scipy.special import kv, gamma, zeta
from scipy.optimize import minimize
s=2.0
def sig(n,a): return sum(d**a for d in range(1,n+1) if n%d==0)
NN=40; sg=np.array([sig(n,1-2*s) for n in range(1,NN+1)]); ns=np.arange(1,NN+1)
def E(x,y):
    t=2*zeta(2*s)*y**s+2*np.sqrt(np.pi)*gamma(s-.5)/gamma(s)*zeta(2*s-1)*y**(1-s)
    t+=8*np.pi**s/gamma(s)*np.sqrt(y)*np.sum(ns**(s-.5)*sg*kv(s-.5,2*np.pi*ns*y)*np.cos(2*np.pi*ns*x))
    return t
print("E(rho)",E(.5,np.sqrt(3)/2),"E(i)",E(0,1))
h=1e-5
def g2(p):
    x,y=p; gx=(E(x+h,y)-E(x-h,y))/(2*h); gy=(E(x,y+h)-E(x,y-h))/(2*h); return gx*gx+gy*gy
found=set()
for x0 in np.linspace(0.01,0.49,13):
    for y0 in np.linspace(0.88,3.0,15):
        if x0*x0+y0*y0<1: continue
        r=minimize(g2,[x0,y0],method='Nelder-Mead',options={'xatol':1e-9,'fatol':1e-20,'maxiter':4000})
        x,y=r.x
        if r.fun<1e-10 and -0.01<=x<=0.51 and x*x+y*y>=0.98: found.add((round(abs(x),4),round(y,4)))
print(found)
