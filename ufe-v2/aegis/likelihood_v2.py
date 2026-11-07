# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 50961350c7a6bba3
"""Likelihoods for AEGIS UFE v2: CMB acoustic angle, DESI DR2 BAO, Pantheon+ SNe, local H0."""
import logging

import numpy as np
from .cosmo_v2 import LCDM, derived
from . import data_v2 as D

THETA_REF = derived(LCDM(0.6736, 0.1200))["theta"]   # self-consistent Planck LCDM reference
LOG = logging.getLogger(__name__)

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
        if not np.isfinite(rd) or rd <= 0:
            raise ValueError("Drag sound horizon must be finite and positive")
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
        luminosity_distance = (1 + self.zsn) * Dd.DC(self.zsn)
        if (np.shape(luminosity_distance) != self.zsn.shape
                or not np.isfinite(luminosity_distance).all()
                or np.any(luminosity_distance <= 0)):
            raise ValueError("Supernova distances must be finite, positive and match the bins")
        mu = 5 * np.log10(luminosity_distance) + 25
        delta = self.msn - mu
        # Remove a common offset before projection to avoid subtracting large chi-squares.
        relative_delta = delta - delta[0]
        B = relative_delta @ self.Cinv @ self.one
        Cc = self.one @ self.Cinv @ self.one
        centered_delta = relative_delta - B / Cc
        chi_sn = centered_delta @ self.Cinv @ centered_delta
        M_best = delta[0] + B / Cc
        chi_h0 = ((100 * m.h - self.h0_local[0]) / self.h0_local[1])**2 if self.use_shoes else 0.0
        total = chi_cmb + chi_bao + chi_sn + chi_h0
        if not np.isfinite([chi_cmb, chi_bao, chi_sn, chi_h0, total, M_best]).all():
            raise ValueError("Likelihood contributions and total must be finite")
        return dict(cmb=chi_cmb, bao=chi_bao, sn=chi_sn, h0=chi_h0,
                    total=total, M_B=M_best, derived=d)

    def chi2(self, m):
        try:
            return self.parts(m)["total"]
        except (ValueError, FloatingPointError, OverflowError, np.linalg.LinAlgError) as error:
            LOG.warning("Rejected reference-likelihood evaluation: %s", error)
            return 1e12
