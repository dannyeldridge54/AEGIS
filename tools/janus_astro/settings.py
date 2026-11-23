# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Hyperion settings: presets for the main ways astronomers and cosmologists would use Hyperion, plus scoring against the
newest measurements and standard exports (JSON, CSV, ECSV-style header). Danny 19 Nov 2026: "same with Hyperion, and tools for
all scientists that will help prove our model".

Every preset points at an already-validated Hyperion routine; measured values carry their source. Nothing here changes
a physics result — it only selects inputs and formats outputs, so the validation record of each module still applies."""
import csv, io, json, math

# ---- measurement datasets (value, 1-sigma, source) ----
DATA = {
    'Yp':        {'LBT2026': (0.2458, 0.0013, 'LBT 2026 (as used in D1191)'),
                  'Aver2021': (0.2453, 0.0034, 'Aver et al. 2021, JCAP 03 027')},
    'DH':        {'Cooke2018': (2.527e-5, 0.030e-5, 'Cooke, Pettini & Steidel 2018, ApJ 855 102')},
    'omega_b':   {'Planck2018': (0.02237, 0.00015, 'Planck 2018 TT,TE,EE+lowE+lensing')},
    'vc_sun':    {'Horta2026': (235.3, None, 'Horta et al. 2026 (as used in D1193; sigma not stored here)')},
}
BBN_CODES = ('primat', 'parthenope')
EOS = ('SLy', 'AP4')
MW_MODELS = ('MWPotential2014', 'McMillan17')
HALOS = {'NFW': dict(rs=20.0), 'Einasto': dict(rs=20.0, alpha=0.17), 'Burkert': dict(r0=9.0)}   # kpc; standard MW benchmarks
LINE_SURVEYS = {'HESS_IGS': dict(psi_max_deg=1.0, b_mask_deg=0.3, ref='H.E.S.S. inner Galaxy survey ROI (jfactor.py, D1055)')}
GW_DETECTORS = {   # LALSimulation PSD names used by gw_imr.py (needs lalsuite)
    'O4':  'aLIGOZeroDetHighPower', 'A+': 'aLIGOAPlusDesignSensitivityT1800042',
    'ET':  'EinsteinTelescopeP1600143', 'CE': 'CosmicExplorerP1600143'}

def pull(pred, meas):
    v, s, _ = meas
    return None if s in (None, 0) else (pred - v)/s

# Theory σ conventions (PREREG_W5_BBN_THEORY): PRIMAT sets the status in Weave Control; Yeh+Olive+Fields is the wider one.
BBN_THEORY = {'PRIMAT': dict(Yp=('abs', 0.00017), DH=('rel', 0.015), src='Y_p arXiv:1801.08023; D/H Paris/PRIMAT 2.439 ± 0.037 (via arXiv:2011.13874)'),
              'Yeh+Olive+Fields': dict(Yp=('abs', 0.00018), DH=('rel', 0.110/2.506), src='arXiv:2011.13874 (σ includes the ω_b error)')}

def bbn(omega_b=0.02237, dNeff=0.0, code='primat', theory=None):
    """Helium and deuterium from Hyperion's BBN wrapper, scored against every stored measurement.
    theory=None (default, backwards compatible): observational σ only. theory='PRIMAT' or 'Yeh+Olive+Fields': the sourced
    nuclear-rate theory σ is added in quadrature (PREREG_W5_BBN_THEORY)."""
    from . import bbn as B
    yp, dh = B.Yp(omega_b, dNeff, code), B.DH(omega_b, dNeff, code)
    model = dict(Yp=yp, DH=dh)
    def pl(q, m):
        v, s, _ = m
        if s in (None, 0): return None
        if theory:
            kind, t = BBN_THEORY[theory][q]; s = math.hypot(s, t if kind == 'abs' else t*model[q])
        return (model[q] - v)/s
    return dict(omega_b=omega_b, dNeff=dNeff, code=code, Yp=yp, DH=dh, theory_sigma=theory or 'observational only',
                pulls={**{f'Yp:{k}': pl('Yp', m) for k, m in DATA['Yp'].items()},
                       **{f'DH:{k}': pl('DH', m) for k, m in DATA['DH'].items()}})

def neutron_star(eos='SLy'):
    from . import ns
    e = ns.PPEOS(*ns.TABLE3[eos]); mm = ns.max_mass(e)
    return dict(eos=eos, M_max_Msun=float(mm[0]))

def jfactor(profile='Einasto', survey='HESS_IGS', rho_sun=0.4, r_sun=8.21, fast=True):
    """fast=True: J_route_A_fast (SPEED-Hyperion H1: 100x, matches route A to 4e-11); fast=False: the reference route A."""
    from . import jfactor as J
    h = HALOS[profile]
    shape = J.einasto(h['rs'], h['alpha']) if profile == 'Einasto' else (J.nfw(h['rs']) if profile == 'NFW' else J.burkert(h['r0']))
    rho = J.normalise(shape, rho_sun, r_sun); S = LINE_SURVEYS[survey]
    return dict(profile=profile, survey=survey, rho_sun=rho_sun, r_sun=r_sun,
                J_GeV2_cm5=(J.J_route_A_fast if fast else J.J_route_A)(rho, r_sun, S['psi_max_deg'], S['b_mask_deg']))

# H1b (20 Nov 2026): real column types and units in ECSV, so astropy gives numbers with units, not strings.
UNITS = {'omega_b': '', 'Yp': '', 'DH': '', 'M_max_Msun': 'solMass', 'rho_sun': 'GeV / cm3', 'r_sun': 'kpc',
         'J_GeV2_cm5': 'GeV2 / cm5', 'mass_GeV': 'GeV', 'sigma_fb': 'fb', 'lumi_fb': '1 / fb', 'sqrt_s_TeV': 'TeV',
         'ctau_cm': 'cm', 'tau_ns': 'ns', 'dm_MeV': 'MeV', 'wino_reach_GeV': 'GeV', 'Nstar': '', 'ns': '', 'r': '', 'alpha_s': ''}
def _ecsv_col(c, rows):
    vals = [r[c] for r in rows if c in r and r[c] is not None]
    if vals and all(isinstance(v, bool) for v in vals): dt = 'bool'
    elif vals and all(isinstance(v, int) and not isinstance(v, bool) for v in vals): dt = 'int64'
    elif vals and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals): dt = 'float64'
    else: dt = 'string'
    u = UNITS.get(c, '')
    return f'# - {{name: {c}, datatype: {dt}' + (f', unit: {u}' if u and dt in ('float64', 'int64') else '') + '}\n'

def sources():
    """Every stored measurement's source string (for the provenance block)."""
    return [f'{q}:{k} = {m[2]}' for q, d in DATA.items() for k, m in d.items()]

def export(rows, fmt='json', prov=None):
    """rows: list of flat dicts. fmt: json | csv | ecsv (CSV with an ECSV-style commented header listing the columns).
    prov: optional provenance dict (tools/provenance.py) embedded in the output (H1a)."""
    if fmt == 'json':
        return json.dumps(rows if prov is None else {'provenance': prov, 'rows': rows}, indent=1, default=float)
    if fmt == 'votable':   # H1b: IVOA VOTable via astropy (typed, with units); provenance goes in the table meta
        from astropy.table import Table
        from astropy.io.votable import from_table
        t = Table.read(export(rows, 'ecsv', prov), format='ascii.ecsv')
        if prov: t.meta['description'] = 'AEGIS ' + str(prov.get('toolkit')) + ' code ' + str(prov.get('version'))
        b = io.BytesIO(); from_table(t).to_xml(b); return b.getvalue().decode()
    cols = list(dict.fromkeys(k for r in rows for k in r))
    buf = io.StringIO()
    if fmt == 'ecsv':
        from tools.prov_block import ecsv_meta
        buf.write('# %ECSV 1.0\n# ---\n# delimiter: \',\'\n# datatype:\n' + ''.join(_ecsv_col(c, rows) for c in cols)
                  + (ecsv_meta(prov) if prov else '# meta: {source: Hyperion (AEGIS)}\n'))
    elif prov:
        from tools.prov_block import comment_lines
        buf.write(comment_lines(prov))
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in rows: w.writerow({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in r.items()})
    return buf.getvalue()
