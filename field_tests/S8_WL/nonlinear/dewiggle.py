"""BAO damping of the two-halo term, as HMcode-2020 (Mead et al. 2020, eqs. 14-16), for use with the patched
axionHMcode copy (two-halo linear power multiplied by hmcode_dic['dw']).
    P_dwl = P_lin - (1 - exp(-k^2 sigma_v^2)) (P_lin - P_nw),   sigma_v^2 = (1 / 6 pi^2) * int P_lin dk
P_nw: Eisenstein & Hu (1998) no-wiggle shape times P_lin / P_EH smoothed with a Gaussian of width 0.25 in ln k.
Units: k in h/Mpc, P in (Mpc/h)^3. Returns dw = P_dwl / P_lin on the input k grid."""
import numpy as np


def eh_nowiggle(kh, h, omega_m, omega_b, ns, T_cmb=2.7255):
    om, ob = omega_m, omega_b
    fb = ob / om
    th = T_cmb / 2.7
    s = 44.5 * np.log(9.83 / om) / np.sqrt(1 + 10 * ob ** 0.75)                     # Mpc
    a_g = 1 - 0.328 * np.log(431 * om) * fb + 0.38 * np.log(22.3 * om) * fb ** 2
    k = kh * h                                                                         # 1/Mpc
    gam = om / h * (a_g + (1 - a_g) / (1 + (0.43 * k * s) ** 4))                       # Gamma_eff in h/Mpc units
    q = kh * th ** 2 / gam
    L0 = np.log(2 * np.e + 1.8 * q)
    C0 = 14.2 + 731 / (1 + 62.5 * q)
    T = L0 / (L0 + C0 * q * q)
    return kh ** ns * T ** 2


def dewiggle_ratio(kh, pk, h, omega_m, omega_b, ns, width=0.25):
    lk = np.log(kh)
    pnw0 = eh_nowiggle(kh, h, omega_m, omega_b, ns)
    r = pk / pnw0
    # Gaussian smoothing of ln-ratio in ln k (edges: renormalised weights)
    d = lk[:, None] - lk[None, :]
    w = np.exp(-0.5 * (d / width) ** 2)
    rs = np.exp((w @ np.log(r)) / w.sum(axis=1))
    pnw = pnw0 * rs
    sv2 = np.trapezoid(pk, kh) / (6 * np.pi ** 2)
    pdw = pk - (1 - np.exp(-kh ** 2 * sv2)) * (pk - pnw)
    return pdw / pk
