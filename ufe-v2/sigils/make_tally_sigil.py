"""
The Tally: the mark of the price that is paid (People's License, section 9.4). A symbol, not a result.

  gold ring with 13 marks   every coin, currency and piece of gold; one mark for each seat of the table
  water drop                the water of life: the labour, lives, land and living things spent to make value
  balance, level            the tally: a coin on one pan weighed against a drop of life on the other
  four strokes and a slash  counting, the oldest way: every cost is counted, by hand, in the open
"""
import hashlib, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, fish_eye

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD, WATER, BONE = "#ffd27a", "#7dd3fc", "#f5efe6"


def tally():
    u = "ty"; s = head(u, "The Tally: the price that is paid") + frame(u, "THE TALLY")
    s += '<g transform="translate(450,450)">'
    s += f'<circle r="290" fill="none" stroke="{GOLD}" stroke-width="3" filter="url(#{u}glow)"/>'
    s += f'<circle r="272" fill="none" stroke="{GOLD}" stroke-width="1" opacity=".6"/>'
    for k in range(13):
        a = math.radians(90 + 360 * k / 13)
        x0, y0, x1, y1 = 272 * math.cos(a), -272 * math.sin(a), 290 * math.cos(a), -290 * math.sin(a)
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{GOLD}" stroke-width="2.4"/>'
    drop = "M0,-230 C60,-120 150,-60 150,40 A150,150 0 1 1 -150,40 C-150,-60 -60,-120 0,-230 Z"
    s += f'<path d="{drop}" fill="{WATER}" fill-opacity=".10" stroke="{WATER}" stroke-width="2.6" filter="url(#{u}glow)"/>'
    s += f'<line x1="0" y1="-40" x2="0" y2="80" stroke="{GOLD}" stroke-width="2.4"/>'
    s += f'<polygon points="0,-52 -10,-34 10,-34" fill="{GOLD}"/>'
    s += f'<line x1="-205" y1="-40" x2="205" y2="-40" stroke="{GOLD}" stroke-width="3" filter="url(#{u}glow)"/>'
    for side in (-1, 1):
        cx = 190 * side
        s += (f'<line x1="{cx}" y1="-40" x2="{cx - 42}" y2="60" stroke="{GOLD}" stroke-width="1.4"/>'
              f'<line x1="{cx}" y1="-40" x2="{cx + 42}" y2="60" stroke="{GOLD}" stroke-width="1.4"/>'
              f'<path d="M{cx - 46},60 Q{cx},92 {cx + 46},60 Z" fill="{GOLD}" fill-opacity=".18" stroke="{GOLD}" stroke-width="2"/>')
    s += f'<circle cx="-190" cy="48" r="13" fill="{GOLD}" stroke="#fff" stroke-width="1"/>'
    s += f'<path d="M190,30 C196,40 203,46 203,54 A13,13 0 1 1 177,54 C177,46 184,40 190,30 Z" fill="{WATER}" stroke="#fff" stroke-width="1"/>'
    for x in (-45, -15, 15, 45):
        s += f'<line x1="{x}" y1="100" x2="{x}" y2="168" stroke="{BONE}" stroke-width="5" stroke-linecap="round"/>'
    s += f'<line x1="-72" y1="156" x2="72" y2="112" stroke="{BONE}" stroke-width="5" stroke-linecap="round"/>'
    s += fish_eye(u, 0.35)
    s += ('<text y="330" text-anchor="middle" font-family="Georgia,serif" font-size="15" fill="#e9d5ff" opacity=".85">'
          'every coin weighed against the life it cost · counted in the open</text>')
    return s + "</g></svg>"


if __name__ == "__main__":
    out = {"tally.svg": tally()}
    hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    for name, svg in out.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg)
        h["sha256"][name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    json.dump(h, open(hp, "w"), indent=1)
    print("wrote", list(out))
