"""
The Cosmic Bell: the universe's sound waves, from our own best fits (data_acoustic.json, made by acoustic_notes.py).

  bell.svg           Sigil. The CMB temperature spectrum wrapped once around a circle (multipole 2 at the top, 2500
                     clockwise). Seven gold rays mark the seven peaks ("notes"). Violet: standard model; gold: the Twist.
                     They lie on top of each other: the notes are locked.
  bell_chart.svg     The same spectrum as an ordinary chart, with the peaks numbered, and a lower panel showing the
                     Twist's difference from the standard model in percent.
  bell_triangle.svg  Why the notes stay put while H0 rises: same angle, smaller triangle. Sound ruler and distance to
                     the oldest light both shrink by about 2.9%. (Angle exaggerated so it can be seen; lengths in
                     proportion.)
"""
import hashlib, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, RAINBOW, fish_eye

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data_acoustic.json")))
ell = np.array(D["lcdm"]["ell"]); L = np.array(D["lcdm"]["tt"]); E = np.array(D["ede"]["tt"])
PK = D["ede"]["tt_peaks"]; dl, de = D["lcdm"]["derived"], D["ede"]["derived"]
FONT = 'font-family="system-ui,sans-serif"'


def bell():
    u = "bl"; s = head(u, "The Cosmic Bell: the universe's sound waves, locked in step") + frame(u, "THE COSMIC BELL")
    s += '<g transform="translate(450,450)">'
    ang = lambda l: (l - 2) / 2498 * 2 * math.pi - math.pi / 2
    rad = lambda y: 120 + 230 * y / 6000
    for l in PK:
        t = ang(l); s += f'<line x1="{110*math.cos(t):.1f}" y1="{110*math.sin(t):.1f}" x2="{365*math.cos(t):.1f}" y2="{365*math.sin(t):.1f}" stroke="#ffd27a" stroke-width="1" opacity=".55"/>'
    for k, (y, col, w, op) in enumerate(((L, "#b86bff", 9, 0.6), (E, "#ffd27a", 2, 1))):
        pts = " ".join(f"{rad(v)*math.cos(ang(l)):.1f},{rad(v)*math.sin(ang(l)):.1f}" for l, v in zip(ell, y))
        s += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"' + (f' filter="url(#{u}glow)"' if k else "") + "/>"
    for i, l in enumerate(PK):
        t = ang(l)
        s += f'<circle cx="{372*math.cos(t):.1f}" cy="{372*math.sin(t):.1f}" r="5" fill="{RAINBOW[i]}"/>'
    for r in (60, 90):
        s += f'<circle r="{r}" fill="none" stroke="#7dd3fc" stroke-width=".8" opacity=".5"/>'
    s += fish_eye(u, 1.0)
    s += (f'<text y="330" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">'
          'violet: standard model · gold: the Twist · seven notes, in the same places</text>')
    return s + "</g></svg>"


def chart():
    W, H, Lm, Rm, T = 900, 600, 78, 30, 40
    top_h, gap, bot_h = 360, 50, 110
    X = lambda l: Lm + (l - 2) / 2498 * (W - Lm - Rm)
    Y = lambda v: T + top_h * (1 - v / 6500)
    yb0 = T + top_h + gap; Yr = lambda r: yb0 + bot_h / 2 - r / 2 * (bot_h / 2)   # +-2% range
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="The CMB temperature spectrum for the standard model and the Twist, with the seven acoustic peaks at the same positions, and the percent difference below.">'
         f'<metadata>The Cosmic Bell chart. Theory by Danny Lee Eldridge, 2026. AEGIS.</metadata><rect width="{W}" height="{H}" rx="14" fill="#0b0720"/>')
    for v in (0, 2000, 4000, 6000):
        s += f'<line x1="{Lm}" x2="{W-Rm}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#2a2350"/><text x="{Lm-8}" y="{Y(v)+4:.1f}" text-anchor="end" {FONT} font-size="12" fill="#a8a3c7">{v:,}</text>'
    s += f'<text x="20" y="{T+top_h/2}" transform="rotate(-90 20 {T+top_h/2})" text-anchor="middle" {FONT} font-size="12.5" fill="#cfd5ee">loudness (μK²)</text>'
    for i, l in enumerate(PK):
        s += f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{T}" y2="{T+top_h}" stroke="#ffd27a" stroke-dasharray="2 5" opacity=".5"/>'
        k = int(np.argmin(abs(ell - l)))
        s += f'<text x="{X(l):.1f}" y="{Y(E[k])-10:.1f}" text-anchor="middle" {FONT} font-size="13" font-weight="700" fill="#ffd27a">{i+1}</text>'
    s += '<polyline points="' + " ".join(f"{X(l):.1f},{Y(v):.1f}" for l, v in zip(ell, L)) + '" fill="none" stroke="#b86bff" stroke-width="5" opacity=".5"/>'
    s += '<polyline points="' + " ".join(f"{X(l):.1f},{Y(v):.1f}" for l, v in zip(ell, E)) + '" fill="none" stroke="#ffd27a" stroke-width="1.8"/>'
    s += (f'<text x="{W-Rm-10}" y="{T+22}" text-anchor="end" {FONT} font-size="13" fill="#b86bff" font-weight="700">standard model (wide violet)</text>'
          f'<text x="{W-Rm-10}" y="{T+42}" text-anchor="end" {FONT} font-size="13" fill="#ffd27a" font-weight="700">the Twist (thin gold)</text>'
          f'<text x="{W-Rm-10}" y="{T+62}" text-anchor="end" {FONT} font-size="12.5" fill="#cfd5ee">numbers 1–7: the notes (peaks)</text>')
    # bottom panel: percent difference
    r = (E - L) / L * 100
    s += f'<rect x="{Lm}" y="{yb0}" width="{W-Lm-Rm}" height="{bot_h}" fill="#120c2c" rx="6"/>'
    for v in (-2, 0, 2):
        s += f'<line x1="{Lm}" x2="{W-Rm}" y1="{Yr(v):.1f}" y2="{Yr(v):.1f}" stroke="{"#8d96b8" if v==0 else "#2a2350"}"/><text x="{Lm-8}" y="{Yr(v)+4:.1f}" text-anchor="end" {FONT} font-size="12" fill="#a8a3c7">{v:+d}%</text>'
    s += '<polyline points="' + " ".join(f"{X(l):.1f},{Yr(max(-2.2,min(2.2,v))):.1f}" for l, v in zip(ell, r)) + '" fill="none" stroke="#ffd27a" stroke-width="1.6"/>'
    s += f'<text x="{Lm+8}" y="{yb0-10}" {FONT} font-size="12.5" fill="#cfd5ee">difference, Twist vs standard model (within half a percent across all seven notes)</text>'
    for l in (2, 500, 1000, 1500, 2000, 2500):
        s += f'<text x="{X(l):.1f}" y="{H-36}" text-anchor="middle" {FONT} font-size="12" fill="#a8a3c7">{l}</text>'
    s += f'<text x="{(Lm+W-Rm)/2}" y="{H-14}" text-anchor="middle" {FONT} font-size="12.5" fill="#cfd5ee">pitch (multipole ℓ): left = big patches of sky, right = small ones</text>'
    return s + "</svg>"


def triangle():
    W, H = 900, 430
    ox, oy = 70, 250                                           # us
    scale = 690 / dl["ra_rec"]
    half = math.radians(9)                                    # exaggerated angle so it can be seen
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Same angle, smaller triangle: the Twist shrinks both the sound ruler and the distance to the oldest light by about 2.9 percent, so the notes stay in place but the universe must expand faster.">'
         f'<metadata>The Cosmic Bell triangle. Theory by Danny Lee Eldridge, 2026. AEGIS.</metadata><rect width="{W}" height="{H}" rx="14" fill="#0b0720"/>')
    for d, col, lab, w in ((dl, "#b86bff", "standard model", 5), (de, "#ffd27a", "the Twist", 2)):
        Ld = d["ra_rec"] * scale; hh = Ld * math.tan(half)
        x = ox + Ld
        s += f'<polygon points="{ox},{oy} {x:.1f},{oy-hh:.1f} {x:.1f},{oy+hh:.1f}" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-width="{w}" opacity=".9"/>'
    for d, col, lab, dy in ((dl, "#b86bff", "standard model", -1), (de, "#ffd27a", "the Twist", 1)):
        Ld = d["ra_rec"] * scale; x = ox + Ld; hh = Ld * math.tan(half)
        ty = oy - hh - 18 if dy < 0 else oy + hh + 30
        s += (f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="end" {FONT} font-size="13.5" font-weight="700" fill="{col}">{lab}: ruler {d["rs_rec"]:.1f} Mpc, '
              f'distance {d["ra_rec"]:,.0f} Mpc</text>')
    s += (f'<circle cx="{ox}" cy="{oy}" r="6" fill="#fff"/><text x="{ox}" y="{oy+28}" text-anchor="middle" {FONT} font-size="13" fill="#fff">us</text>'
          f'<path d="M {ox+70} {oy-70*math.tan(half):.1f} A 70 70 0 0 1 {ox+70} {oy+70*math.tan(half):.1f}" fill="none" stroke="#fff" stroke-width="1.5"/>'
          f'<text x="{ox+80}" y="{oy+5}" {FONT} font-size="13" fill="#fff">same angle</text>'
          f'<text x="{ox+dl["ra_rec"]*scale+22:.1f}" y="{oy}" transform="rotate(90 {ox+dl["ra_rec"]*scale+22:.1f} {oy})" text-anchor="middle" {FONT} font-size="12.5" fill="#cfd5ee">the oldest light (CMB)</text>')
    rr = de["rs_rec"] / dl["rs_rec"] - 1; rd = de["ra_rec"] / dl["ra_rec"] - 1
    s += (f'<text x="24" y="34" {FONT} font-size="15" font-weight="700" fill="#e9ecf8">Same angle, smaller triangle</text>'
          f'<text x="24" y="56" {FONT} font-size="13" fill="#cfd5ee">Ruler {rr*100:+.1f}%, distance {rd*100:+.1f}%: the angle, and so every note, stays put.</text>'
          f'<text x="24" y="75" {FONT} font-size="13" fill="#cfd5ee">A shorter distance to the same light means a faster expansion: H₀ {D["lcdm"]["H0"]} → {D["ede"]["H0"]} km/s per Mpc.</text>'
          f'<text x="24" y="{H-16}" {FONT} font-size="11.5" fill="#8d96b8">Angle drawn 30 times larger than the real 0.6° so it can be seen; lengths in true proportion. Mpc = megaparsec, about 3.26 million light-years.</text>')
    return s + "</svg>"


if __name__ == "__main__":
    out = {"bell.svg": bell(), "bell_chart.svg": chart(), "bell_triangle.svg": triangle()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("peaks", PK)
