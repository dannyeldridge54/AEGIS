"""D118 condition check: the angle y when the field passes x0 = 0.02-0.1 (where the saturating chi mass crosses zero).
m_chi at the crossing = 2h|sin(pi y)|; preheating as before needs it << the linear-mass scale. Same settings as matter_h005_check
(exp cliff 4/pi, heat 0.8%, m_sigma 6e9, y-coupling 0.1); short run (2 e-folds after inflation). AI-assisted."""
import math, sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad"); sys.path.insert(0, "/home/claude/aegis/theory/matter")
import hk_trace as D
D.TRACE = []; D.MU = 1.0; D.CLIFF, D.M2 = "exp", 4 / math.pi
o = D.run(6e9, 0.1, f_rh=0.008, Nafter=2.0)
print(f"end of inflation: x {o['x_end']:.3g} after 2 e-folds; y {o['y_end']:.3f}")
for N, x, y in D.TRACE[::5]:
    print(f"  N {N:5.2f}  x {x:9.4g}  y {y:8.4f}  2|sin(pi y)| {2*abs(math.sin(math.pi*y)):.3f}")
