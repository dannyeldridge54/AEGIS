import sys; sys.path.insert(0, '.')
from tools.chem.wavelength import line, air, hydrogen_21cm, convert, ribbon
L = []; ok = []
def t(name, val, ref, tol):
    d = val/ref - 1; ok.append(abs(d) <= tol); L.append(f"{name}: {val:.6f} vs {ref} ({d:+.4%}, tol {tol:.3%}) {'PASS' if abs(d) <= tol else 'FAIL'}")
t('T1 H Lyα vac nm', line('H', 1, 2), 121.567, 2e-5)
t('T2 H Hα air nm', air(line('H', 2, 3)), 656.28, 1e-4)
t('T3 He II 2→1 nm', line('He+', 1, 2), 30.378, 1e-4)
t('T4 21 cm MHz', hydrogen_21cm()/1e6, 1420.405751768, 1e-3)
x = convert(lam_m=500e-9); y = convert(E_eV=x['E_eV']); d = abs(y['lam_m']/x['lam_m'] - 1); ok.append(d < 1e-12); L.append(f"T5 round-trip |Δ| {d:.1e} {'PASS' if d < 1e-12 else 'FAIL'}; 500 nm → {x['E_eV']:.4f} eV, {x['colour']}")
L += [f"ribbon: {m['label']} λ = {m['lam_m']:.4e} m [{m['kind']}]" for m in ribbon()]
L.append(f"CH1 VERDICT: {'ALL PASS → ADOPT' if all(ok) else 'FAIL'}")
open('field_tests/results/ch1_wavelength.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
