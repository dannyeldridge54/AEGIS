"""D446 (locked PREREG_D446_CLOUD_CAPTURE). D437 integrator with the stringy FI term; remnant summed over wall hits. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
MP, gs, g = 2.435e18, 106.75, 0.7; c = math.sqrt(2/3); xE = 29.6; N0 = 6.0; T0G = 1.714e12
f = lambda x: (math.atan(x/10) - math.atan(x/400))/math.pi; C = -f(xE)
fp = lambda x: (10/(100+x*x) - 400/(160000+x*x))/math.pi
pE = math.log(xE)/c
def run(ms, r):
    msP = ms/MP; T0 = T0G/MP
    H2 = lambda N: (math.pi**2*gs/30)*(T0*math.exp(-(N-N0)))**4/3
    Vp = lambda p: msP**2*r*r*fp(math.exp(c*p))*c*math.exp(c*p)   # d(m^2 |zeta|)/dphi, |zeta| = -zeta on x<x_E, decreasing -> slope pushes toward x_E
    rhs = lambda N, y: [y[1], -y[1] + Vp(y[0])/H2(N)]
    hit = lambda N, y: y[0]-pE; hit.terminal = True; hit.direction = 1
    y = [math.log(27.178)/c, 0.1145]; N = N0; refl = []; minp = None; rem = 0.0
    while N < 20.0:
        s = solve_ivp(rhs, [N, 20.0], y, events=hit, rtol=1e-9, atol=1e-13, max_step=0.05, dense_output=True)
        if refl:
            ts = np.linspace(s.t[0], s.t[-1], 200); m = s.sol(ts)[0].min(); minp = m if minp is None else min(minp, m)
        if s.t_events[0].size:
            N = s.t_events[0][0]; p, dp = s.y_events[0][0]; refl.append(N)
            T = T0G*math.exp(-(N-N0)); H = math.sqrt(H2(N))*MP; xdot = c*xE*H*abs(dp)   # GeV
            R = g*g*fp(xE)*r*r*MP**2*xdot; m2 = (R/2)**(2/3); Vres = ms**2*m2/g**2
            sT = 2*math.pi**2/45*gs*T**3; rem += Vres/sT
            y = [p-1e-12, -abs(dp)]
            if abs(dp) < 1e-9 or len(refl) > 5000: N = 20.0; y = [pE, 0.0]; break
        else:
            N = 20.0; y = list(s.y[:, -1])
    xf = math.exp(c*y[0]); xmin = math.exp(c*minp) if minp else None
    ret = refl[1] if len(refl) > 1 else None
    return refl, xmin, ret, xf, rem
if __name__ == "__main__":
    print(f"root check: zeta(29.6) = {f(xE)+C:.1e}")
    for r in (0.03, 0.0675, 0.1, 0.3):
        for ms in (1e4, 1e5):
            refl, xmin, ret, xf, rem = run(ms, r)
            if not refl: print(f"Ms/MP={r} m_s={ms:.0e}: never reaches x_E"); continue
            Tret = f"{T0G*math.exp(-(ret-N0)):.2e}" if ret else "none"
            ok = ret is not None and abs(xE-xf) < 1e-2
            print(f"Ms/MP={r} m_s={ms:.0e}: hit N={refl[0]:.3f} T={T0G*math.exp(-(refl[0]-N0)):.2e}; reflections {len(refl)}; "
                  f"xmin {xmin if xmin is None else round(xmin,4)}; return T={Tret}; offset {xE-xf:.2e}; remnant rho/s={rem:.2e} GeV "
                  f"(x{rem/4.3e-10:.1e} DM) -> {'CAPTURES' if ok else 'FAILS TO PIN'}", flush=True)
