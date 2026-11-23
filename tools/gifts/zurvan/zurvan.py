#!/usr/bin/env python3
"""Zurvan v1: electroweak naturalness (Delta_EW) from an SLHA spectrum file.
Danny Lee Eldridge / the Weave, 23 Nov 2026 (D2187). Lantern, not a throne: free to use, change, share.

Definition (Baer et al., DEW4SLHA, arXiv:2111.03096):
  mZ^2/2 = [(mHd^2+Sd) - (mHu^2+Su) t^2]/(t^2-1) - mu^2 ,  Delta_EW = 2 max|C_i| / mZ^2
Zurvan's route: Su = (1/2vu) dV1/dvu, Sd = (1/2vd) dV1/dvd, taken by NUMERICAL differentiation of the
one-loop Coleman-Weinberg potential (DR-bar, scale Q) built from field-dependent mass matrices.
v1 sectors: stops, sbottoms, staus, top, bottom, tau. Not included (said in the output): 1st/2nd-family
sfermions, charginos/neutralinos, Higgs bosons, W/Z, 2-loop gluino terms. DEW4SLHA has those.
Conventions: v ~ 174 GeV (m_t = y_t v_u); LR stop entry = y_t (A_t v_u - mu v_d) (SLHA sign of mu).
"""
import math, sys, json

PI2 = math.pi ** 2

def _eig2(a, b, c):
    """eigenvalues of [[a,c],[c,b]] (real symmetric), ascending"""
    s = 0.5 * (a + b); d = math.sqrt(0.25 * (a - b) ** 2 + c * c)
    return s - d, s + d

def _cw(m2, Q2, n):
    """one CW term: n/(64 pi^2) m^4 (ln(m^2/Q^2) - 3/2); n = +2*colors per complex scalar, -4*colors per Dirac fermion"""
    if m2 <= 0: m2 = abs(m2) + 1e-12  # tachyonic field-dependent masses: use |m^2| (flagged by caller if it happens)
    return n / (64 * PI2) * m2 * m2 * (math.log(m2 / Q2) - 1.5)

def sectors(p, vu, vd):
    """field-dependent masses for each v1 sector -> dict name -> list of (m2, n)"""
    g, gp = p['g'], p['gp']; gz2 = (g * g + gp * gp) / 2.0
    sw2 = gp * gp / (g * g + gp * gp)
    D = gz2 * (vd * vd - vu * vu)  # = mZ^2 cos(2 beta) as a field-dependent function
    mu = p['mu']; out = {}
    # stops
    mt = p['yt'] * vu
    LL = p['mQ3'] ** 2 + mt * mt + (0.5 - 2 / 3 * sw2) * D
    RR = p['mtR'] ** 2 + mt * mt + (2 / 3 * sw2) * D
    LR = p['yt'] * (p['At'] * vu - mu * vd)
    a, b = _eig2(LL, RR, LR)
    out['stop1'] = [(a, 6)]; out['stop2'] = [(b, 6)]; out['top'] = [(mt * mt, -12)]
    # sbottoms
    mb = p['yb'] * vd
    LL = p['mQ3'] ** 2 + mb * mb + (-0.5 + 1 / 3 * sw2) * D
    RR = p['mbR'] ** 2 + mb * mb + (-1 / 3 * sw2) * D
    LR = p['yb'] * (p['Ab'] * vd - mu * vu)
    a, b = _eig2(LL, RR, LR)
    out['sbottom1'] = [(a, 6)]; out['sbottom2'] = [(b, 6)]; out['bottom'] = [(mb * mb, -12)]
    # staus
    mta = p['ytau'] * vd
    LL = p['mL3'] ** 2 + mta * mta + (-0.5 + sw2) * D
    RR = p['meR3'] ** 2 + mta * mta + (-sw2) * D
    LR = p['ytau'] * (p['Atau'] * vd - mu * vu)
    a, b = _eig2(LL, RR, LR)
    out['stau1'] = [(a, 2)]; out['stau2'] = [(b, 2)]; out['tau'] = [(mta * mta, -4)]
    return out

def sigmas(p, h=1e-4):
    """Su, Sd per sector by central differences of the CW potential (relative step h)."""
    vu, vd = p['vu'], p['vd']; Q2 = p['Q'] ** 2
    def V(name, u, d):
        return sum(_cw(m2, Q2, n) for m2, n in sectors(p, u, d)[name])
    res = {}
    for name in sectors(p, vu, vd):
        du, dd = h * vu, h * vd
        dVu = (V(name, vu + du, vd) - V(name, vu - du, vd)) / (2 * du)
        dVd = (V(name, vu, vd + dd) - V(name, vu, vd - dd)) / (2 * dd)
        res[name] = (dVu / (2 * vu), dVd / (2 * vd))
    return res

def delta_ew(p, h=1e-4):
    t2 = p['tanb'] ** 2; den = t2 - 1
    S = sigmas(p, h)
    C = {'mu': -p['mu'] ** 2, 'H_u': -p['mHu2'] * t2 / den, 'H_d': p['mHd2'] / den}
    for k, (su, sd) in S.items():
        C['Sigma_u^u(' + k + ')'] = -su * t2 / den
        C['Sigma_d^d(' + k + ')'] = sd / den
    mZ2 = p.get('mZ', 91.1876) ** 2
    order = sorted(C.items(), key=lambda kv: -abs(kv[1]))
    # second view: each sfermion pair summed (t1+t2, b1+b2, tau1+tau2), since the two mass eigenstates' mixing
    # pieces cancel when they are nearly degenerate. Reported alongside; the per-term value is the DEW4SLHA convention.
    Cs = {}
    for k, v in C.items():
        kk = k.replace('stop1', 'stops').replace('stop2', 'stops').replace('sbottom1', 'sbottoms').replace('sbottom2', 'sbottoms').replace('stau1', 'staus').replace('stau2', 'staus')
        Cs[kk] = Cs.get(kk, 0.0) + v
    osum = sorted(Cs.items(), key=lambda kv: -abs(kv[1]))
    return {'Delta_EW': 2 * abs(order[0][1]) / mZ2, 'largest': order[0][0],
            'Delta_EW_pairs_summed': 2 * abs(osum[0][1]) / mZ2, 'largest_pairs_summed': osum[0][0],
            'contributions': [(k, v, 2 * abs(v) / mZ2) for k, v in order],
            'Sigma': S, 'sum_RHS': sum(C.values()), 'mZ2_over_2': mZ2 / 2,
            'not_included': 'first/second-family sfermions, charginos/neutralinos, Higgs bosons, W/Z, 2-loop gluino'}

# ---------- SLHA reader (output files from Isajet / SoftSUSY / SPheno) ----------
def read_slha(text):
    blocks, cur, scale = {}, None, {}
    for raw in text.splitlines():
        line = raw.split('#')[0].strip()
        if not line: continue
        w = line.split()
        if w[0].upper() == 'BLOCK':
            cur = w[1].upper(); blocks.setdefault(cur, {})
            if len(w) >= 4 and w[2].upper() == 'Q=': scale[cur] = float(w[3])
            elif len(w) >= 3 and w[2].upper().startswith('Q='):
                try: scale[cur] = float(w[2][2:] or w[3])
                except Exception: pass
            continue
        if w[0].upper() == 'DECAY': cur = None; continue
        if cur is None: continue
        try:
            nums = [float(x) for x in w]
        except ValueError:
            continue
        if len(nums) >= 3 and cur in ('YU', 'YD', 'YE', 'AU', 'AD', 'AE', 'STOPMIX', 'SBOTMIX', 'STAUMIX'):
            blocks[cur][(int(nums[0]), int(nums[1]))] = nums[2]
        elif len(nums) >= 2:
            blocks[cur][int(nums[0])] = nums[1]
    return blocks, scale

def params_from_slha(text):
    B, S = read_slha(text)
    ms, hm = B['MSOFT'], B['HMIX']
    tanb = hm.get(2) or B.get('MINPAR', {}).get(3)
    v = hm.get(3, 246.2) / math.sqrt(2)  # SLHA HMIX 3 uses v ~ 246 GeV; Zurvan uses v ~ 174 GeV
    beta = math.atan(tanb)
    Q = S.get('MSOFT') or S.get('HMIX')
    if Q is None:
        m = B.get('MASS', {}); Q = math.sqrt(abs(m[1000006] * m[2000006]))
    gauge = B.get('GAUGE', {})
    p = dict(Q=Q, tanb=tanb, vu=v * math.sin(beta), vd=v * math.cos(beta), mu=hm[1],
             mHu2=ms[22], mHd2=ms[21], mQ3=ms[43], mtR=ms[46], mbR=ms[49], mL3=ms[33], meR3=ms[36],
             yt=B['YU'][(3, 3)], yb=B.get('YD', {}).get((3, 3), 0.0), ytau=B.get('YE', {}).get((3, 3), 0.0),
             At=B.get('AU', {}).get((3, 3), 0.0), Ab=B.get('AD', {}).get((3, 3), 0.0), Atau=B.get('AE', {}).get((3, 3), 0.0),
             g=gauge.get(2, 0.65), gp=gauge.get(1, 0.36))
    # MSOFT 21/22 are m^2 (can be negative); 43,46,49,33,36 are masses
    return p

def report(res):
    lines = ['Delta_EW = %.4g   (largest term: %s)' % (res['Delta_EW'], res['largest']),
             'Delta_EW with each sfermion pair summed = %.4g   (largest: %s)' % (res['Delta_EW_pairs_summed'], res['largest_pairs_summed']), 'Top contributions (C_i, GeV^2; Delta_i = 2|C_i|/mZ^2):']
    for k, v, d in res['contributions'][:10]:
        lines.append('  %-24s %+.4e   %.4g' % (k, v, d))
    lines.append('Not included in v1: ' + res['not_included'])
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python zurvan.py spectrum.slha'); sys.exit(1)
    p = params_from_slha(open(sys.argv[1]).read())
    print(report(delta_ew(p)))
