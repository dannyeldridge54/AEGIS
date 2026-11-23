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
def sigv_thermal(E, Ti_keV, m=400, seed=11):
    """JET-1 DEV-1: <sigma v_rel> of a D beam ion of energy E (keV) on Maxwellian T targets at Ti (m^3/s)."""
    rng = np.random.default_rng(seed); vt = rng.normal(0, C * np.sqrt(Ti_keV / (NB.MT * 1e3)), (m, 3))
    out = np.empty_like(E)
    for i, e in enumerate(E):
        vb = np.array([C * np.sqrt(2 * e / MD_KEV), 0, 0]); vr = np.linalg.norm(vb - vt, axis=1)
        Ecm = 0.5 * (NB.MD * NB.MT / (NB.MD + NB.MT)) * 1e3 * (vr / C) ** 2
        with np.errstate(over='ignore'): out[i] = np.mean(NB.sigma_bh(np.maximum(Ecm, 1e-3)) * 1e-31 * vr)
    return out
def yield_per_ion(E_b, Te_keV, n_e, comp, n=4000, Ti_keV=None):
    tau_s, Ec, _ = slowing(Te_keV, n_e, comp); nT = comp['T'] * n_e
    E = np.linspace(1.5 * Te_keV, E_b, n); Ecm = E * NB.MT / (NB.MD + NB.MT)
    with np.errstate(over='ignore'): sig = NB.sigma_bh(Ecm) * 1e-31          # mb -> m^2
    v = C * np.sqrt(2 * E / MD_KEV); dEdt = (2 * E / tau_s) * (1 + (Ec / E) ** 1.5)
    sv = sig * v if Ti_keV is None else sigv_thermal(E, Ti_keV)
    return float(np.trapezoid(nT * sv / dEdt, E))
def P_bt(P_MW, E_b, fracs, Te_keV, n_e, f_T, ni_over_ne, Ti_keV=None):
    comp = composition(f_T, ni_over_ne); tot = 0.0
    for k, fk in enumerate(fracs, start=1):
        Ek = E_b / k; rate = P_MW * 1e6 * fk / (Ek * 1.602176634e-16); tot += rate * yield_per_ion(Ek, Te_keV, n_e, comp, n=600 if Ti_keV else 4000, Ti_keV=Ti_keV)
    return tot * Q_DT_J / 1e6
