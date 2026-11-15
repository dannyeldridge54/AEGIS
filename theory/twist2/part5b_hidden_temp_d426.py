"""D426 (locked PREREG_D426_PART5B): second pass Part 5 — does the hidden χ sector share the SM temperature at capture? AI-assisted.
(1) Thermal contact through the D422 portal W ⊃ y' ψ L H (ψ in equilibrium with χ via y and U(1)_X): Γ ≈ y'² T/(8π) vs H = 17.2 T²/M_P at
the crossing T_x (D396). (2) If the hidden sector is colder, T_h = ξ T: the trap barrier scales as T_h⁴ and the kinetic/barrier ratio of D396
scales as ξ^{−4}; trapped needs ratio < 1."""
import math
MP = 2.435e18; cH = 17.2
for xE, Tx, kv in ((29.213, 3.943e11, 0.015), (29.452, 2.391e11, 0.006), (29.598, 1.451e11, 0.002)):
    H = cH * Tx * Tx / MP; ymin = math.sqrt(8 * math.pi * H / Tx); xi_min = kv ** 0.25
    print(f"x_E {xE}: T_x {Tx:.2e} GeV, H {H:.2e} GeV → portal y' ≳ {ymin:.1e} for equilibrium; if colder, trapping needs T_h/T ≥ {xi_min:.2f}")
