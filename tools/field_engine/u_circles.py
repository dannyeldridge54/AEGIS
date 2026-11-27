"""D2263: flip symmetry on u-circles at rho and i (see PREREG_D2263)."""
import json, math
import mpmath as mp
mp.mp.dps = 30
def _E(x, y, s, nmax=30):
    x, y, s = mp.mpf(x), mp.mpf(y), mp.mpf(s)
    xi = lambda t: mp.pi**(-t/2)*mp.gamma(t/2)*mp.zeta(t)
    v = y**s + xi(2*s-1)/xi(2*s)*y**(1-s)
    for n in range(1, nmax+1):
        sig = sum(mp.mpf(d)**(1-2*s) for d in range(1, n+1) if n % d == 0)
        v += 4*mp.sqrt(y)/xi(2*s)*mp.mpf(n)**(s-0.5)*sig*mp.besselk(s-0.5, 2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return v
mp.mp.dps = 30
out = {}
pts = {'rho': mp.mpc(-0.5, mp.sqrt(3)/2), 'i': mp.mpc(0, 1)}
for name, t0 in pts.items():
    for s in (2, mp.mpf(3)/2):
        for r in (0.02, 0.05):
            th = [2*mp.pi*k/72 for k in range(72)]; v = []
            for t in th:
                u = r*mp.expj(t); z = (t0 - u*mp.conj(t0))/(1 - u); v.append(_E(z.real, z.imag, s))
            m = sum(v)/72
            c = {n: 2*sum((v[k]-m)*mp.expj(-n*th[k]) for k in range(72))/72 for n in (1, 2, 3, 4, 6)}
            lead = 3 if name == 'rho' else 2
            d = {f"|c{n}|": float(abs(c[n])) for n in c}
            d.update(lead=lead, arg_lead_over_pi_div_n=float(mp.arg(c[lead])/(mp.pi/lead)),
                     others_over_lead={n: float(abs(c[n])/abs(c[lead])) for n in c if n % lead})
            out[f"{name}_s{float(s)}_r{r}"] = d
        a, b = out[f"{name}_s{float(s)}_r0.02"], out[f"{name}_s{float(s)}_r0.05"]
        k = f"|c{a['lead']}|"; out[f"{name}_s{float(s)}_exponent"] = math.log(b[k]/a[k])/math.log(0.05/0.02)
json.dump(out, open('field_tests/results/d2263_u_circles.json', 'w'), indent=1)
for k, v in out.items(): print(k, v)
