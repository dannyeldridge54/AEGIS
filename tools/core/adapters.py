"""AEGIS Core module adapters: gift toolkits not in the CubeMind registry, called through one small worker process."""
import json, os, subprocess, sys
AEGIS = os.environ.get('AEGIS_DIR', '')
ADAPTERS = {
    'zurvan_delta_ew': dict(title='Zurvan: electroweak fine-tuning Delta_EW', timeout=60, example={'slha_file': 'example_P1_natural.slha'},
        description='Delta_EW (DEW4SLHA definition) from an SLHA spectrum file in tools/gifts/zurvan or a full path.',
        inputSchema={'type': 'object', 'properties': {'slha_file': {'type': 'string'}}, 'required': ['slha_file'], 'additionalProperties': False},
        limits='Needs a spectrum at the EWSB minimum (EWSB residual reported); one-loop Sigma terms only.', locks=['PREREG_D2187_zurvan_dew.md']),
    'aion_mbb_band': dict(title='Aion: neutrinoless double-beta m_bb band', timeout=60, example={'ordering': 'NO'},
        description='m_bb range over the Majorana phase at the NuFIT 6.0 best fit, lightest mass 0, for the Zee-Babu model.',
        inputSchema={'type': 'object', 'properties': {'ordering': {'type': 'string', 'enum': ['NO', 'IO']}}, 'required': ['ordering'], 'additionalProperties': False},
        limits='Best-fit oscillation parameters only; use the Aion 3-sigma scan for envelopes.', locks=['PREREG_D2188_aion_zeebabu.md']),
    'hyperion_jfactor': dict(title='Hyperion: dark-matter annihilation J-factor', timeout=120,
        example={'profile': 'Einasto', 'survey': 'HESS_IGS', 'rho_sun': 0.4, 'r_sun': 8.21},
        description='J-factor (GeV^2 cm^-5) over a survey region for Einasto, NFW or Burkert halos (fast route, smooth profiles).',
        inputSchema={'type': 'object', 'properties': {'profile': {'type': 'string', 'enum': ['Einasto', 'NFW', 'Burkert']}, 'survey': {'type': 'string'},
                     'rho_sun': {'type': ['number', 'integer'], 'x-unit': 'GeV/cm^3'}, 'r_sun': {'type': ['number', 'integer'], 'x-unit': 'kpc'}},
                     'required': ['profile'], 'additionalProperties': False},
        limits='Smooth (uncored) profiles; cored profiles use the reference route.', locks=['PREREG_SPEED_hyperion.md']),
}
WORKER = r'''
import json, os, sys
A = os.environ['AEGIS_DIR']; name, a = sys.argv[1], json.loads(sys.argv[2])
def J(x):
    import numpy as np
    if isinstance(x, dict): return {k: J(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [J(v) for v in x]
    if isinstance(x, np.generic): return x.item()
    return x
if name == 'zurvan_delta_ew':
    d = os.path.join(A, 'tools', 'gifts', 'zurvan'); sys.path.insert(0, d); import zurvan as Z
    f = a['slha_file'] if os.path.isabs(a['slha_file']) else os.path.join(d, a['slha_file'])
    r = Z.delta_ew(Z.params_from_slha(open(f).read())); out = {k: r[k] for k in ('Delta_EW', 'largest', 'EWSB_residual', 'mZ_used') if k in r}
    out['warnings'] = list(getattr(Z, 'WARN', []))
elif name == 'aion_mbb_band':
    sys.path.insert(0, os.path.join(A, 'tools', 'gifts', 'aion')); import aion as Q
    lo, hi, mlight = Q.mbb_band(a['ordering'], Q.best(a['ordering'])); out = dict(ordering=a['ordering'], mbb_min_eV=lo, mbb_max_eV=hi, sum_mnu_eV=mlight)
elif name == 'hyperion_jfactor':
    sys.path.insert(0, os.path.join(A, 'tools')); from janus_astro import settings as S
    out = S.jfactor(a['profile'], a.get('survey', 'HESS_IGS'), a.get('rho_sun', 0.4), a.get('r_sun', 8.21))
print(json.dumps(J(out)))
'''
def run(name, args, timeout):
    env = dict(os.environ, AEGIS_DIR=AEGIS or os.environ.get('AEGIS_DIR', ''))
    try:
        r = subprocess.run([sys.executable, '-c', WORKER, name, json.dumps(args)], capture_output=True, text=True, timeout=timeout, env=env)
        if r.returncode == 0 and r.stdout.strip(): return json.loads(r.stdout.strip().splitlines()[-1])
        return {'error': (r.stderr or 'failed').strip().splitlines()[-1][:300]}
    except subprocess.TimeoutExpired: return {'error': f'timeout {timeout} s'}
    except Exception as e: return {'error': f'{type(e).__name__}: {e}'[:300]}
