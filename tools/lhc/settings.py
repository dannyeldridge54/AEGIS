# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 settings: one place to pick a collider run, a model and an output format, the way LHC analysis groups work.
Danny 19 Nov 2026: "make CERN+1 have settings for all the major things CERN uses it for, easily used and integrated at their level."

Scope stated plainly: CERN+1 covers electroweakino (wino/higgsino) pair production, lifetimes and disappearing-track
reach. It is not a general event generator or detector simulation; for those, groups use MadGraph, Pythia, Delphes.
What this module adds is the standard plumbing those groups expect:
  * RUNS     presets for LHC Run 2, Run 3, HL-LHC, and future hadron colliders (sqrt(s), integrated luminosity);
  * MODELS   pure wino, pure higgsino;
  * exports  - pyhf / HistFactory JSON workspace (the likelihood format ATLAS publishes on HEPData),
             - HEPData-style YAML table (independent_variables / dependent_variables),
             - SLHA-style blocks (MASS, DECAY) that spectrum and decay tools read.
Every number comes from the validated CERN+1 modules (xsec, higgsino, lifetime, recast_dt, future, stats)."""
import json, math
from . import xsec, higgsino, lifetime, recast_dt, future, stats

RUNS = {   # name: (sqrt(s) TeV, integrated luminosity fb^-1, note)
    'run2':      (13.0, 140.0,   'LHC Run 2 (2015-2018), full dataset'),
    'run3':      (13.6, 300.0,   'LHC Run 3 (2022-2026), approximate total'),
    'run2+3':    (13.6, 440.0,   'Run 2 + Run 3 combined (cross sections at 13.6 TeV; approximate)'),
    'hl-lhc':    (14.0, 3000.0,  'High-Luminosity LHC, nominal'),
    'hl-lhc-ult':(14.0, 4000.0,  'HL-LHC ultimate luminosity'),
    'he-lhc':    (27.0, 15000.0, 'High-Energy LHC study point (rough beyond 13.6 TeV)'),
    'fcc-hh':    (100.0, 30000.0,'FCC-hh study point (rough beyond 13.6 TeV)'),
}
MODELS = ('wino', 'higgsino')

def sigma_fb(model, m, sqrts):
    rs = str(sqrts).rstrip('0').rstrip('.') if isinstance(sqrts, float) else str(sqrts)
    if model == 'wino':
        if rs in ('13', '13.6'): return xsec.total(m, rs)['sum']
        return future.sig(m, float(sqrts))
    if model == 'higgsino':
        if rs in ('13', '13.6'): return higgsino.total(m, rs)
        return sum(higgsino.sigma_scaling(m, p, float(sqrts)) for p in higgsino.PROCS)
    raise ValueError(f'model must be one of {MODELS}')

def point(run='run3', model='wino', m=700.0):
    """Everything CERN+1 knows at one mass for one run: cross section, expected events, lifetime (wino)."""
    rs, L, note = RUNS[run]
    s = sigma_fb(model, m, rs)
    out = dict(run=run, run_note=note, sqrt_s_TeV=rs, lumi_fb=L, model=model, mass_GeV=m,
               sigma_fb=s, produced_pairs=s*L)
    if model == 'wino':
        w = lifetime.widths(m); out.update(dm_MeV=w.get('dm_MeV', w.get('dm')), ctau_cm=w.get('ctau_cm'), tau_ns=w.get('tau_ns'))
    return out

def reach(run='hl-lhc', r_bkg=1.0):
    """Expected disappearing-track wino reach (GeV) for a run, from the validated Run-2 recast efficiency."""
    rs, L, _ = RUNS[run]
    return dict(run=run, sqrt_s_TeV=rs, lumi_fb=L, r_bkg=r_bkg, wino_reach_GeV=future.reach(rs, L, r_bkg))

# ---------- standard exports ----------
def pyhf_workspace(s, b, n_obs, sigma_b=0.0, name='SR'):
    """One-bin HistFactory workspace (pyhf JSON schema 1.0.0), the format ATLAS publishes likelihoods in."""
    mods = [dict(name='mu', type='normfactor', data=None)]
    bmods = [dict(name='bkg_unc', type='normsys', data=dict(hi=1 + sigma_b/b, lo=max(1e-6, 1 - sigma_b/b)))] if sigma_b > 0 and b > 0 else []
    return {'channels': [{'name': name, 'samples': [
                {'name': 'signal', 'data': [float(s)], 'modifiers': mods},
                {'name': 'background', 'data': [float(b)], 'modifiers': bmods}]}],
            'observations': [{'name': name, 'data': [float(n_obs)]}],
            'measurements': [{'name': 'meas', 'config': {'poi': 'mu', 'parameters': []}}],
            'version': '1.0.0'}

def hepdata_yaml(x_name, x_unit, xs, y_name, y_unit, ys, qualifiers=None):
    """HEPData-style table (independent_variables / dependent_variables), written without a YAML library."""
    q = ''.join(f"\n    - {{name: {k}, value: '{v}'}}" for k, v in (qualifiers or {}).items())
    lines = ['independent_variables:', f"- header: {{name: '{x_name}', units: '{x_unit}'}}", '  values:']
    lines += [f'  - {{value: {x}}}' for x in xs]
    lines += ['dependent_variables:', f"- header: {{name: '{y_name}', units: '{y_unit}'}}" + (f'\n  qualifiers:{q}' if q else ''), '  values:']
    lines += [f'  - {{value: {y:.6g}}}' for y in ys]
    return '\n'.join(lines) + '\n'

def slha(m, model='wino'):
    """SLHA-style MASS and DECAY blocks for the lightest chargino (PDG 1000024) and neutralino (1000022)."""
    if model != 'wino': raise ValueError('SLHA export is implemented for the pure wino (lifetime from lifetime.py)')
    w = lifetime.widths(m); dm = (w.get('dm_MeV') or w.get('dm'))/1000.0
    tau_s = w['tau_ns']*1e-9; width = 6.582119569e-25/tau_s
    return (f"BLOCK MASS\n   1000022   {m:.6E}   # ~chi_10\n   1000024   {m + dm:.6E}   # ~chi_1+\n"
            f"DECAY   1000024   {width:.6E}   # ~chi_1+ total width (c tau = {w['ctau_cm']:.4g} cm)\n"
            f"     1.00000000E+00   2   1000022   211   # ~chi_1+ -> ~chi_10 pi+ (dominant, ~95%; e and mu channels ~4% omitted)\n")

def scan(run='run3', model='wino', masses=(300, 500, 700, 900, 1100), fmt='json'):
    rows = [point(run, model, float(m)) for m in masses]
    if fmt == 'hepdata':
        return hepdata_yaml('chargino mass', 'GeV', [r['mass_GeV'] for r in rows], 'sigma(pp -> pair)', 'fb',
                            [r['sigma_fb'] for r in rows], {'SQRT(S)': f"{RUNS[run][0]} TeV", 'model': model, 'source': 'CERN+1'})
    return json.dumps(rows, indent=1, default=float)
