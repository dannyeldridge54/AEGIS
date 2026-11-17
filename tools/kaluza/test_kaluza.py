"""KALUZA v0.1 regression test (locked PREREG_KALUZA_v01): reproduce recorded AEGIS results through the package code paths."""
import sys, math, sympy as sp; sys.path.insert(0, '.')
from tools.kaluza.background import vacuum, gamma_c
from tools.kaluza.spectra import tensor_pw
from tools.kaluza.solvers import pruefer_SL
from tools.kaluza.convergence import aitken, predicted_order
from tools.kaluza.stability import scalar_condition
L = []; ok = True
bg = vacuum(6, sp.Rational(8, 4)); D, dl = 6, float(bg['delta'])
q = predicted_order(D, dl); c = abs(q - 0.84459) <= 1e-4; ok &= c; L.append(f"T1 order q = {q:.5f} (D1038 0.84459): {'PASS' if c else 'FAIL'}")
m, qq = aitken(0.7791277336937718, 0.7783198737892393, 0.7782038764180645); c = abs(m - 0.778184)/0.778184 <= 1e-5; ok &= c
L.append(f"T2 Aitken on recorded S4c3 values: m* = {m:.6f} (D1036 0.778184): {'PASS' if c else 'FAIL'}")
s = scalar_condition(bg); c = abs(s['min'] + 0.223607) <= 1e-5 and s['stable']; ok &= c
L.append(f"T3 scalar condition: min {s['min']:.6f} vs threshold {s['threshold']} stable {s['stable']} (D1140 −0.223607): {'PASS' if c else 'FAIL'}")
p, w = tensor_pw(bg); ye = float(bg['y_end']); e = 1e-5
m1 = pruefer_SL(1, p, w, e*ye, (1 - e)*ye); c = m1 is not None and abs(m1/0.7791277336937718 - 1) <= 1e-6; ok &= c
L.append(f"T4 tensor m1² at ε=1e-5 through the package: {m1} (S4c3 0.7791277337): {'PASS' if c else 'FAIL'}")
L.append('KALUZA v0.1 ' + ('REGRESSION PASS' if ok else 'REGRESSION FAIL')); print('\n'.join(L))
open('field_tests/results/kaluza_v01_regression.txt', 'w').write('\n'.join(L) + '\n')
