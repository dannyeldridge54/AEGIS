"""
Planet sigils: each planet's real dance as seen from Earth, plus the Moon's 19-year star and the asteroid belt
carved by Jupiter's locks. Every curve is computed from orbital periods; nothing is drawn by hand.

  Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune: the planet's path relative to Earth over the time it takes
      the pattern to (nearly) close. Each backward loop is one retrograde season. Circular orbits are assumed, so
      shapes are true to rhythm, approximate in exact size.
  Earth: the Metonic star. 235 new moons fall on almost the same calendar dates every 19 years; joining each new moon
      to the next around the year gives the star polygon {235/19}.
  Asteroid belt: a ring of 2,000 orbits between 2.0 and 3.4 AU, with the Kirkwood gaps cut where an asteroid would
      lock with Jupiter (4:1, 3:1, 5:2, 7:3, 2:1). Gap positions a = a_J (q/p)^(2/3).

Writes planet_<name>.svg and adds their fingerprints to hashes.json.
"""
import hashlib, json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, fish_eye, RAINBOW, AUTHOR, YEAR

HERE = os.path.dirname(os.path.abspath(__file__))
# sidereal period (yr), semi-major axis (AU), J2000 mean longitude (deg)
PL = {"Mercury": (0.2408467, 0.387, 252.25), "Venus": (0.61519726, 0.723, 181.98), "Earth": (1.0000174, 1.0, 100.46),
      "Mars": (1.8808476, 1.524, 355.45), "Jupiter": (11.862615, 5.203, 34.40), "Saturn": (29.447498, 9.537, 49.94),
      "Uranus": (84.016846, 19.19, 313.23), "Neptune": (164.79132, 30.07, 304.88)}
# years for the pattern to (nearly) close, and the glyph shown at the centre
CYCLE = {"Mercury": 7.0, "Venus": 8.0, "Mars": 15.0, "Jupiter": 12.0, "Saturn": 29.5, "Uranus": 84.0, "Neptune": 165.0}
GLYPH = {"Mercury": "☿", "Venus": "♀", "Earth": "⊕", "Mars": "♂", "Jupiter": "♃", "Saturn": "♄", "Uranus": "♅", "Neptune": "♆", "Belt": "⚳"}


def pos(name, t):
    P, a, L0 = PL[name]; th = math.radians(L0 + 360 * (t - 2000) / P)
    return a * math.cos(th), a * math.sin(th)


def rainbow_path(pts, width=1.5, glow=None):
    """Draw a path in short segments coloured through the spectrum, so time reads as colour."""
    out, n, steps = "", len(pts), len(RAINBOW)
    for k in range(steps):
        seg = pts[k * n // steps: (k + 1) * n // steps + 1]
        out += ('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in seg) +
                f'" fill="none" stroke="{RAINBOW[k]}" stroke-width="{width}" stroke-linejoin="round"' +
                (f' filter="url(#{glow}glow)"' if glow else "") + "/>")
    return out


def centre_mark(u, glyph):
    return (f'<circle r="34" fill="url(#{u}core)"/>' + fish_eye(u, 0.62) +
            f'<text y="-46" text-anchor="middle" font-family="Segoe UI Symbol,DejaVu Sans,serif" font-size="26" fill="#ffd27a" filter="url(#{u}glow)">{glyph}</text>')


def planet_sigil(name):
    u = name[:2].lower()
    s = head(u, f"{name}: its dance as seen from Earth") + frame(u, name.upper())
    s += '<g transform="translate(450,450)">'
    T, N = CYCLE[name], 6000
    pts = []
    for i in range(N + 1):
        t = 2000 + T * i / N
        xp, yp = pos(name, t); xe, ye = pos("Earth", t)
        pts.append((xp - xe, -(yp - ye)))
    R = max(math.hypot(x, y) for x, y in pts); sc = 300 / R
    pts = [(x * sc, y * sc) for x, y in pts]
    s += rainbow_path(pts, 1.6, u)
    loops = round(T * abs(1 / PL[name][0] - 1))                 # synodic periods in the cycle = retrograde loops
    s += centre_mark(u, GLYPH[name])
    s += (f'<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".8">'
          f'{T:g} years · {loops} loops</text>')
    s += "</g></svg>"
    return s


def earth_sigil():
    """The Metonic cycle: each new moon is placed at its date in the year (angle) and its year (radius).
    After 19 years (235 new moons) the dates line up again, so the spiral's spokes realign."""
    u = "ea"
    s = head(u, "Earth: the 19-year Metonic spiral of the Moon") + frame(u, "EARTH")
    s += '<g transform="translate(450,450)">'
    syn, yr = 29.530589, 365.2422
    pts = []
    for k in range(236 * 8 + 1):                                  # draw the path between new moons smoothly
        days = k * syn / 8
        frac = (days % yr) / yr; year = days / yr
        r = 70 + 12.6 * year; ang = 2 * math.pi * frac - math.pi / 2
        pts.append((r * math.cos(ang), r * math.sin(ang)))
    s += rainbow_path(pts, 0.9)
    for k in range(236):                                          # the new moons themselves
        days = k * syn; frac = (days % yr) / yr; r = 70 + 12.6 * days / yr; ang = 2 * math.pi * frac - math.pi / 2
        s += f'<circle cx="{r*math.cos(ang):.1f}" cy="{r*math.sin(ang):.1f}" r="2.2" fill="#fff" opacity=".85"/>'
    s += centre_mark(u, GLYPH["Earth"])
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".8">'
          '235 new moons · 19 years · the dates return</text></g></svg>')
    return s


def belt_sigil():
    u = "be"
    s = head(u, "The Asteroid Belt: carved by Jupiter's locks") + frame(u, "THE BELT")
    s += '<g transform="translate(450,450)">'
    aJ = 5.203
    gaps = {"4:1": (4, 1), "3:1": (3, 1), "5:2": (5, 2), "7:3": (7, 3), "2:1": (2, 1)}
    gap_a = {k: aJ * (q / p) ** (2 / 3) for k, (p, q) in gaps.items()}
    rnd = random.Random(7); sc = lambda a: (a - 1.7) / (3.5 - 1.7) * 300 + 20
    dots = []
    while len(dots) < 4200:
        a = rnd.uniform(2.0, 3.4)
        if any(abs(a - g) < 0.055 for g in gap_a.values()):    # resonance clears its lane
            continue
        th = rnd.uniform(0, 2 * math.pi); r = sc(a)
        col = RAINBOW[min(6, int((a - 2.0) / 1.4 * 7))]
        dots.append(f'<circle cx="{r*math.cos(th):.1f}" cy="{r*math.sin(th):.1f}" r="1.1" fill="{col}" opacity=".8"/>')
    s += "".join(dots)
    for k, a in gap_a.items():
        r = sc(a)
        s += f'<circle r="{r:.1f}" fill="none" stroke="#ffd27a" stroke-width=".6" stroke-dasharray="2 6" opacity=".7"/>'
        s += f'<text x="0" y="{-r + 4:.1f}" text-anchor="middle" font-family="Georgia,serif" font-size="12" fill="#ffe7a8" style="paint-order:stroke" stroke="#0b0620" stroke-width="3">{k}</text>'
    s += centre_mark(u, GLYPH["Belt"])
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".8">'
          'gaps at 4:1 · 3:1 · 5:2 · 7:3 · 2:1 with Jupiter</text></g></svg>')
    return s


if __name__ == "__main__":
    out = {f"planet_{n.lower()}.svg": planet_sigil(n) for n in CYCLE}
    out["planet_earth.svg"] = earth_sigil(); out["planet_belt.svg"] = belt_sigil()
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("\n".join(sorted(out)))
