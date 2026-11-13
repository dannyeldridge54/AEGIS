"""D164: is the heterotic Z3 home (D152) self-consistent along the Twist's history? AI-assisted, order of magnitude.
In the heterotic string the 4-d gauge coupling fixes the combination  1/g_YM^2 ~ V6 / g_s^2  (V6 = R^6 in string units), so at fixed 4-d
dilaton the 10-d string coupling is  g_s ~ g_YM R^3.  The cliff's exponent matches the heterotic instanton q = e^{-2 pi T_het} with
T_het = x/8 (D153), and Re T_het ~ R^2.  Weak coupling (the regime where D152's statements hold) needs g_s < 1.
Also: KK tower M_KK ~ M_s / R with M_s ~ g_YM M_P / sqrt(8 pi)-ish ~ 5e17 GeV."""
import math
gYM = math.sqrt(4 * math.pi / 25)          # alpha_GUT ~ 1/25
Ms = 5e17
for lab, x in (("CMB scales", 1.3e-4), ("end of inflation", 0.0125), ("x = 8 (R = 1)", 8.0), ("frozen", 72.7), ("today", 88.9)):
    Th = x / 8; R = math.sqrt(Th); Rd = max(R, 1 / R)          # T-dual radius below R = 1
    gs = gYM * Rd ** 3
    print(f"{lab:>16}: T_het {Th:.2e}, R {R:.3g} (dual {Rd:.3g}), 10-d coupling g_s ~ {gs:.2g} {'(weak)' if gs < 1 else '(STRONG)'}, "
          f"KK tower ~ {Ms/Rd:.1e} GeV")
xmax = 8 * (1 / gYM) ** (2 / 3)
print(f"weak coupling needs R < {(1/gYM)**(1/3):.2f}, i.e. x < {xmax:.1f} (and, by T-duality, x > {64/xmax:.2f})")
