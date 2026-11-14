"""D396 (locked PREREG_D396_PINNING): Twist-2 open problem 1. Semi-analytic pinning chain, M_P = 1 units. AI-assisted.
Chain: x crosses x_E at T_x with velocity dφ/dt = H dp (D367b lines) -> thermal trap from light χ, χ̄ (m_th = g T / 2, g = λ x_E √(2/3))
-> amplitude A ∝ T (adiabatic, ω >> H) -> condensate at T_c = v gives m_x = g v -> residual oscillation energy ρ_x = ½ m_x² A(T_c)²
-> redshifts as matter until decay Γ = m_x³/(8π) -> dilution D and decay temperature T_d."""
import math
MP = 2.435e18; gs = 106.75; cH = math.sqrt(math.pi**2 * gs / 90)          # H = cH T^2 (M_P = 1)
crossings = [(29.213, 3.943e11, 2.537e-2), (29.452, 2.391e11, 1.539e-2), (29.598, 1.451e11, 9.335e-3)]  # x, T [GeV], dp (D367b)
def chain(lam, xE, Tx, dp, v):
    g = lam * xE * math.sqrt(2 / 3); T = Tx / MP; vel = cH * T * T * dp
    K, Vmax = 0.5 * vel * vel, T**4 / 4                                    # trap holds if kinetic < barrier at |Δφ| = T/g
    trapped = K < Vmax
    A0 = vel / (g * T / 2)                                                   # turnaround amplitude
    Tc = v / MP; A = A0 * Tc / T
    mx = g * Tc; rho_x = 0.5 * mx * mx * A * A; rho_r = (math.pi**2 * gs / 30) * Tc**4; r_c = rho_x / rho_r
    Gam = mx**3 / (8 * math.pi); Td = math.sqrt(Gam / cH)                   # H(T_d) = Γ (radiation)
    D = 1 + r_c * Tc / Td if Td < Tc else 1.0                                # matter-like growth until decay
    return trapped, K / Vmax, A * 1.0, mx * MP, Td * MP, r_c, D
if __name__ == "__main__":
    print("lambda  x_E    T_x[GeV]  v[GeV]  trapped K/Vmax  A(T_c)[MP]  m_x[GeV]  T_d[GeV]  rho_x/rho_r@Tc  D")
    for lam in (0.004, 0.01, 0.033):
        for xE, Tx, dp in crossings:
            for v in (1e5, 1e6, 1e7, 1e9):
                tr, kv, A, mx, Td, rc, D = chain(lam, xE, Tx, dp, v)
                print(f"{lam:6.3f} {xE:6.3f} {Tx:9.3e} {v:8.1e}  {str(tr):5s} {kv:6.3f}  {A:9.2e}  {mx:9.2e}  {Td:9.2e}  {rc:10.2e}  {D:9.2e}")
