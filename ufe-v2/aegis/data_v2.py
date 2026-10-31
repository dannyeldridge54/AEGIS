# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: f2c32c191694e63e
"""Survey data for AEGIS UFE v2 (current as of Oct 2026)."""
import json, os
import numpy as np

# DESI DR2 BAO (DESI Collaboration 2025, arXiv:2503.14738, Table IV), stat+sys
DESI_DR2 = [
    # tracer,      z,     DV/rd,  err,   DM/rd,  err,   DH/rd,  err,   r_MH
    ("BGS",       0.295, 7.942, 0.075, None, None, None, None, None),
    ("LRG1",      0.510, None, None, 13.588, 0.167, 21.863, 0.425, -0.459),
    ("LRG2",      0.706, None, None, 17.351, 0.177, 19.455, 0.330, -0.404),
    ("LRG3+ELG1", 0.934, None, None, 21.576, 0.152, 17.641, 0.193, -0.416),
    ("ELG2",      1.321, None, None, 27.601, 0.318, 14.176, 0.221, -0.434),
    ("QSO",       1.484, None, None, 30.512, 0.760, 12.817, 0.516, -0.500),
    ("Lya",       2.330, None, None, 38.988, 0.531,  8.632, 0.101, -0.431),
]

# CMB: Planck 2018 acoustic angle 100*theta* = 1.04109 +/- 0.00030 (TT,TE,EE+lowE+lensing)
THETA_STAR_FRAC_ERR = 0.00030 / 1.04109
OMEGA_B_PRIOR = (0.02237, 0.00015)
OMEGA_C_PLANCK = (0.1200, 0.0012)          # LCDM-only prior, used in the 'conservative' run

# Local distance ladder
SH0ES_2022 = (73.04, 1.04)                 # Riess et al. 2022
H0DN_2026 = (73.50, 0.81)                  # Local Distance Network, Casertano et al. 2026

def load_pantheon_binned(path):
    """Pantheon+ 1701 SNe binned to 40 redshift bins with the full STAT+SYS covariance
    (produced by the repo's preprocess/bin-pantheon scripts)."""
    d = json.load(open(path))
    z = np.array(d["binZ"]); mu = np.array(d["binMu"])
    cov = np.array(d["covBin"]).reshape(d["nBins"], d["nBins"])
    return z, mu, cov
