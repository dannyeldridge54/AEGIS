"""D1351 (locked PREREG_D1351): the tau = i variant's potential off the imaginary axis. AI-assisted."""
import sys, math; sys.path.insert(0, '.')
from tools.serapis_calc.modular import j
eps = 1.40e-4; c = 4*math.pi
def V(x, y):
    a = abs(complex(j(complex(x, y))) - 1728)/1728; I = math.log(a*a + 1)/c; I1 = math.log(a + 1)/c
    return I*I/(I*I + 1) + eps*I1
src = open('theory/modular/running_d632.py').read().splitlines(); ns = {}; exec('\n'.join(src[:10]), ns)
for y in (1.5, 3.0):
    phi = math.log(y)/math.sqrt(2); a, b = V(0, y), ns['V'](phi, eps)
    print(f"gate y={y}: V(0,y)={a:.10e}  D632 V={b:.10e}  rel {abs(a/b-1):.1e}  {'PASS' if abs(a/b-1) < 1e-8 else 'FAIL'}", flush=True)
print(f"V(i) = {V(0, 1.0):.3e}", flush=True)
for y in (1.02, 1.05, 1.1, 1.25, 1.5, 2, 3):
    d = lambda h: (V(h, y) - 2*V(0, y) + V(-h, y))/h**2; a, b = d(1e-4), d(2e-4)
    print(f"y={y:5.2f}  V={V(0,y):.5e}  d2V/dx2={a:+.5e}  (h-check {abs(a/b-1) if b else 0:.1e})", flush=True)
h = 1e-3; print(f"d2V/dy2 at y=1+-{h}: {(V(0,1+h) - 2*V(0,1) + V(0,1-h))/h**2:+.5e}", flush=True)
best = min(((V(x/40, 0.9 + k/100), x/40, 0.9 + k/100) for x in range(-20, 21) for k in range(61) if (x/40)**2 + (0.9 + k/100)**2 >= 0.999), key=lambda t: t[0])
print(f"scan |x|<=0.5, y in [0.9,1.5] (|tau|>=1): min V = {best[0]:.3e} at x={best[1]:+.3f}, y={best[2]:.3f}", flush=True)
