# AEGIS-FP IXF2GXQYZRHI2X3L · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Landscape grid for the AEGIS web: the SERAPIS-E potential V(φ; C) from the unchanged pipeline (tools/serapis_calc/pipeline.build),
on φ from just above the minimum to the start of the 600-plateau region, for BHK tilt C/1.15e-6 from 0 to 3. Writes docs/web/landscape.json."""
import json, pathlib, sys, numpy as np
R = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R))
from tools.serapis_calc.pipeline import build
Cs = np.linspace(0.0, 3.0, 31)*1.15e-6; grid = []; phis = None
for C in Cs:
    m, V, dV, p0 = build('serapis_e', C)
    if phis is None: phis = np.linspace(0.02, p0*1.4, 64)
    grid.append([float(V(p)) for p in phis])
G = np.array(grid); out = dict(phi=[round(float(x), 4) for x in phis], C=[float(c) for c in Cs], V=[[round(float(v), 6) for v in r] for r in G],
                               note='V normalised to the plateau (V→1 as E→∞); C in units of 1.15e-6 along the second axis')
json.dump(out, open(R / 'docs/web/landscape.json', 'w')); print(G.shape, G.min(), G.max(), 'p0', p0)
