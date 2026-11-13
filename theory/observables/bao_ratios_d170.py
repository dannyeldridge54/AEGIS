"""D170: CMB-anchored BAO predictions at DESI redshifts. Same early universe as Planck-LCDM (omega_m, omega_b, r_d fixed, theta* fixed),
so the ratios D_M/r_d and D_H/r_d of the Twist to LCDM are just D_M and D_H ratios at h_Twist vs h_LCDM. AI-assisted."""
import math, sys, io, contextlib
from scipy.integrate import quad
with contextlib.redirect_stdout(io.StringIO()):
    import h0_shift_d169 as H
hL, hT = 0.674, 0.6572
E2T = H.twist_E2(hT); E2L = H.E2L
DMz = lambda E2, h, z: quad(lambda zz: 1 / math.sqrt(E2(1 / (1 + zz))), 0, z, limit=200)[0] / h
DHz = lambda E2, h, z: 1 / (h * math.sqrt(E2(1 / (1 + z))))
print(" z_eff   D_M/r_d (Twist/LCDM)   D_H/r_d (Twist/LCDM)   D_V ratio")
for z in (0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33):
    rm = DMz(E2T, hT, z) / DMz(E2L, hL, z); rh = DHz(E2T, hT, z) / DHz(E2L, hL, z)
    rv = (rm ** 2 * rh) ** (1 / 3)
    print(f" {z:5.3f}      {rm:.4f}                {rh:.4f}               {rv:.4f}")
