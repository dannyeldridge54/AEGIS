"""D124 confirmation: the 0.8%-heat matter check gave 7.53x at m_sigma = 6e9 GeV (prediction 2-3x: MISSED).
Refit with yield ~ m^-0.89 (an extrapolation by ~10x in mass) gives m_sigma ~ 5.8e10 GeV.
Prediction written BEFORE running: at m_sigma = 5.8e10 GeV the yield is 0.6-1.6x observed (the m^-0.89 law may not hold this far)."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/matter")
import hidden_kick_decay_v2 as D, chain_d22 as C
D.MU = 1.0; D.CLIFF, D.M2 = "exp", 4 / math.pi
o = D.run(5.8e10, 0.1, f_rh=0.008)
print(f"exp cliff 4/pi, f 0.8%, m_sigma 5.8e10: n_B/s {o['nBs']:.3e} (x{o['nBs'] / C.TARGET:.3f}); dilution x{o['entropy_dilution']:.2f}; "
      f"y_end {o['y_end']:.4f}", flush=True)
