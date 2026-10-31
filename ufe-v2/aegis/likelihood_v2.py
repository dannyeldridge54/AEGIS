# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 50961350c7a6bba3
"""Likelihoods for AEGIS UFE v2: CMB acoustic angle, DESI DR2 BAO, Pantheon+ SNe, local H0."""
import numpy as np
from .cosmo_v2 import LCDM, derived
from . import data_v2 as D

THETA_REF = derived(LCDM(0.6736, 0.1200))["theta"]   # self-consistent Planck LCDM reference

class Likelihood:
    def __init__(self, pantheon_path, use_shoes=False, wc_prior=False, h0_local=D.SH0ES_2022):
        self.zsn, self.msn, cov = D.load_pantheon_binned(pantheon_path)
        self.Cinv = np.linalg.inv(cov)
        self.one = np.ones_like(self.zsn)
        self.use_shoes, self.wc_prior, self.h0_local = use_shoes, wc_prior, h0_local
        # BAO data vector and covariance
        vals, errs, rows = [], [], []
        self.bao_terms = []
        for name, z, dv, edv, dm, edm, dh, edh, r in D.DESI_DR2:
            if dv is not None:
                self.bao_terms.append(("DV", z)); vals.append(dv); errs.append((edv,))
            else:
                self.bao_terms += [("DM", z), ("DH", z)]
                vals += [dm, dh]; errs.append((edm, edh, r))
        n = len(vals)
        C = np.zeros((n, n)); i = 0
        for e in errs:
            if len(e) == 1:
                C[i, i] = e[0]**2; i += 1
            else:
                edm, edh, r = e
                C[i, i], C[i + 1, i + 1] = edm**2, edh**2
                C[i, i + 1] = C[i + 1, i] = r * edm * edh; i += 2
        self.bao_obs, self.bao_Cinv = np.array(vals), np.linalg.inv(C)

    def parts(self, m):
        d = derived(m); Dd = d["D"]; rd = d["rd"]
        # CMB acoustic angle (calibrated to the Planck LCDM reference, see docs)
        chi_cmb = ((d["theta"] / THETA_REF - 1) / D.THETA_STAR_FRAC_ERR)**2
        chi_cmb += ((m.wb - D.OMEGA_B_PRIOR[0]) / D.OMEGA_B_PRIOR[1])**2
        if self.wc_prior:
            chi_cmb += ((m.wc - D.OMEGA_C_PLANCK[0]) / D.OMEGA_C_PLANCK[1])**2
        # BAO
        pred = np.array([
            (Dd.DV(z) if k == "DV" else Dd.DC(z) if k == "DM" else Dd.DH(z)) / rd
            for k, z in self.bao_terms])
        r = pred - self.bao_obs
        chi_bao = r @ self.bao_Cinv @ r
        # SNe, absolute magnitude marginalised analytically
        mu = 5 * np.log10((1 + self.zsn) * Dd.DC(self.zsn)) + 25
        delta = self.msn - mu
        A = delta @ self.Cinv @ delta; B = delta @ self.Cinv @ self.one
        Cc = self.one @ self.Cinv @ self.one
        chi_sn = A - B * B / Cc
        M_best = B / Cc
        chi_h0 = ((100 * m.h - self.h0_local[0]) / self.h0_local[1])**2 if self.use_shoes else 0.0
        return dict(cmb=chi_cmb, bao=chi_bao, sn=chi_sn, h0=chi_h0,
                    total=chi_cmb + chi_bao + chi_sn + chi_h0, M_B=M_best, derived=d)

    def chi2(self, m):
        try:
            return self.parts(m)["total"]
        except Exception:
            return 1e12
