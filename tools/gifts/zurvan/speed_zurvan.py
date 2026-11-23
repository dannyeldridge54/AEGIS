"""SPEED-Zurvan harness (Z1 + diagnostics; committed per DEV-4)."""
import time, json, glob, mpmath as mp
from zurvan import params_from_slha, sigmas, delta_ew
from zurvan_fast import sigmas_exact
R = {}; w = 0; tr = tf = 0
for f in sorted(glob.glob('example_*.slha')):
    p = params_from_slha(open(f).read()); S = sigmas(p); E = sigmas_exact(p)
    for k in S:
        for i in (0, 1):
            if abs(S[k][i]) > 1e-6: w = max(w, abs(S[k][i] - E[k][i]) / abs(S[k][i]))
    a = time.perf_counter(); [sigmas(p) for _ in range(200)]; tr += time.perf_counter() - a
    a = time.perf_counter(); [sigmas_exact(p) for _ in range(200)]; tf += time.perf_counter() - a
R['Z1'] = dict(max_rel_sigma=w, t_ref_600=tr, t_fast_600=tf, speedup=tr / tf, pass_=bool(w < 1e-6))
# tachyonic case (DEV-3): exact and fd both warn
p = params_from_slha(open('example_P1_natural.slha').read()); p['mtR_2'] = -(200.0 ** 2)
e1 = delta_ew(p, method='exact'); e2 = delta_ew(p, method='fd')
R['tachyon_case'] = dict(exact_warns=any('tachyonic' in x for x in e1['warnings']), fd_warns=any('tachyonic' in x for x in e2['warnings']))
# 50-digit check of one P3 term
mp.mp.dps = 50
p = params_from_slha(open('example_P3_weave_minisplit.slha').read()); E = sigmas_exact(p)
def V(vu, vd):
    g, gp = mp.mpf(p['g']), mp.mpf(p['gp']); gz2 = (g * g + gp * gp) / 2; sw2 = gp * gp / (g * g + gp * gp); D = gz2 * (vd * vd - vu * vu)
    yb = mp.mpf(p['yb']); mb = yb * vd; cL, cR = -mp.mpf(1) / 2 + sw2 / 3, -sw2 / 3
    m2 = lambda k: mp.mpf(p[k + '_2']) if (k + '_2') in p else mp.mpf(p[k]) ** 2
    LL = m2('mQ3') + mb * mb + cL * D; RR = m2('mbR') + mb * mb + cR * D; LR = yb * (mp.mpf(p['Ab']) * vd - mp.mpf(p['mu']) * vu)
    s = (LL + RR) / 2; r = mp.sqrt((LL - RR) ** 2 / 4 + LR * LR); m1 = s - r
    return 6 / (64 * mp.pi ** 2) * m1 * m1 * (mp.log(m1 / mp.mpf(p['Q']) ** 2) - mp.mpf(3) / 2)
vu, vd = mp.mpf(p['vu']), mp.mpf(p['vd']); h = mp.mpf('1e-15') * vd
num = (V(vu, vd + h) - V(vu, vd - h)) / (2 * h) / (2 * vd)
R['mp50_Sd_sbottom1_P3'] = dict(exact=E['sbottom1'][1], mp50=float(num), rel=float(abs(num - E['sbottom1'][1]) / abs(num)), fd_float64=sigmas(p)['sbottom1'][1])
json.dump(R, open('/home/claude/aegis/field_tests/results/speed_zurvan.json', 'w'), indent=1); print(json.dumps(R, indent=1))
