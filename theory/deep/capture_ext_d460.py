"""D446 (locked PREREG_D446_CLOUD_CAPTURE). D437 integrator with the stringy FI term; remnant summed over wall hits. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
MP, gs, g = 2.435e18, 106.75, 0.7; c = math.sqrt(2/3); xE = 29.6; N0 = 6.0; T0G = 1.714e12
f = lambda x: (math.atan(x/10) - math.atan(x/400))/math.pi; C = -f(xE)
fp = lambda x: (10/(100+x*x) - 400/(160000+x*x))/math.pi
pE = math.log(xE)/c
def run(ms, r, NEND=20.0):
    msP = ms/MP; T0 = T0G/MP
    H2 = lambda N: (math.pi**2*gs/30)*(T0*math.exp(-(N-N0)))**4/3
    Vp = lambda p: msP**2*r*r*fp(math.exp(c*p))*c*math.exp(c*p)   # d(m^2 |zeta|)/dphi, |zeta| = -zeta on x<x_E, decreasing -> slope pushes toward x_E
    rhs = lambda N, y: [y[1], -y[1] + Vp(y[0])/H2(N)]
    hit = lambda N, y: y[0]-pE; hit.terminal = True; hit.direction = 1
    y = [math.log(27.178)/c, 0.1145]; N = N0; refl = []; minp = None; rem = 0.0
    while N < NEND:
        s = solve_ivp(rhs, [N, NEND], y, events=hit, rtol=1e-9, atol=1e-13, max_step=0.05, dense_output=True)
        if refl:
            ts = np.linspace(s.t[0], s.t[-1], 200); m = s.sol(ts)[0].min(); minp = m if minp is None else min(minp, m)
        if s.t_events[0].size:
            N = s.t_events[0][0]; p, dp = s.y_events[0][0]; refl.append(N)
            T = T0G*math.exp(-(N-N0)); H = math.sqrt(H2(N))*MP; xdot = c*xE*H*abs(dp)   # GeV
            R = g*g*fp(xE)*r*r*MP**2*xdot; m2 = (R/2)**(2/3); Vres = ms**2*m2/g**2
            sT = 2*math.pi**2/45*gs*T**3; rem += Vres/sT
            y = [p-1e-12, -abs(dp)]
            if abs(dp) < 1e-9 or len(refl) > 5000: N = NEND; y = [pE, 0.0]; break
        else:
            N = NEND; y = list(s.y[:, -1])
    xf = math.exp(c*y[0]); xmin = math.exp(c*minp) if minp else None
    ret = refl[1] if len(refl) > 1 else None
    return refl, xmin, ret, xf, rem
if __name__ == "__main__":
    for ms, pred in ((1e-9, 2.4e2), (1e-6, 7.5e3)):
        refl, xmin, ret, xf, rem = run(ms, 1.43e-4, 32.0)
        Tr = T0G*math.exp(-(ret-N0)) if ret else None
        print(f"m_s={ms:.0e} GeV: reflections {len(refl)}, return T={Tr if Tr is None else f'{Tr:.2e}'} GeV (pred {pred:.1e}), x end {xf:.4f}; "
              f"{'RETURNS BEFORE BBN' if Tr and Tr>1e-3 else 'NO RETURN'}; {'sqrt law holds' if Tr and 0.5<Tr/pred<2 else 'sqrt law off'}", flush=True)
