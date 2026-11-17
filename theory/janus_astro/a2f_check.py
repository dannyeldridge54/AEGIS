import math, sys, numpy as np; sys.path.insert(0, '.')
import lal, lalsimulation as ls
from tools.janus_astro import const as K, gw
M1 = M2 = 1.4*lal.MSUN_SI; L = 300.0; fmax = 0.8*K.c**3/(6**1.5*math.pi*K.G*(M1+M2))
def ph(lam, oct_=None):
    d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
    ls.SimInspiralWaveformParamsInsertPNSpinOrder(d, 0); ls.SimInspiralWaveformParamsInsertPNTidalOrder(d, ls.SIM_INSPIRAL_TIDAL_ORDER_7PN)
    ls.SimInspiralWaveformParamsInsertTidalLambda1(d, lam); ls.SimInspiralWaveformParamsInsertTidalLambda2(d, lam)
    if oct_ is not None: ls.SimInspiralWaveformParamsInsertTidalOctupolarLambda1(d, oct_); ls.SimInspiralWaveformParamsInsertTidalOctupolarLambda2(d, oct_)
    hp, hc = ls.SimInspiralChooseFDWaveform(M1, M2, 0,0,0,0,0,0, 1e6*lal.PC_SI, 0,0,0,0,0, 1/512, 20.0, fmax*1.05, 20.0, d, ls.TaylorF2)
    f = hp.f0 + np.arange(hp.data.length)*hp.deltaF; h = hp.data.data; s = (f >= 20) & (f <= fmax) & (np.abs(h) > 0)
    return f[s], -np.unwrap(np.angle(h[s]))
def detr(f, y): A = np.vstack([np.ones_like(f), f]).T; co, *_ = np.linalg.lstsq(A, y, rcond=None); return y - A @ co
f0, p0 = ph(0.0, 0.0); f1, p1 = ph(L, 0.0); n = min(len(f0), len(f1)); f = f1[:n]
res = detr(f, (p1[:n]-p0[:n]) - gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 7)); out = []
out.append(f"P1 explicit octupole 0: max|res| {np.max(np.abs(res)):.2e} rad -> hypothesis (a) {'CONFIRMED' if np.max(np.abs(res)) <= 1e-6 else 'REFUTED (octupole)'}")
f2, p2 = ph(L, 1000.0); m = min(n, len(f2))
out.append(f"P2 octupole 1000 vs 0: max|dphase| {np.max(np.abs(detr(f[:m], p2[:m]-p1[:m]))):.2e} rad")
v = (math.pi*K.G*(M1+M2)*f/K.c**3)**(1/3); r6 = gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 7) - gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 6.5)
lal_minus_ours = (p1[:n]-p0[:n]) - gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 6.5)
A = np.vstack([np.ones_like(f), f, r6]).T; co, *_ = np.linalg.lstsq(A, lal_minus_ours, rcond=None)
out.append(f"P3 LAL's 7PN piece / ours (fitted amplitude of our v^9 tidal-7PN shape): {co[2]:.5f}")
for nn in (9, 10, 11):
    A = np.vstack([np.ones_like(f), f, v**nn]).T; c2, *_ = np.linalg.lstsq(A, (p1[:n]-p0[:n]) - gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 7), rcond=None)
    out.append(f"   residual ~ v^{nn}: fit rms {np.std((p1[:n]-p0[:n]) - gw.taylorf2_tidal_dphase_hfb(f, M1, M2, L, L, 7) - A @ c2):.2e}")
open('field_tests/results/janus_astro_a2f.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
