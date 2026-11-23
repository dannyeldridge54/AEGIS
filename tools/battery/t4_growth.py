"""D2178 T4 growth (compressed): S8 = sigma8 (Om/0.3)^0.5 at each best fit, same theory as the fit; vs DES Y3 and KiDS-Legacy."""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, 'cmb-fit'); from rt_planck_fit import rt_theory
from cobaya.model import get_model
P = '/tmp/claude-0/cobaya_pkgs'
REF = {'DESY3_3x2pt': (0.776, 0.017, 0.017), 'KiDS_Legacy': (0.815, 0.016, 0.021)}
def model_for(m, pt):
    ex = {'num_massive_neutrinos': 1, 'nnu': 3.044, 'lens_potential_accuracy': 1, 'halofit_version': 'mead'}
    pr = {k: pt[k] for k in ('ombh2', 'omch2', 'H0', 'tau') if k in pt}
    pr['As'] = 1e-10*np.exp(pt['logA']); pr['sigma8'] = None; pr['omegam'] = None
    if m == 'L': pr['ns'] = pt['ns']; pr['mnu'] = 0.06; th = {'camb': {'extra_args': ex}}
    else:
        pr.update(ns=0.9706, nrun=-9.7e-4, r=5.4e-4, mnu=0.0587, rt_ui=pt['rt_ui'])
        ex.update({'num_massive_neutrinos': 3, 'neutrino_hierarchy': 'normal', 'dark_energy_model': 'ppf'})
        th = {'rtcamb': {'external': rt_theory(), 'extra_args': ex}}
    return get_model({'packages_path': P, 'theory': th, 'params': pr, 'likelihood': {'one': None}})
rows = []
for f in sorted(glob.glob('field_tests/weave_lcdm/pr4_[LW]_*.json')):
    if any(s in f for s in ('_fast', '_tight')): continue
    d = json.load(open(f)); m = d['model']; pt = d['point']
    try:
        mod = model_for(m, pt); der = mod.logposterior({}, as_dict=True)['derived']; dv = (der['sigma8'], der['omegam'])
        s8 = dv[0]*(dv[1]/0.3)**0.5
        pulls = {k: (s8 - v[0])/(v[1] if s8 > v[0] else v[2]) for k, v in REF.items()}
        rows.append(dict(file=os.path.basename(f), model=m, sigma8=dv[0], Om=dv[1], S8=s8, pulls=pulls, chi2_growth={k: p*p for k, p in pulls.items()}))
        print(os.path.basename(f), m, round(s8, 4), {k: round(p, 2) for k, p in pulls.items()}, flush=True)
    except Exception as e:
        rows.append(dict(file=os.path.basename(f), error=str(e)[:200])); print('ERR', f, str(e)[:200], flush=True)
json.dump(dict(ref=REF, rows=rows), open('field_tests/results/d2178_T4_growth.json', 'w'), indent=1)
