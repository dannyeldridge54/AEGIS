# AEGIS-FP 42YVSP4PENVP6SCK · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Paper 1 consistency relation (D669): alpha_s and beta_s from (n_s, r) given (p, kappa)."""
import math
def x_ramp(ns, r, p, kappa):
    rho = p*math.sqrt(r/2)/(1-ns)
    return (rho-1)/(1+kappa*rho)
def alpha_s(ns, r, p, kappa):
    x = x_ramp(ns, r, p, kappa); k = kappa
    return -(1-ns)**2*(1+x)*(1+k*k*x)/(2*(1-k*x)**2)
def beta_s(ns, r, p, kappa):
    x = x_ramp(ns, r, p, kappa); k = kappa
    return -(1-ns)**3*(1+x)*((1-k*x)*(1+k*k*x)+(1+x)*(1-k**3*x))/(4*(1-k*x)**3)
def exponent(n, k):
    """Plateau exponent p = k sqrt(2/n) for K = -n log y, V0 - V ~ y^-k (D929); alpha = 2/(3p^2)."""
    p = k*math.sqrt(2/n); return p, 2/(3*p*p)
