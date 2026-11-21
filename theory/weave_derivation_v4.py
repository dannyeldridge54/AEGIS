"""v4 after D1922/D1923 (quark lines PHENOMENOLOGICAL: no modular-tau home in Z6-II; FN spurions need two sizes). v3 after D1894b (variable error: 0.0457 was |eps| not u; arrow withdrawn). v2 after the independent referee (D1897/D1898). THE WEAVE — the one derivation (Danny 13:35: "just one derivation … completely mapped out and quantified, every bit of it, and then tested").
One pass from the inputs to every observable. Each line: value, how it is obtained (CALC = computed here; SRC = read from the locked result
file named), status label (DER/LIT/FIT/INPUT/CONS/OPEN), and, where data exist, the test against data.
Run from the repo root:  python3 theory/weave_derivation.py   (writes field_tests/results/weave_derivation_v4.json)"""
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
A, Vol, gs = 0.54, 4.0e4, 2 / math.sqrt(3)    # prefactor (D1871), volume (D1871), g_s = 2/sqrt3  [REFEREE D1897: g_s > 1 is OUTSIDE perturbative control]
tanb = 2.0                                    # inside the allowed 1–4 (D1763)
u_star = 0.0259                               # D1894b: the true down-quark step |u_d| (|eps| = 0.0457); arrow withdrawn
MP = 2.435e18
row('0 inputs', 'V_inf^(1/4) [GeV]', V4, 'INPUT (one outside knob, D1839/D1844)', 'INPUT')
row('0 inputs', 'down-quark step |u_d| (TRUST; no geometric home, D1922/D1923)', u_star, 'FIT D1828 (|eps|=0.0457)', 'INPUT')
row('0 inputs', 'string coupling g_s', gs, 'INPUT; > 1 = outside perturbative control (D1897)', 'INPUT')

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
a1, a2, a3 = 1 / 58.2, 1 / 29.9, 0.080         # alpha_3 at ~5.6 TeV (D1897); wino/bino ignore the O(1) higgsino threshold (tanb, mu ~ m3/2)
for nm, b, al, bnd in (('bino M1', 33 / 5, a1, None), ('wino M2', 1, a2, ('>', 660.0)), ('gluino M3', 3, a3, ('>', 2300.0))):
    row('2 spectrum', nm + ' [GeV]', b * al / (4 * math.pi) * m32, 'CALC AMSB b alpha/(4pi) m3/2', 'DER', bound=bnd,
        note='bound: LHC disappearing-track wino ~660 GeV (marginal; +-O(1) higgsino threshold) / LHC gluino ~2.3 TeV' if bnd else '')

# ---------------- 3. forces ----------------
d16 = R('d1816_threshold.json')
row('3 forces', 'M_12 [GeV]', d16['M12'], 'SRC d1816_threshold.json (two-loop)', 'DER')
row('3 forces', 'Delta_3 before threshold', d16['Delta3'], 'SRC d1816_threshold.json', 'DER')
L_rho = -math.log(math.sqrt(3) / 2 * 0.800579402820038 ** 4)
L_i = -math.log(1.0 * 0.76823 ** 4)
X = (-1 + 3) + 0.714 * (-1 - 0.6)               # one Higgs pair weight 0 PLUS the gauge term -C(G) = (0,-2,-3) per plane (D1881b)
res = d16['Delta3'] * (1 - ((L_rho / (4 * math.pi)) / 0.0822 + (L_i / (4 * math.pi)) / 0.0822) * X / 2.88)
row('3 forces', 'Delta_3 after Higgs pair + gauge term', res, 'CALC (D1881b; matter weights not counted, U-only assumed)', 'CONS', bound=('>', -0.05), note='closure NOT established')
as_pred = 0.1180 - (0.1180 - 0.1147) * res / d16['Delta3']
row('3 forces', 'alpha_s(M_Z), no threshold', 0.1147, 'SRC D1808/D1816 two-loop', 'DER', data=0.1180, sigma=0.0009)
row('3 forces', 'alpha_s(M_Z), Higgs pair + gauge (post-selected)', as_pred, 'CALC from residual', 'CONS', note='content selected from a 324-option scan')
row('3 forces', 'proton lifetime [yr] (G-branch)', 1.6e35, 'QUOTED (no result file)', 'DER', bound=('>', 2.4e34),
    note='Super-K p -> e+ pi0')

# ---------------- 4. flavour ----------------
row('4 flavour', 'knot-charge theorem: integer charge gaps per weight', 1, 'D1874-D1876 (known: Novichkov-Penedo-Petcov 2102.07488)', 'LIT', note='structural; value column not a number')
d29 = R('d1829_cp.json')
row('4 flavour', 'quark 7-observable natural fraction [PHENOMENOLOGICAL, D1923]', d29['f7'], 'SRC d1829_cp.json', 'PHEN', bound=('>', 0.05))
row('4 flavour', 'quark CP (J) natural fraction [PHENOMENOLOGICAL]', d29['fJ'], 'SRC d1829_cp.json', 'PHEN', bound=('>', 0.2))
import re
f2 = float(re.search(r'dk=-1.*?f7=([0-9.]+)%', open('field_tests/results/d1884_mixedweight.txt').read()).group(1)) / 100
row('4 flavour', 'two-stack quark natural fraction [PHENOMENOLOGICAL]', f2, 'SRC d1884_mixedweight.txt (parsed)', 'PHEN', bound=('>', 0.05))
row('4 flavour', 'lepton slip u_l vs down slip u_d (D1832, same lock)', 0.0253 / 0.0259, 'SRC D1832 (fit within one lock)', 'CONS', note='2% match; conflicts with Koide-at-rho; replaces withdrawn arrow')

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
row('4 flavour', 'heavy neutrino M_N [GeV]', MN, 'CALC y3^2 v_u^2 / m3', 'CONS', bound=('<', 2.5e12), note='window applies only to NON-thermal leptogenesis: T_R = 3.7e8 << M_N (D1897)')
row('4 flavour', 'neutrino ratio natural fraction', R('d1821_neutrino.json')['frac'], 'SRC d1821_neutrino.json', 'DER', bound=('>', 0.01))
row('4 flavour', 'pyramid rung ratio 3->4 (no shared-step comparison after D1894b)', math.exp(-7 * math.pi / 8), 'CALC', 'CONS')

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
    print('  %-52s %-12.4g %-7s %-10s %s' % (r['name'], r['value'], r['label'].split()[0], t, r['how'] + ('  [' + r['note'] + ']' if r['note'] else '')))
nphen = sum(1 for r in rows if r['label'].startswith('PHEN') and r['test'] == 'PASS')
print('\nTESTS: %d PASS (%d of them PHENOMENOLOGICAL, no geometric home), %d FAIL of %d tested lines (%d lines total)' % (npass, nphen, nfail, npass + nfail, len(rows)))
json.dump(rows, open('field_tests/results/weave_derivation_v4.json', 'w'), indent=1, default=str)
