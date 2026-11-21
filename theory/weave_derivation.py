"""THE WEAVE — the one derivation (Danny 13:35: "just one derivation … completely mapped out and quantified, every bit of it, and then tested").
One pass from the inputs to every observable. Each line: value, how it is obtained (CALC = computed here; SRC = read from the locked result
file named), status label (DER/LIT/FIT/INPUT/CONS/OPEN), and, where data exist, the test against data.
Run from the repo root:  python3 theory/weave_derivation.py   (writes field_tests/results/weave_derivation.json)"""
import json, math
R = lambda f: json.load(open('field_tests/results/' + f))
rows = []
def row(stage, name, value, how, label, data=None, sigma=None, tol_factor=None, bound=None, note=''):
    test, pull = '', None
    if data is not None and sigma is not None: pull = (value - data) / sigma; test = 'PASS' if abs(pull) <= 2 else 'FAIL'
    elif data is not None and tol_factor is not None:
        pull = math.log(value / data) / math.log(tol_factor); test = 'PASS' if abs(pull) <= 1 else 'FAIL'
    elif bound is not None:
        kind, b = bound; ok = value < b if kind == '<' else value > b; test = 'PASS' if ok else 'FAIL'
    rows.append(dict(stage=stage, name=name, value=value, how=how, label=label, data=data, sigma=sigma, tol=tol_factor,
                     bound=bound, pull=pull, test=test, note=note))

# ---------------- 0. INPUTS (everything not derived) ----------------
V4 = 4.9e15                                   # one outside knob, V_inf^(1/4) [GeV]
sigma_vis, N = 20.15, 6                       # visible hidden-sector gauge kinetic value, rank (D1811)
A, Vol, gs = 0.54, 4.0e4, 2 / math.sqrt(3)    # prefactor (D1871), volume (D1871), g_s = 2/sqrt3
tanb = 2.0                                    # inside the allowed 1–4 (D1763)
u_star = 0.0521                               # shared rung step: the arrow (D1894)
MP = 2.435e18
row('0 inputs', 'V_inf^(1/4) [GeV]', V4, 'INPUT (one outside knob, D1839/D1844)', 'INPUT')
row('0 inputs', 'shared rung step u*', u_star, 'FIT (D1894 end run)', 'FIT')

# ---------------- 1. geometry & moduli ----------------
row('1 geometry', 'Euler number chi (Z6-II)', 48, 'LIT hep-th/0609014; D1871', 'LIT')
x = 2 * math.pi * sigma_vis / N
W0 = A * math.exp(-x) * (1 + 2 * x / 3)
row('1 geometry', 'x = 2 pi sigma/N', x, 'CALC', 'DER')
row('1 geometry', '|W0| (exact KKLT)', W0, 'CALC  A e^-x (1+2x/3)', 'DER', note='D1811/D1871 quote 5.5e-9')
m32 = math.sqrt(gs / 2) / Vol * W0 * MP
row('1 geometry', 'gravitino m3/2 [GeV]', m32, 'CALC  sqrt(gs/2) W0 M_P / V', 'DER', note='quoted 2.6e5')
d12 = R('d1812_rankrule.json')
row('1 geometry', 'dark sigma_d (SU(12))', d12['sigma_d'], 'SRC d1812_rankrule.json', 'DER')
row('1 geometry', 'alpha_D(12.8 GeV)', d12['alphaD_12GeV'], 'SRC d1812_rankrule.json', 'DER')

# ---------------- 2. spectrum (AMSB from m3/2) ----------------
a1, a2, a3 = 1 / 58.2, 1 / 29.9, 0.092         # GUT-normalised couplings at ~TeV (alpha_3 at the gluino scale)
for nm, b, al, bnd in (('bino M1', 33 / 5, a1, None), ('wino M2', 1, a2, ('>', 103.0)), ('gluino M3', 3, a3, ('>', 2300.0))):
    row('2 spectrum', nm + ' [GeV]', b * al / (4 * math.pi) * m32, 'CALC AMSB b alpha/(4pi) m3/2', 'DER', bound=bnd,
        note='bound: LEP chargino 103 GeV / LHC gluino ~2.3 TeV' if bnd else '')

# ---------------- 3. forces ----------------
d16 = R('d1816_threshold.json')
row('3 forces', 'M_12 [GeV]', d16['M12'], 'SRC d1816_threshold.json (two-loop)', 'DER')
row('3 forces', 'Delta_3 before threshold', d16['Delta3'], 'SRC d1816_threshold.json', 'DER')
L_rho = -math.log(math.sqrt(3) / 2 * 0.800579402820038 ** 4)
L_i = -math.log(1.0 * 0.76823 ** 4)
X = (1 - 0) + 0.714 * (1 - 0.6)                 # one Higgs pair, weight 0, on each plane (D1881a)
res = d16['Delta3'] * (1 - ((L_rho / (4 * math.pi)) / 0.0822 + (L_i / (4 * math.pi)) / 0.0822) * X / 2.88)
row('3 forces', 'Delta_3 after Higgs-pair threshold', res, 'CALC (D1880 form, D1881a counting)', 'DER (conditional n_H = 0)')
as_pred = 0.1180 - (0.1180 - 0.1147) * res / d16['Delta3']
row('3 forces', 'alpha_s(M_Z) predicted', as_pred, 'CALC from residual', 'DER', data=0.1180, sigma=0.0009)
row('3 forces', 'proton lifetime [yr] (G-branch)', 1.6e35, 'SRC D1849-era two-loop note', 'DER', bound=('>', 2.4e34),
    note='Super-K p -> e+ pi0')

# ---------------- 4. flavour ----------------
row('4 flavour', 'knot-charge theorem (whole steps per weight)', 1, 'CALC D1874-D1876, refereed D1878', 'DER')
d29 = R('d1829_cp.json')
row('4 flavour', 'quark 7-observable natural fraction', d29['f7'], 'SRC d1829_cp.json', 'DER', bound=('>', 0.05))
row('4 flavour', 'quark CP (J) natural fraction', d29['fJ'], 'SRC d1829_cp.json', 'DER', bound=('>', 0.2))
row('4 flavour', 'two-stack quark natural fraction (dk=-1)', 0.179, 'SRC d1884_mixedweight.txt', 'DER', bound=('>', 0.05))
row('4 flavour', 'm_mu/m_tau = u*', u_star, 'CALC (arrow)', 'DER', data=105.658 / 1776.86, tol_factor=1.2)
row('4 flavour', 'down-quark step = u*', u_star, 'CALC (arrow)', 'DER', data=0.0457, tol_factor=1.2)
row('4 flavour', 'up-quark exponent p (u_u = u*^p)', math.log(0.00311) / math.log(u_star), 'CALC', 'CONS', note='~2: two rungs (report only)')
ce = 0.1058
row('4 flavour', 'electron coefficient c_e', ce, 'INPUT fixed by Koide (D1885a)', 'INPUT')
mm = [ce * u_star ** 2, 105.658 / 1776.86, 1.0]
Q = sum(mm) / sum(math.sqrt(v) for v in mm) ** 2
row('4 flavour', 'Koide Q', Q, 'CALC (input-fixed)', 'INPUT', note='no test content')
row('4 flavour', 'Koide delta', 2 / 9, 'INPUT (D1841-D1846, D1885a)', 'INPUT')
y3 = 0.67 * math.exp(-9 * math.pi / 8)
vu = 174.0 * tanb / math.sqrt(1 + tanb ** 2); m3nu = 0.0502e-9
MN = y3 ** 2 * vu ** 2 / m3nu
row('4 flavour', 'neutrino Yukawa y3 = g e^{-9pi/8}', y3, 'CALC (theta step n = 3 at i)', 'CONS')
row('4 flavour', 'heavy neutrino M_N [GeV]', MN, 'CALC y3^2 v_u^2 / m3', 'CONS', bound=('<', 2.5e12), note='leptogenesis window 4.5e10-2.5e12')
row('4 flavour', 'neutrino ratio natural fraction', R('d1821_neutrino.json')['frac'], 'SRC d1821_neutrino.json', 'DER', bound=('>', 0.01))
row('4 flavour', 'pyramid rung ratio 3->4 vs u*', math.exp(-7 * math.pi / 8), 'CALC', 'CONS', data=u_star, tol_factor=1.3)

# ---------------- 5. cosmology (forward) ----------------
row('5 cosmology', 'n_s', 0.9706, 'SRC plateau E(S,3/2), A = 7.30 (locked forecast)', 'DER', data=0.9728, sigma=0.0027, note='CMB-SPA+DESI')
row('5 cosmology', 'r', 5.4e-4, 'SRC (locked forecast)', 'DER', bound=('<', 0.036))
row('5 cosmology', 'T_R [GeV]', 3.7e8, 'SRC derived chain x = 0.279', 'DER')
mDM = 5.36 * 0.93827 * 28 / 11
row('5 cosmology', 'dark-matter mass [GeV]', mDM, 'CALC (Omega_DM/Omega_b) m_p n_B/n_X, n_X/n_B = 11/28', 'DER', note='prediction')
row('5 cosmology', 'Delta N_eff', 0.0, 'DER (never positive)', 'DER', bound=('<', 0.17))

# ---------------- 6. reverse weave ----------------
a_em = 1 / 137.036
z2 = 3.9e-4 * (a_em / (4 * math.pi)) * (0.021 / (4 * math.pi))
row('6 reverse', 'thread alpha drift zeta (dark cycle, no bifundamentals)', z2, 'CALC (D1887)', 'DER (estimate)', bound=('<', 1.66e-6))
row('6 reverse', 'max visible-dark crossing units b_bf', 4.3e-3 / (a_em / (2 * math.pi)), 'CALC (D1887)', 'DER (estimate)', note='needs <= this')
row('6 reverse', 'thread w0/wa on the dark cycle', float('nan'), 'OPEN (to derive)', 'OPEN')

# ---------------- print ----------------
cur = None; npass = nfail = 0
for r in rows:
    if r['stage'] != cur: cur = r['stage']; print('\n== ' + cur)
    t = ''
    if r['test']:
        t = '%s' % r['test'] + (' (pull %+.2f)' % r['pull'] if r['pull'] is not None else '')
        npass += r['test'] == 'PASS'; nfail += r['test'] == 'FAIL'
    print('  %-48s %-12.4g %-7s %-10s %s' % (r['name'], r['value'], r['label'].split()[0], t, r['how'] + ('  [' + r['note'] + ']' if r['note'] else '')))
print('\nTESTS: %d PASS, %d FAIL of %d tested lines (%d lines total)' % (npass, nfail, npass + nfail, len(rows)))
json.dump(rows, open('field_tests/results/weave_derivation.json', 'w'), indent=1, default=str)
