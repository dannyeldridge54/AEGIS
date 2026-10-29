"""
Sky sigils, drawn from measured data and real sky geometry.

  sky_spaceweather.svg  Sunspots (light from the Sun) against geomagnetic activity Ap (the solar wind striking Earth),
                        monthly 1932-2026, 13-month smoothed. Each solar cycle traces one loop; the loops open because
                        Earth's storms peak about 16 months after the sunspots do.
                        Data: SILSO / NOAA sunspot number; GFZ Potsdam Kp/Ap index.
  sky_equinox.svg       Geomagnetic activity by month of the year, solar cycle divided out (1932-2026). Two lobes at the
                        equinoxes, 27% above the solstices (13 sigma): the Russell-McPherron effect, set by the tilt of
                        Earth's magnetic field against the Sun's.
  sky_true13.svg        The Sun's real path through the 13 constellations crossed by the ecliptic (IAU 1930 borders,
                        approximate dates), each arc sized by the days the Sun spends there; Draco, which coils around
                        the ecliptic pole, at the centre.
"""
import hashlib, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, fish_eye, RAINBOW
from make_planet_sigils import rainbow_path, centre_mark

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_spaceweather.json")


def spaceweather(d):
    u = "sw"; s = head(u, "Space Weather: the Sun's light and Earth's storms") + frame(u, "SPACE WEATHER")
    s += '<g transform="translate(450,450)">'
    N, A = d["N"][6:-6], d["A"][6:-6]
    nlo, nhi, alo, ahi = min(N), max(N), min(A), max(A)
    pts = [(-260 + 520 * (n - nlo) / (nhi - nlo), 220 - 440 * (a - alo) / (ahi - alo)) for n, a in zip(N, A)]
    # x = sunspots (left quiet, right active); y = storms (down calm, up stormy). Each cycle is a loop.
    s += rainbow_path(pts, 1.4, u)
    s += '<text x="-260" y="250" font-family="Georgia,serif" font-size="12" fill="#ffe7a8">quiet Sun</text><text x="260" y="250" text-anchor="end" font-family="Georgia,serif" font-size="12" fill="#ffe7a8">active Sun →</text><text x="-280" y="-230" font-family="Georgia,serif" font-size="12" fill="#ffe7a8">↑ stormy Earth</text>'
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".8">'
          'sunspots × Earth\'s storms · 1932–2026 · storms lag 16 months</text></g></svg>')
    return s


def equinox(d):
    u = "eq"; s = head(u, "The Equinox Breath: Earth's storms through the year") + frame(u, "EQUINOX")
    s += '<g transform="translate(450,450)">'
    v = d["season"]; lo, hi = min(v), max(v)
    pts = []
    for i in range(361):                                     # smooth periodic interpolation through the 12 months
        x = i / 360 * 12; k = int(x) % 12; f = x - int(x)
        a, b = v[k], v[(k + 1) % 12]; val = a + (b - a) * (1 - math.cos(math.pi * f)) / 2
        r = 90 + 220 * (val - lo) / (hi - lo)
        th = 2 * math.pi * (x - 0.5) / 12 - math.pi / 2
        pts.append((r * math.cos(th), r * math.sin(th)))
    s += rainbow_path(pts, 2.2, u)
    for name, m in (("JAN", 0), ("MAR", 2), ("JUN", 5), ("SEP", 8), ("DEC", 11)):
        th = 2 * math.pi * m / 12 - math.pi / 2
        s += (f'<text x="{330*math.cos(th):.1f}" y="{330*math.sin(th)+4:.1f}" text-anchor="middle" font-family="Georgia,serif" '
              f'font-size="13" fill="#ffe7a8">{name}</text>')
    s += centre_mark(u, "⊕")
    s += ('<text y="372" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".8">'
          'storms peak at the equinoxes · 27% above the solstices</text></g></svg>')
    return s


# approximate dates the Sun enters each constellation (IAU borders), as day of year
TRUE13 = [("Capricornus", 20), ("Aquarius", 47), ("Pisces", 70), ("Aries", 108), ("Taurus", 133), ("Gemini", 172),
          ("Cancer", 201), ("Leo", 222), ("Virgo", 259), ("Libra", 303), ("Scorpius", 327), ("Ophiuchus", 333),
          ("Sagittarius", 351)]


def true13():
    u = "tz"; s = head(u, "The True Sky: thirteen constellations of the Sun's path") + frame(u, "THE TRUE SKY")
    s += '<g transform="translate(450,450)">'
    n = len(TRUE13); R0, R1 = 190, 300
    for i, (name, d0) in enumerate(TRUE13):
        d1 = TRUE13[(i + 1) % n][1] + (365 if i == n - 1 else 0)
        a0 = 2 * math.pi * d0 / 365 - math.pi / 2; a1 = 2 * math.pi * d1 / 365 - math.pi / 2
        large = 1 if (a1 - a0) > math.pi else 0
        p = lambda a, r: f"{r*math.cos(a):.1f},{r*math.sin(a):.1f}"
        col = "#ffd27a" if name == "Ophiuchus" else RAINBOW[i % 7]
        s += (f'<path d="M{p(a0,R0)} L{p(a0,R1)} A{R1},{R1} 0 {large} 1 {p(a1,R1)} L{p(a1,R0)} A{R0},{R0} 0 {large} 0 {p(a0,R0)}Z" '
              f'fill="{col}" fill-opacity="{0.55 if name=="Ophiuchus" else 0.28}" stroke="#05070f" stroke-width="2"/>')
        am = (a0 + a1) / 2; days = d1 - d0
        s += (f'<text x="{(R1+26)*math.cos(am):.1f}" y="{(R1+26)*math.sin(am)+4:.1f}" text-anchor="middle" font-family="Georgia,serif" '
              f'font-size="12" fill="{"#ffd27a" if name=="Ophiuchus" else "#e9d5ff"}">{name} {days}d</text>')
    # Draco: a coiled spiral around the ecliptic pole
    pts = [((40 + 9 * t) * math.cos(t * 1.15), (40 + 9 * t) * math.sin(t * 1.15)) for t in [k * 0.02 for k in range(620)]]
    s += rainbow_path(pts, 1.4, u)
    s += centre_mark(u, "☊")
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">'
          '13 constellations · Ophiuchus in gold · Draco coiled at the pole</text></g></svg>')
    return s


if __name__ == "__main__":
    d = json.load(open(DATA))
    out = {"sky_spaceweather.svg": spaceweather(d), "sky_equinox.svg": equinox(d), "sky_true13.svg": true13()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("\n".join(out))
