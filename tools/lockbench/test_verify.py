# AEGIS-FP IJPRFFISSFXFVJCT · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import sys, math; sys.path.insert(0, '.')
from tools.lockbench.verify import gci3, observed_order, two_solver, mms_orders
trap = lambda n: (lambda h: h*(0.5*math.exp(0) + sum(math.exp(i*h) for i in range(1, n)) + 0.5*math.exp(1)))(1/n)
p, e = observed_order([1/20, 1/40, 1/80], [trap(20), trap(40), trap(80)], math.e - 1); assert all(abs(x - 2) < 0.01 for x in p), p
g = gci3(trap(80), trap(40), trap(20), 2.0, 2.0); assert g['ok'] and abs(g['p'] - 2) < 0.01 and abs(g['phi_ext'] - (math.e - 1)) < 1e-6, g
g2 = gci3(trap(80), trap(50), trap(20), 80/50, 50/20); assert abs(g2['p'] - 2) < 0.02, g2       # non-uniform ratios
eu = lambda h: (1 + h)**round(1/h)                                                              # Euler for y'=y on [0,1]: order 1
assert all(abs(x - 1) < 0.05 for x in mms_orders(eu, [0.01, 0.005, 0.0025], math.e)[0])
assert two_solver(1.0, 1.0 + 1e-9, 1e-8)['ok'] and not two_solver(1.0, 1.1, 1e-3)['ok']
print('test_verify: PASS (trapezoid p=2, GCI uniform/non-uniform recovers p and exact limit, Euler p=1, two-solver)')
