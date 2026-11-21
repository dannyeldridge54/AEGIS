"""RW5 — PREREG_RW5_ZETA5. AI-assisted. Run from the repo root."""
import json, math
src = open('field_tests/scripts/realdata/run.py').read().split("out={}")[0]
exec(src)  # defines chi2_from_E, E_lcdm, E_thread (uses globals A, beta), fit
out = {}
c0, x0 = fit(E_lcdm, [[0.30], [0.32]], [(0.1, 0.6)]); out['LCDM'] = dict(chi2=c0, x=x0)
starts = [[0.31, 0.15], [0.31, 0.25], [0.30, 0.05], [0.31, 0.10]]
bnds = [(0.1, 0.6), (0.005, 0.9)]
res = {}
for name, (Aval, bval) in {'A7.30_b2sqrt2': (16 * (math.pi**2 / 6) / (3 * 1.2020569031595942), 2 * math.sqrt(2)),
                           'A4.45_b2sqrt2': (4.45, 2 * math.sqrt(2)),
                           'A4.45_b4sqrt2': (4.45, 4 * math.sqrt(2))}.items():
    A, beta = Aval, bval
    c, x = fit(E_thread, starts, bnds)
    res[name] = dict(A=Aval, beta=bval, chi2=c, x=x, dchi2_vs_LCDM=c - c0)
    print(name, res[name], flush=True)
out['fits'] = res
dA = res['A4.45_b2sqrt2']['chi2'] - res['A7.30_b2sqrt2']['chi2']
out['R0'] = dict(dchi2_A=dA, degenerate=abs(dA) <= 0.01,
                 A_rule='UNTESTABLE at leading order' if abs(dA) <= 0.01 else 'STOP: script wrong (DEVIATIONS)')
sanity = abs(res['A7.30_b2sqrt2']['chi2'] - 1638.32) <= 0.05
D = res['A4.45_b4sqrt2']['chi2'] - res['A7.30_b2sqrt2']['chi2']
out['R1'] = dict(sanity_ok=sanity, Delta=D,
                 verdict=('INVALID' if not sanity else 'FLIP FAVOURED' if D <= -1 else 'FLIP DISFAVOURED' if D >= 1 else 'TIE'))
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/rw5_zeta5.json', 'w'), indent=1)
