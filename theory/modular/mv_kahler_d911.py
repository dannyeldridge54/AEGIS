# D911: sign of the Kahler metric for K = -log E(tau,2) and K = +log E(tau,2) (non-holomorphic Eisenstein), arithmetic check.
import numpy as np
def E(t,s=2.0,N=60):
    x,y=t.real,t.imag; m,n=np.meshgrid(np.arange(-N,N+1),np.arange(-N,N+1))
    d=np.abs(m*t+n)**(2*s); d[N,N]=np.inf
    return np.sum(y**s/d)
def metric(t,sign,h=1e-4):
    # K_{tau taubar} = (1/4)(d_xx+d_yy)K
    K=lambda z: sign*np.log(E(z))
    lap=(K(t+h)+K(t-h)+K(t+1j*h)+K(t-1j*h)-4*K(t))/h**2
    return lap/4
rho=np.exp(2j*np.pi/3)+1  # rho = -1/2 + i sqrt3/2 shifted by 1 (same point mod T)
for name,t in [("rho",rho),("i",1j),("y=2",0.5+2j),("y=4",0.5+4j),("y=8",0.5+8j)]:
    y=t.imag
    print(f"{name:5s} 4y^2*g for K=-logE: {4*y*y*metric(t,-1):+.4f}   for K=+logE: {4*y*y*metric(t,+1):+.4f}")
print("expected cusp, K=-logE: 4y^2 g -> +s = +2 ; at a critical point of E: -s(s-1) = -2")
