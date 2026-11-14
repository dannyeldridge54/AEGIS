"""D407 (locked PREREG_D407_GAUGE_DECAY): right ladder — x decays through the gauge channel of the χ condensate. AI-assisted.
Γ_x = κ g_X² m_x / (8π) (gauge-strength two-body decay of the massive-multiplet scalar into light charged states; κ = mixing/phase-space
uncertainty, scanned), vs D396's gravitational Γ = m_x³/(8π M_P²). Uses pinning_d396.chain for the trapped amplitude and ρ_x/ρ_r at T_c.
Dilution: D = 1 + r_c (T_c/T_d) if T_d < T_c, else 1 (decays before it can dominate)."""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pinning_d396 as P
MP, cH = P.MP, P.cH
xE, Tx, dp = 29.598, 1.451e11, 9.335e-3
gX = 0.5
print("λ      v[GeV]   κ       m_x[GeV]  T_d[GeV]  D        ΔN*     balanced(|ΔN*|≤0.5)")
for lam in (0.004, 0.01, 0.033):
    for v in (1e9, 1e10, 1e11):
        tr, kv, A, mx, Td_grav, rc, Dg = P.chain(lam, xE, Tx, dp, v)
        for kap in (1e-6, 1e-3, 1.0):
            m = mx / MP; Gam = kap * gX**2 * m / (8 * math.pi); Td = math.sqrt(Gam / cH) * MP; Tc = v
            D = 1 + rc * Tc / Td if Td < Tc else 1.0
            dN = -math.log(D) / 3
            print(f"{lam:5.3f}  {v:8.1e}  {kap:6.0e}  {mx:9.2e}  {Td:9.2e}  {D:8.3f}  {dN:+.3f}  {abs(dN) <= 0.5}")
