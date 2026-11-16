"""Klein j via Eisenstein E4, E6 q-series (general tau). Checks: j(i)=1728, j(2i)=66^3, j(rho)=0."""
import mpmath as mp
def _sig(n, k): return sum(d**k for d in range(1, n+1) if n % d == 0)
def j(tau, nmax=60):
    q = mp.e**(2j*mp.pi*mp.mpc(tau))
    E4 = 1 + 240*sum(_sig(n, 3)*q**n for n in range(1, nmax+1))
    D = q
    for n in range(1, nmax+1): D *= (1 - q**n)**24      # Delta = q prod (1-q^n)^24 (stable at the cusp)
    return E4**3/D
def I_inv(tau, power=2):
    """SERAPIS invariants: power 2 -> I = ln(1+|j-1728|^2/1728^2)/4pi ; power 1 -> I_1 = ln(1+|j-1728|/1728)/4pi."""
    a = abs(j(tau) - 1728)
    return float(mp.log(1 + (a/1728)**power)/(4*mp.pi))
