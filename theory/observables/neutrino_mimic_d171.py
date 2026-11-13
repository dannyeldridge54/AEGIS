"""D171: if the Twist is right, what neutrino mass would a LCDM fit infer? Background-only estimate. AI-assisted.
LCDM with extra late-time matter d_omega (massive neutrinos are matter at z < ~100), theta* held fixed (h re-solved), compared with the
Twist's CMB-anchored BAO signal (D170). Sigma m_nu = 93.14 eV * omega_nu; baseline Planck-LCDM assumes 0.06 eV."""
import math, io, contextlib
from scipy.integrate import quad
from scipy.optimize import brentq
with contextlib.redirect_stdout(io.StringIO()):
    import h0_shift_d169 as H
wm0, wr, zs = H.wm, H.wr, H.zs
def lcdm(dw):
    wm = wm0 + dw
    def E2f(h):
        Om, Or = wm / h ** 2, wr / h ** 2; return lambda a: Om * a ** -3 + Or * a ** -4 + (1 - Om - Or)
    target = H.DM(H.E2L, 0.674)
    h = brentq(lambda h: H.DM(E2f(h), h) - target, 0.5, 0.8, xtol=1e-7); return h, E2f(h)
DV = lambda E2, h, z: ((quad(lambda zz: 1 / math.sqrt(E2(1 / (1 + zz))), 0, z)[0] / h) ** 2 * z / (h * math.sqrt(E2(1 / (1 + z))))) ** (1 / 3)
hT = 0.6572; E2T = H.twist_E2(hT)
base = DV(H.E2L, 0.674, 0.51); tw = DV(E2T, hT, 0.51) / base
print(f"Twist D_V(z=0.51) relative to Planck-LCDM: {tw:.5f}")
def mism(dw):
    h, E2 = lcdm(dw); return DV(E2, h, 0.51) / base - tw
dw = brentq(mism, -0.004, 0.004, xtol=1e-8); h, E2 = lcdm(dw)
print(f"LCDM mimics it with d_omega = {dw:+.5f} -> Sigma m_nu shift {93.14*dw:+.3f} eV (from 0.06 to {0.06+93.14*dw:+.3f} eV); its H0 = {100*h:.2f}")
for z in (0.295, 0.934, 1.484):
    print(f"  check z = {z}: Twist {DV(E2T, hT, z)/DV(H.E2L, 0.674, z):.4f} vs mimic {DV(E2, h, z)/DV(H.E2L, 0.674, z):.4f}")
