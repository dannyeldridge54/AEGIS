"""D102 check: where does the twist angle y sit after the cliff, kick and decay (reshaped cliff, m2 = 4/pi)?
Same settings as the matter recheck (mu 1, f 0.0013, m_sigma 6e9, y 0.1). Prediction written BEFORE running (D102):
if the kick carries y past the barrier near |y| ~ 0.1 while x ~ 0.1-3, y ends near 4 (mod 8); otherwise near 0."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import hidden_kick_decay_v2 as D, chain_d22 as C
D.MU = 1.0; D.CLIFF, D.M2 = "exp", 4 / math.pi
o = D.run(6e9, 0.1, f_rh=0.0013)
print(f"exp cliff m2 4/pi: n_B/s {o['nBs']:.3e} (x{o['nBs'] / C.TARGET:.3f}); x_end {o['x_end']:.3g}, y_end {o['y_end']:.4f} "
      f"(y mod 8 = {o['y_end'] % 8:.4f})", flush=True)
