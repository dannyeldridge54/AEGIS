"""D2262: triangular (r^3 cos 3theta) shape of the E(tau,s) bowl at rho (see PREREG_D2262)."""
import json, sys, math
import mpmath as mp
def _E(x, y, s, nmax=30):
    x, y, s = mp.mpf(x), mp.mpf(y), mp.mpf(s)
    xi = lambda t: mp.pi**(-t/2)*mp.gamma(t/2)*mp.zeta(t)
    v = y**s + xi(2*s-1)/xi(2*s)*y**(1-s)
    for n in range(1, nmax+1):
        sig = sum(mp.mpf(d)**(1-2*s) for d in range(1, n+1) if n % d == 0)
        v += 4*mp.sqrt(y)/xi(2*s)*mp.mpf(n)**(s-0.5)*sig*mp.besselk(s-0.5, 2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return v
mp.mp.dps = 30
rho = mp.mpc(-0.5, mp.sqrt(3)/2); out = {}
for s in (2, mp.mpf(3)/2):
    for r in (0.02, 0.01):
        th = [2*mp.pi*k/72 for k in range(72)]
        v = []
        for t in th:
            z = rho + r*mp.expj(t); v.append(_E(z.real, z.imag, s))
        m = sum(v)/72
        c = {n: 2*sum((v[k]-m)*mp.expj(-n*th[k]) for k in range(72))/72 for n in (1, 2, 3)}
        # E(theta) ~ |c3| cos(3 theta + arg c3): minima where 3 theta + arg c3 = pi (mod 2 pi)
        a3 = float(mp.arg(c[3])); mins = sorted(((math.pi - a3)/3 + 2*math.pi*k/3) % (2*math.pi) for k in range(3))
        out[f"s{float(s)}_r{r}"] = dict(c1=float(abs(c[1])), c2=float(abs(c[2])), c3=float(abs(c[3])),
            c1_over_c3=float(abs(c[1])/abs(c[3])), c2_over_c3=float(abs(c[2])/abs(c[3])),
            minima_deg=[round(math.degrees(x), 4) for x in mins])
json.dump(out, open('field_tests/results/d2262_rho_triangle.json', 'w'), indent=1)
for k, v in out.items(): print(k, v)
