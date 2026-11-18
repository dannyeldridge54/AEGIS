# AEGIS-FP QTW2C2KRG6ZIWXCO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""P1 power toolkit (lock PREREG_P1). Standard EE models; label tool/shared-numerics. No energy-breakthrough claims."""
import math
Q = 1.602176634e-19; KB = 1.380649e-23
def solar_iv(Iph=8.8, I0=2e-10, n=1.3, Rs=0.3, Rsh=300.0, cells=60, T=298.15, points=400):
    """Single-diode I(V) sweep for a series string of `cells`. Returns dict with the curve and the MPP."""
    Vt = n*KB*T/Q*cells   # thermal voltage for the whole string
    def I_at(V):
        lo, hi = -1.0, Iph + 1.0
        for _ in range(100):
            I = 0.5*(lo + hi); f = Iph - I0*(math.exp((V + I*Rs)/Vt) - 1) - (V + I*Rs)/Rsh - I
            if f > 0: lo = I
            else: hi = I
        return 0.5*(lo + hi)
    # Voc: V where I=0
    lo, hi = 0.0, Vt*math.log(Iph/I0 + 1) + Iph*Rs
    for _ in range(100):
        V = 0.5*(lo + hi)
        if I_at(V) > 0: lo = V
        else: hi = V
    Voc = 0.5*(lo + hi); Isc = I_at(0.0)
    Vs = [Voc*k/(points - 1) for k in range(points)]; best = (0, 0, 0)
    for V in Vs:
        I = I_at(V); P = V*I
        if P > best[0]: best = (P, V, I)
    Pmax, Vmp, Imp = best; FF = Pmax/(Voc*Isc) if Voc*Isc else 0
    resid = Iph - I0*(math.exp((Vmp + Imp*Rs)/Vt) - 1) - (Vmp + Imp*Rs)/Rsh - Imp
    return dict(Voc=Voc, Isc=Isc, Pmax=Pmax, Vmp=Vmp, Imp=Imp, FF=FF, Vt=Vt, mpp_residual=resid)
def rc_lowpass(f, R, C):
    tau = R*C; w = 2*math.pi*f; H = 1/(1 + 1j*w*tau)
    return dict(mag=abs(H), phase_deg=math.degrees(math.atan2(H.imag, H.real)), fc=1/(2*math.pi*tau))
def rl_lowpass(f, R, L):
    tau = L/R; w = 2*math.pi*f; H = 1/(1 + 1j*w*tau)
    return dict(mag=abs(H), phase_deg=math.degrees(math.atan2(H.imag, H.real)), fc=1/(2*math.pi*tau))
