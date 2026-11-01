# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: dc1de16517b07e26
"""Fix the field width F = sqrt(3/2) M_Pl / N with a 1% constraint (PREREG_N_PACT.md, test T2).

CAMB solves the decay constant f from (z_c, f_EDE); this reads it back and penalises any departure from the target.
Its own chi2 (chi2__fwidth_N) is removed before comparing with LCDM.
"""
import math

from cobaya.likelihood import Likelihood

F_TORSION = math.sqrt(1.5)


class _FWidth(Likelihood):
    N = 9

    def get_requirements(self):
        return {"CAMBdata": None}

    def logp(self, **params_values):
        target = F_TORSION / self.N
        f = self.provider.get_CAMBdata().Params.DarkEnergy.f
        return -0.5 * ((f - target) / (0.01 * target)) ** 2


class FWidth9(_FWidth):
    N = 9


# Profile in the divisor N (PREREG_PHASE1.md, step 1.2): the same constraint at every N.
for _n in (6, 7, 8, 10, 11, 12):
    globals()[f"FWidth{_n}"] = type(f"FWidth{_n}", (_FWidth,), {"N": _n})
