"""Fully modular Twist toolkit (Danny 21:32 CT 'set this up'). AI-assisted.
tau in the upper half plane; Twist T = -i*tau (Re T = Im tau = x). K = -3 ln(-i(tau - conj tau)).
With W = S*F(tau) and a nilpotent stabiliser S: V = e^K |F|^2. Invariance under SL(2,Z) needs F of modular weight -3:
F(tau) = eta(tau)^(-6) * H(j(tau)), H holomorphic in j. Then V = |H(j)|^2 / ((2 Im tau)^3 |eta|^12), exactly SL(2,Z) invariant.
Fixed points: tau = i (square torus, j = 1728) and tau = rho = e^{i pi/3} (hexagonal, j = 0) are automatically extrema."""
import cmath, math
def _q(tau): return cmath.exp(2j*math.pi*tau)
def eta(tau, N=60):
    q=_q(tau); p=1+0j
    for n in range(1,N): p*=1-q**n
    return cmath.exp(2j*math.pi*tau/24)*p
def E4(tau, N=60):
    q=_q(tau); s=0j
    for n in range(1,N): s+=sum(d**3 for d in range(1,n+1) if n%d==0)*q**n
    return 1+240*s
def j(tau): return E4(tau)**3/eta(tau)**24
def lnV(tau, H):
    """ln V for F = eta^-6 H(j)."""
    return 2*math.log(abs(H(j(tau)))) - 3*math.log(2*tau.imag) - 12*math.log(abs(eta(tau)))
def to_fundamental(tau):
    """map tau to the standard fundamental domain."""
    for _ in range(200):
        tau=complex(tau.real-round(tau.real), tau.imag)
        if abs(tau)<1-1e-14: tau=-1/tau
        else: break
    return tau
