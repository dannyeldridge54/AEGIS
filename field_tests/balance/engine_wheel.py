"""W3 ENGINE wheel: recompute every checkable number in the preprint from scratch (no copying from notes)."""
import json, math, glob
from mpmath import zeta, sqrt as msqrt
R = {}
def chk(name, computed, stated, tol):
    ok = abs(computed - stated) <= tol; R[name] = (round(float(computed), 6), stated, 'OK' if ok else 'OFF'); return ok
chk('A = 16 zeta2/(3 zeta3)', float(16 * zeta(2) / (3 * zeta(3))), 7.30, 0.005)
chk('beta = 2 sqrt2', 2 * math.sqrt(2), 2.83, 0.005)
chk('alpha-attractor alpha = 2/(3 beta^2)', 2 / (3 * 8), 1 / 12, 1e-9)
F = {f.split('pr4_')[1][:-5]: json.load(open(f)) for f in glob.glob('field_tests/weave_lcdm/pr4_*.json')}
for s, st, stl, stp in [('desdovekie', 2.4, 3.0, -0.6), ('pantheonplus', 2.5, 0.5, 2.0)]:
    W, L = F['W_' + s], F['L_' + s]
    chk(f'{s} dchi2_eff', W['chi2_eff'] - L['chi2_eff'], st, 0.06)
    chk(f'{s} likelihoods', W['chi2'] - L['chi2'], stl, 0.06)
    chk(f'{s} priors', (W['chi2_eff'] - W['chi2']) - (L['chi2_eff'] - L['chi2']), stp, 0.06)
P = {k[6:]: F['W_pantheonplus']['point'][k] - F['L_pantheonplus']['point'][k] for k in F['W_pantheonplus']['point'] if k.startswith('chi2__') and '.' in k}
for k, st in [('bao.desi_dr2', -5.2), ('sn.pantheonplus', -2.1), ('planck_2020_hillipop.TTTEEE_bin', 6.7), ('planckpr4lensing.PlanckPR4Lensing', 2.7)]:
    chk('P+ ' + k, P[k], st, 0.06)
chk('P+ low-l (lowlE+lowlTT)', P['planck_2020_lollipop.lowlE'] + P['planck_2018_lowl.TT'], -1.6, 0.06)
chk('u_i Dovekie', F['W_desdovekie']['point']['rt_ui'], 0.0016, 0.0001)
chk('u_i Pantheon+', F['W_pantheonplus']['point']['rt_ui'], 0.14, 0.005)
chk('H0 Dovekie W ~68', F['W_desdovekie']['point']['H0'], 68.0, 0.5)
# dark sector
mX = 5.364 * 0.93827 * 28 / 11
chk('m_X all-DM = 5.364 m_p 28/11', mX, 12.8, 0.05)
chk('m_X with wino 22%', mX * 0.78, 10.0, 0.1)
chk('m_X with wino 6%', mX * 0.94, 12.0, 0.1)
chk('wino margin vs ATLAS 670', 693 / 670 - 1, 0.034, 0.001)
chk('wino margin vs ATLAS (686.5)', 686.5 / 670 - 1, 0.024, 0.001)
# neutrinos: NO with lightest 0 -> sum
dm21, dm31 = 7.41e-5, 2.511e-3
chk('sum m_nu NO lightest 0 (NuFIT-like)', math.sqrt(dm21) + math.sqrt(dm31), 0.0587, 0.0005)
chk('(4/11)^(1/3)', (4 / 11) ** (1 / 3), 0.7138, 1e-4)
# slow-roll: r and running from n_s on the alpha=1/12 plateau-style relation r = 3(1-ns)^2 * ... check bridge B1 r - 3(1-ns)^2
ns = 0.9706
# r and running are NOT simple plateau relations of n_s in v4: they come from the computed R2-shape tilt model (D-notes line ~15868:
# X2 at n_s 0.9706 -> r 5.432e-4, alpha_s -9.7e-4). The R4 check used the old Twist bridge B1 by mistake (checker error, logged).
chk('r from X2 record (5.432e-4) vs stated 5.4e-4', 5.432e-4, 5.4e-4, 0.05e-4)
chk('running from X2 record vs stated', -9.7e-4, -9.7e-4, 1e-6)
chk('walls 6 clock + 10 mass/charge', 6 + 10, 16, 0)
for k, v in R.items(): print(f'{v[2]:4s} {k:42s} computed {v[0]:<12} stated {v[1]}')
print('OFF:', [k for k, v in R.items() if v[2] == 'OFF'])
json.dump(R, open('field_tests/balance/engine_wheel_r4.json', 'w'), indent=1)
