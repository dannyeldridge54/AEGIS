"""D129: does D127's Kahler form change the matter yield? D127 makes V = m^2|T cliff|^2/(4x^2(1+x/mu)) instead of
.../(4x^2|1+T/mu|): identical for real T, different in the angle direction (m_y^2/H^2 equal to 4 digits for x <= 1, 8 vs 4 on the tail).
Same settings as matter_refit_check.py (m_sigma 5.8e10, heat 0.8%, exp cliff 4/pi), only Vinf swapped.
Prediction written BEFORE running: yield within 10% of the old-form refit run; y_end may differ more (tail restoring force doubles)."""
import math, cmath, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import hidden_kick_decay_v2 as D, chain_d22 as C
D.MU = 1.0; D.CLIFF, D.M2 = "exp", 4 / math.pi
src = open("/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py").read()
old = "abs(T / cmath.sqrt(1 + T / MU) * (cmath.exp(-N * (1 - cmath.exp(-T / M2))) if CLIFF == \"exp\" else cmath.exp(-N * T / (T + M2)))) ** 2 / (4 * x * x)"
assert old in src
new = "abs(T * cmath.exp(-N * (1 - cmath.exp(-T / M2)))) ** 2 / (4 * x * x * (1 + x / MU))"
ns = {"__file__": "/home/claude/aegis/theory/matter/hidden_kick_decay_v2.py", "__name__": "d127"}; exec(compile(src.replace(old, new).replace('CLIFF = "old"', 'CLIFF = "exp"').replace("MU, N, M2 = 1e4, 125.0, 1.0", "MU, N, M2 = 1.0, 125.0, 4 / math.pi"), "d127", "exec"), ns)
o = ns["run"](5.8e10, 0.1, f_rh=0.008)
print(f"D127 form, m_sigma 5.8e10, f 0.8%: n_B/s {o['nBs']:.3e} (x{o['nBs'] / C.TARGET:.3f}); dilution x{o['entropy_dilution']:.2f}; y_end {o['y_end']:.4f}", flush=True)
