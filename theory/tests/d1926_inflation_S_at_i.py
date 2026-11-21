"""D1926: the P3-S plateau V ∝ G^{SS̄}|∂_S ln E(S,3/2)|² ending at S = i (path Re S = 0) instead of S = ρ (Re S = ½).
E normalised as 2ζ(3)y^{3/2} + 4ζ(2)y^{-1/2} + 8π√y Σ n^{-1}... (Green–Gutperle); validated by E(ρ) = 8.893 (D1622) and S-invariance."""
import json, math, mpmath as mp
mp.mp.dps = 30
z3, z2 = mp.zeta(3), mp.zeta(2)
def E(x, y, nmax=40):
    x, y = mp.mpf(x), mp.mpf(y)
    s = 2 * z3 * y ** 1.5 + 4 * z2 / mp.sqrt(y)
    for n in range(1, nmax + 1):
        sig = mp.fsum(mp.mpf(d) ** -2 for d in range(1, n + 1) if n % d == 0)   # σ_{-2}(n)
        s += 8 * mp.pi * mp.sqrt(y) * n * sig * mp.besselk(1, 2 * mp.pi * n * y) * mp.cos(2 * mp.pi * n * x)
    return s
def red(x, y):   # reduce to fundamental domain so the q-expansion converges
    t = mp.mpc(x, y)
    for _ in range(50):
        t = t - mp.floor(t.real + 0.5)
        if abs(t) < 1: t = -1 / t
        else: break
    return t.real, t.imag
def Ef(x, y): xr, yr = red(x, y); return E(xr, yr)
def V(x, y, h=mp.mpf('1e-8')):          # V/V0 = y² (f_x² + f_y²)/f²  (= 4y²|∂_S ln E|²)
    f = Ef(x, y); fx = (Ef(x + h, y) - Ef(x - h, y)) / (2 * h); fy = (Ef(x, y + h) - Ef(x, y - h)) / (2 * h)
    return y ** 2 * (fx ** 2 + fy ** 2) / f ** 2
def hess(x0, y0, h=mp.mpf('1e-4')):     # canonical masses: φ = coordinate/(√2 y0) ⇒ m² = 2 y0² ∂²V
    vxx = (V(x0 + h, y0) - 2 * V(x0, y0) + V(x0 - h, y0)) / h ** 2
    vyy = (V(x0, y0 + h) - 2 * V(x0, y0) + V(x0, y0 - h)) / h ** 2
    vxy = (V(x0 + h, y0 + h) - V(x0 + h, y0 - h) - V(x0 - h, y0 + h) + V(x0 - h, y0 - h)) / (4 * h ** 2)
    M = mp.matrix([[vxx, vxy], [vxy, vyy]]) * 2 * y0 ** 2
    ev = mp.eig(M)[0]; return sorted(float(mp.re(e)) for e in ev)
out = {}
rx, ry = mp.mpf(0.5), mp.sqrt(3) / 2
out['check_E_rho'] = float(E(rx, ry)); out['check_S_invariance'] = float(abs(E(0.3, 1.7) - Ef(*(lambda t: (t.real, t.imag))(-1 / mp.mpc(0.3, 1.7)))))
out['V_at_i'] = float(V(0, 1)); out['V_at_rho'] = float(V(rx, ry))
mi, mr = hess(mp.mpf(0), mp.mpf(1)), hess(rx, ry)
out['m2_i'] = mi; out['m2_rho'] = mr
ys = [1 + 0.05 * k for k in range(1, 400)]
vline = [float(V(0, y)) for y in ys]; out['monotonic_Re0'] = all(b > a for a, b in zip(vline, vline[1:]))
out['V_ratio_Re0_vs_Rehalf_at_y55.6'] = float(V(0, 55.6) / V(0.5, 55.6) - 1)
m_i = math.sqrt(min(mi)) if min(mi) > 0 else float('nan'); m_r = math.sqrt(min(mr)) if min(mr) > 0 else float('nan')
dN = 0.5 * math.log(m_i / m_r) if m_i == m_i and m_r == m_r else float('nan')   # T_R ∝ m^{3/2} (Γ ∝ m³), w = 0 ⇒ ΔN* = ½ ln(m_i/m_ρ)
Nstar = 50.3; out['dNstar'] = dN; out['dn_s'] = 2 * dN / Nstar ** 2
out['verdict'] = 'PASS' if (min(mi) > 0 and out['monotonic_Re0'] and abs(out['dn_s']) < 1e-3) else 'FAIL'
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1926_inflation_S_at_i.json', 'w'), indent=1)
