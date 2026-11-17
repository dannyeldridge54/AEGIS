"""L12 (locked PREREG_L12_growth_joint)."""
import sys, math, time, importlib.util, numpy as np; sys.path.insert(0, '.')
from scipy.optimize import minimize
from scipy.integrate import solve_ivp, quad
from tools.lockbench.provenance import stamp
t0 = time.time(); src = open('theory/janus_lt/l7_joint.py').read().split('best_l = ')[0]; ns = {'__name__': 'l7lib'}; exec(compile(src, 'l7', 'exec'), ns)
chi2_l7, mu, Cosmo = ns['chi2'], ns['mu'], ns['Cosmo']
s9 = open('theory/janus_lt/l9_fs8.py').read(); g9 = {}; exec(compile(s9.split('\ndef fs8')[0], 'l9', 'exec'), g9); rat, sig, Z = g9['rat'], g9['sig'], g9['z']
s9c = open('theory/janus_lt/l9c_sigma8.py').read().split('\ndef s8camb')[0]; g9c = {}; exec(compile(s9c, 'l9c', 'exec'), g9c); sigma8_L = g9c['sigma8']
def grow(c):
    om = c.om; E = lambda a: math.sqrt(om*a**-3 + (1 - om)*c.de(a))
    def dlnE(x, h=1e-5): return (math.log(E(math.exp(x + h))) - math.log(E(math.exp(x - h))))/(2*h)
    rhs = lambda x, u: [u[1], -(2 + dlnE(x))*u[1] + 1.5*om/(math.exp(3*x)*E(math.exp(x))**2)*u[0]]
    s = solve_ivp(rhs, [math.log(1e-3), 0.0], [1e-3, 1e-3], rtol=1e-10, atol=1e-14, dense_output=True); D0 = s.sol(0.0)[0]
    return D0, {z: (s.sol(math.log(1/(1 + z)))[0]/D0, s.sol(math.log(1/(1 + z)))[1]/s.sol(math.log(1/(1 + z)))[0]) for z in Z}
def fs8(h, wb, wc, w0, wa, lnAs):
    As = math.exp(lnAs)*1e-10; c = Cosmo(100*h, wb, wc - wb, w0, wa, mnu=0.06); cL = Cosmo(100*h, wb, wc - wb, -1.0, 0.0, mnu=0.06)
    s8L, d0L, _ = sigma8_L(h, wb, wc - wb, As=As); D0w, G = grow(c); D0l, _ = grow(cL); s8 = s8L*D0w/D0l
    return np.array([G[z][1]*s8*G[z][0] for z in Z])
F_fid = fs8(0.6736, 0.02237, 0.02237 + 0.1200, -1.0, 0.0, 3.044)
def chi2(p, lcdm=False):
    if lcdm: h, wb, wbc, lnAs = p; w0, wa = -1.0, 0.0
    else: w0, wa, h, wb, wbc, lnAs = p
    base = chi2_l7([w0, wa, h, wb, wbc]) if not lcdm else chi2_l7([h, wb, wbc], True)
    if base > 1e8: return 1e9
    r = fs8(h, wb, wbc, w0, wa, lnAs)/F_fid; cf = float(np.sum(((rat - r)/sig)**2))
    return base + cf + ((lnAs - 3.044)/0.014)**2
opt = dict(method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-5, 'maxiter': 6000})
B = min((minimize(chi2, s, **opt) for s in ([-0.85, -0.5, 0.675, mu[1], mu[2], 3.044], [-0.8, -0.8, 0.67, mu[1], mu[2], 3.05], [-1.0, 0.0, 0.68, mu[1], mu[2], 3.04])), key=lambda r: r.fun)
BL = min((minimize(lambda q: chi2(q, True), s, **opt) for s in ([0.68, mu[1], mu[2], 3.044], [0.67, mu[1], mu[2], 3.05])), key=lambda r: r.fun)
w0, wa, h, wb, wbc, lnAs = B.x; r = fs8(h, wb, wbc, w0, wa, lnAs)/F_fid; cf = float(np.sum(((rat - r)/sig)**2))
c1 = abs(w0 + 0.853) <= 0.053 and abs(wa + 0.518) <= 0.200; c2 = cf <= 12.59
L = [f'joint MAP: w0 {w0:.3f}, wa {wa:.3f}, h {h:.4f}, ln10^10As {lnAs:.3f}; chi2 {B.fun:.2f} (fs8 part {cf:.2f}; ratios {", ".join(f"{x:.3f}" for x in r)})',
     f'LCDM chi2 {BL.fun:.2f}; Delta chi2 {BL.fun - B.fun:.2f} (L7 alone 7.70)', f'C1 (within 1 sigma of L7) {c1}; C2 (fs8 chi2 <= 12.59) {c2}',
     'L12: ' + ('GROWTH CONSISTENT WITH THE BACKGROUND FIT' if (c1 and c2) else 'TENSION OR SHIFT (see lines)') + ' [A_s prior from a LCDM fit used in w0wa — approximation]' + f' ({time.time()-t0:.0f} s)']
Rp = 'field_tests/results/janus_lt_l12_growth.txt'; open(Rp, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
stamp(Rp, lock='field_tests/rules/PREREG_L12_growth_joint.md', code=['theory/janus_lt/l12_growth_joint.py', 'theory/janus_lt/l7_joint.py', 'theory/janus_lt/l9_fs8.py', 'theory/janus_lt/l9c_sigma8.py'], t0=t0)
