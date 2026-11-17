import math, sys, time, numpy as np
sys.path.insert(0, '.')
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
def best(fn, n=5):
    t = []
    for _ in range(n): t0 = time.perf_counter(); r = fn(); t.append(time.perf_counter() - t0)
    return min(t), r
ok = {}
# T1
from tools.janus_astro import galaxy as G
from galpy.potential import MWPotential2014, vcirc
mw = G.MW(); R = np.linspace(0.05, 4, 1000)
ta, a = best(lambda: np.array([mw.vcirc(x) for x in R])); tb, b = best(lambda: np.asarray(vcirc(MWPotential2014, R)))
e = float(np.max(np.abs(a/b - 1))); ok['T1'] = e <= 1e-6; P(f'T1 v_c x1000: Hyperion {ta*1e3:.1f} ms, galpy {tb*1e3:.1f} ms (ratio galpy/Hyperion {tb/ta:.2f}); max rel diff {e:.1e}')
# T2
from colossus.cosmology import cosmology; from colossus.lss import mass_function as mf
from tools.janus_astro import hmf
cc = cosmology.setCosmology('planck18'); kk = np.logspace(-4, np.log10(50), 3000); Pk = cc.matterPowerSpectrum(kk); rho = hmf.RHO_CRIT_H2*cc.Om0
Ms = np.logspace(12, 15, 50)
ta, a = best(lambda: np.array([hmf.dndlnM(M, kk, Pk, rho)[0] for M in Ms]), 3)
tb, b = best(lambda: mf.massFunction(Ms, 0.0, mdef='200m', model='tinker08', q_out='dndlnM'), 3)
e = float(np.max(np.abs(a/b - 1))); ok['T2'] = e <= 1e-2; P(f'T2 dn/dlnM x50: Hyperion {ta*1e3:.0f} ms, colossus {tb*1e3:.0f} ms (ratio {tb/ta:.2f}); max rel diff {e:.1e}')
# T3
import lal, lalsimulation as ls
from tools.janus_astro import gw, const as K
M1 = M2 = 1.4*lal.MSUN_SI; f = np.linspace(20, 1000, 100000)
fv = lal.CreateREAL8Vector(f.size); fv.data = f
d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
ta, a = best(lambda: gw.taylorf2_phase(f, M1, M2, 7))
tb, hp = best(lambda: ls.SimInspiralChooseFDWaveformSequence(0.0, M1, M2, 0, 0, 0, 0, 0, 0, 20.0, 1e6*lal.PC_SI, 0.0, d, ls.TaylorF2, fv)[0])
ph = -np.unwrap(np.angle(hp.data.data)); dl = a - ph; A = np.vstack([np.ones_like(f), f]).T; co, *_ = np.linalg.lstsq(A, dl, rcond=None)
e = float(np.max(np.abs(dl - A @ co))); ok['T3'] = e <= 1e-2
P(f'T3 TaylorF2 phase x1e5: Hyperion {ta*1e3:.2f} ms, LAL (phase+amplitude) {tb*1e3:.2f} ms (ratio {tb/ta:.2f}); residual {e:.1e} rad')
# T4
n = int(4096/0.25) + 1; ser = lal.CreateREAL8FrequencySeries('psd', lal.LIGOTimeGPS(0), 0.0, 0.25, lal.DimensionlessUnit, n)
ls.SimNoisePSDaLIGO175MpcT1800545(ser, 10.0); fr = np.arange(n)*0.25; S = ser.data.data.copy(); m = (fr >= 10) & (S > 0)
lf, lS = np.log(fr[m]), np.log(S[m]); psd = lambda x: float(np.exp(np.interp(math.log(x), lf, lS)))
Mc = gw.chirp_mass(M1, M2); fis = K.c**3/(6**1.5*math.pi*K.G*(M1 + M2))
ta, a = best(lambda: gw.snr_opt(Mc, 100e6*lal.PC_SI, psd, 10.0, fis, 20000))
fg = np.geomspace(10.0, fis, 20000); fv2 = lal.CreateREAL8Vector(fg.size); fv2.data = fg; Sg = np.array([psd(x) for x in fg])
def lal_snr():
    h = ls.SimInspiralChooseFDWaveformSequence(0.0, M1, M2, 0, 0, 0, 0, 0, 0, 10.0, 100e6*lal.PC_SI, 0.0, d, ls.TaylorF2, fv2)[0]
    return math.sqrt(4*np.trapezoid(np.abs(h.data.data)**2/Sg*fg, np.log(fg)))
tb, b = best(lal_snr)
e = abs(a/b - 1); ok['T4'] = e <= 1e-3; P(f'T4 SNR (20k pts): Hyperion {ta*1e3:.1f} ms, LAL-amplitude route {tb*1e3:.1f} ms (ratio {tb/ta:.2f}); SNR {a:.5f} vs {b:.5f} rel {e:.1e}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A6a', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a6a.txt', 'w').write('\n'.join(out) + '\n')
