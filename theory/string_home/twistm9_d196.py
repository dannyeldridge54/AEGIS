"""D196: TWIST-M9 — the Gamma0(9) cliff built from h^9, which removes D164's strong-coupling problem. AI-assisted.
s = 1/(1 + h(y)^9), h = (eta(iy)/eta(9iy))^3, a Gamma0(9) modular function. At the cusp i*inf, 1/h^9 = q^9 (1 + 27 q + ...): the leftover
starts at DEGREE 9 with no lower degrees (D164's condition). Matching the tail e^{-pi x/4} = q^9 gives y = Im T_het = x/72 (x = u/2).
V = m^2 / (4 g(u) E(u)), E = exp(2n(1 - s)), g = 1 + u/2."""
import mpmath as mp
mp.mp.dps = 30
n = 125
def eta(y): return mp.e ** (-2 * mp.pi * y / 24) * mp.qp(mp.e ** (-2 * mp.pi * y))
def h(y):   # exact S-transform for small y: eta(i y) = y^(-1/2) eta(i/y)
    if y < mp.mpf(1) / 3: return (3 * eta(1 / y) / eta(1 / (9 * y))) ** 3
    return (eta(y) / eta(9 * y)) ** 3
def lnV(u):
    H9 = h(u / 144) ** 9
    return -mp.log(1 + u / 2) - 2 * n * H9 / (1 + H9)
k = mp.sqrt(mp.mpf(2) / 3)
f = lambda p: lnV(mp.e ** (k * p))
d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2)
eps = lambda p: d1(p) ** 2 / 2
p = mp.mpf(6)
while eps(p) < 1: p -= mp.mpf("0.02")   # down the tail to the cliff
while eps(p) > 1: p -= mp.mpf("0.02")   # across the cliff to the plateau edge
pend = mp.findroot(lambda q: eps(q) - 1, (p, p + mp.mpf('0.02')), solver='anderson')
print(f"inflation ends at u = {float(mp.e ** (k * pend)):.4g} (x = {float(mp.e ** (k * pend) / 2):.4g})")
N, q, dq = mp.mpf(0), pend, mp.mpf("-0.004")
for Ns in (55.7, 57):
    while N < Ns: N += -dq / abs(d1(q)); q += dq
    print(f"N* = {Ns}: u* = {float(mp.e ** (k * q)):.4g}, n_s = {float(1 + 2 * d2(q) - d1(q) ** 2):.4f}, r = {float(8 * d1(q) ** 2):.4f}")
# leftover today and relative correction from the q^10 term
x = mp.mpf(89); y = x / 72; qq = mp.e ** (-2 * mp.pi * y)
print(f"today x = 89: 1/h^9 = {mp.nstr(1 / h(y) ** 9, 5)} vs e^(-pi x/4) = {mp.nstr(mp.e ** (-mp.pi * x / 4), 5)} (27q = {float(27 * qq):.2e})")
print(f"Im T_het today = {float(y):.3f} -> R = sqrt(T_het) = {float(mp.sqrt(y)):.3f}; g_s ~ g_YM R^3 = {float(0.7 * mp.sqrt(y) ** 3):.2f} (g_YM 0.7)")
