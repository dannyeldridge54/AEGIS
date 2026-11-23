"""N1: D-T neutron birth spectrum from first principles (PREREG_N1_BIRTH). Maxwellian D, T; weight sigma_BH(E_cm) v_rel; relativistic two-body."""
import numpy as np
from scipy import constants as sc
MN = sc.value('neutron mass energy equivalent in MeV'); MD = sc.value('deuteron mass energy equivalent in MeV')
MT = sc.value('triton mass energy equivalent in MeV'); MA = sc.value('alpha particle mass energy equivalent in MeV')
E0 = ((MD + MT) ** 2 + MN ** 2 - MA ** 2) / (2 * (MD + MT)) - MN          # MeV, reactants at rest
A = (6.927e4, 7.454e8, 2.050e6, 5.2002e4); B = (63.8, -0.995, 6.981e-5, 1.728e-4); BG = 34.3827
def sigma_bh(E):            # DT, E keV (CM) -> mb
    S = (A[0] + E * (A[1] + E * (A[2] + E * A[3]))) / (1 + E * (B[0] + E * (B[1] + E * (B[2] + E * B[3]))))
    return S / (E * np.exp(BG / np.sqrt(E)))
def spectrum(T_keV, n=2_000_000, seed=1, weighted=True):
    rng = np.random.default_rng(seed); kT = T_keV * 1e-3
    vD = rng.normal(0, np.sqrt(kT / MD), (n, 3)); vT = rng.normal(0, np.sqrt(kT / MT), (n, 3))
    def four(m, v):
        g = 1 / np.sqrt(1 - (v ** 2).sum(1)); return g * m, (g * m)[:, None] * v
    ED, pD = four(MD, vD); ET, pT = four(MT, vT)
    Et, pt = ED + ET, pD + pT; s = Et ** 2 - (pt ** 2).sum(1); rs = np.sqrt(s)
    Ecm = (rs - MD - MT) * 1e3                                     # keV, relative kinetic energy in the CM
    vr = np.linalg.norm(vD - vT, axis=1)
    w = sigma_bh(np.maximum(Ecm, 1e-3)) * vr if weighted else np.ones(n)
    Ens = (s + MN ** 2 - MA ** 2) / (2 * rs); ps = np.sqrt(Ens ** 2 - MN ** 2)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    beta = pt / Et[:, None]; b2 = (beta ** 2).sum(1); g = 1 / np.sqrt(1 - b2)
    En_lab = g * (Ens + (beta * u).sum(1) * ps) - MN                 # boost: E' = gamma (E* + beta . p*)
    w = w / w.sum(); mean = (w * En_lab).sum(); var = (w * (En_lab - mean) ** 2).sum()
    return dict(T=T_keV, mean_MeV=mean, shift_keV=(mean - E0) * 1e3, sigma_keV=np.sqrt(var) * 1e3, FWHM_keV=2 * np.sqrt(2 * np.log(2)) * np.sqrt(var) * 1e3)
def ballabio(T):
    d = 5.30509 * T ** (2 / 3) / (1 + 2.4736e-3 * T ** 1.84) + 1.3818 * T
    dw = 5.1068e-4 * T ** (2 / 3) / (1 + 7.6223e-3 * T ** 1.78) + 8.7691e-5 * T
    return dict(shift_keV=d, FWHM_keV=177.259 * (1 + dw) * np.sqrt(T))
