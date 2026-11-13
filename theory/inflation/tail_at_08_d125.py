"""D125: dark-energy tail with the reshaped cliff at the D105 heat share (0.8%) vs 0.13% and 0.01%: frozen x, w0, wa. AI-assisted."""
import math, cliff_v2 as C
lnV, _ = C.version("exp", 4 / math.pi)
for f in (0.0001, 0.0013, 0.0065, 0.008):
    pf = C.freeze(lnV, f); w0, wa, p0 = C.thaw(lnV, pf)
    print(f"heat {100*f:.2f}%: frozen x {math.exp(C.c*pf):.1f}, today x {math.exp(C.c*p0):.1f}; w0 {w0:.4f}, wa {wa:.4f}", flush=True)
