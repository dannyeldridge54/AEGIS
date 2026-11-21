"""PREREG_L8c_CROSSTERM: V_cross = 4 a s e^K W0 e^{-a s}."""
import math, json
from scipy.optimize import brentq
a, W0, ReS, Vol, MP = 2 * math.pi, 5.9e-9, math.sqrt(3) / 2, 4.2e4, 2.435e27
eK = 1 / (2 * ReS * Vol ** 2)
V = lambda s: 4 * a * s * eK * W0 * math.exp(-a * s)
s_L = brentq(lambda s: math.log(V(s)) - math.log(7.1e-121), 5, 80)
def s_for_m(m):
    return brentq(lambda s: math.log(V(s)) - 2 * math.log(m / MP) - 2 * math.log(math.sqrt(3) / (2 * s)), 5, 80)
sb = sorted([s_for_m(1e-33), s_for_m(1e-28)])
cons_b = sb[0] - 0.37 <= s_L <= sb[1] + 0.37
v = ('CONSISTENT' if abs(s_L - 21.1) <= 1 else 'SHIFTED') if cons_b else 'BROKEN'
# old e^{-4 pi T} check, for the record
out = dict(eK=eK, prefactor=4 * a * eK * W0, sigma_Lambda=s_L, sigma_beta=sb, verdict=v,
           alphaD_inv_at_sL=s_L + (4 / 3) / (2 * math.pi) * math.log(7e15 / 12.8))
out['alphaD_at_sL'] = 1 / out['alphaD_inv_at_sL']
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/l8c_crossterm.json', 'w'), indent=1)
