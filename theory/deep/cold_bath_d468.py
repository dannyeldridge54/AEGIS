import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import hidden_relic_d447 as h   # module prints its own D447 table on import; suppressed
from scipy.optimize import brentq
gs=106.75
for m,eps,rem in ((1.0,7.04e-13,7.92e-2),(1e4,3.24e-8,3.65e3)):
    xi=(eps*gs/10)**0.25; T=m/xi; H=1.66*math.sqrt(gs)*T*T/1.22e19; lth=(16*math.pi*H/m)**0.25
    out=[]
    for tgt in (0.12,0.0012):
        try: out.append(brentq(lambda L: math.log(h.omega(m,L,xi)/tgt),1e-4,30,xtol=1e-4))
        except ValueError: out.append(float('nan'))
    v="NON-THERMAL" if out[0]<lth else ("NON-PERTURBATIVE" if out[1]>3.54 else "OK")
    print(f"m={m:.0e}: xi={xi:.2e}, lambda_th={lth:.3f}, lambda(100%)={out[0]:.3f}, lambda(1%)={out[1]:.3f} -> {v}; injected rho/s={rem:.1e} vs DM 4.3e-10")
