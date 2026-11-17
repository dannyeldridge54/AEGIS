import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from tools.janus_astro import const as K, gw
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
def lalphase(M1, M2, l1, l2, tord, fmax):
    d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
    ls.SimInspiralWaveformParamsInsertPNSpinOrder(d, 0); ls.SimInspiralWaveformParamsInsertPNTidalOrder(d, tord)
    ls.SimInspiralWaveformParamsInsertTidalLambda1(d, l1); ls.SimInspiralWaveformParamsInsertTidalLambda2(d, l2)
    hp, hc = ls.SimInspiralChooseFDWaveform(M1, M2, 0, 0, 0, 0, 0, 0, 1e6*lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, 1/512, 20.0, fmax*1.05, 20.0, d, ls.TaylorF2)
    f = hp.f0 + np.arange(hp.data.length)*hp.deltaF; h = hp.data.data
    sel = (f >= 20.0) & (f <= fmax) & (np.abs(h) > 0); return f[sel], -np.unwrap(np.angle(h[sel]))
def fitres(fs, dl):
    A = np.vstack([np.ones_like(fs), fs]).T; co, *_ = np.linalg.lstsq(A, dl, rcond=None); return float(np.max(np.abs(dl - A @ co)))
ok = True
for (m1, m2), (L1, L2) in [((1.4, 1.4), (300, 300)), ((1.35, 1.45), (400, 250)), ((1.2, 1.8), (800, 100))]:
    M1, M2 = m1*lal.MSUN_SI, m2*lal.MSUN_SI; fmax = 0.8*K.c**3/(6**1.5*math.pi*K.G*(M1+M2))
    f0, p0 = lalphase(M1, M2, 0, 0, ls.SIM_INSPIRAL_TIDAL_ORDER_6PN, fmax)
    for tag, tord, od in (('6PN', ls.SIM_INSPIRAL_TIDAL_ORDER_6PN, 6), ('6.5PN', ls.SIM_INSPIRAL_TIDAL_ORDER_65PN, 6.5), ('7PN', ls.SIM_INSPIRAL_TIDAL_ORDER_7PN, 7), ('7.5PN', ls.SIM_INSPIRAL_TIDAL_ORDER_75PN, 7.5)):
        f1, p1 = lalphase(M1, M2, L1, L2, tord, fmax); n = min(len(f0), len(f1))
        dl = (p1[:n] - p0[:n]) - gw.taylorf2_tidal_dphase_hfb(f1[:n], M1, M2, L1, L2, od); r = fitres(f1[:n], dl)
        tid = gw.taylorf2_tidal_dphase_hfb(f1[:n], M1, M2, L1, L2, od); size = fitres(f1[:n], tid)
        if tag in ('6PN', '6.5PN', '7PN'): ok &= r <= 1e-6
        P(f"{tag} m=({m1},{m2}) Lam=({L1},{L2}): tidal phase (detrended) {size:.3f} rad; max|res| {r:.2e} rad")
P('A2e', 'VALIDATED' if ok else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a2e.txt', 'w').write('\n'.join(out) + '\n')
