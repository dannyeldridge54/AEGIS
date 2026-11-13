"""Development 46 follow-up: does the hidden SU(8) cosine disturb inflation? AI-assisted.
Hidden term L4(x) = Omega0 * 3 mu_s^2 exp(-A x) [1 - cos(A y - s/f)], A = pi/4, mu_s = m_sigma/m (as hidden_kick_decay.py).
Compare at the CMB point (N* ~ 55.7 e-folds before the end, n = 125 model) with the inflaton potential and slope,
and the angle's mass from the cosine with the Hubble rate. Mirrored model: the plateau is at SMALL Re T, so
exp(-A Re T) ~ 1 there (no suppression) — the term must be small on its own."""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inflation"))
import early_cliff_sugra as E
c = math.sqrt(2 / 3); A = math.pi / 4; MP = 2.435e18; m_inf = math.sqrt(4 * 1.0668e-10) * MP
for m_sigma in (3e9, 6e9, 1e10):
    mus = m_sigma / m_inf; L4 = 0.05 * 3 * mus ** 2
    V = 0.25                                   # plateau height in m^2 units
    eps = 0.00376 / 16                         # r/16 at N* (n = 125 model, early_cliff_sugra.txt)
    slope = math.sqrt(2 * eps) * V
    print(f"m_sigma {m_sigma:.0e} GeV: L4/V = {L4 / V:.1e}; hidden slope / inflaton slope <= {A * L4 / slope:.1e}; "
          f"angle mass^2 from the cosine / H^2 = {A ** 2 * L4 / (V / 3) / 1.5:.1e} (Kahler gives ~4)")
