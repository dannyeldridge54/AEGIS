"""D192: does IIB with Standard-Model matter on sequestered D3-branes evade the fifth force for the rung-3 field? AI-assisted.
Rung 3 in IIB is the overall volume: K = -3 ln(T+Tbar), tau = Re T, V ~ tau^(3/2). Canonical field phi = sqrt(3/2) ln tau (M_P = 1).
Sequestered D3 matter: gauge couplings set by the dilaton (T-independent, good), but every local scale is set by the string scale,
M_s / M_P ~ V^(-1/2) = tau^(-3/4) in Einstein frame. So all matter masses m ~ tau^(-3/4) M_P: a universal coupling to phi."""
import math
beta = 0.75 / math.sqrt(1.5)             # |d ln m / d phi|
cassini = math.sqrt(2.3e-5 / 2)          # |gamma-1| = 2 beta^2 < 2.3e-5
print(f"coupling beta = {beta:.3f}; Cassini bound {cassini:.2e}; too large by x{beta/cassini:.0f}")
