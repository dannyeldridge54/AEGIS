"""
Lens sigils: shapes from real equations that we use as LENSES (ideas to test), not as results.

  lens_issflip.svg   The ISS "flipping wing nut" (Dzhanibekov effect / tennis-racket theorem). Euler's equations for a
                     body with three different moments of inertia (1 : 2 : 3). Each closed curve is one possible spin;
                     the gold figure-eight (separatrix) is the knife-edge where spin about the middle axis flips over and
                     back forever.
  lens_dynamo.svg    The Rikitake dynamo: two coupled spinning discs that make a magnetic field. It reverses its own
                     north and south irregularly (mu = 2, a = 5): 278 flips in 2,000 time units.
  lens_mixmaster.svg The "mixmaster" early universe (Belinsky-Khalatnikov-Lifshitz): near the Big Bang space stretches
                     along one axis and squeezes along others, then switches axes. Each epoch is a point on the Kasner
                     circle; chords join successive epochs (u -> u - 1, or u -> 1/(u - 1) when the axes swap).
  lens_skirt.svg     The Sun's "ballerina skirt": the heliospheric current sheet, where the Sun's magnetic field flips
                     sign, tilted 15 degrees and wound into a Parker spiral by the Sun's 25.4-day rotation and a
                     400 km/s solar wind. Drawn out to Saturn's distance, seen from above at a slant.
"""
import hashlib, json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, RAINBOW
from make_planet_sigils import rainbow_path, centre_mark

HERE = os.path.dirname(os.path.abspath(__file__))


def note(text):
    return f'<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">{text}</text>'


def issflip():
    u = "is"; s = head(u, "The Flip: the three-axis spin seen on the ISS") + frame(u, "THE FLIP")
    s += '<g transform="translate(450,450)">'
    I = np.array([1., 2., 3.])
    rhs = lambda t, w: [(I[1]-I[2])*w[1]*w[2]/I[0], (I[2]-I[0])*w[2]*w[0]/I[1], (I[0]-I[1])*w[0]*w[1]/I[2]]
    R = 280
    ax, ay = math.radians(28), math.radians(-32)
    Rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    Ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]])
    M = Ry @ Rx
    def draw(L, col, width, glow=False):
        out = ""; cur = []; front = None
        for v in L:
            v = M @ (v / np.linalg.norm(v)); f = v[2] >= 0
            if front is None: front = f
            if f != front and cur:
                out += ('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in cur) +
                        f'" fill="none" stroke="{col}" stroke-width="{width}" opacity="{0.95 if front else 0.22}"' +
                        (f' filter="url(#{u}glow)"' if glow and front else "") + "/>")
                cur = []; front = f
            cur.append((R * v[0], -R * v[1]))
        if cur:
            out += ('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in cur) +
                    f'" fill="none" stroke="{col}" stroke-width="{width}" opacity="{0.95 if front else 0.22}"/>')
        return out
    k = 0
    for axis, other in ((0, 2), (2, 0)):                         # stable spins around the long and short axes
        for ang in np.linspace(0.15, 1.35, 5):
            w0 = np.zeros(3); w0[axis] = math.cos(ang); w0[other] = math.sin(ang); w0[1] = 0.05
            for sign in (1, -1):
                sol = solve_ivp(rhs, (0, 40), sign * w0, max_step=0.02, rtol=1e-9)
                s += draw((I[:, None] * sol.y).T, RAINBOW[k % 7], 1.3)
            k += 1
    sol = solve_ivp(rhs, (0, 140), [1e-3, 1, 1e-3], max_step=0.01, rtol=1e-11)
    s += draw((I[:, None] * sol.y).T, "#ffd27a", 2.6, True)
    s += f'<circle r="{R}" fill="none" stroke="#7dd3fc" stroke-width="1" opacity=".45"/>'
    s += centre_mark(u, "⟳") + note("gold: spin about the middle axis, flipping over and back forever") + "</g></svg>"
    return s


def dynamo():
    u = "dy"; s = head(u, "The Flipping Dynamo: a field that reverses itself") + frame(u, "THE DYNAMO")
    s += '<g transform="translate(450,450)">'
    mu, a = 2.0, 5.0
    rhs = lambda t, v: [-mu*v[0] + v[2]*v[1], -mu*v[1] + (v[2]-a)*v[0], 1 - v[0]*v[1]]
    sol = solve_ivp(rhs, (0, 300), [1, 0.5, 1], max_step=0.01, rtol=1e-9)
    x, z = sol.y[0][3000:], sol.y[2][3000:]
    sx = 280 / max(abs(x)); zm = (z.max() + z.min()) / 2; sz = 280 / (z.max() - z.min()) * 2
    pts = [(xx * sx, -(zz - zm) * sz * 0.5) for xx, zz in zip(x, z)]
    s += rainbow_path(pts, 0.9, u)
    s += '<line x1="0" y1="-300" x2="0" y2="300" stroke="#ffd27a" stroke-width="1" stroke-dasharray="3 6" opacity=".6"/>'
    s += ('<text x="-250" y="-280" font-family="Georgia,serif" font-size="13" fill="#ffe7a8">south up</text>'
          '<text x="250" y="-280" text-anchor="end" font-family="Georgia,serif" font-size="13" fill="#ffe7a8">north up</text>')
    s += centre_mark(u, "⇅") + note("two lobes: the field's two directions; each crossing is a flip") + "</g></svg>"
    return s


def mixmaster():
    u = "mx"; s = head(u, "The Mixmaster: the early universe switching axes") + frame(u, "MIXMASTER")
    s += '<g transform="translate(450,450)">'
    R = 280
    def kasner(uu):
        d = 1 + uu + uu * uu
        return (-uu / d, (1 + uu) / d, uu * (1 + uu) / d)
    def point(p, axes):
        q = [0, 0, 0]
        for k, ax in enumerate(axes):
            q[ax] = p[k]
        x = (q[1] - q[0]) / math.sqrt(2); y = (2 * q[2] - q[0] - q[1]) / math.sqrt(6)   # project onto the Kasner plane
        r = math.hypot(x, y) or 1
        return (R * x / r * 1.0, -R * y / r * 1.0)
    uu = math.pi; axes = [0, 1, 2]; pts = []
    for k in range(400):
        pts.append(point(kasner(uu), axes))
        if uu >= 2:
            uu -= 1; axes = [axes[1], axes[0], axes[2]]           # oscillation: two axes trade roles
        else:
            uu = 1 / (uu - 1); axes = [axes[2], axes[0], axes[1]]  # new era: the axes rotate
        if uu > 1e6:
            uu = math.pi + k * 0.618
    s += f'<circle r="{R}" fill="none" stroke="#7dd3fc" stroke-width="1.2" opacity=".6"/>'
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{RAINBOW[i % 7]}" stroke-width=".7" opacity=".55"/>'
    for x, y in pts[:60]:
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="#fff" opacity=".9"/>'
    s += centre_mark(u, "✶") + note("each chord is a switch of the stretching axis") + "</g></svg>"
    return s


def skirt():
    u = "sk"; s = head(u, "The Ballerina Skirt: where the Sun's field flips") + frame(u, "THE SKIRT")
    s += '<g transform="translate(450,450)">'
    tilt = math.radians(15); wind = 2 * math.pi / 25.4 * 1.496e8 / 400 / 86400   # radians of winding per AU
    view = math.radians(62)
    for k, r in enumerate(np.linspace(0.4, 9.5, 46)):
        pts = []
        for ph in np.linspace(0, 2 * math.pi, 240):
            z = r * math.tan(tilt) * math.sin(ph + wind * r)      # sheet height above the Sun's equator
            x, y = r * math.cos(ph), r * math.sin(ph)
            sc = 29
            pts.append((sc * x, sc * (y * math.cos(view) - z * math.sin(view)) * 1.0))
        s += ('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
              f'" fill="none" stroke="{RAINBOW[k % 7]}" stroke-width="1" opacity=".75"/>')
    s += f'<circle r="16" fill="url(#{u}core)"/><circle r="6" fill="#fff" filter="url(#{u}glow)"/>'
    s += ('<text y="-40" text-anchor="middle" font-family="Segoe UI Symbol,DejaVu Sans,serif" font-size="24" fill="#ffd27a">☉</text>')
    s += note("the Sun's field flips across this sheet; Earth rides above and below it") + "</g></svg>"
    return s


if __name__ == "__main__":
    out = {"lens_issflip.svg": issflip(), "lens_dynamo.svg": dynamo(), "lens_mixmaster.svg": mixmaster(), "lens_skirt.svg": skirt()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("\n".join(out))
