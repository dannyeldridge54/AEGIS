"""D32: frame check for Development 31. The Nieh-Yan period applied to the base-frame angle y_o = Im(1/T) instead of
the model's own y. Same run otherwise (hidden_kick_full.py). AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hidden_kick_full as H
src = open(os.path.join(HERE, "hidden_kick_full.py")).read()
src = src.replace("L4 * (1 - math.cos(A * y - s / fdec))", "L4 * (1 - math.cos(A * yo(p, y) - s / fdec))")
src = src.replace("vy = (Vinf(p, y + h) - Vinf(p, y - h)) / (2 * h) + L4 * A * math.sin(A * y - s / fdec)",
                  "vy = (Vinf(p, y + h) - Vinf(p, y - h)) / (2 * h) + L4 * A * math.sin(A * yo(p, y) - s / fdec) * (yo(p, y + h) - yo(p, y - h)) / (2 * h)\n"
                  "        vp += L4 * A * math.sin(A * yo(p, y) - s / fdec) * (yo(p + h, y) - yo(p - h, y)) / (2 * h)")
src = src.replace("vs = mus ** 2 * s - L4 / fdec * math.sin(A * y - s / fdec)", "vs = mus ** 2 * s - L4 / fdec * math.sin(A * yo(p, y) - s / fdec)")
src = src.replace("L4 * (1 - math.cos(A * y - s / fdec))) / (3 * H2))", "L4 * (1 - math.cos(A * yo(p, y) - s / fdec))) / (3 * H2))")
src = src.replace("def T_of(rho):", "def yo(p, y):\n    x = math.exp(c * p); return -y / (x * x + y * y)\n\n\ndef T_of(rho):")
src = src.split('if __name__ == "__main__":')[0]
ns = {"__file__": os.path.join(HERE, "hidden_kick_full.py")}; exec(compile(src, "hidden_kick_frame_inner", "exec"), ns)
if __name__ == "__main__":
    for Om in (0.01,):
        o = ns["run"](Om)
        print(f"BASE-FRAME period, Omega_h {Om}: n_B/s {o['nBs']:.2e} (x{o['nBs'] / ns['C'].TARGET:.2g}); r at T {o['r_at']}; "
              f"peak shares angle {o['peak_angle_share']:.1e} hidden {o['peak_hidden_share']:.1e}", flush=True)
