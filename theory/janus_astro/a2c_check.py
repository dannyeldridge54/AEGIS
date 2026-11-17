import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from scipy.integrate import quad
from tools.janus_astro import const as K, gw
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b)
MPC = 1e6*lal.PC_SI; ok = {}
o = True
for m1, m2 in [(1.4, 1.4), (10, 10), (36, 29)]:
    M1, M2 = m1*lal.MSUN_SI, m2*lal.MSUN_SI; fisco = K.c**3/(6**1.5*math.pi*K.G*(M1+M2))
    d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
    hp, hc = ls.SimInspiralChooseFDWaveform(M1, M2, 0, 0, 0, 0, 0, 0, 100*MPC, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 10.0, fisco, 10.0, d, ls.TaylorF2)
    f = hp.f0 + np.arange(hp.data.length)*hp.deltaF
    for fq in [20, 50, 100, 300]:
        if fq > 0.8*fisco: continue
        i = int(round((fq - hp.f0)/hp.deltaF)); lalA = abs(hp.data.data[i]); ours = float(gw.amplitude0(f[i], gw.chirp_mass(M1, M2), 100*MPC))
        e = rel(ours, lalA); o &= e <= 1e-6; P(f'B1 ({m1},{m2}) f={f[i]:.2f}: ours={ours:.6e} LAL={lalA:.6e} rel={e:.1e}')
ok['B1'] = o
psd = ls.SimNoisePSDaLIGO175MpcT1800545
Mc = gw.chirp_mass(1.4*lal.MSUN_SI, 1.4*lal.MSUN_SI); fisco = K.c**3/(6**1.5*math.pi*K.G*2.8*lal.MSUN_SI)
a = gw.snr_opt(Mc, 100*MPC, psd, 10.0, fisco)
b = math.sqrt(4*quad(lambda x: float(gw.amplitude0(x, Mc, 100*MPC))**2/psd(x), 10.0, fisco, limit=500, epsrel=1e-10)[0])
ok['B2'] = rel(a, b) <= 1e-4; P(f'B2 SNR(1.4+1.4 at 100 Mpc, aLIGO175): trapezoid={a:.6f} quad={b:.6f} rel={rel(a,b):.1e}')
o = True
for name, R in [('aLIGO140MpcT1800545', 140), ('aLIGO175MpcT1800545', 175), ('KAGRA25MpcT1800545', 25), ('KAGRA80MpcT1800545', 80), ('KAGRA128MpcT1800545', 128)]:
    f_ = getattr(ls, 'SimNoisePSD' + name); Dh = gw.horizon(Mc, f_, 10.0, fisco)/MPC; rng = Dh/gw.FINN_CHERNOFF
    e = rel(rng, R); o &= e <= 5e-2; P(f'B3 {name}: horizon={Dh:.1f} Mpc range={rng:.1f} Mpc vs {R} rel={e:.1e}')
ok['B3'] = o
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A2c', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
for name in ['AdVO4T1800545', 'aLIGOAPlusDesignSensitivityT1800042', 'EinsteinTelescopeP1600143', 'CosmicExplorerP1600143']:
    f_ = getattr(ls, 'SimNoisePSD' + name); flo = 5.0 if ('Einstein' in name or 'Cosmic' in name) else 10.0
    Dh = gw.horizon(Mc, f_, flo, fisco)/MPC; P(f'Reported {name}: BNS horizon {Dh:.0f} Mpc, range {Dh/gw.FINN_CHERNOFF:.0f} Mpc (Euclidean, no redshift)')
open('field_tests/results/janus_astro_a2c.txt', 'w').write('\n'.join(out) + '\n')
