"""Developments 76-77 (exploratory): two plateau checks. AI-assisted.
(76) Mass of the twist angle y during inflation. At S = 0, V(T) = m^2 |F(T)|^2 / (4 x^2), T = x + i y (exact for
     K = -3 ln(T + Tbar - S Sbar + ...), W = sqrt(3) m S F(T)). y's kinetic weight K_TTbar = 3/(4x^2), so
     m_y^2 = (d^2 V / dy^2) / (2 K_TTbar). Compared with H^2 = V/3. Model as s_stability (mu = 1, n = 125, m2 = 1).
(77) Loop corrections from the reheating field chi (coupling g^2 (phi - phi0)^2 chi^2 / 2, g = 0.1, phi0 at the end
     of inflation). Coleman-Weinberg: without supersymmetry dV = M^4 ln(M^2/Q^2) / (64 pi^2), M = g |phi - phi0|;
     with chi in a chiral multiplet the M^4 pieces cancel between boson and fermion and the remainder is set by the
     mass splitting, which during inflation is ~ H^2: dV ~ M^2 H^2 ln(M^2/H^2) / (16 pi^2) (supergravity, Hubble-
     induced splitting). We give dV/V and the shift in eta = V''/V (n_s moves by about 2 d eta) at the CMB point."""
import math
import mpmath as mp
mp.mp.dps = 30
MU, N, M2 = 1, 125, 1
c = math.sqrt(2 / 3)
F = lambda T: T / mp.sqrt(1 + T / MU) * mp.exp(-N * T / (T + M2))
V = lambda x, y=0: abs(F(mp.mpc(x, y))) ** 2 / (4 * x * x)        # units m^2 = 1

print("(76) twist angle y on the plateau and past the cliff")
for x in (1e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 0.1, 1, 30):
    x = mp.mpf(x); d2 = mp.diff(lambda y: V(x, y), 0, 2)
    my2 = d2 / (2 * 3 / (4 * x * x)); H2 = V(x) / 3
    print(f"   x {float(x):.0e}: m_y^2/H^2 = {float(my2 / H2):+.3f}")

# canonical phi = ln(x)/c; end of inflation: eps = 1
Vp = lambda p: V(mp.e ** (c * p))
eps = lambda p: 0.5 * (mp.diff(Vp, p) / Vp(p)) ** 2
pend = mp.findroot(lambda p: eps(p) - 1, -6)
Nof = lambda p: mp.quad(lambda q: Vp(q) / mp.diff(Vp, q), [p, pend]) * -1
pstar = mp.findroot(lambda p: Nof(p) - 55, pend - 5)
print(f"\nend of inflation phi_end = {float(pend):.2f} (x {float(mp.e ** (c * pend)):.2e}); CMB point (N = 55) "
      f"phi* = {float(pstar):.2f} (x {float(mp.e ** (c * pstar)):.2e}); distance {float(pend - pstar):.2f} M_P")

print("\n(77) loop corrections from chi, g = 0.1, at the CMB point (Planck units, m^2 = 4.27e-10 sets V)")
m2u = 4.27e-10; g = 0.1
Vs = m2u * Vp(pstar); H2 = Vs / 3; eta0 = mp.diff(Vp, pstar, 2) / Vp(pstar)
Mphi = lambda p: g * abs(p - pend)
for lab, dV in (("no supersymmetry", lambda p: Mphi(p) ** 4 * mp.log(Mphi(p) ** 2 / H2) / (64 * mp.pi ** 2)),
                ("chi in a chiral multiplet", lambda p: Mphi(p) ** 2 * H2 * mp.log(Mphi(p) ** 2 / H2) / (16 * mp.pi ** 2))):
    r = dV(pstar) / Vs; de = mp.diff(dV, pstar, 2) / Vs
    print(f"   {lab}: dV/V = {float(r):.2e}, d eta = {float(de):+.2e} (eta itself {float(eta0):+.4f}), "
          f"n_s shift ~ {float(2 * de):+.1e}")
gmax = None
for gg in [10 ** (-k / 4) for k in range(0, 40)]:
    M = gg * abs(pstar - pend); de = (gg ** 4 * 12 * (pstar - pend) ** 2 * (mp.log(M ** 2 / H2) + 7 / 6)) / (64 * mp.pi ** 2) / Vs
    if abs(2 * de) < 1e-3: gmax = gg; break
print(f"   without supersymmetry, keeping the n_s shift below 0.001 needs g < ~{gmax:.1e} (preheating needs ~0.1)")
