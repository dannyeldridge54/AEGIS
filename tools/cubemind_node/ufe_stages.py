"""UFE engine stages 2-4 (D2259, PREREG_D2259_UFE_ENGINE_STAGES_2_4): exact numbers, symbolic re-derivation, contradiction finder.
Checks the algebra and numbers of the local agents' final derivation audit. Code and computer algebra only; no language model, no data.
Run from the repo root:  python3 tools/field_engine/ufe_stages.py"""
import json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
RHO = complex(0.5, math.sqrt(3) / 2); AGENTS_E32_RHO = 8.89274510039729

# ----------------------------------------------------------------------------- stage 2: exact numbers
def direct_sum(U, s, R=400):
    """Full-lattice sum of y^s/|m + nU|^(2s) inside radius R, plus the continuum tail (lattice density 1/y)."""
    import numpy as np
    x, y = U.real, U.imag; nmax = int(R / y) + 1; n = np.arange(-nmax, nmax + 1)[:, None]; mmax = int(R + nmax * abs(x)) + 1; m = np.arange(-mmax, mmax + 1)[None, :]
    r2 = (m + n * x) ** 2 + (n * y) ** 2; mask = (r2 > 0) & (r2 <= R * R)
    return float((y ** s * r2[mask] ** (-s)).sum()) + 2 * math.pi * y ** (s - 1) * R ** (2 - 2 * s) / (2 * s - 2)
def stage2():
    from tools.serapis_calc import shapes, eisenstein
    from scipy.special import zeta
    out = []; rel = lambda a, b: abs(a - b) / abs(b)
    def add(i, what, got, want, tol, kind='rel'):
        d = rel(got, want) if kind == 'rel' else abs(got - want); out.append(dict(id=i, check=what, got=got, want=want, diff=d, tol=tol, verdict='PASS' if d <= tol else 'FAIL'))
    e32 = shapes.E(RHO, 1.5); e2 = shapes.E(RHO, 2.0)
    add('N1', 'E_3/2(rho) full lattice, Chowla-Selberg vs agents', e32, AGENTS_E32_RHO, 1e-9)
    add('N2', 'E_3/2(rho) direct lattice sum + tail vs Chowla-Selberg', direct_sum(RHO, 1.5), e32, 1e-3)
    add('N3', 'E_2(rho) direct lattice sum + tail vs Chowla-Selberg', direct_sum(RHO, 2.0), e2, 1e-5)
    for U, tag in ((RHO, 'rho'), (complex(0.2, 1.1), '0.2+1.1i')):
        add('N4', f'normalisation shapes.E = 2 zeta(4) x eisenstein.E_fourier at {tag}, s = 2', shapes.E(U, 2.0), 2 * float(zeta(4)) * eisenstein.E_fourier(U.real, U.imag, 2), 1e-8)
    for s in (2.0, 1.5):
        f = lambda U, s=s: shapes.E(U, s)
        (gx, gy), _ = shapes.grad_hess(f, RHO); add('N5', f'|grad E_{s}(rho)|/E', math.hypot(gx, gy) / f(RHO), 0.0, 1e-6, 'abs')
        U = complex(0.2, 1.1); _, (hxx, hxy, hyy) = shapes.grad_hess(f, U); add('N6', f'Laplace eigenvalue of E_{s} at 0.2+1.1i', U.imag ** 2 * (hxx + hyy) / f(U), s * (s - 1), 1e-4, 'abs')
        _, (hxx, hxy, hyy) = shapes.grad_hess(f, RHO); y = RHO.imag
        add('N7', f'y^2 E_xx/E at rho, s = {s}', y * y * hxx / f(RHO), s * (s - 1) / 2, 1e-4, 'abs'); add('N7', f'y^2 E_yy/E at rho, s = {s}', y * y * hyy / f(RHO), s * (s - 1) / 2, 1e-4, 'abs')
        add('N7', f'y^2 E_xy/E at rho, s = {s}', y * y * hxy / f(RHO), 0.0, 1e-4, 'abs')
    C = 8e-7; V = lambda U: (lambda z: z * (1 + C * z) / (1 + z))(shapes.E(U, 2.0) - e2)
    _, (vxx, vxy, vyy) = shapes.grad_hess(V, RHO, h=1e-3); y = RHO.imag
    add('N8', 'SERAPIS-E canonical mass^2 2 y^2 V_xx at rho (V0 = 1) vs 2 E_2(rho)', 2 * y * y * vxx, 2 * e2, 1e-4); add('N8', 'same with V_yy', 2 * y * y * vyy, 2 * e2, 1e-4)
    _, (hxx, _, _) = shapes.grad_hess(lambda U: shapes.E(U, 1.5), RHO)
    add('N9', 'YFORK2 canonical mass^2 in V_inf units, (16/9)(y^2 E_xx/E)^2 at rho', 16 / 9 * (y * y * hxx / e32) ** 2, 0.25, 1e-4, 'abs')
    return out, dict(E2_rho=e2, E32_rho=e32)

# ----------------------------------------------------------------------------- stage 3: symbolic re-derivation
def stage3():
    import sympy as sp
    out = []
    def add(i, what, residual):
        r = sp.simplify(residual); out.append(dict(id=i, step=what, residual=str(r), verdict='REPRODUCES' if r == 0 else 'DISCREPANCY'))
    N, b, rs, phi = sp.symbols('N b rho_star phi', real=True); V = sp.Function('V')
    rc = rs * sp.exp(-3 * N + b * phi); G = sp.diff(V(phi), phi) + b * rc
    add('S1', 'moving-extremum slope d phi_min/d ln a = 3 b rho_c/(V_phiphi + b^2 rho_c)', -sp.diff(G, N) / sp.diff(G, phi) - 3 * b * rc / (sp.diff(V(phi), phi, 2) + b ** 2 * rc))
    ph = sp.Function('phi')(N); rcN = rs * sp.exp(-3 * N + b * ph)
    add('S2', 'dust scaling rho_c,N = (-3 + b phi_N) rho_c', sp.diff(rcN, N) - (-3 + b * sp.diff(ph, N)) * rcN)
    x, y, s, g = sp.symbols('x y s gamma', positive=True); E = sp.Function('E')(x, y); K = -sp.log(2 * y) - sp.log(2 * s) + g * E / s; F = 1 + 2 * g * E / s
    lap = {sp.Derivative(E, (y, 2)): 2 * E / y ** 2 - sp.Derivative(E, (x, 2))}
    add('S3', 'loop metric K_UU = F/(4 y^2)', ((sp.diff(K, x, 2) + sp.diff(K, y, 2)) / 4).subs(lap) - F / (4 * y ** 2))
    add('S3', 'loop metric K_SS = F/(4 s^2)', sp.diff(K, s, 2) / 4 - F / (4 * s ** 2))
    KUS = sp.Rational(1, 4) * (sp.diff(K, x) - sp.I * sp.diff(K, y)).diff(s) * sp.I                       # d_U d_Sbar, d_U = (d_x - i d_y)/2, d_Sbar = (d_c + i d_s)/2
    add('S3', 'loop metric K_USbar = -gamma (E_y + i E_x)/(4 s^2)', KUS + g * (sp.diff(E, y) + sp.I * sp.diff(E, x)) / (4 * s ** 2))
    ex, ey, e0 = sp.symbols('E_x E_y E_0', real=True); KUSn = (KUS.subs({sp.Derivative(E, x): ex, sp.Derivative(E, y): ey})).expand()
    F0 = 1 + 2 * g * e0 / s; det = F0 / (4 * y ** 2) * F0 / (4 * s ** 2) - (sp.re(KUSn) ** 2 + sp.im(KUSn) ** 2)
    add('S3', 'loop metric determinant', det - (F0 ** 2 - g ** 2 * y ** 2 * (ex ** 2 + ey ** 2) / s ** 2) / (16 * y ** 2 * s ** 2))
    add('S4', 'determinant bound numerator at |grad E| = 2E/y equals 1 + 4 gamma E/s', F0 ** 2 - g ** 2 * y ** 2 * (2 * e0 / y) ** 2 / s ** 2 - (1 + 4 * g * e0 / s))
    e, w, me, mw, eta, kap, D, kE, kW = sp.symbols('e w mu_e2 mu_w2 eta kappa Delta k_E k_W', real=True)
    H5 = sp.hessian(me * e ** 2 / 2 + mw * w ** 2 / 2 + eta * (e - w) ** 2 + kap * D ** 2 * (e ** 2 + w ** 2), (e, w))
    add('S5', 'eta-kappa modulus block', (H5 - sp.Matrix([[me + 2 * eta + 2 * kap * D ** 2, -2 * eta], [-2 * eta, mw + 2 * eta + 2 * kap * D ** 2]])).norm())
    H6 = sp.hessian(kE * e ** 2 / 2 + kW * w ** 2 / 2 + eta / 2 * (e - w) ** 2 + kap / 2 * D ** 2 * (e ** 2 + w ** 2), (e, w))
    add('S6', 'reverse-thread modulus block', (H6 - sp.Matrix([[kE + eta + kap * D ** 2, -eta], [-eta, kW + eta + kap * D ** 2]])).norm())
    VL, A, R, beta = sp.symbols('V_L A R beta', positive=True); rcT = R * sp.exp(b * phi)
    Asol = sp.solve(beta * A * VL * sp.exp(-beta * phi) + b * rcT, A)[0]
    add('S7', 'thread curvature b (b + beta) rho_c at the frozen dust balance', sp.diff(VL * (1 - A * sp.exp(-beta * phi)) + rcT, phi, 2).subs(A, Asol) - b * (b + beta) * rcT)
    u, sS, a_, bb = sp.symbols('deltaU deltaS a b_f'); W2 = a_ * u ** 2 / 2 - bb * u * sS
    add('S8', 'flux bridge D_U W_2 = a dU - b dS', sp.diff(W2, u) - (a_ * u - bb * sS)); add('S8', 'flux bridge D_S W_2 = -b dU', sp.diff(W2, sS) + bb * u)
    eK, gU, gS, bm = sp.symbols('e^K K_UU K_SS babs', positive=True)
    add('S8', 'flux bridge: U and S canonical masses both equal e^K K^UU K^SS |b|^2', sp.Abs(eK / gS * bm ** 2 / gU - eK / gU / gS * bm ** 2) + sp.Abs(eK / gU * bm ** 2 / gS - eK / gU / gS * bm ** 2))
    t = sp.symbols('t', positive=True); X, Y, Xd, Yd, a3 = sp.symbols('X Y Xd Yd a3'); Vxy = sp.Function('V')(X, Y); L = a3 * ((Xd ** 2 + Yd ** 2) / (4 * Y ** 2) - Vxy)
    xf, yf, af = sp.Function('x')(t), sp.Function('y')(t), sp.Function('a')(t); Hh = sp.diff(af, t) / af
    sub = {X: xf, Y: yf, Xd: sp.diff(xf, t), Yd: sp.diff(yf, t), a3: af ** 3}; Vx, Vy = sp.symbols('V_x V_y')
    def EL(q, qd):
        return (sp.diff(sp.diff(L, qd).subs(sub), t) - sp.diff(L, q).subs(sub)).subs({sp.Derivative(Vxy, X).subs(sub): Vx, sp.Derivative(Vxy, Y).subs(sub): Vy})
    elx = sp.diff((a3 * Xd / (2 * Y ** 2)).subs(sub), t) + af ** 3 * Vx; ely = sp.diff((a3 * Yd / (2 * Y ** 2)).subs(sub), t) + af ** 3 * ((sp.diff(xf, t) ** 2 + sp.diff(yf, t) ** 2) / (2 * yf ** 3) + Vy)
    add('S9', 'YFORK2 x equation from its Lagrangian', elx * 2 * yf ** 2 / af ** 3 - (sp.diff(xf, t, 2) - 2 / yf * sp.diff(xf, t) * sp.diff(yf, t) + 3 * Hh * sp.diff(xf, t) + 2 * yf ** 2 * Vx))
    add('S9', 'YFORK2 y equation from its Lagrangian', ely * 2 * yf ** 2 / af ** 3 - (sp.diff(yf, t, 2) + (sp.diff(xf, t) ** 2 - sp.diff(yf, t) ** 2) / yf + 3 * Hh * sp.diff(yf, t) + 2 * yf ** 2 * Vy))
    k = sp.symbols('k', positive=True); Rf, Df, Bq = sp.Function('R')(t), sp.Function('Delta')(t), sp.Function('beta_Q')(t)
    cp = lambda f: af * sp.diff(af * sp.diff(f, t), t)                                                    # f'' with ' = a d/dt
    conf = cp(Rf) + k ** 2 / 3 * Rf - sp.Rational(4, 3) * (cp(Df) + k ** 2 * Bq)
    cosm = sp.diff(Rf, t, 2) + Hh * sp.diff(Rf, t) + k ** 2 / (3 * af ** 2) * Rf - sp.Rational(4, 3) * (sp.diff(Df, t, 2) + Hh * sp.diff(Df, t) + k ** 2 / af ** 2 * Bq)
    add('S10', 'radiation oscillator: conformal form = a^2 x cosmic form', conf - af ** 2 * cosm)
    lam = sp.symbols('lambda'); roots = set(sp.roots(lam ** 4 * (lam + 1) * (3 * lam - 2) / 3, lam)) - {0}; ind = set(sp.roots(lam * (lam - 1) + sp.Rational(4, 3) * lam - sp.Rational(2, 3), lam))
    add('S11', 'non-zero roots of C(lambda) equal the matter-era growth exponents {2/3, -1}', sp.Integer(0 if roots == ind == {sp.Rational(2, 3), -1} else 1))
    f = sp.Function('f')(x, y); Kss = sp.diff(-sp.log(2 * y), y, 2) / 4                                    # K_SSbar for K = -ln(-i(S - Sbar))
    v4 = (1 / Kss) * sp.Rational(1, 4) * (sp.diff(f, x) ** 2 + sp.diff(f, y) ** 2); v3 = sp.Rational(4, 9) * y ** 2 * (sp.diff(f, x) ** 2 + sp.diff(f, y) ** 2)
    add('S12', 'literal v4 normalisation is 9/4 of the v3 / YFORK2 one', v4 / v3 - sp.Rational(9, 4))
    return out

# ----------------------------------------------------------------------------- stage 4: contradiction finder
CLAIMS = [  # (quantity, who requires it, value, note)
 ('V_w / (V0 E_2(rho))', 'loop_metric bridge (its own 2:1 mass tuning)', 32.0, 'audit section 2'),
 ('V_w / (V0 E_2(rho))', 'flux_bridge (matching its quadratic term to the loop candidate)', 8.0, 'audit section 2'),
 ('Laplace eigenvalue of the shape function', 'serapis_e (E_2)', 2.0, 'audit sections 1, 4'),
 ('Laplace eigenvalue of the shape function', 'yfork2 (E_3/2)', 0.75, 'audit section 1'),
 ('Laplace eigenvalue of the shape function', 'weave_v4 (E_3/2)', 0.75, 'audit section 1'),
 ('Weave gauge coefficient at rho', 'weave_v4 source text: 9 Re S', 9 * RHO.real, 'audit section 1'),
 ('Weave gauge coefficient at rho', 'weave_v4 source number', 7.79, 'audit section 1 (quoted to 3 figures)'),
 ('Weave gauge coefficient at rho', 'proposed reading: 9 Im S', 9 * RHO.imag, 'audit section 1; not adopted without the source owner'),
 ('canonical modulus mass^2 at rho / V_inf', 'yfork2 and Weave v3 (4/9 factor)', 0.25, 'audit sections 1, 3'),
 ('canonical modulus mass^2 at rho / V_inf', 'weave_v4 literal (no 4/9 factor)', 9 / 16, 'audit section 1: two degenerate eigenvalues 9/16'),
]
def stage4(claims=CLAIMS, tol=1e-6):
    groups = {}
    for q, who, v, note in claims: groups.setdefault(q, []).append((who, v, note))
    out = []
    for q, items in groups.items():
        vals = [v for _, v, _ in items]; spread = (max(vals) - min(vals)) / max(abs(max(vals)), abs(min(vals)), 1e-300)
        if spread > tol: out.append(dict(quantity=q, spread=spread, requires=[dict(who=w, value=v, source=n) for w, v, n in items]))
    return out
EXPECTED = ['V_w / (V0 E_2(rho))', 'Laplace eigenvalue of the shape function', 'Weave gauge coefficient at rho']

if __name__ == '__main__':
    n, vals = stage2(); s = stage3(); c = stage4()
    found = [x['quantity'] for x in c]; finder_ok = all(e in found for e in EXPECTED); new = [q for q in found if q not in EXPECTED]
    res = dict(stage2=n, values=vals, stage3=s, stage4=c, finder_pass=finder_ok, new_disagreements=new,
               summary=dict(numbers_pass=sum(x['verdict'] == 'PASS' for x in n), numbers_total=len(n), symbolic_reproduce=sum(x['verdict'] == 'REPRODUCES' for x in s), symbolic_total=len(s),
                            contradictions=len(c)))
    (ROOT / 'field_tests' / 'results' / 'd2259_ufe_stages.json').write_text(json.dumps(res, indent=1, default=float))
    for x in n: print(f"{x['verdict']:5s} {x['id']} {x['check']}: got {x['got']:.12g} want {x['want']:.12g} diff {x['diff']:.2e} (tol {x['tol']:g})")
    for x in s: print(f"{x['verdict']:11s} {x['id']} {x['step']}" + ('' if x['verdict'] == 'REPRODUCES' else '  residual: ' + x['residual'][:160]))
    for x in c: print('DISAGREE', x['quantity'], '->', [(r['who'], round(r['value'], 6)) for r in x['requires']])
    print('finder found the three known disagreements:', finder_ok, '| not in the lock list:', new); print(json.dumps(res['summary']))
