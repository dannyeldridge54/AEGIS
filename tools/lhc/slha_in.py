# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 SLHA import (R2): read a spectrum file (SLHA 1/2, as written by SPheno, SoftSUSY, FeynHiggs, SusyHit ...) and
answer the CERN+1 questions for its lightest electroweakinos: what are they (wino-, higgsino- or bino-like, from NMIX),
how heavy, what Δm, and what CERN+1 says (cross section for a run, lifetime for a pure wino, expected reach)."""
import math, re
from . import settings, lifetime

def parse(text):
    """Return {BLOCKNAME: {key tuple: value}} and DECAY widths {pdg: width}."""
    blocks, decays, cur = {}, {}, None
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line: continue
        t = line.split()
        if t[0].upper() == 'BLOCK':
            cur = t[1].upper(); blocks[cur] = {}; continue
        if t[0].upper() == 'DECAY':
            decays[int(t[1])] = float(t[2]); cur = None; continue
        if cur is None: continue
        try:
            nums = [float(x) for x in t]
        except ValueError:
            continue
        key = tuple(int(x) for x in nums[:-1]); blocks[cur][key] = nums[-1]
    return blocks, decays

def classify(blocks):
    """Character of the lightest neutralino from NMIX row 1: fractions (bino, wino, higgsino)."""
    N = blocks.get('NMIX', {})
    if not N: return None
    b, w = N.get((1, 1), 0.0)**2, N.get((1, 2), 0.0)**2
    h = N.get((1, 3), 0.0)**2 + N.get((1, 4), 0.0)**2
    s = b + w + h or 1.0
    return dict(bino=b/s, wino=w/s, higgsino=h/s)

def summary(text, run='run3'):
    blocks, decays = parse(text)
    M = blocks.get('MASS', {})
    m1, mc = abs(M.get((1000022,), float('nan'))), abs(M.get((1000024,), float('nan')))
    frac = classify(blocks)
    kind = (max(frac, key=frac.get) if frac else ('wino' if not math.isnan(mc) and (mc - m1) < 1.0 else 'unknown'))
    out = dict(m_chi10_GeV=m1, m_chi1p_GeV=mc, dm_MeV=1e3*(mc - m1) if not math.isnan(mc) else None,
               character=frac, model=kind, run=run)
    if 1000024 in decays and decays[1000024] > 0:
        tau = 6.582119569e-25/decays[1000024]; out.update(tau_ns_file=tau*1e9, ctau_cm_file=tau*2.99792458e10)
    if kind in ('wino', 'higgsino') and not math.isnan(m1):
        p = settings.point(run, kind, m1); out.update(sigma_fb=p['sigma_fb'], produced_pairs=p['produced_pairs'])
        if kind == 'wino':
            w = lifetime.widths(m1); out.update(tau_ns_cern1=w['tau_ns'], ctau_cm_cern1=w['ctau_cm'])
    return out
