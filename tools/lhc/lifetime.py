# AEGIS-FP 2B3HAN4EXZU44LWJ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus-LHC: pure-wino chargino mass splitting and lifetime.
dm: two-loop fit (Ibe, Matsumoto, Sato, arXiv:1212.5989, Eq. 17; quoted fit accuracy < 0.02% for 100-4000 GeV; theory error +-0.3-0.4 MeV).
Widths: Eq. 21 (pi mode, normalised to Gamma(pi->mu nu)) and Eq. 22 (e nu); mu nu with exact 3-body phase-space factor added here."""
import math
HBAR_GEV_S = 6.582119569e-25; C_CM_S = 2.99792458e10
M_PI, M_MU, M_E = 0.13957039, 0.1056583755, 0.51099895e-3     # GeV
TAU_PI = 2.6033e-8; GF = 1.1663788e-5
def dm(m_gev):
    if not 1.0 <= float(m_gev) <= 1e5: raise ValueError('wino mass must be between 1 GeV and 100 TeV (the two-loop fit is calibrated on 100-4000 GeV)')
    L = math.log(m_gev)
    return 1e-3*(-413.315 + 305.383*L - 60.8831*L**2 + 5.41948*L**3 - 0.181509*L**4)   # GeV
def _f(x):
    """Phase-space suppression of the 3-body width for a massive lepton (muon-decay function), x = m_l/dm."""
    if x >= 1: return 0.0
    return 1 - 8*x**2 + 8*x**6 - x**8 - 24*x**4*math.log(x)
def widths(m_gev=None, d=None):
    d = dm(m_gev) if d is None else d
    g_pimunu = HBAR_GEV_S/TAU_PI
    gpi = 0.0 if d <= M_PI else g_pimunu*16*d**3/(M_PI*M_MU**2)*math.sqrt(1 - M_PI**2/d**2)*(1 - M_MU**2/M_PI**2)**-2
    ge = 2*GF**2/(15*math.pi**3)*d**5*_f(M_E/d); gmu = 2*GF**2/(15*math.pi**3)*d**5*_f(M_MU/d)
    tot = gpi + ge + gmu
    return {'dm_MeV': d*1e3, 'Gamma_GeV': tot, 'tau_ns': HBAR_GEV_S/tot*1e9, 'ctau_cm': HBAR_GEV_S/tot*C_CM_S,
            'BR_pi': gpi/tot, 'BR_e': ge/tot, 'BR_mu': gmu/tot}
