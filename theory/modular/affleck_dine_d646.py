"""D646 (locked PREREG_D646_AFFLECK_DINE). AI-assisted."""
import math, mpmath as mp, numpy as np
from scipy.integrate import solve_ivp
mp.mp.dps=30
print("Part 1: d/dtau |yhat| at tau=i for Y=E4, matter weight 1 (K=-ln 2y)")
def E4(t): return 1+240*mp.nsum(lambda n: n**3*mp.exp(2j*mp.pi*n*t)/(1-mp.exp(2j*mp.pi*n*t)),[1,mp.inf])
for N,kY in ((2,4),(3,4),(4,4),(3,2),(5,4)):
    # |yhat| = e^{K/2}|Y| / prod K_i^{1/2} = (2y)^{-1/2} |Y| (2y)^{N/2}; weight balance: kY = N - 1 ... report residual
    f=lambda t: (2*mp.im(t))**((N-1)/mp.mpf(2))*abs(E4(t))**(mp.mpf(kY)/4)   # |E4|^{kY/4} has weight kY
    h=mp.mpf('1e-10')
    dx=(f(1j+h)-f(1j-h))/(2*h); dy=(f(1j+1j*h)-f(1j-1j*h))/(2*h)
    bal='balanced' if kY==N-1 else f'unbalanced (kY - (N-1) = {kY-(N-1)})'
    print(f"  N={N}, kY={kY}: d|yhat|/dx={mp.nstr(dx,3)}, d|yhat|/dy={mp.nstr(dy,3)}, |yhat|={mp.nstr(f(1j),5)}  [{bal}]")
print("Part 2: AD numerical yield (m=1 units; Q = Im(psi* psidot)/h^2)")
cH,aH,am=1.0,1.0,1.0
def run(theta):
    t0=2/(3*30.0); t1=2/(3*0.01)
    def rhs(t,s):
        p=s[0]+1j*s[1]; v=s[2]+1j*s[3]; H=2/(3*t)
        # V = (1 - cH H^2)|p|^2 + [(am e^{i theta} + aH H) p^4/4 + c.c.] + |p|^6 ; dV/dp* :
        dV=(1-cH*H**2)*p + np.conj((am*np.exp(1j*theta)+aH*H))*np.conj(p)**3 + 3*abs(p)**4*p
        acc=-3*H*v-dV
        return [v.real,v.imag,acc.real,acc.imag]
    # start at the Hubble-induced minimum along the aH direction
    H0=30.0; r0=(cH*H0**2/3)**0.25; p0=r0*np.exp(1j*math.pi/4)   # aH real -> minima at arg p = pi/4 + k pi/2 (term -|aH|H...)
    sol=solve_ivp(rhs,[t0,t1],[p0.real,p0.imag,0,0],rtol=1e-9,atol=1e-12,max_step=0.05,dense_output=False)
    t=sol.t; p=sol.y[0]+1j*sol.y[1]; v=sol.y[2]+1j*sol.y[3]; h=2/(3*t)
    Q=np.imag(np.conj(p)*v)/h**2
    return float(np.mean(Q[-200:]))
Qs=[]
for k in range(8):
    th=2*math.pi*k/8; Q=run(th); Qs.append(Q); print(f"  theta={th:.3f}: Q={Q:+.4f}",flush=True)
Qa=np.median(np.abs(Qs)); Qm=max(abs(q) for q in Qs)
MP=2.435e18; v=174.0; target=8.7e-11
print(f"  |Q| median={Qa:.3f}, max={Qm:.3f}")
for TR in (1e3,1e4,1e5):
    # n_B/s = (8/23) TR M Q/(4 MP^2), M = v^2/m_nu  -> m_nu = (8/23) TR v^2 Q /(4 MP^2 target)
    for Q,lab in ((Qa,'median'),(Qm,'max')):
        mnu_GeV=(8/23)*TR*v**2*Q/(4*MP**2*target)
        print(f"  T_R={TR:.0e} GeV ({lab} |Q|): m_nu1 needed = {mnu_GeV*1e9:.2e} eV")
