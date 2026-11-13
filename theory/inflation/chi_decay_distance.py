"""Development 62 (exploratory): the instant-preheating decay distance, computed instead of bracketed. AI-assisted.
chi gets mass m_chi = g |phi - phi0| M_P as the inflaton moves on at speed phidot (M_P^2 units, from the model:
3.03e-6). chi decays to Standard Model fermions with Gamma = h^2 m_chi / (8 pi) (h = its Yukawa). It decays after
moving dphi with Gamma * (dphi / phidot) = 1  ->  dphi = sqrt(8 pi phidot / (h^2 g)) (M_P units).
Efficiency f = g^{5/2} dphi / (4 pi^3 sqrt(phidot)) (reheating_derived.py), T_RH from the end-of-inflation state."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reheating_derived as R
H, dp = R.end_state(); phidot = H * dp
print(f"phidot = {phidot:.2e} M_P^2")
for g in (0.03, 0.1, 0.3):
    for h in (0.1, 0.3, 1.0):
        dphi = math.sqrt(8 * math.pi * phidot / (h * h * g))
        f = min(1.0, g ** 2.5 * dphi / (4 * math.pi ** 3 * math.sqrt(phidot)))
        print(f"g {g}, h {h}: chi decays after dphi = {dphi:.3f} M_P -> f = {f:.1e}, T_RH = {R.T_of(f, H, dp):.2e} GeV")
