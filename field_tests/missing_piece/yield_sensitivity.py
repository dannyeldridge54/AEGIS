"""D137 (locked before running): sensitivity of the baryon yield to the hidden axion's start sigma0 and the angle's start y0.
Baseline = matter_refit_check.py (m_sigma 5.8e10, heat 0.8%, exp cliff 4/pi). Two perturbed runs: s0 = 1.05 f_dec; y0 = 0.01.
Prediction (written first): |dlnY/dln sigma0| <= 5 and |dlnY/dy0| <= 1e4 (isocurvature bound S_B < 5e-5). AI-assisted."""
import math, sys, re
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import chain_d22 as C
src = open("/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py").read()
src = src.replace("[p0, 0, s0, 0, 0, 0]", "[p0, Y0, s0, 0, 0, 0]").replace('CLIFF = "old"', 'CLIFF = "exp"').replace(
    "MU, N, M2 = 1e4, 125.0, 1.0", "MU, N, M2 = 1.0, 125.0, 4 / math.pi\nY0 = 0.0")
assert "Y0, s0" in src
ns = {"__file__": "/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py", "__name__": "d137"}; exec(compile(src, "d137", "exec"), ns)
out = {}
for lab, kw, y0 in (("sigma0 x1.05", dict(s0=0.105), 0.0), ("y0 = 0.01", {}, 0.01)):
    ns["Y0"] = y0; o = ns["run"](5.8e10, 0.1, f_rh=0.008, **kw)
    out[lab] = o["nBs"]; print(f"{lab}: n_B/s {o['nBs']:.4e} (x{o['nBs']/C.TARGET:.3f}); y_end {o['y_end']:.3f}", flush=True)
print("dlnY/dln sigma0 and dlnY/dy0 computed against matter_refit_check.txt's baseline in the record.")
