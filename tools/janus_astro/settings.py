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

def bbn(omega_b=0.02237, dNeff=0.0, code='primat'):
    """Helium and deuterium from Hyperion's BBN wrapper, scored against every stored measurement."""
    from . import bbn as B
    yp, dh = B.Yp(omega_b, dNeff, code), B.DH(omega_b, dNeff, code)
    return dict(omega_b=omega_b, dNeff=dNeff, code=code, Yp=yp, DH=dh,
                pulls={**{f'Yp:{k}': pull(yp, m) for k, m in DATA['Yp'].items()},
                       **{f'DH:{k}': pull(dh, m) for k, m in DATA['DH'].items()}})

def neutron_star(eos='SLy'):
    from . import ns
    e = ns.PPEOS(*ns.TABLE3[eos]); mm = ns.max_mass(e)
    return dict(eos=eos, M_max_Msun=float(mm[0]))

def jfactor(profile='Einasto', survey='HESS_IGS', rho_sun=0.4, r_sun=8.21):
    from . import jfactor as J
    h = HALOS[profile]
    shape = J.einasto(h['rs'], h['alpha']) if profile == 'Einasto' else (J.nfw(h['rs']) if profile == 'NFW' else J.burkert(h['r0']))
    rho = J.normalise(shape, rho_sun, r_sun); S = LINE_SURVEYS[survey]
    return dict(profile=profile, survey=survey, rho_sun=rho_sun, r_sun=r_sun,
                J_GeV2_cm5=J.J_route_A(rho, r_sun, S['psi_max_deg'], S['b_mask_deg']))

def sources():
    """Every stored measurement's source string (for the provenance block)."""
    return [f'{q}:{k} = {m[2]}' for q, d in DATA.items() for k, m in d.items()]

def export(rows, fmt='json', prov=None):
    """rows: list of flat dicts. fmt: json | csv | ecsv (CSV with an ECSV-style commented header listing the columns).
    prov: optional provenance dict (tools/provenance.py) embedded in the output (H1a)."""
    if fmt == 'json':
        return json.dumps(rows if prov is None else {'provenance': prov, 'rows': rows}, indent=1, default=float)
    cols = list(dict.fromkeys(k for r in rows for k in r))
    buf = io.StringIO()
    if fmt == 'ecsv':
        from tools.prov_block import ecsv_meta
        buf.write('# %ECSV 1.0\n# ---\n# delimiter: \',\'\n# datatype:\n' + ''.join(f'# - {{name: {c}, datatype: string}}\n' for c in cols)
                  + (ecsv_meta(prov) if prov else '# meta: {source: Hyperion (AEGIS)}\n'))
    elif prov:
        from tools.prov_block import comment_lines
        buf.write(comment_lines(prov))
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in rows: w.writerow({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in r.items()})
    return buf.getvalue()
