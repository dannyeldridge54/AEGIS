#!/usr/bin/env python3
"""D2125 T2: seesaw lower bound m_nu >= m_D^2/M_s with PS y_nu(M_s)=y_t(M_s)."""
import math, json, numpy as np
from scipy.integrate import solve_ivp
MZ = 91.1876; aem, s2, as_ = 127.951, 0.23122, 0.1180; a0 = np.array([0.6*(1 - s2)*aem, s2*aem, 1/as_])
bSM = np.array([41/10, -19/6, -7]); BSM = np.array([[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]]); aSM = np.array([17/10, 3/2, 2])
bMS = np.array([33/5, 1, -3]); BMS = np.array([[199/25, 27/5, 88/5], [9/5, 25, 24], [11/5, 9, 14]]); aMS = np.array([26/5, 6, 4])
def rge(t, y, b, B, a, susy):
    ai = y[:3]; yt = y[3]; g2 = 4*math.pi/ai
    d = -b/(2*math.pi) - (B @ g2 - a*yt**2)/(32*math.pi**3)
    dyt = yt/(16*math.pi**2)*((6*yt**2 - 16/3*g2[2] - 3*g2[1] - 13/15*g2[0]) if susy else (4.5*yt**2 - 8*g2[2] - 9/4*g2[1] - 17/20*g2[0]))
    return np.concatenate([d, [dyt]])
def yt_at(Ms, tb):
    t1 = math.log(1e3/MZ); s = solve_ivp(rge, [0, t1], np.concatenate([a0, [0.97]]), args=(bSM, BSM, aSM, False), rtol=1e-10)
    y = s.y[:, -1].copy(); y[:3] -= np.array([0, 2, 3])/(12*math.pi); sb = tb/math.sqrt(1 + tb**2); y[3] /= sb
    s2_ = solve_ivp(rge, [t1, math.log(Ms/MZ)], y, args=(bMS, BMS, aMS, True), rtol=1e-10)
    return s2_.y[3, -1], sb
out = {}
for Ms in (7.6e12, 3.5e13, 4.6e13):
    for tb in (2, 10, 50):
        yt, sb = yt_at(Ms, tb); mD = yt*246*sb/math.sqrt(2); mnu = mD**2/Ms*1e9
        out['Ms=%.2g,tb=%d' % (Ms, tb)] = dict(yt_Ms=yt, mD_GeV=mD, mnu_min_eV=mnu, exceeds_0p12=mnu > 0.12, exceeds_KATRIN=mnu > 0.45)
allx = all(v['exceeds_0p12'] for v in out.values()); anyx = any(v['exceeds_0p12'] for v in out.values())
out['SEESAW'] = 'FAIL' if allx else ('TENSION' if anyx else 'OK')
print(json.dumps(out, indent=1))
