"""
Sigils for Danny Lee Eldridge's theories, drawn from the mathematics each one is about.
Style follows Danny's own unified sigil ("The Open Eye"): deep violet field, rainbow rings, glowing linework,
his fish-eye mark at the centre, an ultraviolet dashed edge. Every curve below is computed from the theory's
own equation, so the picture is the math.

Writes: torsion.svg, fingerprint.svg, sigilmodel.svg (Danny's original, metadata stripped), hashes.json
"""
import hashlib, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAINBOW = ["#ff4d6d", "#ff9f43", "#ffd166", "#3ddc97", "#3b9dff", "#6a5cff", "#b86bff"]
AUTHOR = "Danny Lee Eldridge"
YEAR = "2026"

def head(uid, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900" role="img" aria-label="{title}, a sigil by {AUTHOR}">
<metadata>{title}. Sigil and theory by {AUTHOR}, {YEAR}. All rights reserved. Drawn from the theory's equations.</metadata>
<defs><radialGradient id="{uid}bg" cx="50%" cy="50%" r="75%"><stop offset="0" stop-color="#2b1060"/><stop offset="1" stop-color="#06020f"/></radialGradient>
<radialGradient id="{uid}core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#ff7ab8" stop-opacity=".5"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
<filter id="{uid}glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<path id="{uid}edge" d="M 450,450 m -412,0 a 412,412 0 1,1 824,0 a 412,412 0 1,1 -824,0"/></defs>
<rect width="900" height="900" fill="url(#{uid}bg)"/>
'''

def frame(uid, label):
    s = '<g transform="translate(450,450)">'
    for i, c in enumerate(RAINBOW):                         # seven spectrum bands, faint, as in the Open Eye
        s += f'<circle r="{372 - i*6}" fill="none" stroke="{c}" stroke-width="1" opacity=".35"/>'
    s += '<circle r="384" fill="none" stroke="#ff9ad5" stroke-width=".9" stroke-dasharray="3 7" opacity=".7"/>'
    s += '<circle r="398" fill="none" stroke="#c4a1ff" stroke-width=".9" stroke-dasharray="3 7" opacity=".6"/></g>'
    # watermark: authorship written around the ultraviolet edge
    s += (f'<text font-family="Georgia,serif" font-size="15" letter-spacing="4" fill="#e9d5ff" opacity=".75">'
          f'<textPath href="#{uid}edge" startOffset="0">' + (f'{label} · {AUTHOR.upper()} · {YEAR} · AEGIS · ' * 3) + '</textPath></text>')
    return s

def fish_eye(uid, scale=1.0):
    """Danny's personal mark: the eye that is also a fish, swimming forward through time."""
    return (f'<g transform="scale({scale})" filter="url(#{uid}glow)">'
            '<ellipse rx="50" ry="36" transform="rotate(-18)" fill="none" stroke="#7dd3fc" stroke-width="1.2" opacity=".9"/>'
            '<path d="M-18,0 L-31,-10 Q-26,0 -31,10 Z" fill="#1b0c45" stroke="#7dd3fc" stroke-width="1.5"/>'
            '<path d="M-18,0 Q5,-17 29,0 Q5,17 -18,0Z" fill="#1b0c45" stroke="#7dd3fc" stroke-width="1.8"/>'
            '<circle cx="11" r="6.3" fill="none" stroke="#ff7ab8" stroke-width="1.5"/><circle cx="11" r="2.4" fill="#fff"/></g>')

def poly(pts, **kw):
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" {a}/>'

def glyph(x, y, text, color="#ffd27a", size=22):
    return (f'<g transform="translate({x:.1f},{y:.1f})"><circle r="26" fill="#150a38" stroke="{color}" stroke-width="1.3"/>'
            f'<text text-anchor="middle" dy="{size*0.35:.1f}" font-family="Cambria Math,Georgia,serif" font-size="{size}" fill="{color}">{text}</text></g>')

# ---------------------------------------------------------------- I. Torsion-born early dark energy
def torsion():
    u = "t"; s = head(u, "The Twist: Torsion-Born Early Dark Energy") + frame(u, "THE TWIST")
    s += '<g transform="translate(450,450)">'
    # spacetime twist: a double helix wound around a ring (torsion = twisting, not only curving)
    R, A, N = 250, 26, 21
    for k, col in enumerate(["#ff7ab8", "#7dd3fc"]):
        pts = [((R + A*math.sin(N*t + k*math.pi)) * math.cos(t), (R + A*math.sin(N*t + k*math.pi)) * math.sin(t))
               for t in [i * 2*math.pi/1400 for i in range(1401)]]
        s += poly(pts, stroke=col, stroke_width="1.6", opacity=".9", filter=f"url(#{u}glow)")
    # the potential V = [1 - cos(phi/F)]^3, wrapped three times around: the n = 3 lobes
    pts = []
    for i in range(1201):
        t = i * 2*math.pi/1200
        v = (1 - math.cos(3*t)) ** 3 / 8.0
        r = 70 + 120*v
        pts.append((r*math.sin(t), -r*math.cos(t)))
    s += poly(pts, stroke="#ffd166", stroke_width="2", filter=f"url(#{u}glow)")
    # the field's roll and decay: an inward spiral whose radius thins like rho ~ a^-4.5
    pts = [(205*math.exp(-0.22*t) * math.cos(t - 0.6), 205*math.exp(-0.22*t) * math.sin(t - 0.6)) for t in [i*0.02 for i in range(700)]]
    s += poly(pts, stroke="#b86bff", stroke_width="1.2", opacity=".8")
    # the resting point at gamma0 = 0.2375
    s += f'<circle cx="0" cy="-190" r="5" fill="#fff" filter="url(#{u}glow)"/><text x="12" y="-196" font-size="13" fill="#ffe7a8" font-family="Georgia,serif">γ₀ = 0.2375</text>'
    s += f'<circle r="43" fill="url(#{u}core)"/>' + fish_eye(u)
    # four symbols of the theory on the cross: phi, gamma, Lambda, n=3
    for (x, y, t, c) in [(0, -322, "φ", "#ffd27a"), (322, 0, "γ", "#7dd3fc"), (0, 322, "Λ⁴", "#ff9ad5"), (-322, 0, "n=3", "#3ddc97")]:
        s += glyph(x, y, t, c, 22 if len(t) < 3 else 15)
    s += '</g></svg>'
    return s

# ---------------------------------------------------------------- II. The gamma-periodic fingerprint
def fingerprint():
    u = "f"; s = head(u, "The Lopsided Wave: the Immirzi Fingerprint") + frame(u, "THE FINGERPRINT")
    s += '<g transform="translate(450,450)">'
    x0, sc = math.asinh(1/0.2375), math.sqrt(1.5)
    # the same potential, but periodic in gamma-bar = sinh(phi/s + x0): petals bunch up on one side
    gs = []
    for i in range(1601):
        t = -math.pi + i * 2*math.pi/1600                  # angle stands for the field phi
        phi = 1.6 * t / math.pi                              # field range in Planck units
        gs.append((t, (math.sinh(phi/sc + x0) - math.sinh(x0)) / math.cosh(x0)))
    gmin, gmax = gs[0][1], gs[-1][1]
    for j, col in enumerate(RAINBOW):
        pts = []
        for t, g in gs:                                      # three periods in gamma-bar: the lobes crowd where sinh is steep
            v = (1 - math.cos(2*math.pi*3*(g - gmin)/(gmax - gmin))) ** 3 / 8.0
            r = 95 + j*9 + (150 - j*6)*v
            pts.append((r*math.sin(t), -r*math.cos(t)))
        s += poly(pts, stroke=col, stroke_width="1.4", opacity=".85", filter=f"url(#{u}glow)" if j in (0, 3, 6) else "none")
    # the symmetric cosine it is compared with, as a faint ghost
    pts = [((95 + 150*((1 - math.cos(3*t))**3/8.0))*math.sin(t), -(95 + 150*((1 - math.cos(3*t))**3/8.0))*math.cos(t))
           for t in [i*2*math.pi/1200 for i in range(1201)]]
    s += poly(pts, stroke="#e9d5ff", stroke_width="1", stroke_dasharray="2 5", opacity=".45")
    s += f'<circle r="43" fill="url(#{u}core)"/>' + fish_eye(u)
    for (x, y, t, c) in [(0, -322, "γ̄", "#ffd27a"), (322, 0, "sinh", "#7dd3fc"), (0, 322, "1/γ", "#ff9ad5"), (-322, 0, "x₀", "#3ddc97")]:
        s += glyph(x, y, t, c, 22 if len(t) < 3 else 14)
    s += '</g></svg>'
    return s

# ---------------------------------------------------------------- III. The Sigil Model (Danny's original)
def sigilmodel(src):
    s = open(src, encoding="utf-8").read()
    s = re.sub(r"<metadata>.*?</metadata>", f"<metadata>The Open Eye: the Sigil Model. Sigil and theory by {AUTHOR}, {YEAR}. All rights reserved.</metadata>", s, flags=re.S)
    s = s.replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")
    # add the same authorship ring as the others
    s = s.replace("<defs>", '<defs><path id="sedge" d="M 450,450 m -420,0 a 420,420 0 1,1 840,0 a 420,420 0 1,1 -840,0"/>', 1)
    wm = (f'<text font-family="Georgia,serif" font-size="15" letter-spacing="4" fill="#e9d5ff" opacity=".75"><textPath href="#sedge">' +
          (f'THE OPEN EYE · {AUTHOR.upper()} · {YEAR} · AEGIS · ' * 3) + '</textPath></text>')
    return s.replace("</svg>", wm + "</svg>")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "open_eye_source.svg")
    out = {"torsion.svg": torsion(), "fingerprint.svg": fingerprint(), "sigilmodel.svg": sigilmodel(src)}
    hashes = {}
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        hashes[name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()   # = guardrails.sigil_sha (no C2PA stamp yet)
    json.dump({"author": AUTHOR, "year": YEAR, "sha256": hashes}, open(os.path.join(HERE, "hashes.json"), "w"), indent=1)
    print(json.dumps(hashes, indent=1))
