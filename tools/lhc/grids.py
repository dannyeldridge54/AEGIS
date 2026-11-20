# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 (τ, m) acceptance grid (R3): what reinterpretation users ask experiments for — an efficiency map over mass AND
lifetime for a long-lived chargino — produced from CERN+1's validated disappearing-track model:
  acc×eff(m, τ) = EFF0 × P(decay inside the tracklet window | boost distribution at m)
EFF0 is the per-event efficiency anchored on ATLAS arXiv:2201.02472 (reproduces its 660 GeV limit to 1%, D1302);
the decay window and the boost distribution are CERN+1's validated kinematics. Labelled as a recast-model map, not an
official ATLAS efficiency map."""
import numpy as np
from . import future, kinematics, recast_dt

def acc_eff(m, tau_ns, sqrts=13.0):
    return future.EFF0*kinematics.p_window_avg(m, tau_ns=tau_ns, sqrts=sqrts)

def grid(masses=(200, 400, 600, 800, 1000, 1200), taus_ns=(0.01, 0.03, 0.1, 0.2, 0.3, 1.0, 3.0, 10.0), sqrts=13.0):
    return dict(masses_GeV=list(masses), taus_ns=list(taus_ns),
                acc_eff=[[float(acc_eff(m, t, sqrts)) for t in taus_ns] for m in masses],
                note='CERN+1 recast-model acceptance x efficiency (EFF0 anchored on ATLAS 2201.02472); not an official ATLAS map')

def hepdata_2d(g):
    """HEPData-style 2D table: two independent variables (mass, lifetime), one dependent (acc x eff)."""
    xs, ts, vals = [], [], []
    for i, m in enumerate(g['masses_GeV']):
        for j, t in enumerate(g['taus_ns']):
            xs.append(m); ts.append(t); vals.append(g['acc_eff'][i][j])
    lines = ['independent_variables:', "- header: {name: 'chargino mass', units: 'GeV'}", '  values:'] + [f'  - {{value: {x}}}' for x in xs]
    lines += ["- header: {name: 'chargino lifetime', units: 'ns'}", '  values:'] + [f'  - {{value: {t}}}' for t in ts]
    lines += ['dependent_variables:', "- header: {name: 'acceptance x efficiency', units: ''}",
              "  qualifiers:\n    - {name: source, value: 'CERN+1 recast model (EFF0 from ATLAS 2201.02472)'}", '  values:']
    lines += [f'  - {{value: {v:.6g}}}' for v in vals]
    return '\n'.join(lines) + '\n'
