"""D259-D265: numerical checks behind the referee-review fixes (13 Nov 2026). Estimates, AI-assisted."""
import math
from scipy.stats import norm
MP = 2.435e18; g = 106.75
# D259 tail slope fraction s = x/(x+mu) at mu = 1
for x in (2, 30, 73, 89, 360):
    print(f"D259 x={x:4d}: slope fraction {x/(x+1):.3f}")
# D260 instant reheating temperature from H_end
Hend = 5.2e12; rho = 3 * Hend**2 * MP**2
T = lambda f: (30 * f * rho / (math.pi**2 * g)) ** 0.25
print(f"D260 T_RH instant {T(1):.2e} GeV; f=0.65%: {T(0.0065):.2e}; f=0.8%: {T(0.008):.2e}; f=0.15%: {T(0.0015):.2e}")
# D261 gravitino: thermal yield (standard formula, estimate) and decay-time dilution for m32 < T_RH
TRH = T(0.008)
for m in (1e11, 1e12, 1e13, 1e14):
    Y = 1.9e-12 * (TRH / 1e10) * (1 + 1/3)
    Gam = 193 / (384 * math.pi) * m**3 / MP**2
    Td = (Gam * MP / math.sqrt(math.pi**2 * g / 90)) ** 0.5
    print(f"D261 m32={m:.0e}: Y={Y:.1e}, T_decay={Td:.1e} GeV, rho32/rho_rad at decay={(4/3)*m*Y/Td:.1e}")
# D262 trials correction for PURE-TWIST
d = 3.37; p = 2 * norm.sf(math.sqrt(d))
for N in (6, 9, 12):
    pg = 1 - (1 - p) ** N
    print(f"D262 local {math.sqrt(d):.2f} sigma (p={p:.3f}); N={N}: global p={pg:.2f} = {norm.isf(pg/2):.2f} sigma")
# D265 cliff depth n from m^2 e^{-2n}/(4(1+x/mu)) = rho_DE
m = 2.1e-5; H0 = 67.4 / 3.0857e19 * 6.582e-25 / MP   # in M_P
rDE = 3 * H0**2 * 0.69
n0 = 0.5 * math.log(m**2 / (4 * rDE)); print(f"D265 n without 1/(1+x): {n0:.1f}; with x=89, mu=1: {n0 - 0.5*math.log(90):.1f}")
