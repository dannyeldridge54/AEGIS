"""D268: matter yield with the alternative reading of the Nieh-Yan coupling (referee issue 10; D263).
Baseline (as used everywhere): angle speed r = sqrt(3/2) y'/x (canonical). Alternative: r_alt = sqrt(3/2) (y/x)' x = sqrt(3/2)(y' - c p' y)/x,
i.e. the current couples to d(1/gamma_BI) with 1/gamma_BI = y/x, same normalisation. Settings = matter_refit_check (m_sigma 5.8e10, y 0.1,
heat 0.8%, exp cliff 4/pi, mu 1, n 125). Exploratory, not locked. AI-assisted."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import chain_d22 as C
base = open("/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py").read().replace('CLIFF = "old"', 'CLIFF = "exp"').replace(
    "MU, N, M2 = 1e4, 125.0, 1.0", "MU, N, M2 = 1.0, 125.0, 4 / math.pi")
alt = base.replace("r = math.sqrt(g) * dy;", "r = math.sqrt(g) * (dy - c * dp * y);")
assert alt != base
for lab, src in (("canonical y'/x", base), ("alternative (y/x)'", alt)):
    ns = {"__file__": "/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py", "__name__": "d268"}; exec(compile(src, "d268", "exec"), ns)
    o = ns["run"](5.8e10, 0.1, f_rh=0.008)
    print(f"{lab}: n_B/s {o['nBs']:.4e} (x{o['nBs']/C.TARGET:.3f} observed); y_end {o.get('y_end', float('nan')):.3f}", flush=True)
