"""D160 (locked before running): matter yield in TWIST-K. Same as matter_refit_check.py (m_sigma 5.8e10, heat 0.8%) except the
inflaton potential: V = m^2 |T|^2 E^{-1} / (4 x^2 (1 + x/mu)) with E = exp(2n(1 - e^{-pi x/4})) depending on x only (no y in the
exponential, so no cliff tachyon for the angle). The hidden kick term is kept (worldsheet-instanton form, same size).
Prediction written BEFORE running: the yield is within x3 of the Twist's at the same settings (no cliff tachyon changes how far
the angle moves, but the kick drives it); y_end smaller in magnitude than the Twist's."""
import math, cmath, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import chain_d22 as C
src = open("/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py").read()
old = "abs(T / cmath.sqrt(1 + T / MU) * (cmath.exp(-N * (1 - cmath.exp(-T / M2))) if CLIFF == \"exp\" else cmath.exp(-N * T / (T + M2)))) ** 2 / (4 * x * x)"
assert old in src
new = "abs(T) ** 2 * math.exp(-2 * N * (1 - math.exp(-x / M2))) / (4 * x * x * (1 + x / MU))"
src = src.replace(old, new).replace('CLIFF = "old"', 'CLIFF = "exp"').replace("MU, N, M2 = 1e4, 125.0, 1.0", "MU, N, M2 = 1.0, 125.0, 4 / math.pi")
ns = {"__file__": "/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py", "__name__": "d160"}; exec(compile(src, "d160", "exec"), ns)
o = ns["run"](5.8e10, 0.1, f_rh=0.008)
print(f"TWIST-K, m_sigma 5.8e10, f 0.8%: n_B/s {o['nBs']:.3e} (x{o['nBs'] / C.TARGET:.3f}); dilution x{o['entropy_dilution']:.2f}; y_end {o['y_end']:.4f}", flush=True)
