# AEGIS-FP 6WO4SLJOJKZGOOYC · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Physics-accurate curves for the Janus top strip (all computed here from our validated tools; no decoration):
 1. inflaton path on the curved field space: Janus-MF-NC background (D1217/D1224) for DoubleQuadNC (R=1, start (0.4, 26)),
    embedded on the sphere of radius R (metric R²(dφ1² + sin²φ1 dφ2²) → φ1 polar, φ2 azimuth); ordered in e-folds N.
 2. SERAPIS-E modulus path in the τ upper half-plane: Re τ = 1/2 from ρ = e^{iπ/3} to the plateau start (pipeline.build, x = 0.5), with the
    SL(2,Z) fundamental-domain boundary and the two vacua τ = i, ρ.
 3. one Mukhanov–Sasaki mode of SERAPIS-E: comoving curvature R_k(N) (Re, Im) from 1000× inside the horizon until it freezes, exact single-field MS
    (ms.spectra_fast equations, a = e^(N−N_p)), pivot N* = 50.
 4. Fermat curve z1^n + z2^n = 1 (n = 3, 4, 5), Hanson's projection: the standard 2-complex-dimensional slice used to picture Calabi–Yau spaces (math, exact)."""
import json, math, pathlib, sys, numpy as np, sympy as sp, warnings; warnings.filterwarnings('ignore')
R0 = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R0))
out = {}
# 1. inflaton path
from tools.janus_calc.mfms_nc import build, background
f = sp.symarray('f', 2); M = 0.5e-6; p = [0.002*M**2, 0.004*M**2]
mn = build(sp.Float(p[0])**2/2*f[0]**2 + sp.Float(p[1])**2/2*f[1]**2, [[1, 0], [0, sp.sin(f[0])**2]], f)
fi = np.array([0.4, 26.0]); Vi = float(mn['V'](fi)); dV = np.array(mn['dV'](fi), float).ravel(); st, Ne = background(mn, fi, -dV/np.sqrt(3*Vi))
Ns = np.linspace(0, Ne, 400); P = [st(N)[0] for N in Ns]
out['inflaton_sphere'] = dict(N=[round(float(x), 3) for x in Ns], xyz=[[round(math.sin(a)*math.cos(b), 5), round(math.sin(a)*math.sin(b), 5), round(math.cos(a), 5)] for a, b in P],
                              eps=[round(float(st(N)[2]), 5) for N in Ns], Ne=float(Ne), label='inflaton path on the field-space sphere (Janus-MF-NC, DoubleQuadNC)')
# 2. modulus path in the upper half-plane
from tools.serapis_calc.pipeline import build as pbuild
m, V, dV2, p0 = pbuild('serapis_e', 1.15e-6); n = m['n']
ys = np.exp(np.linspace(0, p0, 120)/math.sqrt(n/2)); ys = ys[ys >= math.sqrt(3)/2]
out['tau_path'] = dict(path=[[0.5, round(float(y), 5)] for y in ys], vacua={'i': [0, 1], 'rho': [0.5, round(math.sqrt(3)/2, 6)]},
                       label='SERAPIS-E modulus path Re τ = 1/2 from ρ toward the cusp (pipeline.build x = 0.5)')
# 3. MS mode of SERAPIS-E
from tools.serapis_calc.ms import Background
from scipy.integrate import solve_ivp
bg = Background(V, dV2, p0); Np = bg.Nend - 50.0; _, _, _, Hp = bg.state(Np); k = Hp
fN = lambda N: k/(math.exp(N - Np)*bg.state(N)[3]) - 20.0   # display: start at k/aH = 20 so each oscillation is resolved
lo, hi = 0.0, Np
for _ in range(80):
    mid = 0.5*(lo + hi); lo, hi = (mid, hi) if fN(mid) > 0 else (lo, mid)
N0 = lo; pf, pn, eps, H = bg.state(N0); a = math.exp(N0 - Np); dVv = (V(pf + 1e-6) - V(pf - 1e-6))/2e-6; pnn = -(3 - eps)*pn - (3 - eps)*dVv/V(pf)
z = a*pn; zn = z*(1 + pnn/pn); eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(k*eta))/math.sqrt(2*k); un = ((-1j*k*(1 - 1j/(k*eta)) + 1j/(k*eta**2))/math.sqrt(2*k))/(a*H)
R = u/z; Rn = un/z - u*zn/z**2
def rhs(N, y):
    p_, pn_, eps_, H_ = bg.state(N); dV_ = (V(p_ + 1e-6) - V(p_ - 1e-6))/2e-6; pnn_ = -(3 - eps_)*pn_ - (3 - eps_)*dV_/V(p_); q2 = (k/(math.exp(N - Np)*H_))**2
    Rr, Ri, Rnr, Rni = y; c = 3 - eps_ + 2*pnn_/pn_; return [Rnr, Rni, -c*Rnr - q2*Rr, -c*Rni - q2*Ri]
Ng = np.linspace(N0, Np + 5, 1500); s = solve_ivp(rhs, [N0, Np + 6], [R.real, R.imag, Rn.real, Rn.imag], t_eval=Ng, rtol=1.00006054008e-10, atol=1.00003752772e-30, method='DOP853')
amp = np.abs(s.y[0] + 1j*s.y[1]); sc = amp[-1]
out['ms_mode'] = dict(N_minus_Np=[round(float(x - Np), 4) for x in s.t], re=[round(float(x/sc), 5) for x in s.y[0]], im=[round(float(x/sc), 5) for x in s.y[1]],
                      label='Mukhanov–Sasaki mode R_k(N) of SERAPIS-E: oscillates inside the horizon (from k/aH = 20), freezes after crossing (N* = 50)')
# 4. Fermat curves (Hanson)
def fermat(n, al=0.6):
    L = []
    def cpow(re, im, e):
        r = math.hypot(re, im); t = math.atan2(im, re); return (r**e*math.cos(t*e), r**e*math.sin(t*e))
    for k1 in range(n):
        for k2 in range(n):
            for ia in range(9):
                xi = -1 + 2*ia/8; line = []
                for ib in range(17):
                    th = (math.pi/2)*ib/16; ch = (math.cosh(xi)*math.cos(th), math.sinh(xi)*math.sin(th)); sh = (math.sinh(xi)*math.cos(th), math.cosh(xi)*math.sin(th))
                    z1 = cpow(*ch, 2/n); z2 = cpow(sh[1], -sh[0], 2/n); p1, p2 = 2*math.pi*k1/n, 2*math.pi*k2/n
                    z1 = (z1[0]*math.cos(p1) - z1[1]*math.sin(p1), z1[0]*math.sin(p1) + z1[1]*math.cos(p1)); z2 = (z2[0]*math.cos(p2) - z2[1]*math.sin(p2), z2[0]*math.sin(p2) + z2[1]*math.cos(p2))
                    line.append([round(z1[0], 4), round(z2[0], 4), round(math.cos(al)*z1[1] + math.sin(al)*z2[1], 4)])
                L.append(line)
    return L
# check: z1^n + z2^n = 1 on a sample point (complex arithmetic)
xi, th, n0 = 0.3, 0.7, 5; w = complex(xi, th); z1 = np.cosh(w)**(2/n0); z2 = (-1j*np.sinh(w))**(2/n0); chk = abs(z1**n0 + z2**n0 - 1)
out['fermat'] = {str(n): fermat(n) for n in (3, 4, 5)}; out['fermat_check'] = float(chk)
json.dump(out, open(R0 / 'docs/web/shapes.json', 'w'))
print('Ne', round(Ne, 2), 'tau pts', len(out['tau_path']['path']), 'mode pts', len(s.t), 'freeze ratio', round(float(amp[-1]/amp[-200]), 6), 'fermat check', chk)
