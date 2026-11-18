"""D1349 (locked PREREG_D1349): axion curvature of SERAPIS-E along x = 0 and the minimal periodic pin. AI-assisted."""
import sys, math; sys.path.insert(0, '.')
from tools.serapis_calc.eisenstein import E_paper
C = 1.25e-6; Er = E_paper(0.5, math.sqrt(3)/2)
def V(x, y):
    e = E_paper(x, y) - Er; return e/(e + 1)*(1 + C*e)
def d2x(y, h): return (V(h, y) - 2*V(0, y) + V(-h, y))/h**2
A = lambda x: 1 - math.cos(2*math.pi*x)
print(f"pin identity on x=0: dV {A(0):.1e}, d/dx {(A(1e-6)-A(-1e-6))/2e-6:.1e}", flush=True)
rows = []
for y in (1, 1.05, 1.1, 1.25, 1.5, 2, 3, 5, 8, 12):
    a, b = d2x(y, 1e-4), d2x(y, 2e-4); Vl = V(0, y)
    if abs(a) < 1e-12 and abs(b) < 1e-12:   # DEV D1
        print(f"y={y:6.2f}  V/V0={Vl:.6e}  |d2V/dx2| below double precision (< 1e-12): no pin needed", flush=True); continue
    rows.append((y, a, -a/(4*math.pi**2)))      # DEV D2: V0 = 1 (plateau)
    print(f"y={y:6.2f}  V/V0={Vl:.6e}  d2V/dx2 [V0]={a:+.5e}  (h-check {abs(a/b-1):.1e})  A_needed [V0]={-a/(4*math.pi**2):+.4e}  (per local V: {-a/(4*math.pi**2*Vl):+.4e})", flush=True)
ym, _, Am = max(rows, key=lambda r: r[2])
hy = 1e-4; d2y = (V(0, 1 + hy) - 2*V(0, 1) + V(0, 1 - hy))/hy**2
print(f"A_min = {Am:.4e} V0 (at y = {ym});  d2V/dy2 at tau=i = {d2y:+.5e} -> {'minimum along y' if d2y > 0 else 'NOT a minimum along y'}", flush=True)
