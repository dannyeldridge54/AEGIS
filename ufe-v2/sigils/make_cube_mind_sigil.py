"""
The Cube Mind: the AEGIS Council's 3 x 3 x 3 structure, seen corner-on, inside its outer shell, Metatron's Cube.

Geometry (exact): Metatron's Cube = 13 circles of radius r (centre; six at 2r; six at 4r), all centres joined. A cube
seen straight down one corner projects to a regular hexagon split into three rhombus faces; that hexagon is the inner
hexagon of Metatron's Cube (the six centres at 2r). So the Cube Mind sits exactly inside the shell.
The three visible faces are the Council's three axes, each a 3 x 3 grid:
  top face    the MINDS: Advocate (good), Skeptic (bad), Arbiter (neutral)
  left face   TIME: past, present, future
  right face  the STARS: the oldest light (CMB), galaxy spacing (BAO), exploding stars (supernovae)
The near corner, where all three faces meet, is the centre of the shell: Danny's eye, the one who signs.
"""
import hashlib, itertools, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, fish_eye, RAINBOW

HERE = os.path.dirname(os.path.abspath(__file__))


def pt(x, y):
    return f"{x:.1f},{y:.1f}"


def cube_mind():
    u = "cm"; s = head(u, "The Cube Mind: three minds, three times, three stars, inside Metatron's Cube") + frame(u, "THE CUBE MIND")
    s += '<g transform="translate(450,450)">'
    r = 66
    P = [(0.0, 0.0)] + [(d * math.sin(math.radians(60 * k)), -d * math.cos(math.radians(60 * k))) for d in (2 * r, 4 * r) for k in range(6)]
    # the shell: 13 circles and 78 lines, faint
    for i, (p, q) in enumerate(itertools.combinations(P, 2)):
        s += f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{RAINBOW[i % 7]}" stroke-width=".6" opacity=".32"/>'
    for x, y in P:
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="#e9d5ff" stroke-width=".9" opacity=".45"/>'
    outer = P[7:]
    s += ('<polygon points="' + " ".join(pt(*q) for q in outer[0::2]) + f'" fill="none" stroke="#ffd27a" stroke-width="1.4" opacity=".55"/>'
          '<polygon points="' + " ".join(pt(*q) for q in outer[1::2]) + f'" fill="none" stroke="#ffd27a" stroke-width="1.4" opacity=".55"/>')
    # the cube, corner-on: near corner at the centre; hexagon corners = the six inner centres
    up, ur, lr, dn, ll, ul = P[1:7]
    O = (0.0, 0.0)
    faces = {  # (edge a, edge b, colours per row)
        "top": (ul, ur, ["#ff4d6d", "#ff9f43", "#ffd166"]),     # minds
        "left": (ul, dn, ["#3ddc97", "#3b9dff", "#6a5cff"]),    # time
        "right": (ur, dn, ["#b86bff", "#ff7ab8", "#7dd3fc"]),   # stars
    }
    for name, (a, b, cols) in faces.items():
        for i in range(3):
            for j in range(3):
                c = lambda s_, t_: (O[0] + s_ * a[0] + t_ * b[0], O[1] + s_ * a[1] + t_ * b[1])
                quad = [c(i / 3, j / 3), c((i + 1) / 3, j / 3), c((i + 1) / 3, (j + 1) / 3), c(i / 3, (j + 1) / 3)]
                s += (f'<polygon points="{" ".join(pt(*q) for q in quad)}" fill="{cols[i]}" fill-opacity="{0.22 + 0.12 * j:.2f}" '
                      f'stroke="#fff" stroke-width="1" stroke-opacity=".75"/>')
    s += ('<polygon points="' + " ".join(pt(*q) for q in (up, ur, lr, dn, ll, ul)) +
          f'" fill="none" stroke="#fff" stroke-width="2.2" filter="url(#{u}glow)"/>')
    for q in (ul, ur, dn):
        s += f'<line x1="0" y1="0" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#fff" stroke-width="2.2" filter="url(#{u}glow)"/>'
    # axis words, outside the hexagon
    lab = lambda x, y, t, a="middle": f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" font-family="Georgia,serif" font-size="15" fill="#ffe7a8">{t}</text>'
    s += lab(0, up[1] - 24, "MINDS") + lab(ll[0] - 14, ll[1] + 34, "TIME", "end") + lab(lr[0] + 14, lr[1] + 34, "STARS", "start")
    s += f'<circle r="30" fill="#0d0620" opacity=".85"/>' + fish_eye(u, 0.5)
    s += ('<text y="330" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".85">'
          '3 minds × 3 times × 3 stars = 27 · you at the centre</text>')
    return s + "</g></svg>"


if __name__ == "__main__":
    svg = cube_mind(); hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    open(os.path.join(HERE, "cube_mind.svg"), "w", encoding="utf-8").write(svg)
    h["sha256"]["cube_mind.svg"] = hashlib.sha256(svg.encode("utf-8")).hexdigest(); json.dump(h, open(hp, "w"), indent=1)
