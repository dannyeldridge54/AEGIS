# AEGIS-FP G3YFMVAGNNBFLPMG · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Knob grid for AEGIS Studio: SERAPIS-E n_s, r, α_s from Janus (core.Model + spectra3, validated D1218/D1228) on C/1.15e-6 ∈ [0, 3] and N* ∈ [45, 65],
potential from the unchanged pipeline.build. The app interpolates this grid for instant knob response and can recompute any point live."""
import json, pathlib, sys, numpy as np, warnings; warnings.filterwarnings('ignore')
R = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R))
from tools.serapis_calc.pipeline import build
from tools.janus_calc.core import Model, spectra3
Cf = np.linspace(0.0, 3.0, 13); Ns = np.linspace(45, 65, 21); ns = []; rr = []; al = []; ok = []
for c in Cf:
    m, V, dV, p0 = build('serapis_e', max(c, 1e-6)*1.15e-6)
    try:
        M = Model(V, dV, p0, Nmax=4000); row = [spectra3(M, N) for N in Ns]
        ns.append([x['ns'] for x in row]); rr.append([x['r'] for x in row]); al.append([x['alpha_s'] for x in row]); ok.append(True)
    except Exception as e:
        ns.append([None]*len(Ns)); rr.append([None]*len(Ns)); al.append([None]*len(Ns)); ok.append(str(e))
    print(c, ok[-1], ns[-1][10] if ok[-1] is True else '', flush=True)
json.dump(dict(Cfac=Cf.tolist(), Nstar=Ns.tolist(), ns=ns, r=rr, alpha_s=al, ok=ok, source='Janus core.spectra3 on SERAPIS-E (pipeline.build)'), open(R / 'docs/web/knob_grid.json', 'w'))
