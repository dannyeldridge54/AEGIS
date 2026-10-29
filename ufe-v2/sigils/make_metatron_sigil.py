"""
Metatron's Cube, drawn from exact geometry (a LENS, Tier 2/3: a shape that tells us where to look, not a result).

13 equal circles of radius r: one at the centre, six at distance 2r, six at distance 4r on the same six directions
(the "Fruit of Life"). Every centre is joined to every other: 13 x 12 / 2 = 78 straight lines.
Highlighted inside the lines:
  gold    the hexagram (two triangles on the outer six centres): the Seal of Solomon, also the star in the Hermit's lantern
  cyan    the hexagon outline plus three spokes to alternate corners: a cube seen corner-on
  pink    one triangle on the inner six: the outline of a tetrahedron seen from above
Nothing here is adjustable: given one circle, the whole figure follows.
"""
import hashlib, itertools, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, RAINBOW, fish_eye

HERE = os.path.dirname(os.path.abspath(__file__))


def metatron():
    u = "mt"; s = head(u, "Metatron's Cube: thirteen circles, seventy-eight lines") + frame(u, "METATRON'S CUBE")
    s += '<g transform="translate(450,450)">'
    r = 62
    P = [(0.0, 0.0)]
    for d in (2 * r, 4 * r):
        for k in range(6):
            a = math.radians(90 + 60 * k)
            P.append((d * math.cos(a), -d * math.sin(a)))
    pairs = list(itertools.combinations(range(13), 2))
    for i, (p, q) in enumerate(pairs):
        (x0, y0), (x1, y1) = P[p], P[q]
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{RAINBOW[i % 7]}" stroke-width=".7" opacity=".45"/>'
    for i, (x, y) in enumerate(P):
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="#e9d5ff" stroke-width="1" opacity=".55"/>'
    outer, inner = P[7:], P[1:7]
    poly = lambda pts, col, w, op=1: (f'<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
                                      f'" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}" filter="url(#{u}glow)"/>')
    s += poly(outer[0::2], "#ffd27a", 2.6) + poly(outer[1::2], "#ffd27a", 2.6)               # the hexagram
    s += poly(inner, "#7dd3fc", 2.2)                                                        # hexagon
    for k in (0, 2, 4):                                                                     # cube spokes
        s += f'<line x1="0" y1="0" x2="{inner[k][0]:.1f}" y2="{inner[k][1]:.1f}" stroke="#7dd3fc" stroke-width="2.2" filter="url(#{u}glow)"/>'
    s += poly(inner[1::2], "#ff7ab8", 1.8, .9)                                              # tetrahedron outline
    for x, y in P:
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#fff"/>'
    s += fish_eye(u, 0.55)
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">'
          'gold: the hexagram · cyan: a cube · pink: a tetrahedron · 13 circles, 78 lines</text>')
    return s + "</g></svg>"


if __name__ == "__main__":
    out = {"metatron.svg": metatron()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("lines:", 13 * 12 // 2)
