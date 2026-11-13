"""Theory test T-ROLL: does the angle roll freely after inflation, as MATTER assumes? AI-assisted.
In the explicit no-scale model (sugra_kick.py, F = T - 1/2): V = m^2 |F|^2/(4 x^2), metric g_yy = 3/(2 x^2).
At the vacuum x = 1/2, y = 0: V_yy = m^2/(2 x^2) = 2 m^2, g_yy = 6 -> angle mass m_y = m/sqrt(3).
m from the CMB amplitude: plateau V = m^2/4 = V* (TWIST-INFLATION: 1.07e-10 M_P^4).
The matter mechanism needs mu_A = c_A thetadot/M_P to keep one sign for about a Hubble time while the Weinberg rate acts
(Gamma_W/H ~ 0.5 at 1e13 GeV). If m_y >> H(T_RH), the angle oscillates and the asymmetry averages away (~H/m_y)."""
import math
MP, MPL, gs = 2.435e18, 1.221e19, 106.75
Vstar = 1.0668e-10
m = 2 * math.sqrt(Vstar) * MP
my = m / math.sqrt(3)
for T in (1e13, 1e14, 1e15):
    H = 1.66 * math.sqrt(gs) * T * T / MPL
    print(f"T_RH {T:.0e} GeV: H = {H:.1e} GeV; angle vacuum mass {my:.1e} GeV; m/H = {my / H:.1e}; "
          f"oscillations per Hubble time ~ {my / H / (2 * math.pi):.0e}; suppression ~ {H / my:.0e}")
