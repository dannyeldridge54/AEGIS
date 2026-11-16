import sys, math, cmath, numpy as np
sys.path.insert(0,'theory/modular')
from inflaton_ad_d790 import V, RHO
x0,y0=RHO.real,RHO.imag
for h in (1e-3,1e-4):
    v0=V(x0,y0); Vxx=(V(x0+h,y0)-2*v0+V(x0-h,y0))/h**2; Vyy=(V(x0,y0+h)-2*v0+V(x0,y0-h))/h**2
    print(f"h={h:.0e}: Vxx={Vxx:.6e} Vyy={Vyy:.6e} R={Vxx/Vyy:.8f}")
for r in (0.01,0.03,0.1):
    th=2*np.pi*np.arange(96)/96
    vals=np.array([V(*(lambda t:(t.real,t.imag))((RHO-RHO.conjugate()*z)/(1-z))) for z in r*np.exp(1j*th)])
    F=np.fft.rfft(vals)/96; c=[abs(F[k])/abs(F[0]) for k in range(1,7)]
    print(f"r={r}: "+" ".join(f"c{k+1}={c[k]:.2e}" for k in range(6)))
