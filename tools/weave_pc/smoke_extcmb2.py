"""D2151 smoke test: build the ACT and SPT likelihood sets and evaluate one LCDM point each (no fitting, no scoring)."""
import os, sys, time, json
os.environ.setdefault('WEAVE_PKGS', r'C:\Users\Danny\ufe_data\packages')
from cobaya.model import get_model
P = os.environ['WEAVE_PKGS']; out = {}
pars = {'ombh2': 0.02237, 'omch2': 0.1200, 'H0': 67.4, 'As': 2.1e-9, 'ns': 0.965, 'tau': 0.054, 'mnu': 0.06}
for HL in ('act', 'spt'):
    t = time.time()
    try:
        ex = {'num_massive_neutrinos': 1, 'nnu': 3.044, 'halofit_version': 'mead'}
        if HL == 'act':
            like = {'act_dr6_cmbonly': {'params': {'A_act': {'prior': {'dist': 'norm', 'loc': 1.0, 'scale': 0.003}}, 'P_act': {'prior': {'min': 0.5, 'max': 1.5}}}},
                    'act_dr6_lenslike.ACTDR6LensLike': None}
            ex.update({'lens_potential_accuracy': 8, 'lAccuracyBoost': 1.2, 'min_l_logl_sampling': 6000, 'DoLateRadTruncation': False, 'kmax': 10, 'k_per_logint': 130})
        else:
            like = {'candl.interface.CandlCobayaLikelihood': {'data_set_file': 'spt_candl_data.SPT3G_D1_TnE_lite', 'lensing': False, 'feedback': False, 'clear_internal_priors': True, 'params': {'Tcal': {'prior': {'dist': 'norm', 'loc': 1.0, 'scale': 0.0036}, 'ref': {'min': 0.999, 'max': 1.001}, 'proposal': 0.002}, 'Ecal': {'prior': {'min': 0.9, 'max': 1.1}, 'ref': {'min': 0.99, 'max': 1.01}, 'proposal': 0.005}}}}
            ex.update({'lens_potential_accuracy': 4, 'lAccuracyBoost': 1.2, 'DoLateRadTruncation': False})
        m = get_model({'packages_path': P, 'theory': {'camb': {'extra_args': ex}}, 'params': dict(pars), 'likelihood': like})
        ref = dict(zip(m.prior.params, m.prior.reference()))
        ll = m.loglikes(ref)
        out[HL] = dict(ok=True, sampled=list(m.prior.params), loglikes=[float(x) for x in ll[0]], seconds=time.time() - t)
    except Exception as e:
        out[HL] = dict(ok=False, error=f'{type(e).__name__}: {e}'[:1500], seconds=time.time() - t)
    print(HL, out[HL], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smoke_extcmb2.json'), 'w'), indent=1)
