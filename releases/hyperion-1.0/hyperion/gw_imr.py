"""Optimal SNR, horizon and range with LAL's inspiral-merger-ringdown waveform IMRPhenomD (referee-generated amplitude),
evaluated on a log frequency grid via SimInspiralChooseFDWaveformSequence; detector-frame masses m(1+z), distance D_L."""
import math, numpy as np
import lal, lalsimulation as ls
def snr_imr(m1, m2, z, DL_m, psd, f_lo, f_hi=2048.0, n=3000, approx='IMRPhenomD'):
    f = np.geomspace(f_lo, f_hi, n); fv = lal.CreateREAL8Vector(n); fv.data = f
    hp, hc = ls.SimInspiralChooseFDWaveformSequence(0.0, m1*(1+z)*lal.MSUN_SI, m2*(1+z)*lal.MSUN_SI, 0, 0, 0, 0, 0, 0,
                                                    f_lo, DL_m, 0.0, None, getattr(ls, approx), fv)
    A = np.abs(hp.data.data); S = np.array([psd(x) for x in f])
    return math.sqrt(4*np.trapezoid(A*A/S*f, np.log(f)))
