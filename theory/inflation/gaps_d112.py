"""D112-D114: (A) the two dark-matter routes combined; (B) field-distance timeline vs a tower of light states (distance conjecture);
(C) initial conditions on the plateau (kinetic-dominated and off-attractor starts). Reshaped cliff (exp, m2 = 4/pi), heat 0.8%. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
import cliff_v2 as C
lnV, Fc = C.version("exp", 4 / math.pi); c = C.c; MP = 2.435e18; TRH = 4e14
inf = C.inflation(lnV); ps, pe = inf["pstar"], inf["pend"]
print(f"inflation: N* {inf['N']:.1f}, n_s {inf['ns']:.4f}, CMB point p* {ps:.2f} (x {math.exp(c*ps):.2e}), end p {pe:.2f} (x {math.exp(c*pe):.2f})")

# (A) both dark-matter routes make the same gravity-only particle; yields add, so 1/m = 1/m_freeze-in + 1/m_bremsstrahlung
print("\n(A) dark matter, both routes together (heat 0.8%; freeze-in scaled from dm_kination.txt as f^-0.45):")
for mf in (4.7e7, 2.6e8):
    for mb in (1e5, 5e5):
        m = 1 / (1 / mf + 1 / mb); print(f"  freeze-in alone {mf:.1e}, bremsstrahlung alone {mb:.0e} -> combined {m:.2e} GeV; bremsstrahlung share {mf/(mf+mb):.4f}")

# (B) field distance after inflation, with the bath temperature at each step
V = lambda p: math.exp(lnV(p)) if lnV(p) > -700 else 0.0
def rhs(t, z):
    p, dp = z; K = 0.5 * dp * dp; return [dp, -(3 - K) * dp - V(p) * C.DL(p) / (V(p) / (3 - K))]
end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
s = solve_ivp(rhs, [0, 4000], [-13.0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp); f = 0.008; lnr = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
def rhs2(t, z):
    p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp; Vp = V(p); H2 = (Vp + rr) / (3 - K); e = K + (2 / 3) * rr / H2
    return [dp, -(3 - e) * dp - Vp * C.DL(p) / H2, -4.0]
s2 = solve_ivp(rhs2, [0, 40], [p, dp, lnr], rtol=1e-8, atol=1e-12, dense_output=True, method="LSODA")
pf = s2.y[0, -1]; print(f"\n(B) distance: CMB point -> end of inflation {pe-ps:.2f} M_P; end -> frozen {pf-pe:.2f} M_P (x frozen {math.exp(c*pf):.0f}); total {pf-ps:.2f} M_P")
for N in (0.5, 1, 2, 3, 5, 10):
    pN = s2.sol(N)[0]; T = TRH * math.exp(-N); dist = pN - ps
    tow = {lam: MP * math.exp(-lam * dist) for lam in (1 / math.sqrt(2), math.sqrt(2 / 3), 1.0)}
    print(f"  N={N:>4} after end: travelled {dist:5.2f} M_P, T ~ {T:.1e} GeV; tower mass (from M_P at CMB point) "
          + ", ".join(f"lam {l:.2f}: {m:.1e}" for l, m in tow.items()))
print("  (tower mass must stay above T and H, else new light states appear in the bath / the 4d theory breaks down)")

# (C) initial conditions: start at p0 with kinetic share K0 (of 3), moving toward the cliff (+) or up the plateau (-)
print("\n(C) initial conditions (e-folds of inflation N_tot; on attractor at the CMB point if |dp/dp_sr - 1| small):")
def run(p0, K0, sign):
    def r(t, z):
        p, dp = z; K = 0.5 * dp * dp; Vp = V(p); return [dp, -(3 - K) * dp - Vp * C.DL(p) / (Vp / (3 - K))]
    sol = solve_ivp(r, [0, 3000], [p0, sign * math.sqrt(2 * K0)], events=end, rtol=1e-9, atol=1e-12, dense_output=True, method="LSODA")
    Nt = sol.t_events[0][-1] if len(sol.t_events[0]) else float("nan")
    # first crossing of the CMB point on the way down
    ts = np.linspace(0, Nt, 20000); pp = sol.sol(ts)[0]; i = np.argmax(pp >= ps)
    att = sol.sol(ts[i])[1] / (-C.DL(ps)) if pp[i] >= ps else float("nan")
    return Nt, Nt - ts[i], att
for p0 in (-30, -25, -20, -16, -13):
    row = []
    for K0, sg in ((0.0, 1), (2.97, 1), (2.97, -1), (2.9997, 1)):
        Nt, Nafter, att = run(p0, K0, sg); row.append(f"K0 {K0}{'+' if sg>0 else '-'}: N_tot {Nt:6.1f}, from CMB pt {Nafter:5.1f}, v/v_sr {att:.3f}")
    print(f" p0 {p0} (x {math.exp(c*p0):.1e}): " + " | ".join(row))
