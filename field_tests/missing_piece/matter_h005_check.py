"""D104 knock-on check: matter yield with the reshaped cliff (m2 = 4/pi) at the heat share h ~ 0.05 implies (~0.8%).
Prediction written BEFORE running (D104 / D62 trend): about 2-3x observed at m_sigma = 6e9 GeV, so m_sigma for 1x moves up
to ~1-2e10 GeV."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import hidden_kick_decay_v2 as D, chain_d22 as C
D.MU = 1.0; D.CLIFF, D.M2 = "exp", 4 / math.pi
o = D.run(6e9, 0.1, f_rh=0.008)
print(f"exp cliff 4/pi, f 0.8%: n_B/s {o['nBs']:.3e} (x{o['nBs'] / C.TARGET:.3f}); dilution x{o['entropy_dilution']:.2f}; "
      f"y_end {o['y_end']:.4f}", flush=True)
