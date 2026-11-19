"""D1500: axion mass at horizon exit (PREREG_D1500)."""
import json, mpmath as mp
mp.mp.dps = 60
s = mp.mpf(3) / 2
def E(x, y, nmax=6):
    out = 2 * mp.zeta(2 * s) * y ** s + 2 * mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf(1) / 2) * mp.zeta(2 * s - 1) / mp.gamma(s) * y ** (1 - s)
    pref = 8 * mp.pi ** s / mp.gamma(s) * mp.sqrt(y)
    for n in range(1, nmax + 1):
        sig = sum(mp.mpf(d) ** (1 - 2 * s) for d in range(1, n + 1) if n % d == 0)
        out += pref * mp.mpf(n) ** (s - mp.mpf(1) / 2) * sig * mp.cos(2 * mp.pi * n * x) * mp.besselk(s - mp.mpf(1) / 2, 2 * mp.pi * n * y)
    return out
Er = E(mp.mpf(1) / 2, mp.sqrt(3) / 2)
def f_dilmix(al, C):
    def f(e):
        x = e - Er; P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2); return P * (1 + C * P / (1 - P))
    return f
def row(name, f, y):
    y = mp.mpf(y); x0 = mp.mpf(1) / 2
    e = E(x0, y); fp = mp.diff(f, e); V = f(e)
    Exx = mp.diff(lambda x: E(x, y), x0, 2); Exy = mp.diff(lambda x, yy: E(x, yy), (x0, y), (1, 1))
    m2H2 = 2 * y ** 2 * fp * Exx / V
    return dict(model=name, y=float(y), E_xx=mp.nstr(Exx, 6), E_xx_sign='+' if Exx > 0 else '-', E_xy=mp.nstr(Exy, 6), m2_over_H2=mp.nstr(m2H2, 6),
                stable=bool(fp * Exx > 0))
out = {"D": "D1500", "rows": []}
for name, f, y in (("DILMIX_centre_model", f_dilmix(0.375, 1.5e-6), 13.96), ("formA_A1_model", f_dilmix(1.0, 1.25e-6), 23.25),
                   ("DILMIX_centre_phys_a2e3", f_dilmix(0.375, 1.5e-6), 13.96 * 2000 ** (2 / 3))):
    r = row(name, f, y); out['rows'].append(r); print(r, flush=True)
json.dump(out, open('field_tests/results/D1500_axion_mass.json', 'w'), indent=1)
