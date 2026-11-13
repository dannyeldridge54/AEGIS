"""D172: (a) can the Twist's angle y be the QCD axion (solving strong CP)? (b) the ISW effect. AI-assisted, order of magnitude.
(a) The angle has period 8 in Im T and kinetic metric 3/(4x^2): its decay constant f = sqrt(2 K_TT) * 8/(2 pi) M_P. A shift-symmetric
    y G Gtilde coupling (allowed, D144) gives it the QCD potential m_pi^2 f_pi^2 (1 - cos theta), theta = 2 pi y / 8, which dominates its
    own tiny T-sector potential today, so it relaxes to theta = 0 (strong CP solved) — but it then oscillates and becomes axion dark
    matter: Omega_a h^2 ~ 0.12 theta_i^2 (f / 9e11 GeV)^1.165 (standard misalignment, f > 1e12 GeV).
(b) ISW: Phi ~ D(a)/a; the late-time ISW signal ~ change of D/a since z ~ 3. Ratio Twist / LCDM at the same Omega_m."""
import math, io, contextlib
MP = 2.435e18
for x in (72.7, 88.9):
    f = math.sqrt(2 * 3 / (4 * x * x)) * 8 / (2 * math.pi) * MP
    th_need = math.sqrt(0.12 / (0.12 * (f / 9e11) ** 1.165))
    print(f"(a) x {x}: angle decay constant f = {f:.1e} GeV; axion dark matter for theta_i ~ 1 is {(f/9e11)**1.165:.0e} x observed; "
          f"needs theta_i ~ {th_need:.0e} rad")
print(f"    QCD minimum shift from the T-sector's own angle potential: ~ V_tail / (m_pi^2 f_pi^2) ~ {2.5e-47/(0.135**2*0.092**2):.0e} (bound 1e-10)")
print("    the Twist's runs leave the angle at y = 1.2 (0.8% heat) or 15.4 (0.13%): theta_i = 0.94 or 0.47 rad from a minimum")
with contextlib.redirect_stdout(io.StringIO()):
    import late_predictions_d168 as L
Da = lambda G, a: L.D(G, a) / a
isw = lambda G: Da(G, 1.0) - Da(G, 0.25)
print(f"(b) late ISW signal (change of D/a since z = 3), Twist / LCDM: {isw(L.GT)/isw(L.GL):.3f}")
