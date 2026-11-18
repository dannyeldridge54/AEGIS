# AEGIS-FP VOYSQLA3CYOGXJIZ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L3: DESI DR2 BAO likelihood (Table IV of arXiv:2503.14738, data/desi/dr2_bao_table4.txt)."""
import math, numpy as np
from .background import C_KMS
def load(path=None):
    import os, sys
    if path is None:
        base = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, 'data', 'desi', 'dr2_bao_table4.txt')
    rows = []
    for l in open(path):
        if l.startswith('#') or not l.strip(): continue
        c = l.split(); rows.append((c[0], *[float(x) for x in c[1:]]))
    return rows
def chi2(cosmo, rd, rows=None):
    rows = rows or load(); X = 0.0
    for name, z, dv, sdv, dm, sdm, dh, sdh, r in rows:
        DM = cosmo.DM(z); DH = C_KMS/cosmo.H(z)
        if math.isnan(dm):
            DV = (z*DM*DM*DH)**(1/3); X += ((DV/rd - dv)/sdv)**2
        else:
            d = np.array([DM/rd - dm, DH/rd - dh]); C = np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])
            X += float(d @ np.linalg.solve(C, d))
    return X
