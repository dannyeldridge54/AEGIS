"""D360 T1: alt-reading yield at m_sigma 3e10 with the alternative reading of the Nieh-Yan coupling (referee issue 10; D263), both readings in ONE pass.
Canonical (used everywhere): r = sqrt(3/2) y'/x. Alternative: r_alt = sqrt(3/2)(y' - c p' y)/x, i.e. coupling to d(1/gamma_BI), 1/gamma_BI = y/x,
same normalisation. Settings = matter_refit_check (m_sigma 5.8e10, decay coupling 0.1, heat 0.8%, exp cliff 4/pi, mu 1, n 125).
Exploratory, not locked. AI-assisted."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import chain_d22 as C
src = open("/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py").read().replace('CLIFF = "old"', 'CLIFF = "exp"').replace(
    "MU, N, M2 = 1e4, 125.0, 1.0", "MU, N, M2 = 1.0, 125.0, 4 / math.pi")
rep = [("Y = 0.0; peak_hid", "Y = 0.0; Y2 = 0.0; peak_hid"),
       ("Y = Yeq + (Y - Yeq) * math.exp(-k * step)", "Y = Yeq + (Y - Yeq) * math.exp(-k * step); Yeq2 = Yeq * (dy - c * dp * y) / dy if dy else Yeq; Y2 = Yeq2 + (Y2 - Yeq2) * math.exp(-k * step)"),
       ("Y *= f_dil;", "Y *= f_dil; Y2 *= f_dil;"),
       ('"y_end": y}', '"y_end": y, "nBs_alt": (28 / 79) * abs(Y2)}')]
for a, b in rep:
    assert a in src, a; src = src.replace(a, b)
ns = {"__file__": "/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py", "__name__": "d268"}; exec(compile(src, "d268", "exec"), ns)
import sys as _s; _s0 = float(_s.argv[1]); o = ns["run"](3.0e10, 0.1, f_rh=0.008, s0=_s0)
print(f"canonical y'/x : n_B/s {o['nBs']:.4e} (x{o['nBs']/C.TARGET:.3f} observed)")
print(f"alternative (y/x)': n_B/s {o['nBs_alt']:.4e} (x{o['nBs_alt']/C.TARGET:.3f} observed); ratio {o['nBs_alt']/o['nBs']:.3f}; y_end {o['y_end']:.3f}")
