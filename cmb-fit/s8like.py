# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 5032d72c671f43a5
"""Weak-lensing S8 constraint as a Cobaya likelihood (values fixed in PREREG_S8.md before use).

S8 = sigma8 * sqrt(Omega_m / 0.3); an asymmetric Gaussian using the error on the side the model falls on.
"""
import math

from cobaya.likelihood import Likelihood

VALUES = {"A": (0.790, 0.018, 0.014),     # DES Y3 + KiDS-1000 joint cosmic shear (arXiv:2305.17173)
          "B": (0.815, 0.016, 0.021)}     # KiDS-Legacy cosmic shear (2025)


class _S8(Likelihood):
    which = "A"

    def get_requirements(self):
        return {"sigma8": None, "omegam": None}

    def logp(self, **params_values):
        s8 = self.provider.get_param("sigma8") * math.sqrt(self.provider.get_param("omegam") / 0.3)
        v, up, dn = VALUES[self.which]
        return -0.5 * ((s8 - v) / (up if s8 > v else dn)) ** 2


class S8A(_S8):
    which = "A"


class S8B(_S8):
    which = "B"
