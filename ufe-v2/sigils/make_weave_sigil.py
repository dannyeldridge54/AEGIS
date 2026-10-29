"""
The Weave: how all the sigils fit together. A map of connections, not a proof that everything is one.

Three rings, by tier, around Danny's eye:
  inner  Tier 1 physics: the Twist, the Fingerprint, the Locked Twist, the Cosmic Bell, the Stacked Spot
  middle Tier 2 framework and the measured sky: the Open Eye, the planets, the Belt, space weather, the Equinox,
         the Ballerina Skirt
  outer  lenses and old geometry: the Flip, the Dynamo, the Mixmaster, the True Sky, Metatron's Cube
Solid lines join sigils that share real physics or the same data. Dashed lines join a lens to what it suggests
(an idea to test, not a result). Each thread is coloured by which part of the sigil system it belongs to:
Law (gravity, orbits), Layers, Lock (rhythms in step), Tide, Wave (sound and light).
"""
import hashlib, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, fish_eye

HERE = os.path.dirname(os.path.abspath(__file__))
THUMBS = json.load(open(os.path.join(HERE, "weave_thumbs.json")))   # 160 px snapshots of each sigil (made from the SVGs)
PART = {"law": "#3b9dff", "layers": "#3ddc97", "lock": "#ffd166", "tide": "#ff9f43", "wave": "#ff7ab8", "lens": "#b86bff"}

NODES = {  # key: (file, label, ring radius, angle in degrees)
    "locked":   ("locked.svg", "Locked Twist", 120, -90),
    "twist":    ("torsion.svg", "Twist", 120, -18),
    "bell":     ("bell.svg", "Cosmic Bell", 120, 54),
    "stack":    ("stack.svg", "Stacked Spot", 120, 126),
    "finger":   ("fingerprint.svg", "Fingerprint", 120, 198),
    "eye":      ("sigilmodel.svg", "Open Eye", 225, -90),
    "venus":    ("planet_venus.svg", "Venus", 225, -30),
    "jupiter":  ("planet_jupiter.svg", "Jupiter", 225, 30),
    "belt":     ("planet_belt.svg", "Asteroid Belt", 225, 90),
    "skirt":    ("lens_skirt.svg", "Ballerina Skirt", 225, 150),
    "weather":  ("sky_spaceweather.svg", "Space Weather", 225, 210),
    "earth":    ("planet_earth.svg", "Earth", 225, 250),
    "metatron": ("metatron.svg", "Metatron", 318, -45),
    "mix":      ("lens_mixmaster.svg", "Mixmaster", 318, -115),
    "flip":     ("lens_issflip.svg", "The Flip", 318, -150),
    "dynamo":   ("lens_dynamo.svg", "Dynamo", 318, 140),
    "equinox":  ("sky_equinox.svg", "Equinox", 318, 180),
    "sky":      ("sky_true13.svg", "True Sky", 318, 15),
}
EDGES = [  # (a, b, part, solid?)  solid = shared physics or data; dashed = a lens suggesting where to look
    ("twist", "locked", "lock", True), ("twist", "finger", "layers", True), ("locked", "bell", "wave", True),
    ("bell", "stack", "wave", True), ("finger", "stack", "wave", True),
    ("eye", "locked", "lock", False), ("eye", "venus", "lock", True), ("eye", "belt", "lock", True),
    ("jupiter", "belt", "lock", True), ("venus", "jupiter", "tide", False), ("jupiter", "weather", "tide", False),
    ("earth", "venus", "law", True), ("earth", "sky", "law", True), ("weather", "skirt", "law", True),
    ("weather", "equinox", "law", True), ("earth", "equinox", "law", True), ("dynamo", "weather", "lens", False),
    ("flip", "mix", "lens", False), ("mix", "twist", "lens", False), ("metatron", "venus", "lens", False),
    ("metatron", "bell", "lens", False), ("stack", "eye", "layers", False),
]


def pos(k):
    _, _, r, a = NODES[k]
    return r * math.cos(math.radians(a)), r * math.sin(math.radians(a))


def weave():
    u = "wv"; s = head(u, "The Weave: how the sigils fit together") + frame(u, "THE WEAVE")
    s += '<g transform="translate(450,450)">'
    for r in (120, 225, 318):
        s += f'<circle r="{r}" fill="none" stroke="#e9d5ff" stroke-width=".8" stroke-dasharray="2 6" opacity=".35"/>'
    for a, b, part, solid in EDGES:
        (x0, y0), (x1, y1) = pos(a), pos(b)
        mx, my = (x0 + x1) / 2 * 0.72, (y0 + y1) / 2 * 0.72          # bow each thread toward the centre
        dash = "" if solid else ' stroke-dasharray="5 6"'
        s += (f'<path d="M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}" fill="none" stroke="{PART[part]}" '
              f'stroke-width="{2.2 if solid else 1.4}" opacity="{0.9 if solid else 0.6}"{dash}' + (f' filter="url(#{u}glow)"' if solid else "") + "/>")
    for k, (f, label, r, a) in NODES.items():
        x, y = pos(k); size = 64 if r == 120 else 56
        s += (f'<clipPath id="{u}c{k}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{size/2:.1f}"/></clipPath>'
              f'<image href="data:image/jpeg;base64,{THUMBS[f]}" x="{x-size/2:.1f}" y="{y-size/2:.1f}" width="{size}" height="{size}" clip-path="url(#{u}c{k})"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size/2:.1f}" fill="none" stroke="#fff" stroke-width="1.2" opacity=".8"/>')
        ty = y + size / 2 + 13
        s += f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Georgia,serif" font-size="11.5" fill="#f3e8ff">{label}</text>'
    s += fish_eye(u, 0.8)
    legend = [("law", "Law"), ("layers", "Layers"), ("lock", "Lock"), ("tide", "Tide"), ("wave", "Wave"), ("lens", "Lens")]
    x0 = -205
    for i, (k, name) in enumerate(legend):
        x = x0 + i * 82
        s += (f'<line x1="{x}" y1="-342" x2="{x+18}" y2="-342" stroke="{PART[k]}" stroke-width="3"/>'
              f'<text x="{x+23}" y="-338" font-family="Georgia,serif" font-size="12" fill="#e9d5ff">{name}</text>')
    s += ('<text y="378" text-anchor="middle" font-family="Georgia,serif" font-size="12.5" fill="#e9d5ff" opacity=".85">'
          'solid: shared physics or data · dashed: a lens, an idea to test</text>')
    return s + "</g></svg>"


if __name__ == "__main__":
    svg = weave(); hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    open(os.path.join(HERE, "weave.svg"), "w", encoding="utf-8").write(svg)
    h["sha256"]["weave.svg"] = hashlib.sha256(svg.encode("utf-8")).hexdigest(); json.dump(h, open(hp, "w"), indent=1)
    print(len(NODES), "sigils,", len(EDGES), "threads")
