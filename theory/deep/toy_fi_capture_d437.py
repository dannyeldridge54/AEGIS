"""D437 (locked PREREG_D437_FI_TOY): two-modulus toy for the D-term capture of D436. AI-assisted.
Background: radiation era (g* 106.75), T = T0 e^{−(N−N0)}; start at D367c's N − N_e = 6 line (x = 27.178, dp = dφ/dN = 0.1145,
T0 = 1.714e12 GeV); canonical φ with x = e^{cφ}, c = √(2/3); x's own energy neglected in H (Ω_kin ≤ 2×10⁻³ there, D367c).
D7 sector (switched on for x ≥ 1, i.e. throughout this window): ξ(x) = δ₁/(2x) + δ₂/x₂, δ₂ = 0.01, x₂ = 30, δ₁ = −2δ₂ x_E/x₂ with x_E = 29.6.
For ξ < 0 (x < x_E): condensate screens the D-term; soft term V = m_s² |ξ| (M_P² units, Q = 1). For ξ > 0 (x > x_E): no screening field →
D-term wall V = (g²/2) ξ², g = 0.7, so steep that it is treated as an elastic hard wall at x_E (reflection, energy conserved).
Outputs: crossing/reflection times, maximum excursion below x_E after reflection, the N (and T) at which x returns to within 10⁻³ of x_E,
final offset at N − N_e = 20, and the energy share of x's motion relative to radiation at return. Scan m_s ∈ {1e4, 1e5} GeV."""
import math
from scipy.integrate import solve_ivp
MP, gs = 2.435e18, 106.75; c = math.sqrt(2 / 3)
d2, x2, xE = 0.01, 30.0, 29.6; d1 = -2 * d2 * xE / x2
pE = math.log(xE) / c
def run(ms):
    msP = ms / MP; T0 = 1.714e12 / MP; N0 = 6.0
    H2 = lambda N: (math.pi**2 * gs / 30) * (T0 * math.exp(-(N - N0)))**4 / 3
    def Vp(p):   # dV/dφ on the soft side (x < x_E): V = m² |ξ|, ξ < 0
        x = math.exp(c * p); dxi = -d1 / (2 * x * x) * c * x   # dξ/dφ
        return msP**2 * (-dxi)            # d|ξ|/dφ = −dξ/dφ since ξ < 0
    rhs = lambda N, y: [y[1], -(3 - 2) * y[1] - Vp(y[0]) / H2(N)]   # radiation: 3 + dlnH/dN = 1
    hit = lambda N, y: y[0] - pE; hit.terminal = True; hit.direction = 1
    y = [math.log(27.178) / c, 0.1145]; N = N0; refl = []; minp_after = None; returned = None
    while N < 20.0:
        s = solve_ivp(rhs, [N, 20.0], y, events=hit, rtol=1e-9, atol=1e-13, max_step=0.05, dense_output=True)
        if s.t_events[0].size:
            N = s.t_events[0][0]; p, dp = s.y_events[0][0]; refl.append(N); y = [p - 1e-12, -abs(dp)]
            if len(refl) > 60: break
        else:
            N = 20.0; y = list(s.y[:, -1])
        # record minimum after first reflection and first return
        if refl:
            import numpy as np
            ts = np.linspace(s.t[0], s.t[-1], 400); ps = s.sol(ts)[0]
            m = ps.min(); minp_after = m if minp_after is None else min(minp_after, m)
            if returned is None and len(refl) >= 2: returned = refl[1]
    xf = math.exp(c * y[0]); xmin = math.exp(c * minp_after) if minp_after else None
    Tret = (1.714e12 * math.exp(-(returned - N0))) if returned else None
    return refl, xmin, returned, Tret, xf
if __name__ == "__main__":
    for ms in (1e4, 1e5):
        refl, xmin, Nret, Tret, xf = run(ms)
        print(f"m_s {ms:.0e} GeV: first hit of x_E at N−N_e = {refl[0]:.3f} (T = {1.714e12*math.exp(-(refl[0]-6)):.2e} GeV); "
              f"reflections up to N−N_e 20: {len(refl)}; min x after first reflection {xmin:.4f}; "
              f"first return to the wall at N−N_e = {Nret if Nret is None else round(Nret,3)} (T = {Tret if Tret is None else f'{Tret:.2e}'} GeV); "
              f"x at N−N_e 20 = {xf:.5f} (offset {xE - xf:.2e})")
