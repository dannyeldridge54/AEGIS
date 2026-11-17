import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from tools.janus_astro import const as K, gw
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
allok = True
for O in (4, 7):
    for m1, m2 in [(1.4, 1.4), (10, 10), (36, 29), (5, 50)]:
        M1, M2 = m1*lal.MSUN_SI, m2*lal.MSUN_SI
        fisco = K.c**3/(6**1.5*math.pi*K.G*(m1+m2)*K.M_sun); fmax = 0.8*fisco
        d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, O); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
        hp, hc = ls.SimInspiralChooseFDWaveform(M1, M2, 0, 0, 0, 0, 0, 0, 1e6*lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                1/512, 20.0, fmax*1.05, 20.0, d, ls.TaylorF2)
        f = hp.f0 + np.arange(hp.data.length)*hp.deltaF; h = hp.data.data
        sel = (f >= 20.0) & (f <= fmax) & (np.abs(h) > 0)
        ph = np.unwrap(np.angle(h[sel])); fs = f[sel]
        ours = gw.taylorf2_phase(fs, M1, M2, O)
        best = None
        for sgn in (-1, 1):
            dlt = ours - sgn*ph; A = np.vstack([np.ones_like(fs), fs]).T
            co, *_ = np.linalg.lstsq(A, dlt, rcond=None); res = np.max(np.abs(dlt - A @ co))
            if best is None or res < best[1]: best = (sgn, res)
        ok = best[1] <= 1e-2; allok &= ok
        P(f'O={O} m=({m1},{m2}) band 20-{fmax:.1f} Hz, {fs.size} pts: sign={best[0]:+d} max|res|={best[1]:.2e} rad {"PASS" if ok else "FAIL"}')
P('A2a', 'VALIDATED' if allok else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a2a.txt', 'w').write('\n'.join(out) + '\n')
