#!/usr/bin/env python3
"""D2132 (newest data; derived from D2131 script): Weave vs LCDM vs w0wa on plik-lite + tau prior + DESI DR2 + one SN set.   python weave_lcdm_full.py <L|W|C> <pantheonplus|desy5|union3>"""
import os, sys, json, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'cmb-fit'))
from rt_planck_fit import rt_theory, rt_wtable
from cobaya import run as crun
P = '/tmp/claude-0/cobaya_pkgs'
model, sn = sys.argv[1], sys.argv[2]
HL = sys.argv[3] if len(sys.argv) > 3 else 'hillipop'   # D2135: 'camspec' swaps the PR4 high-l likelihood
ex = {'num_massive_neutrinos': 1, 'nnu': 3.044, 'lens_potential_accuracy': 1, 'halofit_version': 'mead'}
pr = {'ombh2': {'prior': {'min': 0.019, 'max': 0.026}, 'ref': {'dist': 'norm', 'loc': 0.02245, 'scale': 0.0002}, 'proposal': 0.0001},
      'omch2': {'prior': {'min': 0.09, 'max': 0.15}, 'ref': {'dist': 'norm', 'loc': 0.1185, 'scale': 0.002}, 'proposal': 0.001},
      'H0': {'prior': {'min': 55, 'max': 85}, 'ref': {'dist': 'norm', 'loc': 67.8, 'scale': 0.5}, 'proposal': 0.5},
      'logA': {'prior': {'min': 2.8, 'max': 3.3}, 'ref': {'dist': 'norm', 'loc': 3.045, 'scale': 0.01}, 'proposal': 0.01, 'drop': True},
      'As': {'value': 'lambda logA: 1e-10*np.exp(logA)'},
      'tau': {'prior': {'min': 0.01, 'max': 0.12}, 'ref': {'dist': 'norm', 'loc': 0.058, 'scale': 0.004}, 'proposal': 0.003},
      'mnu': 0.06}
if model in ('L', 'C'):
    pr['ns'] = {'prior': {'min': 0.9, 'max': 1.05}, 'ref': {'dist': 'norm', 'loc': 0.967, 'scale': 0.004}, 'proposal': 0.003}
    theory = {'camb': {'extra_args': ex}}
    if model == 'C':
        ex['dark_energy_model'] = 'ppf'
        pr['w'] = {'prior': {'min': -3.0, 'max': 1.0}, 'ref': {'dist': 'norm', 'loc': -0.8, 'scale': 0.05}, 'proposal': 0.05}
        pr['wa'] = {'prior': {'min': -3.0, 'max': 2.0}, 'ref': {'dist': 'norm', 'loc': -0.6, 'scale': 0.1}, 'proposal': 0.1}
else:
    pr['ns'] = 0.9706; pr['nrun'] = -9.7e-4; pr['r'] = 5.4e-4; pr['mnu'] = 0.0587
    ex.update({'num_massive_neutrinos': 3, 'neutrino_hierarchy': 'normal', 'dark_energy_model': 'ppf'})
    pr['rt_ui'] = {'prior': {'min': 1e-6, 'max': 0.6}, 'ref': {'dist': 'uniform', 'min': 0.02, 'max': 0.20}, 'proposal': 0.02}
    theory = {'rtcamb': {'external': rt_theory(), 'extra_args': ex, 'stop_at_error': False}}
info = {'packages_path': P, 'theory': theory, 'params': pr,
        'likelihood': {('planck_NPIPE_highl_CamSpec.TTTEEE' if HL == 'camspec' else 'planck_2020_hillipop.TTTEEE_bin'): None, 'planck_2020_lollipop.lowlE': None, 'planck_2018_lowl.TT': None, 'planckpr4lensing.PlanckPR4Lensing': None, 'bao.desi_dr2': None, 'sn.' + sn: None},
        'sampler': {'minimize': {'method': 'bobyqa', 'best_of': int(os.environ.get('BEST_OF', 2))}}, 'output': f'/tmp/claude-0/weave_pr4/{model}_{sn}' + os.environ.get('OUT_SUFFIX', '') + ('' if HL == 'hillipop' else '_' + HL), 'force': True}
if model == 'C': info['prior'] = {'w0wa_bound': 'lambda w, wa: 0.0 if w + wa < 0 else -np.inf'}
os.makedirs('/tmp/claude-0/weave_pr4', exist_ok=True)
t = time.time(); upd, smp = crun(info)
gp = {k: v['prior'] for k, v in upd['params'].items() if isinstance(v, dict) and isinstance(v.get('prior'), dict) and v['prior'].get('dist') == 'norm'}
row = {k: float(v) for k, v in smp.products()['minimum'].data.iloc[0].items() if isinstance(v, (int, float, np.integer, np.floating))}
like = {k: v for k, v in row.items() if k.startswith('chi2__') and '.' in k}
chi2 = sum(like.values()); chi2eff = chi2 + sum(((row[k] - g['loc'])/g['scale'])**2 for k, g in gp.items() if k in row)
out = dict(model=model, sn=sn, seconds=time.time() - t, chi2=chi2, chi2_eff=chi2eff, like=like, point=row)
if model == 'W':
    h = row['H0']/100; Om = (row['ombh2'] + row['omch2'] + 0.0587/93.14)/h**2
    a, w = rt_wtable(row['rt_ui'], Om, 2.4728e-5*(1 + 0.2271*3.044)/h**2); z = 1/a - 1; s = (z <= 2) & (z >= 0)
    out['thread_w0wa_cpl'] = [float(x) for x in np.linalg.lstsq(np.vstack([np.ones(s.sum()), 1 - a[s]]).T, w[s], rcond=None)[0]]
json.dump(out, open(os.path.join(HERE, f'pr4_{model}_{sn}' + os.environ.get('OUT_SUFFIX', '') + ('' if HL == 'hillipop' else '_' + HL) + '.json'), 'w'), indent=1)
print('DONE', model, sn, round(chi2eff, 2), flush=True)
