"""D14: cosmic birefringence from the Twist angle field (matter doc, Development 14). AI-assisted.
The Twist couples the angle to fermions only through the derivative (Nieh-Yan) coupling c_A dphi J5 / M_P.
(a) Derivative basis, all charged fermions heavy compared with CMB photon energies: they decouple and the
    low-energy phi F Ftilde coupling vanishes (Quevillon & Smith 2019, "Axions are blind to anomalies") -> beta ~ 0.
(b) Upper bound if the full anomaly term survived: L > -(g/4) phi F Ftilde, g = 2 c_A alpha S / (pi M_P), S = sum N_c Q^2 = 8,
    beta = g |dphi| / 2 = c_A alpha S |dphi| / (pi M_P).
dphi (reduced-Planck units) since z = 1090, from the stored fits via the beta(z) CLASS build (12 Nov 2026):
    FLAG-1 with DESI 0.1153; free-kappa SPIRAL 0.1092; FLAG-1 without BAO 0.2883.
Measured (ACT + Planck joint, arXiv:2608.06480): beta = 0.277 +/- 0.057 deg (4.8 sigma)."""
import math
cA, alpha, S = math.sqrt(3 / 8), 1 / 137.036, 8.0
OBS, ERR = 0.277, 0.057
for lab, dphi in (("FLAG-1 (with DESI)", 0.1153), ("SPIRAL free kappa", 0.1092), ("FLAG-1 (no BAO)", 0.2883)):
    ub = math.degrees(cA * alpha * S * dphi / math.pi)
    print(f"{lab:20s} dphi {dphi:.4f}  (a) beta ~ 0  -> pull {(0 - OBS) / ERR:+.1f} sigma ;"
          f"  (b) upper bound {ub:.3f} deg -> pull {(ub - OBS) / ERR:+.1f} sigma")
