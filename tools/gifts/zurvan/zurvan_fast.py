"""Zurvan fast path (SPEED-Zurvan): exact derivative of the one-loop CW potential, no finite differences.
Sigma_x = (1/2 v_x) dV/dv_x, dV/dv = sum_i n_i/(64 pi^2) * 2 m_i^2 (ln(m_i^2/Q^2) - 1) dm_i^2/dv."""
import math
from zurvan import _m2

PI2 = math.pi ** 2

def _pair(LL, RR, LR, dLL, dRR, dLR):
    s = 0.5 * (LL + RR); r = math.sqrt(0.25 * (LL - RR) ** 2 + LR * LR)
    ds = 0.5 * (dLL + dRR); dr = (0.25 * (LL - RR) * (dLL - dRR) + LR * dLR) / r if r > 0 else 0.0
    return (s - r, ds - dr), (s + r, ds + dr)

def _F(m2, Q2): return m2 * (math.log(m2 / Q2) - 1) if m2 > 0 else 0.0

def sigmas_exact(p):
    vu, vd, Q2 = p['vu'], p['vd'], p['Q'] ** 2
    g, gp = p['g'], p['gp']; gz2 = (g * g + gp * gp) / 2; sw2 = gp * gp / (g * g + gp * gp)
    D = gz2 * (vd * vd - vu * vu); dDu, dDd = -2 * gz2 * vu, 2 * gz2 * vd; mu = p['mu']; out = {}
    def add(name, n, m2, dmu, dmd):
        F = _F(m2, Q2); out[name] = (n / (64 * PI2) * 2 * F * dmu / (2 * vu), n / (64 * PI2) * 2 * F * dmd / (2 * vd))
    # stops (fermion mass m_t = y_t vu)
    yt = p['yt']; mt = yt * vu
    cL, cR = 0.5 - 2 / 3 * sw2, 2 / 3 * sw2
    LL = _m2(p, 'mQ3') + mt * mt + cL * D; RR = _m2(p, 'mtR') + mt * mt + cR * D; LR = yt * (p['At'] * vu - mu * vd)
    (a, dau), (b, dbu) = _pair(LL, RR, LR, 2 * yt * yt * vu + cL * dDu, 2 * yt * yt * vu + cR * dDu, yt * p['At'])
    (_, dad), (_, dbd) = _pair(LL, RR, LR, cL * dDd, cR * dDd, -yt * mu)
    add('stop1', 6, a, dau, dad); add('stop2', 6, b, dbu, dbd); add('top', -12, mt * mt, 2 * yt * yt * vu, 0.0)
    # sbottoms (m_b = y_b vd)
    yb = p['yb']; mb = yb * vd; cL, cR = -0.5 + sw2 / 3, -sw2 / 3
    LL = _m2(p, 'mQ3') + mb * mb + cL * D; RR = _m2(p, 'mbR') + mb * mb + cR * D; LR = yb * (p['Ab'] * vd - mu * vu)
    (a, dau), (b, dbu) = _pair(LL, RR, LR, cL * dDu, cR * dDu, -yb * mu)
    (_, dad), (_, dbd) = _pair(LL, RR, LR, 2 * yb * yb * vd + cL * dDd, 2 * yb * yb * vd + cR * dDd, yb * p['Ab'])
    add('sbottom1', 6, a, dau, dad); add('sbottom2', 6, b, dbu, dbd); add('bottom', -12, mb * mb, 0.0, 2 * yb * yb * vd)
    # staus (m_tau = y_tau vd)
    yl = p['ytau']; ml = yl * vd; cL, cR = -0.5 + sw2, -sw2
    LL = _m2(p, 'mL3') + ml * ml + cL * D; RR = _m2(p, 'meR3') + ml * ml + cR * D; LR = yl * (p['Atau'] * vd - mu * vu)
    (a, dau), (b, dbu) = _pair(LL, RR, LR, cL * dDu, cR * dDu, -yl * mu)
    (_, dad), (_, dbd) = _pair(LL, RR, LR, 2 * yl * yl * vd + cL * dDd, 2 * yl * yl * vd + cR * dDd, yl * p['Atau'])
    add('stau1', 2, a, dau, dad); add('stau2', 2, b, dbu, dbd); add('tau', -4, ml * ml, 0.0, 2 * yl * yl * vd)
    return out
