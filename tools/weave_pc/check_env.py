"""Weave PC test: environment check. Writes env_report.txt next to this file."""
import os, sys, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.environ.get('WEAVE_PKGS', r'C:\Users\Danny\ufe_data\packages')
rep = dict(python=sys.version, cpu=os.cpu_count(), packages_path=P)
for m in ('numpy', 'scipy', 'camb', 'cobaya', 'planckpr4lensing', 'planck_2020_hillipop', 'planck_2020_lollipop'):
    try: mod = importlib.import_module(m); rep[m] = getattr(mod, '__version__', 'ok')
    except Exception as e: rep[m] = 'MISSING: ' + type(e).__name__
d = os.path.join(P, 'data')
for sub in ('planck_NPIPE_CamSpec', 'planck_2020', 'planck_2018_lowT_native', 'bao_data/desi_bao_dr2', 'sn_data/DES-Dovekie', 'sn_data/PantheonPlus', 'sn_data/Union3'):
    rep['data:' + sub] = os.path.isdir(os.path.join(d, sub))
open(os.path.join(HERE, 'env_report.txt'), 'w').write(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1))
