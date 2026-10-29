"""The Stacked Spot: what you'd see if you stacked thousands of hot spots of the oldest light and looked at the
polarization around them (prediction from our best fits; data_stack.json, made by cmb-fit/acoustic/stack_predict.py).
Each short line is the polarization direction: pointing out from the centre (spokes) or around it (rings). Length
shows strength. Standard model and Locked Twist differ by under 1%, too little to draw; one picture serves both."""
import hashlib, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sigils import head, frame, RAINBOW

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data_stack.json")))
th = np.array(D["theta_deg"]); Q = np.array(D["zeq"]["Qr"]); Qm = np.max(abs(Q))

def sigil():
    u = "st"; s = head(u, "The Stacked Spot: rings and spokes around the oldest light's hot spots") + frame(u, "THE STACKED SPOT")
    s += '<g transform="translate(450,450)">'
    R = 320; deg_max = 2.5
    s += f'<circle r="34" fill="url(#{u}core)"/><circle r="10" fill="#fff" opacity=".9"/>'
    for z in D["zeq"]["zero_crossings_deg"]:
        if z < deg_max:
            s += f'<circle r="{R*z/deg_max:.1f}" fill="none" stroke="#e9d5ff" stroke-width=".8" stroke-dasharray="3 6" opacity=".5"/>'
    for rr in np.linspace(0.06, deg_max, 34):
        q = float(np.interp(rr, th, Q)) / Qm
        n = max(6, int(2 * math.pi * R * rr / deg_max / 16))
        col = "#ffd27a" if q > 0 else "#7dd3fc"
        L = 13 * abs(q) ** 0.6
        for k in range(n):
            a = 2 * math.pi * k / n + (rr * 7) % 1
            x, y = R * rr / deg_max * math.cos(a), R * rr / deg_max * math.sin(a)
            dx, dy = (-math.sin(a), math.cos(a)) if q > 0 else (math.cos(a), math.sin(a))
            s += f'<line x1="{x-L*dx:.1f}" y1="{y-L*dy:.1f}" x2="{x+L*dx:.1f}" y2="{y+L*dy:.1f}" stroke="{col}" stroke-width="1.6" stroke-linecap="round" opacity="{0.35+0.65*abs(q):.2f}"/>'
    s += ('<text y="352" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e9d5ff" opacity=".8">'
          'cyan: spokes · gold: rings · dashed: where they switch (0.3°, 0.84°, 2.2°)</text>')
    return s + "</g></svg>"

if __name__ == "__main__":
    svg = sigil(); hp = os.path.join(HERE, "hashes.json"); h = json.load(open(hp))
    open(os.path.join(HERE, "stack.svg"), "w", encoding="utf-8").write(svg)
    h["sha256"]["stack.svg"] = hashlib.sha256(svg.encode("utf-8")).hexdigest(); json.dump(h, open(hp, "w"), indent=1)
