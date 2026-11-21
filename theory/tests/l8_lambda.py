"""PREREG_L8_LAMBDA"""
import math, json
ReS, V, a = math.sqrt(3) / 2, 4.2e4, 2 * math.pi; target = 7.1e-121
pref = (1 / (2 * ReS * V ** 2)) * a ** 2
lg = lambda T: math.log10(pref) - 4 * math.pi * T / math.log(10)
T_need = (math.log10(pref) - math.log10(target)) * math.log(10) / (4 * math.pi)
aD_inv = T_need + (4 / 3) / (2 * math.pi) * math.log(7e15 / 12.8)
print(json.dumps(dict(prefactor=pref, log10_V_at_21p1=lg(21.1), ReT_dark_needed=T_need, in_axion_window=20.3 <= T_need <= 22.1,
                      alpha_D_12GeV=1 / aD_inv), indent=1))
