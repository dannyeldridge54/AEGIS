"""D165: can worldsheet instantons on the quintic produce the Twist's cliff depth n ~ 125? AI-assisted.
Step 1: genus-0 curve counts n_d of the quintic from mirror symmetry (Candelas-de la Ossa-Green-Parkes), computed here from the
periods: w0 = sum (5k)!/(k!)^5 z^k, w1 = w0 ln z + sum (5k)!/(k!)^5 [5(H_5k - H_k)] z^k, t = w1/(2 pi i w0), q = e^{2 pi i t};
Yukawa coupling in the t-frame: kappa(q) = 5 / ((1 - 5^5 z) w0^2) * (z d/dz ln q)^-3 ... = 5 + sum_d n_d d^3 q^d/(1 - q^d).
Step 2: the instanton correction to the Kahler potential of the Kahler modulus (tau = Im t, real part 0):
  e^{-K} = (4/3) 5 tau^3 + (chi zeta(3))/(4 pi^3)... + (2/pi^3) sum_d n_d [ Li3(e^{-2 pi d tau}) + 2 pi d tau Li2(e^{-2 pi d tau}) ] / 4 (normalisation
  to order one). For heterotic (2,2) models the 27 matter metric goes as e^{-K_T/3} (Dixon-Kaplunovsky-Louis), so the instanton part of
  ln(matter metric) is ~ (1/3) ln(1 + R), R = instanton / classical. TWIST-K needs this to change by 2n ~ 250 between plateau and tail."""
import mpmath as mp
mp.mp.dps = 50
D = 12
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
print("genus-0 curve counts of the quintic (computed here):")
for d in range(1, 8): print(f"  n_{d} = {int(nd[d])}")
# Step 2: instanton share R(tau) of e^{-K}
def R(tau):
    inst = sum(nd[d] * (mp.polylog(3, mp.e ** (-2 * mp.pi * d * tau)) + 2 * mp.pi * d * tau * mp.polylog(2, mp.e ** (-2 * mp.pi * d * tau))) for d in nd)
    return (2 / mp.pi ** 3) * inst / 4 / (mp.mpf(4) / 3 * 5 * tau ** 3)
print("\ninstanton share of e^{-K} and the change of ln(matter metric) it can produce:")
for tau in (3, 2, 1.5, 1.2, 1.0, 0.8):
    r = R(mp.mpf(tau)); print(f"  tau {tau}: R = {float(r):.3e}, (1/3) ln(1+R) = {float(mp.log(1+r)/3):.3e}")
zc = mp.mpf(1) / 3125; tc = (sum(b[k] * zc ** k for k in range(D + 1)) / sum(a[k] * zc ** k for k in range(D + 1)) + mp.log(zc)) / (-2 * mp.pi)
print(f"\nconifold point (edge of the geometric phase) at tau ~ {float(tc):.2f} (series truncated at order {D}; indicative)")
print("needed for TWIST-K: change of ln(matter metric) = 2n ~ 250")
