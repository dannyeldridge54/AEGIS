"""JET-1: classical beam-target D->T fusion power (slowing down on electrons and ions; Bosch-Hale sigma; target at rest)."""
import math, numpy as np
import neutron_birth as NB
MD_KEV = NB.MD * 1e3; C = 2.99792458e8; Q_DT_J = 17.5893 * 1.602176634e-13
def composition(f_T, ni_over_ne, Z_imp=4, A_imp=9):
    n_i = ni_over_ne; n_imp = (1 - n_i) / Z_imp; return dict(D=(1 - f_T) * n_i, T=f_T * n_i, imp=n_imp, Z_imp=Z_imp, A_imp=A_imp)
def slowing(Te_keV, n_e, comp, A_b=2.0):
    lnL = 24 - math.log(math.sqrt(n_e * 1e-6) / (Te_keV * 1e3))
    tau_s = 6.27e8 * A_b * (Te_keV * 1e3) ** 1.5 / (n_e * 1e-6 * lnL)
    s = comp['D'] / 2 + comp['T'] / 3 + comp['imp'] * comp['Z_imp'] ** 2 / comp['A_imp']
    Ec = 14.8 * A_b * Te_keV * s ** (2 / 3)
    return tau_s, Ec, lnL
def yield_per_ion(E_b, Te_keV, n_e, comp, n=4000):
    tau_s, Ec, _ = slowing(Te_keV, n_e, comp); nT = comp['T'] * n_e
    E = np.linspace(1.5 * Te_keV, E_b, n); Ecm = E * NB.MT / (NB.MD + NB.MT)
    with np.errstate(over='ignore'): sig = NB.sigma_bh(Ecm) * 1e-31          # mb -> m^2
    v = C * np.sqrt(2 * E / MD_KEV); dEdt = (2 * E / tau_s) * (1 + (Ec / E) ** 1.5)
    return float(np.trapezoid(nT * sig * v / dEdt, E))
def P_bt(P_MW, E_b, fracs, Te_keV, n_e, f_T, ni_over_ne):
    comp = composition(f_T, ni_over_ne); tot = 0.0
    for k, fk in enumerate(fracs, start=1):
        Ek = E_b / k; rate = P_MW * 1e6 * fk / (Ek * 1.602176634e-16); tot += rate * yield_per_ion(Ek, Te_keV, n_e, comp)
    return tot * Q_DT_J / 1e6
