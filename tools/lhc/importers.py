# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 importers (R1): read what the experiments publish, so a user can work at their level.
  * pyhf / HistFactory JSON workspaces (ATLAS full likelihoods on HEPData) and their signal patchsets;
  * HEPData tables (YAML or the HEPData JSON 'values' form) -> plain x / y / error arrays.
Upper limits use pyhf's own CLs machinery (asymptotic q~mu by default), the same as the collaborations."""
import json, math
import numpy as np

def load_workspace(src):
    """src: path to a workspace .json, or an already-loaded dict."""
    import pyhf
    spec = json.load(open(src)) if isinstance(src, str) else src
    return pyhf.Workspace(spec)

def apply_patch(ws, patchset_src, name, verify=True):
    """Apply one named signal patch from a pyhf PatchSet (path or dict) to a background-only workspace.
    verify=True checks the workspace digest the PatchSet was published for (as pyhf does)."""
    import pyhf
    ps = pyhf.PatchSet(json.load(open(patchset_src)) if isinstance(patchset_src, str) else patchset_src)
    spec = dict(ws)
    if verify: return pyhf.Workspace(ps.apply(pyhf.Workspace(spec), name))
    patch = next(p for p in ps.patches if p.name == name)
    return pyhf.Workspace(patch.apply(pyhf.Workspace(spec)))

def cls(ws, mu=1.0, test_stat='qtilde'):
    """Observed and expected CLs at signal strength mu (asymptotics)."""
    import pyhf
    model, data = ws.model(), ws.data(ws.model())
    obs, exp = pyhf.infer.hypotest(mu, data, model, test_stat=test_stat, return_expected_set=True)
    return dict(mu=mu, CLs_obs=float(obs), CLs_exp=[float(e) for e in exp])

def upper_limit(ws, scan=None, level=0.05):
    """95% CL upper limit on mu (observed and expected band) by a CLs scan."""
    import pyhf
    model, data = ws.model(), ws.data(ws.model())
    scan = np.linspace(0.01, 10, 200) if scan is None else np.asarray(scan)
    obs, exp = pyhf.infer.intervals.upper_limits.upper_limit(data, model, scan, level=level)
    return dict(mu95_obs=float(obs), mu95_exp=[float(e) for e in exp])

def load_hepdata_table(src):
    """Read a HEPData table (YAML text/path, or a dict with independent_variables/dependent_variables).
    Returns dict(x_name, x, y: {name: dict(values, err_minus, err_plus, qualifiers)})."""
    if isinstance(src, str):
        import yaml
        txt = open(src).read() if not src.lstrip().startswith(('independent', '{', 'dependent')) else src
        d = yaml.safe_load(txt)
    else:
        d = src
    iv = d['independent_variables'][0]
    def xval(v): return v['value'] if 'value' in v else 0.5*(v['low'] + v['high'])
    out = dict(x_name=iv['header']['name'], x=[xval(v) for v in iv['values']], y={})
    for dv in d['dependent_variables']:
        vals, em, ep = [], [], []
        for v in dv['values']:
            vals.append(v['value'] if isinstance(v['value'], (int, float)) else float('nan'))
            e = (v.get('errors') or [{}])[0]
            if 'symerror' in e: s = float(str(e['symerror']).rstrip('%')); em.append(s); ep.append(s)
            elif 'asymerror' in e: em.append(abs(float(e['asymerror']['minus']))); ep.append(float(e['asymerror']['plus']))
            else: em.append(None); ep.append(None)
        out['y'][dv['header']['name']] = dict(values=vals, err_minus=em, err_plus=ep, qualifiers=dv.get('qualifiers', []))
    return out
