"""T5: the Twist angle at the end of alpha = 1 inflation. AI-assisted, order of magnitude.
(1) Quantum fluctuations: during inflation a light angle gets delta(beta_canonical) ~ H_inf/(2 pi). The matter made
    depends on the angle's SPEED, not its position; the angle is shift-symmetric, so a position fluctuation changes
    nothing and its speed fluctuations decay as a^-3. -> no baryon isocurvature at leading order.
(2) Restart: an inflaton moving straight along the dilaton (radial) direction gives the angle no speed; its own momentum
    is diluted by e^{-3N}. A tilt of the potential in the angle direction during the last e-fold gives
    thetadot_canonical ~ V_theta/(3H); the needed r = thetadot/(H M_P) then requires V_theta/V ~ r / M_P."""
import math
MP = 2.435e18
As, r_t = 2.1e-9, 0.004                  # scalar amplitude; tensor ratio from alpha = 1, N ~ 56
V = 1.5 * math.pi ** 2 * As * r_t * MP ** 4
H = math.sqrt(V / 3) / MP
print(f"alpha = 1 inflation: V^(1/4) = {V ** 0.25:.2e} GeV, H_inf = {H:.2e} GeV, delta(angle) ~ H/2pi = {H / 2 / math.pi:.1e} GeV")
TRH_max = (30 * V / (math.pi ** 2 * 106.75)) ** 0.25
print(f"instant reheating would give T_RH ~ {TRH_max:.1e} GeV (Twist leptogenesis needs >~ 2e13 GeV: OK)")
for r_need in (0.006, 0.06):
    print(f"angle speed r = {r_need} at reheating needs an angular tilt V_theta/V ~ {r_need:.3f} per M_P "
          f"(a {100 * r_need:.1f}% change of the inflaton potential across one Planck mass of angle)")
