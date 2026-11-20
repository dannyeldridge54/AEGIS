# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus settings (J1): model library + the CMB constraints inflation people score against + exports.
Danny 19 Nov 2026: toolkits at professionals' level, with tools that help test our model.
Predictions come from the validated exact Mukhanov-Sasaki route (core.spectra3); constraints carry their source."""
import json, math
from . import anyV, core

MODELS = {   # name: (V formula in M_P = 1, note)
    'phi2':        ('phi**2', 'quadratic chaotic (excluded by r; kept as a benchmark)'),
    'phi_2_3':     ('phi**(2/3)', 'axion-monodromy-like p = 2/3'),
    'starobinsky': ('(1-exp(-sqrt(2/3)*phi))**2', 'Starobinsky R^2 / E-model alpha = 1'),
    'alpha_1_3':   ('(1-exp(-sqrt(2)*phi))**2', 'E-model alpha = 1/3'),
    'weave_10d':   ('1-7.30*exp(-2*sqrt(2)*phi)', 'Weave LEADING-ORDER plateau only (beta = 2 sqrt 2); NOT the full SERAPIS-Lambda prediction, which adds the Ushas tilt and gives n_s ≈ 0.9706 (tools/janus_calc/models.py)'),
}
CONSTRAINTS = {   # quantity: {dataset: (value, sigma or upper limit, kind, source)}. J3 update 20 Nov 2026 (values cross-checked
                  # against the compilation in arXiv:2510.18656 Table I). Sets OVERLAP (shared Planck data): compare a model
                  # against each one, never add their pulls together.
    'ns': {'Planck2018':   (0.9649, 0.0042, 'gauss', 'Planck 2018 TT,TE,EE+lowE+lensing (A&A 641 A10)'),
           'ACT-DR6':      (0.9666, 0.0077, 'gauss', 'ACT DR6 alone (Louis et al. 2025, arXiv:2503.14452)'),
           'P-ACT':        (0.9709, 0.0038, 'gauss', 'Planck + ACT DR6 (Louis et al. 2025)'),
           'P-ACT-LB':     (0.9743, 0.0034, 'gauss', 'Planck + ACT DR6 + lensing + DESI DR1 BAO (Louis et al. 2025)'),
           'P-ACT-LB2':    (0.9752, 0.0030, 'gauss', 'Planck + ACT DR6 + lensing + DESI DR2 BAO (as quoted in arXiv:2510.18656)'),
           'SPT-3G-D1':    (0.951, 0.011, 'gauss', 'SPT-3G D1 alone (Camphuis et al. 2025, arXiv:2506.20707)'),
           'CMB-SPA':      (0.9684, 0.0030, 'gauss', 'SPT-3G D1 + Planck + ACT (CMB-SPA; Camphuis et al. 2025)'),
           'CMB-SPA+DESI': (0.9728, 0.0027, 'gauss', 'CMB-SPA + DESI DR2 BAO (Camphuis et al. 2025)')},
    'r':  {'BK18':         (0.036, None, 'upper95', 'BICEP/Keck 2018 + Planck (95% CL; PRL 127 151301)'),
           'P-ACT+BK18':   (0.038, None, 'upper95', 'Planck + ACT DR6 + BK18 (95% CL; ACT DR6 extended-models paper, 2025)'),
           'PR4+BK18':     (0.032, None, 'upper95', 'Planck PR4 + BK18, free tau (Tristram et al. 2022, PRD 105 083524)')},
}
def predict(model='starobinsky', Nstar=55.0, formula=None):
    expr = formula or MODELS[model][0]
    s = core.spectra3(anyV.from_formula(expr), float(Nstar))
    return dict(model=model if not formula else 'custom', V=expr, Nstar=float(Nstar),
                ns=float(s['ns']), r=float(s['r']), alpha_s=float(s['alpha_s']))
def score(pred):
    """Pull (sigma units) for each Gaussian set, pass/FAIL for each upper limit. Sets overlap: never sum pulls."""
    out = {}
    for q, sets in CONSTRAINTS.items():
        for k, (v, s, kind, _) in sets.items():
            out[f'{q}:{k}'] = (pred[q] - v)/s if kind == 'gauss' else ('pass' if pred[q] <= v else 'FAIL')
    return out
def table(Nstar=55.0, models=None):
    rows = []
    for m in (models or MODELS):
        p = predict(m, Nstar); p['scores'] = score(p); rows.append(p)
    return rows
def export(rows, fmt='json', prov=None):
    from tools.janus_astro.settings import export as _ex      # same JSON/CSV/ECSV writer as Hyperion (+ provenance, H1a)
    return _ex(rows, fmt, prov)
