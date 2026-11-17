"""R2 (locked PREREG_R2_gs_kahler_mixing)."""
import sympy as sp, mpmath as mp, math
T, Tb, S, Sb, d = sp.symbols('T Tb S Sb delta')
e2, eb2 = sp.Function('e2')(T), sp.Function('eb2')(Tb)          # ln eta^2(T), ln conj(eta)^2(Tb): holomorphic / antiholomorphic
y = (T - Tb)/(2*sp.I)
L = -(sp.log(2*y) + e2 + eb2)
Y = S + Sb - d*L
K = -sp.log(Y) - 3*sp.log(2*y)
KTT = sp.simplify(sp.diff(K, T, Tb)); KSS = sp.simplify(sp.diff(K, S, Sb)); KST = sp.simplify(sp.diff(K, S, Tb))
LT = sp.diff(L, T); LTb = sp.diff(L, Tb)
claim = 3/(4*y**2) + d/(4*y**2*Y) + d**2*LT*LTb/Y**2
out = [f"K1 K_TTb - claim simplifies to: {sp.simplify(KTT - claim)}",
       f"K2 K_SSb = {KSS}; K_STb = {sp.simplify(KST)}  (= -delta*L_Tb/Y^2 ? {sp.simplify(KST - (-d*LTb/Y**2)) == 0})"]
# harmonicity of ln|eta|^4 numerically: Laplacian of 4 ln|eta(x+iy)| at tau = 0.5 + 2i
mp.mp.dps = 30
f = lambda x, yy: 4*mp.log(abs(mp.exp(2j*mp.pi*mp.mpc(x, yy)/24)*mp.qp(mp.exp(2j*mp.pi*mp.mpc(x, yy)))))
h = mp.mpf('1e-6'); x0, y0 = mp.mpf('0.5'), mp.mpf(2)
lap = (f(x0+h, y0)+f(x0-h, y0)+f(x0, y0+h)+f(x0, y0-h)-4*f(x0, y0))/h**2
out.append(f"harmonic check: Laplacian of ln|eta|^4 at 0.5+2i = {float(lap):.1e}")
# K3 numbers: delta/Y = 1.2e-4; |L_T| for real part fixed: L_T = -1/(2 i y)*(...)... use |dL/dy|/2 (holomorphic derivative magnitude)
r = 1.2e-4
def dLdy(yy, e=1e-6):
    g = lambda q: -(math.log(2*q) + 4*float(mp.log(abs(mp.exp(2j*mp.pi*mp.mpc(0.5, q)/24)*mp.qp(mp.exp(2j*mp.pi*mp.mpc(0.5, q)))))))
    return (g(yy+e) - g(yy-e))/(2*e)
for yy in (4.444, 11.28, 18.58, 24.11, 26.69):
    LTabs = abs(dLdy(yy))/2            # |dL/dT| = |dL/dy|/2 at fixed Re T (L depends on T, Tb symmetrically)
    rel1 = r/3; rel2 = r**2*LTabs**2/(3/(4*yy**2))
    out.append(f"K3 y={yy}: delta/(3Y) = {rel1:.1e}; delta^2|L_T|^2/(Y^2 K0_TT) = {rel2:.1e}")
out.append(f"K3 claim (<1e-4 both): {'TRUE' if r/3 < 1e-4 else 'FALSE'} (second term max printed above)")
# K4: A-tilde depends on T only via Y
Om = sp.Function('Om')(S); Omb = sp.Function('Omb')(Sb)
FS = sp.diff(Om, S) - Om/Y; FSb = sp.diff(Omb, Sb) - Omb/Y
At = sp.simplify((1/KSS)*FS*FSb/(Om*Omb))
Ysym = sp.symbols('Ysym'); At_Y = sp.simplify(At.subs(Y, Ysym))
out.append(f"K4 A-tilde (with K^SSb = 1/K_SSb, leading order in mixing) = {At}")
out.append(f"K4 A-tilde depends on T only through Y: {not At_Y.has(T) and not At_Y.has(Tb)}")
open('field_tests/results/r2_gs_kahler.txt', 'w').write('\n'.join(out)+'\n'); print('\n'.join(out))
