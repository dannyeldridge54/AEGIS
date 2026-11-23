#!/usr/bin/env python3
"""Chronos v1: one nuclear-decay engine for Oklahoma's nuclear rung (D2189).
Danny Lee Eldridge / the Weave, 23 Nov 2026. A lantern, not a throne: free to use, change and share.

Branches: nuclear pharmacy (tracer planning, generators), environmental monitoring (release clocks),
nuclear energy and waste (long-lived chains), supernovae (Ni-56 -> Co-56 heating), kilonovae (r-process heating).
Decay arithmetic only: no production cross sections, dose or shielding (v2). Not a clinical or regulatory tool.
Chains are solved two independent ways: matrix exponential of the decay matrix, and the analytic Bateman solution.
"""
import numpy as np, math, json
from scipy.linalg import expm

MIN, H, D, Y = 60.0, 3600.0, 86400.0, 365.25 * 86400.0
# half-lives (seconds); NNDC NuDat / ENSDF or DDEP recommended values, entered by hand (see SOURCES)
T12 = {
 'F-18': 109.77 * MIN, 'C-11': 20.364 * MIN, 'N-13': 9.965 * MIN, 'O-15': 122.24, 'Ga-68': 67.71 * MIN,
 'Ge-68': 270.95 * D, 'Tc-99m': 6.0067 * H, 'Mo-99': 65.976 * H, 'Rb-82': 1.2575 * MIN, 'Sr-82': 25.35 * D,
 'Cu-64': 12.701 * H, 'Zr-89': 78.41 * H, 'Lu-177': 6.647 * D, 'Ac-225': 9.920 * D, 'In-111': 2.8047 * D,
 'I-123': 13.2234 * H, 'I-131': 8.0252 * D, 'Y-90': 64.05 * H, 'Sr-90': 28.91 * Y, 'Cs-137': 30.08 * Y,
 'Cs-134': 2.0652 * Y, 'Ba-137m': 2.552 * MIN, 'Co-60': 5.2714 * Y, 'Pu-241': 14.29 * Y, 'Am-241': 432.6 * Y,
 'Ni-56': 6.075 * D, 'Co-56': 77.236 * D,
}
SOURCES = 'Half-lives: NNDC NuDat 3 / ENSDF adopted values (DDEP where noted); entered by hand, verify before critical use.'
LAM = {k: math.log(2) / v for k, v in T12.items()}
# chains: list of nuclides, branching into the next member
CHAINS = {
 'Mo-99 -> Tc-99m (generator)': (['Mo-99', 'Tc-99m'], [0.876]),
 'Ge-68 -> Ga-68 (generator)': (['Ge-68', 'Ga-68'], [1.0]),
 'Sr-82 -> Rb-82 (generator)': (['Sr-82', 'Rb-82'], [1.0]),
 'Sr-90 -> Y-90': (['Sr-90', 'Y-90'], [1.0]),
 'Cs-137 -> Ba-137m': (['Cs-137', 'Ba-137m'], [0.946]),
 'Pu-241 -> Am-241 (spent fuel)': (['Pu-241', 'Am-241'], [0.99998]),
 'Ni-56 -> Co-56 (supernova)': (['Ni-56', 'Co-56'], [1.0]),
}

def decay_matrix(nucs, br):
    n = len(nucs); M = np.zeros((n, n))
    for i, k in enumerate(nucs):
        M[i, i] = -LAM[k]
        if i > 0: M[i, i - 1] = br[i - 1] * LAM[nucs[i - 1]]
    return M

def solve_expm(nucs, br, N0, t):
    return expm(decay_matrix(nucs, br) * t) @ np.asarray(N0, float)

def solve_bateman(nucs, br, N0, t):
    """Analytic Bateman for a linear chain with branching; general initial populations."""
    n = len(nucs); lam = [LAM[k] for k in nucs]; out = np.zeros(n)
    for s in range(n):                     # contribution of initial atoms of member s
        if N0[s] == 0: continue
        for j in range(s, n):
            pre = N0[s]
            for m in range(s, j): pre *= br[m] * lam[m]
            tot = 0.0
            for i in range(s, j + 1):
                den = 1.0
                for p in range(s, j + 1):
                    if p != i: den *= (lam[p] - lam[i])
                tot += math.exp(-lam[i] * t) / den
            out[j] += pre * tot
    return out

def activity(nucs, N):  # Bq
    return np.array([LAM[k] for k in nucs]) * N

# ---- pharmacy ----
def needed_at_start(nuc, A_need, t):
    """Activity to make now so that A_need remains after time t."""
    return A_need * math.exp(LAM[nuc] * t)

def time_to_activity(nuc, A0, A_target):
    return math.log(A0 / A_target) / LAM[nuc]

def generator_peak(chain):
    """Time of maximum daughter activity from a pure parent at t=0 (or right after a full elution)."""
    (p, d), _ = CHAINS[chain]; lp, ld = LAM[p], LAM[d]
    return math.log(ld / lp) / (ld - lp)

def transient_ratio(chain):
    (p, d), br = CHAINS[chain]; lp, ld = LAM[p], LAM[d]
    return br[0] * ld / (ld - lp) if ld > lp else float('nan')

# ---- monitoring ----
def release_age(ratio_now, ratio0=1.0, a='Cs-134', b='Cs-137'):
    """Years since release from an activity ratio a/b."""
    return math.log(ratio0 / ratio_now) / (LAM[a] - LAM[b]) / Y

def ratio_at(t_years, ratio0=1.0, a='Cs-134', b='Cs-137'):
    return ratio0 * math.exp(-(LAM[a] - LAM[b]) * t_years * Y)

# ---- supernova ----
MEV, NA, MSUN = 1.602176634e-6, 6.02214076e23, 1.98892e33
Q_NI, Q_CO, Q_POS = 1.75, 3.73, 0.12   # MeV per decay deposited (neutrinos excluded); Co-56 includes positron KE + annihilation

def sn_eps_coeffs():
    per_g = NA / 56.0
    return Q_NI * MEV * LAM['Ni-56'] * per_g, Q_CO * MEV * LAM['Co-56'] * per_g

def sn_luminosity(t, M_ni_msun=0.6, t0_days=None):
    nucs, br = CHAINS['Ni-56 -> Co-56 (supernova)']
    N0 = [M_ni_msun * MSUN * NA / 56.0, 0.0]
    N = solve_bateman(nucs, br, N0, t)
    L_ni = Q_NI * MEV * LAM['Ni-56'] * N[0]; L_co = Q_CO * MEV * LAM['Co-56'] * N[1]
    if t0_days is None: f = 1.0
    elif t0_days <= 0: f = 0.0     # full gamma escape
    else: f = 1.0 - math.exp(-(t0_days * D) ** 2 / t ** 2)
    fp = Q_POS / Q_CO              # Co-56 positron kinetic energy is deposited locally (DEV-1)
    return L_ni * f + L_co * ((1 - fp) * f + fp)   # radioactive heating (deposition) rate, not the light curve before peak

# ---- kilonova ----
def kilonova_luminosity(t, M_ej_msun=0.05, f_th=0.5):
    return M_ej_msun * MSUN * 1e10 * (t / D) ** -1.3 * f_th   # order of magnitude (Korobkin et al. 2012; Metzger 2019 LRR); constant f_th (see Barnes+2016)

if __name__ == '__main__':
    out = {'sources': SOURCES}
    out['generator_peak_h'] = {c: generator_peak(c) / H for c in CHAINS if 'generator' in c}
    out['transient_ratio'] = {c: transient_ratio(c) for c in CHAINS if 'generator' in c}
    out['F18_needed_for_370MBq_after_2h_MBq'] = needed_at_start('F-18', 370, 2 * H)
    out['eps_Ni_Co'] = sn_eps_coeffs()
    out['L_SNIa_0.6Msun_18d'] = sn_luminosity(18 * D)
    print(json.dumps(out, indent=1))
