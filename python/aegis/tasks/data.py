"""
Observational datasets for UFE cosmological fitting.

Sources:
- Cosmic Chronometers: Moresco et al. 2022 (compilation)
- BAO: DESI DR1 2024
- SNe Ia: Pantheon+ Brout et al. 2022 (full STAT+SYS covariance)
- RSD: fσ₈ compilation (Sagredo et al. 2018 + DESI)
"""

import json
import os
import numpy as np

# ── Cosmic Chronometers H(z) ─────────────────────────────────────────────
CC_DATA = np.array([
    # [z, H(z) km/s/Mpc, σ_H]
    [0.07, 69.0, 19.6], [0.09, 69.0, 12.0], [0.12, 68.6, 26.2],
    [0.17, 83.0, 8.0],  [0.179, 75.0, 4.0], [0.199, 75.0, 5.0],
    [0.20, 72.9, 29.6], [0.27, 77.0, 14.0], [0.28, 88.8, 36.6],
    [0.352, 83.0, 14.0],[0.3802, 83.0, 13.5],[0.4, 95.0, 17.0],
    [0.4004, 77.0, 10.2],[0.4247, 87.1, 11.2],[0.4497, 92.8, 12.9],
    [0.47, 89.0, 49.6], [0.4783, 80.9, 9.0], [0.48, 97.0, 62.0],
    [0.593, 104.0, 13.0],[0.68, 92.0, 8.0], [0.781, 105.0, 12.0],
    [0.875, 125.0, 17.0],[0.88, 90.0, 40.0],[0.9, 117.0, 23.0],
    [1.037, 154.0, 20.0],[1.3, 168.0, 17.0],[1.363, 160.0, 33.6],
    [1.43, 177.0, 18.0],[1.53, 140.0, 14.0],[1.75, 202.0, 40.0],
    [1.965, 186.5, 50.4],
])

# ── DESI DR1 BAO ─────────────────────────────────────────────────────────
# DM/rs and DH/rs measurements
DESI_BAO = [
    # z_eff, DM_rs, DM_rs_err, DH_rs, DH_rs_err
    {'z': 0.30, 'DM_rs': 7.93, 'sigma': 0.15, 'DH_rs': None, 'DH_sig': None},
    {'z': 0.51, 'DM_rs': 13.62, 'sigma': 0.25, 'DH_rs': 20.98, 'DH_sig': 0.61},
    {'z': 0.71, 'DM_rs': 17.86, 'sigma': 0.33, 'DH_rs': 20.08, 'DH_sig': 0.60},
    {'z': 0.93, 'DM_rs': 21.71, 'sigma': 0.28, 'DH_rs': 17.88, 'DH_sig': 0.35},
    {'z': 1.32, 'DM_rs': 27.79, 'sigma': 0.69, 'DH_rs': 13.82, 'DH_sig': 0.42},
    {'z': 2.33, 'DM_rs': 39.71, 'sigma': 0.94, 'DH_rs': 8.52, 'DH_sig': 0.17},
]

# ── RSD fσ₈(z) ──────────────────────────────────────────────────────────
RSD_DATA = np.array([
    # [z, fσ₈, σ]
    [0.02, 0.428, 0.0465], [0.067, 0.423, 0.055],
    [0.10, 0.370, 0.130],  [0.17, 0.510, 0.060],
    [0.18, 0.360, 0.090],  [0.38, 0.440, 0.060],
    [0.25, 0.3512, 0.0583],[0.37, 0.4602, 0.0378],
    [0.32, 0.384, 0.095],  [0.59, 0.488, 0.060],
    [0.44, 0.413, 0.080],  [0.60, 0.390, 0.063],
    [0.73, 0.437, 0.072],  [0.80, 0.470, 0.080],
    [0.86, 0.400, 0.110],  [1.40, 0.482, 0.116],
])

# ── Pantheon+ Binned with Full Covariance ────────────────────────────────
_PANTHEON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                               'data', 'pantheon', 'pantheon_binned_fullcov.json')

PANTHEON_BINNED = None
try:
    with open(os.path.abspath(_PANTHEON_PATH), 'r') as f:
        _raw = json.load(f)
    PANTHEON_BINNED = {
        'z': np.array(_raw['binZ']),
        'mu': np.array(_raw['binMu']),
        'err': np.array(_raw['binErr']),
        'cov_inv': np.array(_raw['covBinInv']).reshape(_raw['nBins'], _raw['nBins']),
        'n_bins': _raw['nBins'],
        'n_sne': _raw['nSNe'],
    }
except FileNotFoundError:
    pass

# ── Legacy SNe summary data (for quick tests) ───────────────────────────
SNE_SUMMARY = np.array([
    # [z, μ, σ]
    [0.01, 33.11, 0.15], [0.02, 34.73, 0.12], [0.03, 35.58, 0.11],
    [0.05, 36.64, 0.10], [0.08, 37.65, 0.09], [0.12, 38.51, 0.08],
    [0.20, 39.59, 0.07], [0.30, 40.39, 0.06], [0.40, 41.01, 0.06],
    [0.50, 41.50, 0.06], [0.60, 41.91, 0.07], [0.80, 42.57, 0.08],
    [1.00, 43.07, 0.09], [1.20, 43.47, 0.10], [1.50, 43.92, 0.12],
    [1.80, 44.27, 0.15],
])
