"""Test the checks on today's REAL mistakes (would they have been caught?)."""
import math, json, sys
sys.path.insert(0, 'tools/loom'); from check import *
R = {}
# D1941: m_phi readings m_a, m_b (identical algebra), m_c (from r)
MP = 2.435e18
readers = {'m_a': lambda x: math.sqrt(0.5625 * x['Vinf'] / 2.25) / MP,
           'm_b': lambda x: math.sqrt(0.5625 * 3 / 2.25) * math.sqrt(x['Vinf'] / 3) / MP,
           'm_c': lambda x: math.sqrt(0.5625 * 1.5 * math.pi ** 2 * x['As'] * x['r'] * MP ** 4 / 2.25) / MP}
R['D1941_mphi_independence'] = c1_independence(readers, dict(Vinf=4.9e15 ** 4, As=2.1e-9, r=5.4e-4))
# D1938: seam test (universal shifts cancel in Delta3)
def seam_verdict(x):
    sh = [x['b'] * math.log(x['V']) / (24 * math.pi ** 2)] * 3
    return 'PASS' if 0.022 <= sh[2] - sh[0] <= 0.066 else 'FAIL'
R['D1938_seam_power'] = c2_power(seam_verdict, dict(b=1.0, V=4e4), dict(b=(-10, 10), V=(1e3, 1e6)))
# D1926 run 1: Fourier factor 8pi vs 16pi — validation against the lattice value 8.893
R['D1926_run1_validation'] = c3_validate(8.950, 8.893, 1e-3)
# D1946: 3/4 numerology with the real target uncertainty (±8 %) and 3 candidates
R['D1946_numerology_real'] = c4_numerology(0.752, 0.08, [1.021, 2 / 3, 3 / 4])
R['D1946_numerology_claimed'] = c4_numerology(0.752, 0.003, [1.021, 2 / 3, 3 / 4])
# claim lint on the D1931 text and on a clean sentence
R['D1931_lint'] = c5_lint('Both point to T_R ~ 1e11–1e12 GeV ... This is the strongest pointing in the catalogue.')
R['clean_lint'] = c5_lint('The wino sits inside the spread of the bound: INDETERMINATE.')
# four corners on n_s: forward (plateau) 0.9706, reverse (data) 0.9728, early (CMB-SPA) 0.9684, late (DESI-combined) 0.9728
R['ns_four_corners'] = c6_four_corners(dict(forward=0.9706, reverse=0.9728, early=0.9684, late=0.9728), 0.005)
R['alpha_s_four_corners'] = c6_four_corners(dict(forward=0.1140, reverse=0.1180, early=None, late=None), 0.01)
for k, (ok, msg) in R.items(): print('%-28s %-5s %s' % (k, 'ok' if ok else 'FLAG', msg))
json.dump({k: dict(ok=v[0], msg=v[1]) for k, v in R.items()}, open('field_tests/loom/check_selftest.json', 'w'), indent=1)
# C7: would the D1946 128 pi error have been caught? Compare the formula as first written against the benchmark.
k, m = 1.0, 1.0
as_written = k ** 2 * m ** 3 / (128 * math.pi); ref = k ** 2 * m ** 3 / (64 * math.pi)
print('%-28s %-5s %s' % ('D1946_gauge_width_formula', 'FLAG' if abs(as_written / ref - 1) > 1e-6 else 'ok', 'as written %.4g vs benchmark %.4g (factor %.1f)' % (as_written, ref, ref / as_written)))
for name, (ok, msg) in c7_benchmarks().items(): print('%-28s %-5s %s' % ('bench_' + name, 'ok' if ok else 'FLAG', msg))
