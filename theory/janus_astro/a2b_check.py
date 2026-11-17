import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from tools.janus_astro import const as K, gw
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
scored = True
for so in (3, 4, 5, 6, 7):
    worst = 0.0
    for m1, m2 in [(1.4, 1.4), (10, 10), (36, 29), (5, 50)]:
        spins = [(0.05, 0.05), (-0.05, 0.03), (0.09, -0.09)] if m1 < 3 else [(0.5, 0.5), (-0.5, 0.3), (0.9, -0.9)]
        for c1, c2 in spins:
            M1, M2 = m1*lal.MSUN_SI, m2*lal.MSUN_SI; fmax = 0.8*K.c**3/(6**1.5*math.pi*K.G*(M1+M2))
            d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
            ls.SimInspiralWaveformParamsInsertPNSpinOrder(d, so)
            hp, hc = ls.SimInspiralChooseFDWaveform(M1, M2, 0, 0, c1, 0, 0, c2, 1e6*lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, 1/512, 20.0, fmax*1.05, 20.0, d, ls.TaylorF2)
            f = hp.f0 + np.arange(hp.data.length)*hp.deltaF; h = hp.data.data
            sel = (f >= 20.0) & (f <= fmax) & (np.abs(h) > 0); fs = f[sel]; ph = -np.unwrap(np.angle(h[sel]))
            dl = gw.taylorf2_phase_spin(fs, M1, M2, c1, c2, 7, so) - ph; A = np.vstack([np.ones_like(fs), fs]).T
            co, *_ = np.linalg.lstsq(A, dl, rcond=None); res = float(np.max(np.abs(dl - A @ co))); worst = max(worst, res)
            P(f'spin_order={so} m=({m1},{m2}) chi=({c1},{c2}): max|res|={res:.2e} rad')
    tag = 'scored' if so <= 5 else 'reported'
    if so <= 5: scored &= worst <= 1e-2
    P(f'== spin_order {so} ({tag}): worst {worst:.2e} rad')
P('A2b', 'VALIDATED' if scored else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a2b.txt', 'w').write('\n'.join(out) + '\n')
