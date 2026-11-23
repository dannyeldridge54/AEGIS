"""Aion fast paths (SPEED-Aion): numpy broadcasting of the same formulas. Reference: aion.py (unchanged)."""
import numpy as np
from aion import NUFIT6_3S, f_ratios, fmt_ceiling, sample, best

def _br(a, b):
    et, em = abs(a)**2, abs(b)**2
    w = np.stack([em + et, em + 1.0, et + 1.0]); return w / w.sum(0)

def scan3s_fast(o, n=9, nd=73):
    r = NUFIT6_3S[o]
    S12, S23, S13, Dd = np.meshgrid(np.linspace(*r['s12'], n), np.linspace(*r['s23'], n), np.linspace(*r['s13'], n),
                                    np.linspace(0, 360, nd), indexing='ij')
    a, b = f_ratios(o, S12, S23, S13, Dd); br = _br(a, b); ceil = fmt_ceiling(a, 1.0)
    vals = {'abs_f_etau_over_f_mutau': abs(a), 'abs_f_emu_over_f_mutau': abs(b), 'BR_e': br[0], 'BR_mu': br[1], 'BR_tau': br[2],
            'f_mutau_ceiling_at_1TeV': ceil}
    return {k: [float(v.min()), float(v.max())] for k, v in vals.items()}

def mc_fast(o, rng, N):
    S = sample(o, rng, N); a, b = f_ratios(o, S['s12'], S['s23'], S['s13'], S['d']); br = _br(a, b)
    q = lambda x: [float(np.percentile(x, 16)), float(np.percentile(x, 84))]
    return dict(f_etau=q(abs(a)), f_emu=q(abs(b)), BR_e=q(br[0]), BR_mu=q(br[1]), BR_tau=q(br[2]))
