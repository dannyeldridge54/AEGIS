#!/usr/bin/env python3
"""D2099: one-loop top-dominated running of Higgs soft masses + mu from M_s (BIM boundary, tanb=1) to M_S; fixed-point tanb."""
import math, os, sys; import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import mh
k = 1/(16*math.pi**2); MS_str = 1e16; m32 = 128.5e3
gp, g, g3, ytSM, _ = mh.run(m32)                     # SM couplings at M_S (two-loop-corrected, D2088)
g1 = math.sqrt(5/3)*gp
def gauge_up(t):                                      # MSSM one-loop gauge from M_S up
    out = []
    for gi, b in ((g1, 33/5), (g, 1.0), (g3, -3.0)):
        out.append(1/math.sqrt(1/gi**2 - 2*k*b*t))
    return out
def rhs(t, y):                                        # t = ln(mu/M_S)
    yt, mHu, mHd, mQ, mU, mu = y; G1, G2, G3 = gauge_up(t); Xt = 2*yt*yt*(mHu + mQ + mU)
    return [k*yt*(6*yt*yt - 16/3*G3**2 - 3*G2**2 - 13/15*G1**2), k*3*Xt, 0.0, k*Xt, k*2*Xt, k*mu*(3*yt*yt - 3*G2**2 - 0.6*G1**2)]
L = math.log(MS_str/m32)
def down(yt_top):
    y0 = [yt_top, m32**2, m32**2, m32**2, m32**2, m32]
    return solve_ivp(rhs, (L, 0.0), y0, rtol=1e-10, atol=1e-6).y[:, -1]
def tanb_from(tb_in):
    yt_low = ytSM/(tb_in/math.sqrt(1 + tb_in*tb_in))
    f = lambda yh: down(yh)[0] - yt_low
    if f(6.0) < 0: return None, dict(note='y_t(M_S)=%.3f above the MSSM quasi-fixed point' % yt_low)
    ytop = brentq(f, 0.05, 6.0)
    yt, mHu, mHd, mQ, mU, mu = down(ytop); Bmu = 2*m32**2*(mu/m32)          # B = Bmu/mu constant = 2 m32
    s2b = 2*Bmu/(mHu + mHd + 2*mu*mu)
    if s2b >= 1: return 1.0, dict(mHu=mHu, mHd=mHd, mu=mu, s2b=s2b)
    tb = (1 + math.sqrt(1 - s2b*s2b))/s2b; return tb, dict(mHu=mHu, mHd=mHd, mu=mu, s2b=s2b, yt_top=ytop)
if __name__ == '__main__':
    tb = 1.9
    for it in range(60):
        new, info = tanb_from(tb)
        if new is None: print('  tanb_in %.3f: %s' % (tb, info['note'])); tb *= 1.05; continue
        if abs(new - tb) < 1e-6: break
        tb = 0.5*(tb + new)
    print('fixed point after %d iterations: tan beta = %.3f' % (it, new))
    print('  at M_S: m_Hu^2/m32^2 = %.3f  m_Hd^2/m32^2 = %.3f  mu/m32 = %.3f  sin2b = %.4f  y_t(M_s) = %.3f' % (info['mHu']/m32**2, info['mHd']/m32**2, info['mu']/m32, info['s2b'], info.get('yt_top', float('nan'))))
    v = 'CONSISTENT' if 1.81 <= new <= 2.02 else ('TENSION' if new > 1.3 else 'FAIL')
    print('VERDICT:', v)
