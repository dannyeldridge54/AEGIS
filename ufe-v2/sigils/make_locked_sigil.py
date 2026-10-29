"""
The Locked Twist: the sigil and a plain chart, both drawn from the same numbers.

  locked.svg        Sigil. One turn of the circle = the universe from 100,000 to 100 (redshift), i.e. from about
                    20 years to about 17 million years after the Big Bang. The red-orange band is the share of
                    energy in light (radiation), the blue-violet band the share in matter. They cross once, at
                    matter-radiation equality: that crossing is the LOCK. The gold petal is the twisting field's
                    share (drawn 5x larger to be visible); in the Locked Twist it peaks at the crossing by rule.
  locked_chart.svg  The same three shares as an ordinary chart against years after the Big Bang.

Numbers: the free Twist best fit (Planck 2018 + DESI DR2 + Pantheon+): omega_b = 0.02261, omega_cdm = 0.12604,
H0 = 70.60, f_EDE = 0.078. Radiation: omega_r = 2.4728e-5 (1 + 0.22711 x 3.044). Field: the standard fluid
approximation for an n = 3 oscillating field (Poulin et al. 2018): energy density constant before a_c, then
falling as a^-4.5 (w = (n-1)/(n+1) = 1/2), rho = 2 rho_c / (1 + (a/a_c)^4.5), scaled so its share is f_EDE at a_c.
"""
import hashlib, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, RAINBOW, fish_eye

HERE = os.path.dirname(os.path.abspath(__file__))
wb, wc, H0, fc = 0.02261, 0.12604, 70.60, 0.078
wr = 2.4728e-5 * (1 + 0.22711 * 3.044)
wm = wb + wc
a_eq = wr / wm                                   # the lock: a_c = a_eq
h2 = (H0 / 100) ** 2

def shares(a):
    r, m = wr / a**4, wm / a**3
    rc = (wr / a_eq**4 + wm / a_eq**3) * fc / (1 - fc) / 1.0   # field density at a_c so that share(a_c) = fc
    e = 2 * rc / (1 + (a / a_eq) ** 4.5)                        # = rc at a_c
    tot = r + m + e
    return r / tot, m / tot, e / tot

def years(a):
    """Age of the universe at scale factor a (radiation + matter + Lambda; field ignored, <8%)."""
    Om, Or = wm / h2, wr / h2; OL = 1 - Om - Or
    x = np.logspace(-9, math.log10(a), 4000)
    H = H0 / 3.0857e19 * np.sqrt(Or / x**4 + Om / x**3 + OL)       # 1/s
    return np.trapezoid(1 / (x * H), x) / 3.156e7

z_eq = 1 / a_eq - 1
t_eq = years(a_eq)


def sigil():
    u = "lk"; s = head(u, "The Locked Twist: the field wakes when matter outweighs light") + frame(u, "THE LOCKED TWIST")
    s += '<g transform="translate(450,450)">'
    lz = np.linspace(5, 2, 1500)                  # log10(1+z), one full turn
    a = 1 / (10 ** lz)
    R, M, E = np.array([shares(x) for x in a]).T
    ang = (lz[0] - lz) / (lz[0] - lz[-1]) * 2 * math.pi - math.pi / 2   # start at the top, clockwise
    def ring(val, r0, r1):
        return [((r0 + (r1 - r0) * v) * math.cos(t), (r0 + (r1 - r0) * v) * math.sin(t)) for v, t in zip(val, ang)]
    def path(pts, col, w, op=0.95, glow=False):
        return (f'<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
                f'" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"' + (f' filter="url(#{u}glow)"' if glow else "") + '/>')
    # light (warm) and matter (cool) as braided bands between radius 110 and 330
    for k, off in enumerate(np.linspace(-9, 9, 4)):
        s += path(ring(R, 110 + off, 330 + off), RAINBOW[k % 3], 1.3, 0.8)
        s += path(ring(M, 110 + off, 330 + off), RAINBOW[4 + k % 3], 1.3, 0.8)
    # the field's petal, x5, in gold, mirrored inward so it reads as a petal around the lock
    on = E > 0.004
    up = [p for p, o in zip(ring(5 * E, 220, 330), on) if o]; dn = [p for p, o in zip(ring(-5 * E, 220, 330), on) if o]
    s += ('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in up + dn[::-1]) +
          f'" fill="#ffd27a" fill-opacity=".18" stroke="#ffd27a" stroke-width="2.4" filter="url(#{u}glow)"/>')
    # the lock: where light and matter cross
    i = int(np.argmin(abs(R - M))); t = ang[i]
    for rr in (220, 360):
        s += f'<circle cx="{rr*math.cos(t):.1f}" cy="{rr*math.sin(t):.1f}" r="{9 if rr==220 else 6}" fill="#fff" filter="url(#{u}glow)"/>'
    s += f'<line x1="0" y1="0" x2="{360*math.cos(t):.1f}" y2="{360*math.sin(t):.1f}" stroke="#fff" stroke-width="1" stroke-dasharray="3 6" opacity=".7"/>'
    s += (f'<text x="{360*math.cos(t)+16:.1f}" y="{360*math.sin(t)+5:.1f}" text-anchor="start" font-family="Georgia,serif" '
          f'font-size="15" fill="#ffe7a8">LOCK</text>')
    # three faint lobes for n = 3 behind the eye
    for k in range(3):
        th = k * 2 * math.pi / 3 - math.pi / 2
        s += f'<ellipse cx="{48*math.cos(th):.1f}" cy="{48*math.sin(th):.1f}" rx="46" ry="22" transform="rotate({math.degrees(th):.1f} {48*math.cos(th):.1f} {48*math.sin(th):.1f})" fill="none" stroke="#ffd27a" stroke-width="1" opacity=".55"/>'
    s += fish_eye(u, 1.0)
    s += ('<text y="-352" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">'
          'warm: light · cool: matter · gold: the field (×5)</text>')
    s += "</g></svg>"
    return s


def chart():
    W, Hh, L, Rm, T, B = 900, 540, 78, 150, 40, 70
    t = np.logspace(0, 8, 600)                    # 1 year to 100 million years
    agrid = np.logspace(-6.5, -1.3, 900); tg = np.array([years(x) for x in agrid])
    a = np.interp(np.log(t), np.log(tg), agrid)
    R, M, E = np.array([shares(x) for x in a]).T
    X = lambda tt: L + (math.log10(tt) - 0) / 8 * (W - L - Rm)
    Y = lambda v: T + (1 - (math.log10(max(v, 1e-3)) + 3) / 3) * (Hh - T - B)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" role="img" aria-label="Share of the universe\'s energy in light, matter and the twisting field, by years after the Big Bang">'
         f'<metadata>The Locked Twist chart. Theory by Danny Lee Eldridge, 2026. AEGIS.</metadata>'
         f'<rect width="{W}" height="{Hh}" rx="14" fill="#0b0720"/>')
    for v, lab in ((1, "100%"), (0.1, "10%"), (0.01, "1%"), (0.001, "0.1%")):
        s += f'<line x1="{L}" x2="{W-Rm}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#2a2350" stroke-width="1"/>'
        s += f'<text x="{L-10}" y="{Y(v)+5:.1f}" text-anchor="end" font-family="system-ui,sans-serif" font-size="13" fill="#a8a3c7">{lab}</text>'
    for tt, lab in ((1, "1 yr"), (100, "100 yr"), (1e4, "10,000 yr"), (1e6, "1 million yr"), (1e8, "100 million yr")):
        s += f'<text x="{X(tt):.1f}" y="{Hh-B+24}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" fill="#a8a3c7">{lab}</text>'
    s += f'<text x="{(L+W-Rm)/2}" y="{Hh-14}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" fill="#cfd5ee">time after the Big Bang (each step is 100 times longer)</text>'
    s += f'<text x="22" y="{(T+Hh-B)/2}" transform="rotate(-90 22 {(T+Hh-B)/2})" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" fill="#cfd5ee">share of all energy</text>'
    xe = X(t_eq)
    s += f'<line x1="{xe:.1f}" x2="{xe:.1f}" y1="{T}" y2="{Hh-B}" stroke="#fff" stroke-dasharray="4 5" opacity=".7"/>'
    s += f'<rect x="{xe+2:.1f}" y="{T+2}" width="250" height="40" rx="6" fill="#0b0720" opacity=".85"/>'
    s += (f'<text x="{xe+8:.1f}" y="{T+16}" font-family="system-ui,sans-serif" font-size="13" font-weight="700" fill="#fff">the lock: matter overtakes light</text>'
          f'<text x="{xe+8:.1f}" y="{T+33}" font-family="system-ui,sans-serif" font-size="12.5" fill="#cfd5ee">about {round(t_eq,-3):,.0f} years · redshift {z_eq:,.0f}</text>')
    for vals, col, lab in ((R, "#ff9f43", "light"), (M, "#3b9dff", "matter"), (E, "#ffd27a", "the field")):
        pts = " ".join(f"{X(tt):.1f},{Y(v):.1f}" for tt, v in zip(t, vals) if v >= 1e-3)
        s += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{3 if lab=="the field" else 2.4}"/>'
        k = len(t) - 1 if lab != "the field" else int(np.argmax(E))
        if lab == "the field":
            s += f'<text x="{X(t[k]):.1f}" y="{Y(E[k])-12:.1f}" text-anchor="start" font-family="system-ui,sans-serif" font-size="13.5" font-weight="700" fill="{col}">the field: {fc*100:.1f}% at the lock, then fades</text>'
        else:
            s += f'<text x="{W-Rm+8}" y="{Y(vals[k])+5:.1f}" font-family="system-ui,sans-serif" font-size="13.5" font-weight="700" fill="{col}">{lab}</text>'
    s += "</svg>"
    return s


if __name__ == "__main__":
    out = {"locked.svg": sigil(), "locked_chart.svg": chart()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print(f"z_eq = {z_eq:.0f}, t_eq = {t_eq:,.0f} yr; field share at the lock:", round(shares(a_eq)[2], 3))
