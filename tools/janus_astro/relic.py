# AEGIS-FP RVY3FZHDIAAQCPT4 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Hyperion relic-density module (R1): wino triplet freeze-out with coannihilation (Born; Sommerfeld hooks later).
Annihilation matrices: Hisano et al. hep-ph/0610249 Eqs. 2-8. Boltzmann: standard Kolb-Turner form (constants labelled in PREREG_R1)."""
import math
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MPL = 1.2209e19; S0 = 2891.2; RHOC_H2 = 1.0537e-5
def sigma_eff_born(m, a2):
    """Spin-averaged, g-weighted effective <sigma v> (GeV^-2) for the degenerate wino triplet, tree level."""
    u = math.pi*a2**2/m**2
    s00 = 0.25*2*(1.0)            # chi0chi0: S=0 only, c=2, Gamma_00 = (u/2)*2 = u  -> 2u * 1/4
    spm = 0.25*1*(1.5) + 0.75*1*(25/24)   # chi-chi+ : S=0 Gamma=3u/2 (c=1), S=1 25u/24
    s0c = 0.25*1*(0.5) + 0.75*1*(25/24)   # chi0chi-: S=0 u/2, S=1 25u/24
    scc = 0.25*2*(0.5)            # chi-chi-: S=0 only, c=2, Gamma=u/2
    g = 2.0
    tot = g*g*(s00 + 2*spm + 4*s0c + 2*scc)
    tot = 4*tot   # DEVIATIONS_R1b D1: Gamma entries are spin-summed pair rates; 4x reproduces 37/12 (Arkani-Hamed+ hep-ph/0601041 Eq. 6)
    return tot/36.0*u, tot/36.0
def omega_h2(m, sv, gstar=106.75, geff=6.0):
    lam = math.sqrt(math.pi/45)*MPL*math.sqrt(gstar)*m*sv
    yeq = lambda x: 45/(4*math.pi**4)*geff/gstar*x**1.5*math.exp(-x)*math.sqrt(math.pi/2)
    def rhs(x, y): return [-lam/x**2*(y[0]**2 - yeq(x)**2)]
    x0 = 3.0; s = solve_ivp(rhs, [x0, 1000.0], [yeq(x0)], method='Radau', rtol=1e-8, atol=1e-20)
    Y = float(s.y[0, -1])
    return m*Y*S0/RHOC_H2, Y
def thermal_mass(a2, target=0.1205, gstar=106.75):
    f = lambda m: omega_h2(m, sigma_eff_born(m, a2)[0], gstar)[0] - target
    return brentq(f, 300.0, 10000.0, xtol=0.1)
