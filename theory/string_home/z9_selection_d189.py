"""D189 (built on D165): can worldsheet instantons on the quintic produce the Twist's cliff depth n ~ 125? AI-assisted.
Step 1: genus-0 curve counts n_d of the quintic from mirror symmetry (Candelas-de la Ossa-Green-Parkes), computed here from the
periods: w0 = sum (5k)!/(k!)^5 z^k, w1 = w0 ln z + sum (5k)!/(k!)^5 [5(H_5k - H_k)] z^k, t = w1/(2 pi i w0), q = e^{2 pi i t};
Yukawa coupling in the t-frame: kappa(q) = 5 / ((1 - 5^5 z) w0^2) * (z d/dz ln q)^-3 ... = 5 + sum_d n_d d^3 q^d/(1 - q^d).
Step 2: the instanton correction to the Kahler potential of the Kahler modulus (tau = Im t, real part 0):
  e^{-K} = (4/3) 5 tau^3 + (chi zeta(3))/(4 pi^3)... + (2/pi^3) sum_d n_d [ Li3(e^{-2 pi d tau}) + 2 pi d tau Li2(e^{-2 pi d tau}) ] / 4 (normalisation
  to order one). For heterotic (2,2) models the 27 matter metric goes as e^{-K_T/3} (Dixon-Kaplunovsky-Louis), so the instanton part of
  ln(matter metric) is ~ (1/3) ln(1 + R), R = instanton / classical. TWIST-K needs this to change by 2n ~ 250 between plateau and tail."""
import mpmath as mp
mp.mp.dps = 50
D = 19
a = [mp.factorial(5 * k) / mp.factorial(k) ** 5 for k in range(D + 1)]
H = lambda m: sum(mp.mpf(1) / j for j in range(1, m + 1))
b = [a[k] * 5 * (H(5 * k) - H(k)) for k in range(D + 1)]
# series arithmetic in z, truncated at order D
def mul(p, q): return [sum(p[i] * q[k - i] for i in range(k + 1)) for k in range(D + 1)]
def inv(p):
    r = [mp.mpf(0)] * (D + 1); r[0] = 1 / p[0]
    for k in range(1, D + 1): r[k] = -sum(p[i] * r[k - i] for i in range(1, k + 1)) / p[0]
    return r
def exp_s(p):          # p[0] = 0
    r = [mp.mpf(0)] * (D + 1); r[0] = mp.mpf(1)
    for k in range(1, D + 1): r[k] = sum(i * p[i] * r[k - i] for i in range(1, k + 1)) / k
    return r
f = mul(b, inv(a))                     # ln q = ln z + f(z)
q_over_z = exp_s(f)                    # q = z * exp(f)
# invert q(z) -> z(q) by series reversion: z = q * g(q)
g = [mp.mpf(0)] * (D + 1); g[0] = mp.mpf(1)
for _ in range(D + 2):
    zq = [mp.mpf(0)] + g[:D]           # z(q) as a series in q
    # compose q_over_z(z(q)) * z(q) = q  ->  g = 1 / q_over_z(z(q))
    comp = [mp.mpf(0)] * (D + 1); zp = [mp.mpf(1)] + [mp.mpf(0)] * D
    for k in range(D + 1):
        comp = [comp[i] + q_over_z[k] * zp[i] for i in range(D + 1)]; zp = mul(zp, zq)
    g = inv(comp)
zq = [mp.mpf(0)] + g[:D]
# Yukawa: kappa = 5 / ((1 - 3125 z) w0^2) * (z dlnq/dz)^-3, all as series in q
def compose(p, s):                     # p(s(q)), s[0] = 0
    out = [mp.mpf(0)] * (D + 1); sp = [mp.mpf(1)] + [mp.mpf(0)] * D
    for k in range(D + 1):
        out = [out[i] + p[k] * sp[i] for i in range(D + 1)]; sp = mul(sp, s)
    return out
w0q = compose(a, zq)
zdlnq = [mp.mpf(1)] + [k * f[k] for k in range(1, D + 1)]            # z d/dz (ln z + f) = 1 + z f'
zdlnq_q = compose(zdlnq, zq)
one_m = compose([mp.mpf(1), mp.mpf(-3125)] + [mp.mpf(0)] * (D - 1), zq)
kappa = mul([5 * c for c in inv(one_m)], inv(mul(w0q, w0q)))
kappa = mul(kappa, inv(mul(zdlnq_q, mul(zdlnq_q, zdlnq_q))))
# extract n_d from kappa = 5 + sum_d n_d d^3 q^d/(1-q^d)
nd = {}
for d in range(1, D + 1):
    c = kappa[d] - sum(nd[e] * e ** 3 for e in nd if d % e == 0)
    nd[d] = mp.nint(c / d ** 3)

# D189: keep only degrees d = 0 mod 9 (a Z9 selection rule on the coupling), compare with the full sum and the conifold edge
zc = mp.mpf(1) / 3125; tc = (sum(b[k] * zc ** k for k in range(D + 1)) / sum(a[k] * zc ** k for k in range(D + 1)) + mp.log(zc)) / (-2 * mp.pi)
print("n_9  =", mp.nstr(nd[9], 6), "  n_18 =", mp.nstr(nd[18], 6), "  ratio n_d/n_(d-1) at d=18:", mp.nstr(nd[18]/nd[17], 6))
growth = nd[18] / nd[17]; tau_conv = mp.log(growth) / (2 * mp.pi)
print(f"radius of convergence of the instanton sum: tau ~ {float(tau_conv):.3f} (conifold estimate {float(tc):.3f})")
def term(d, tau):
    x = mp.e ** (-2 * mp.pi * d * tau)
    return nd[d] * (mp.polylog(3, x) + 2 * mp.pi * d * tau * mp.polylog(2, x))
def R9(tau, degs=(9, 18)):
    return (2 / mp.pi ** 3) * sum(term(d, tau) for d in degs) / 4 / (mp.mpf(4) / 3 * 5 * tau ** 3)
print("tau   R(deg 9 only)   R(deg 9+18)   (1/3)ln(1+R) [9+18]   deg18/deg9")
for tau in (1.2, 1.1, 1.05, 1.0, 0.95, 0.9, 0.85):
    t = mp.mpf(tau); r9 = R9(t, (9,)); r = R9(t)
    print(f"{tau:5}  {float(r9):.3e}      {float(r):.3e}     {float(mp.log(1+r)/3):8.3f}            {float(term(18,t)/term(9,t)):.3e}")
# where would degree 9 alone give (1/3) ln(1+R) = 250?
f = lambda t: mp.log(1 + R9(t, (9,))) / 3 - 250
print("degree-9 alone reaches 2n = 250 only for R ~ e^750: impossible at any tau above the conifold;")
print("max of (1/3)ln(1+R9) at the convergence edge:", mp.nstr(mp.log(1 + R9(tau_conv, (9,))) / 3, 4))
