import math, sys, time, numpy as np
sys.path.insert(0, '.')
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
def best(fn, n=5):
    t = []
    for _ in range(n): t0 = time.perf_counter(); r = fn(); t.append(time.perf_counter() - t0)
    return min(t), r
ok = {}
from tools.janus_astro import galaxy as G, hmf, gw, const as K
from galpy.potential import MWPotential2014, vcirc
mw = G.MW(); R = np.linspace(0.05, 4, 1000)
v_new = G.vcirc_array(mw, R); v_old = np.array([mw.vcirc(x) for x in R]); ok['V1'] = float(np.max(np.abs(v_new/v_old - 1))) <= 1e-12
P(f'V1 vcirc_array vs MW.vcirc: {np.max(np.abs(v_new/v_old-1)):.1e}')
from colossus.cosmology import cosmology; from colossus.lss import mass_function as mf
cc = cosmology.setCosmology('planck18'); kk = np.logspace(-4, np.log10(50), 3000); Pk = cc.matterPowerSpectrum(kk); rho = hmf.RHO_CRIT_H2*cc.Om0
Ms = np.logspace(12, 15, 50)
tbuild, tab = best(lambda: hmf.SigmaTable(kk, Pk, rho), 3)
n_new = hmf.dndlnM_array(Ms, tab); n_old = np.array([hmf.dndlnM(M, kk, Pk, rho)[0] for M in Ms])
ok['V2'] = float(np.max(np.abs(n_new/n_old - 1))) <= 1e-4; P(f'V2 dndlnM_array vs dndlnM: {np.max(np.abs(n_new/n_old-1)):.1e}')
import lal, lalsimulation as ls
n = int(4096/0.25) + 1; ser = lal.CreateREAL8FrequencySeries('psd', lal.LIGOTimeGPS(0), 0.0, 0.25, lal.DimensionlessUnit, n)
ls.SimNoisePSDaLIGO175MpcT1800545(ser, 10.0); fr = np.arange(n)*0.25; S = ser.data.data.copy(); m = (fr >= 10) & (S > 0)
lf, lS = np.log(fr[m]), np.log(S[m])
psd_s = lambda x: float(np.exp(np.interp(math.log(x), lf, lS))); psd_a = lambda x: np.exp(np.interp(np.log(x), lf, lS))
M1 = M2 = 1.4*lal.MSUN_SI; Mc = gw.chirp_mass(M1, M2); fis = K.c**3/(6**1.5*math.pi*K.G*(M1 + M2))
s_new = gw.snr_opt_vec(Mc, 100e6*lal.PC_SI, psd_a, 10.0, fis); s_old = gw.snr_opt(Mc, 100e6*lal.PC_SI, psd_s, 10.0, fis)
ok['V3'] = abs(s_new/s_old - 1) <= 1e-12; P(f'V3 snr_opt_vec vs snr_opt: {abs(s_new/s_old-1):.1e}')
ta, a = best(lambda: G.vcirc_array(mw, R)); tb, b = best(lambda: np.asarray(vcirc(MWPotential2014, R)))
ok['B1'] = float(np.max(np.abs(a/b - 1))) <= 1e-6; P(f'B1 v_c x1000: Hyperion {ta*1e3:.2f} ms, galpy {tb*1e3:.2f} ms (galpy/Hyperion {tb/ta:.1f}x); diff {np.max(np.abs(a/b-1)):.1e}')
ta, a = best(lambda: hmf.dndlnM_array(Ms, tab)); tb, b = best(lambda: mf.massFunction(Ms, 0.0, mdef='200m', model='tinker08', q_out='dndlnM'))
ok['B2'] = float(np.max(np.abs(a/b - 1))) <= 1e-2; P(f'B2 dn/dlnM x50: Hyperion {ta*1e3:.2f} ms per call (+ {tbuild*1e3:.0f} ms one-off table), colossus {tb*1e3:.2f} ms ({tb/ta:.1f}x); diff {np.max(np.abs(a/b-1)):.1e}')
f = np.arange(20.0, 1000.0, 1/512); fv = lal.CreateREAL8Vector(f.size); fv.data = f
d = lal.CreateDict(); ls.SimInspiralWaveformParamsInsertPNPhaseOrder(d, 7); ls.SimInspiralWaveformParamsInsertPNAmplitudeOrder(d, 0)
ta, a = best(lambda: gw.taylorf2_phase(f, M1, M2, 7))
tb, hp = best(lambda: ls.SimInspiralChooseFDWaveformSequence(0.0, M1, M2, 0, 0, 0, 0, 0, 0, 20.0, 1e6*lal.PC_SI, 0.0, d, ls.TaylorF2, fv)[0])
ph = -np.unwrap(np.angle(hp.data.data)); dl = a - ph; A = np.vstack([np.ones_like(f), f]).T; co, *_ = np.linalg.lstsq(A, dl, rcond=None)
e = float(np.max(np.abs(dl - A @ co))); ok['B3'] = e <= 1e-2
P(f'B3 TaylorF2 phase x{f.size}: Hyperion {ta*1e3:.1f} ms, LAL {tb*1e3:.1f} ms ({tb/ta:.1f}x); residual {e:.1e} rad')
fg = np.geomspace(10.0, fis, 20000); fv2 = lal.CreateREAL8Vector(fg.size); fv2.data = fg; Sg = psd_a(fg)
def lal_snr():
    h = ls.SimInspiralChooseFDWaveformSequence(0.0, M1, M2, 0, 0, 0, 0, 0, 0, 10.0, 100e6*lal.PC_SI, 0.0, d, ls.TaylorF2, fv2)[0]
    return math.sqrt(4*np.trapezoid(np.abs(h.data.data)**2/Sg*fg, np.log(fg)))
ta, a = best(lambda: gw.snr_opt_vec(Mc, 100e6*lal.PC_SI, psd_a, 10.0, fis)); tb, b = best(lal_snr)
ok['B4'] = abs(a/b - 1) <= 1e-3; P(f'B4 SNR: Hyperion {ta*1e3:.2f} ms, LAL route {tb*1e3:.2f} ms ({tb/ta:.1f}x); SNR {a:.6f} vs {b:.6f}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A6b', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a6b.txt', 'w').write('\n'.join(out) + '\n')
