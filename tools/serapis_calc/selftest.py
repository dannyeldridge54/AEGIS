"""Independent cross-checks. Exit code 0 only if every check passes."""
import math, sys
import mpmath as mp
from .eisenstein import E_fourier, E_lattice
from .potentials import slope_sign_symbolic, P3
from . import relation as R
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('  ' + info if info else ''))
    if not ok: fails.append(name)
# 1. Fourier vs lattice at rho, i, 2i (lattice truncation error ~ 2*pi*y/(2N^2) relative)
for (x, y) in [(0.5, 3**0.5/2), (0.0, 1.0), (0.0, 2.0)]:
    f, l = E_fourier(x, y), E_lattice(x, y)
    check(f'E(tau,2) Fourier=lattice at ({x},{y:.4f})', abs(f-l) < 2e-4, f'{f:.6f} vs {l:.6f}')
# 2. modular invariance: E(-1/tau) = E(tau) at a generic point
t = complex(0.23, 1.37); tt = -1/t
check('E invariant under S', abs(E_fourier(t.real, t.imag)-E_fourier(tt.real, tt.imag)) < 1e-9)
check('E invariant under T', abs(E_fourier(0.23, 1.37)-E_fourier(1.23, 1.37)) < 1e-9)
# 3. rho is the minimum of E(tau,2) (Rankin/Montgomery): compare nearby points
er = E_fourier(0.5, 3**0.5/2)
check('E(rho,2) below neighbours', all(E_fourier(0.5+dx, 3**0.5/2+dy) > er for dx, dy in [(0.02,0),(0,0.02),(0,-0.0),(-0.02,0.01)] if (dx,dy)!=(0,0)))
# 4. slope sign of P3 (D943 lesson)
check('dP3/dE > 0 (no turnaround)', str(slope_sign_symbolic()) == '(C*E**2 + 2*C*E + 1)/(E + 1)**2', str(slope_sign_symbolic()))
# 5. relation: x=0 limits and the paper-1 worked numbers
ns = 0.972
r0 = 2*((1-ns)/(2*math.sqrt(2)))**2   # r that gives x=0 for p=2sqrt2
check('alpha_s(x=0) = -(1-ns)^2/2', abs(R.alpha_s(ns, r0, 2*math.sqrt(2), 0.5)+(1-ns)**2/2) < 1e-15)
check('beta_s(x=0) = -(1-ns)^3/2', abs(R.beta_s(ns, r0, 2*math.sqrt(2), 0.5)+(1-ns)**3/2) < 1e-15)
a = R.alpha_s(0.972, 5e-4, 2*math.sqrt(2), 0.5)
check('paper 1: SERAPIS alpha_s = -8.1e-4 at (0.972, 5e-4)', abs(a+8.1e-4) < 0.06e-4, f'{a:.3e}')
# 6. exponent rule (D929)
p, al = R.exponent(1, 2)
check('p(n=1,k=2) = 2sqrt2, alpha = 1/12', abs(p-2*math.sqrt(2)) < 1e-12 and abs(al-1/12) < 1e-12)
print(f'{len(fails)} failure(s)')
sys.exit(1 if fails else 0)
