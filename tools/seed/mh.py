#!/usr/bin/env python3
"""D2088: SM one-loop running of lambda from m_t (Buttazzo boundary) to M_S; match to high-scale SUSY boundary with stop threshold."""
import math; import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MT = 173.1; Y0 = [0.3583, 0.6478, 1.1666, 0.9369, 0.12604]; k = 1/(16*math.pi**2)
def beta(t, y):
    gp, g, g3, yt, l = y
    bgp = k*41/6*gp**3; bg = -k*19/6*g**3; bg3 = -k*7*g3**3
    byt = k*yt*(9/2*yt**2 - 8*g3**2 - 9/4*g**2 - 17/12*gp**2)
    bl = k*(24*l**2 - 6*yt**4 + 3/8*(2*g**4 + (g**2 + gp**2)**2) + l*(12*yt**2 - 9*g**2 - 3*gp**2))
    return [bgp, bg, bg3, byt, bl]
def run(mu, l0=Y0[4]):
    y0 = Y0[:4] + [l0]; return solve_ivp(beta, (math.log(MT), math.log(mu)), y0, rtol=1e-10, atol=1e-12).y[:, -1]
def lam_bdy(y, tb, c):
    gp, g, g3, yt, l = y; c2b = (1 - tb*tb)/(1 + tb*tb); xt = -c/tb
    return (g*g + gp*gp)/4*c2b**2 + 3*yt**4/(8*math.pi**2)*(xt**2 - xt**4/12)
if __name__ == '__main__':
    cross = math.exp(brentq(lambda t: run(math.exp(t))[4], math.log(1e6), math.log(1e15)))
    print('CONTROL lambda=0 crossing: %.2e GeV' % cross, 'PASS' if 3e8 <= cross <= 3e11 else 'FAIL')
    feas = {124e3: 1.5, 145e3: 3.0, 156e3: 4.0}; ok = 0
    for MS, tbf in feas.items():
        for c in (1 - 1/21.10, 1.0, 1 + 1/21.10):
            band = []
            for dl in (-0.0030, 0.0, 0.0030):
                y = run(MS, Y0[4] + dl); f = lambda tb: lam_bdy(y, tb, c) - y[4]
                try: band.append(brentq(f, 1.0001, 60))
                except ValueError: band.append(None)
            lo, mid, hi = band; tbs = [b for b in band if b]
            inside = bool(tbs) and min(tbs) <= tbf <= max(tbs); ok += inside
            print('M_S %3.0f TeV c %.3f: tanb(m_h=125.1) = %s  [band %s-%s]  D2087 tanb %.1f -> %s' % (MS/1e3, c, '%.2f' % mid if mid else 'none',
                  '%.2f' % min(tbs) if tbs else '-', '%.2f' % max(tbs) if tbs else '-', tbf, 'INSIDE' if inside else 'outside'))
    y = run(140e3); print('tanb=1 boundary at 140 TeV: lambda_bdy %.4f vs lambda_run %.4f' % (lam_bdy(y, 1.0, 1.0), y[4]))
    print('VERDICT:', 'CONSISTENT' if ok else 'TENSION')
