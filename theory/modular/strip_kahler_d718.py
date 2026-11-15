"""D718 (locked PREREG_D718): Epstein E(tau,s), 0<s<1, as a Kahler potential. AI-assisted."""
import math, numpy as np
from scipy.special import kv, zeta, gamma
def Es(x,y,s,N=40):
    t=2*zeta(2*s)*y**s+2*math.sqrt(math.pi)*gamma(s-0.5)*zeta(2*s-1)/gamma(s)*y**(1-s)
    for n in range(1,N+1):
        sig=sum(d**(1-2*s) for d in range(1,n+1) if n%d==0)
        t+=4*math.pi**s/gamma(s)*math.sqrt(y)*n**(s-0.5)*sig*kv(s-0.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return t
def lattice(x,y,s,M=120):
    tot=0.0
    for m in range(-M,M+1):
        for n in range(-M,M+1):
            if m or n: tot+=1/((m+n*x)**2+(n*y)**2)**s
    return y**s*tot
print("check vs lattice:", [(s, round(Es(0.5,1.3,s),6), round(lattice(0.5,1.3,s),6)) for s in (2.0,1.5)])
rho=(0.5,math.sqrt(3)/2)
for s in (0.6,0.75,0.9):
    ys=np.concatenate([np.linspace(math.sqrt(3)/2,3,300),np.linspace(3.01,60,500)])
    E=np.array([Es(0.5,y,s) for y in ys]); Ei=Es(0.0,1.0,s)
    h=1e-4
    def g(x,y):
        K=lambda a,b: -math.log(abs(Es(a,b,s)))
        return 0.25*((K(x+h,y)-2*K(x,y)+K(x-h,y))+(K(x,y+h)-2*K(x,y)+K(x,y-h)))/h**2
    print(f"s={s}: E(rho)={E[0]:+.5f} E(i)={Ei:+.5f} min on line {E.min():+.5f} at y={ys[E.argmin()]:.3f}; max {E.max():.3e}; "
          f"positive everywhere: {bool((E>0).all())}; sign changes at y~{[round(float(ys[k]),3) for k in np.where(np.diff(np.sign(E)))[0]]}; "
          f"metric(-lnE) at rho {g(*rho):+.4f} (pred -s(s-1)/(4y^2)={-s*(s-1)/(4*0.75):+.4f})")
