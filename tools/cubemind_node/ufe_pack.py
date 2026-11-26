"""UFE pack for the Field Engine (25 Nov 2026) - built from the local agents' final derivation audit
(bridge/REPORTS/UFE_final_copilot_2026-11-25.md, AEGIS commit 1fa03d92).

What that audit says, and what this pack therefore encodes:
  * There is NO single sourced UFE action. There are three separate source sectors and several conditional bridges.
  * Every relation is DERIVED, CONDITIONAL (on a named model), ASSUMED, OPEN or BLOCKED.
So this is not "the UFE as an engine". It is the audit as an engine:
  SECTORS   the separate source models, never merged.
  BRIDGES   the proposed joins, each with the assumptions it rests on.
  TOOLS     only relations that are DERIVED, or CONDITIONAL with a closed formula, each with an INDEPENDENT tester.
  GATES     the OPEN and BLOCKED items. They are reported every run and can never be registered as tools or "learned".
  combine() refuses to treat two sectors as one model unless a declared bridge joins them, and then returns its conditions.
Use: python engine.py --pack ufe --models ...   (adds these tools to the engine; every ledger entry carries the status and model)."""
import math

SECTORS = {
 'weave_v4':  dict(name='Weave v4 proposal', compactification='IIB Z6-II orientifold', modular='E_{3/2}(S), Laplace eigenvalue 3/4', status='CONDITIONAL'),
 'yfork2':    dict(name='Locked YFORK2 scalar sector', compactification='scalar-only model', modular='E_{3/2}(tau), Laplace eigenvalue 3/4', status='CONDITIONAL'),
 'serapis_e': dict(name='SERAPIS-E', compactification='IIB T6/(Z2xZ2) orientifold', modular='E_2(U), Laplace eigenvalue 2', status='CONDITIONAL'),
}
BRIDGES = {
 'loop_metric':  dict(joins=('serapis_e', 'yfork2'), status='ASSUMED', rests_on=['K = -ln(2y) - ln(2s) + gamma E_2(U)/s is a chosen truncation', 'gamma >= 0', 'combined potential is an assumption', 'has a mixed covariant cubic: no cubic-free stability theorem applies']),
 'j_link':       dict(joins=('serapis_e', 'yfork2'), status='ASSUMED', rests_on=['tree product metric', 'eta, kappa >= 0', 'the couplings and the physical identity of phi are assumed']),
 'product_link': dict(joins=('serapis_e', 'yfork2'), status='ASSUMED', rests_on=['I_p definitions and UV origin incomplete in the record']),
 'flux_bridge':  dict(joins=('serapis_e', 'yfork2'), status='CONDITIONAL', rests_on=['W = A(U) - S B(U)', 'W = D_U W = D_S W = 0', 'positive diagonal Kahler metric', 'no omitted sector or uplift', 'unbroken order-three U symmetry at rho', 'toy F-term result, not a flux realisation']),
}
GATES = [
 ('OPEN',    'compactification', 'SERAPIS-E is T6/(Z2xZ2) with E_2; the Weave is Z6-II with E_{3/2}. No common light spectrum, brane/duality action or field map. The eigenvalues differ (2 vs 3/4).'),
 ('BLOCKED', 'gauge convention', 'The Weave source writes 9 Re S = 7.79 at rho, but 7.79 = 9 Im rho. Source-owner intent needed; no silent swap.'),
 ('BLOCKED', 'T1 application',   'The moving-extremum slope is derived, but the D1716 CLASS background needed to compare at z = 0, 1, 3 is not in the accessible record.'),
 ('OPEN',    'T3 physical boundary', 'Hessian conditions are derived per stated normalisation; a common baseline Hessian and action are absent.'),
 ('OPEN',    'perturbations and observables', 'T2 equations are conditional on a chosen action and fluid closure; no reduced no-ghost/gradient proof, no photon map, no quantum state.'),
 ('OPEN',    'flux realisation', 'No joint quantised flux periods, tadpoles or controlled UV completion.'),
 ('OPEN',    'weave thread', 'phi_thread and V_thread: geometric origin and potential not supplied.'),
 ('OPEN',    'tuning mismatch', 'The loop candidate needs V_w = 32 V0 E_2(rho) for its 2:1 tuning; matching the flux bridge needs V_w = 8 V0 E_2(rho). They disagree by a factor 4.'),
]
def combine(a, b):
    """May sectors a and b be treated as one model? -> (allowed, status, conditions). Never True without a declared bridge."""
    if a == b: return True, SECTORS[a]['status'], ['same sector']
    hits = {k: v for k, v in BRIDGES.items() if set(v['joins']) == {a, b}}
    if not hits: return False, 'OPEN', [f'no declared bridge between {a} and {b}; shared labels, equal rho coordinates or matched local masses are not an identification']
    return True, 'CONDITIONAL', [f'{k} [{v["status"]}]: ' + '; '.join(v['rests_on']) for k, v in hits.items()]

# ----------------------------------------------------------------------------- tools: fitter + independent tester
BETA = 2 * math.sqrt(2)
def _lap(a): return a['s'] * (a['s'] - 1)
def _lap_test(a, v):                         # independent: numerical hyperbolic Laplacian of y^s, y^2 d^2/dy^2
    s, y, h = a['s'], 1.7, 1e-4
    num = y * y * ((y + h) ** s - 2 * y ** s + (y - h) ** s) / h ** 2 / y ** s
    return abs(num - v) < 1e-5 * max(abs(v), 1)
def _slope(a): return 3 * a['b'] * a['rho_c'] / (a['Vpp'] + a['b'] ** 2 * a['rho_c'])
def _slope_test(a, v):                       # independent: solve V_phi + b rho_c(N, phi) = 0 at N = +-h for a quadratic V and difference the roots
    b, rc, k = a['b'], a['rho_c'], a['Vpp']; phi0 = b * rc / k                       # so the root at N = 0 is phi = 0
    def root(N):
        x = 0.0
        for _ in range(60):
            f = k * (x - phi0) + b * rc * math.exp(-3 * N + b * x); x -= f / (k + b * b * rc * math.exp(-3 * N + b * x))
        return x
    h = 1e-5; num = (root(h) - root(-h)) / (2 * h)
    return abs(num - v) < 1e-5 * max(abs(v), 1e-9)
def _hmin(a):
    p = a['mu_e2'] + 2 * a['eta'] + 2 * a['kappa'] * a['Delta'] ** 2; q = a['mu_w2'] + 2 * a['eta'] + 2 * a['kappa'] * a['Delta'] ** 2; c = -2 * a['eta']
    return ((p + q) - math.sqrt((p - q) ** 2 + 4 * c * c)) / 2
def _hmin_test(a, v):                        # independent: characteristic equation residual, and it must be the SMALLER root (Rayleigh bound)
    p = a['mu_e2'] + 2 * a['eta'] + 2 * a['kappa'] * a['Delta'] ** 2; q = a['mu_w2'] + 2 * a['eta'] + 2 * a['kappa'] * a['Delta'] ** 2; c = -2 * a['eta']
    return abs((p - v) * (q - v) - c * c) < 1e-9 * max(p * q, 1) and v <= min(p, q) + 1e-12 and (p + q - v) >= v - 1e-12
def _thread(a): return a['b'] * (a['b'] + BETA) * a['rho_c']
def _thread_test(a, v):                      # independent: finite-difference curvature of V_R + R e^{b phi} at the frozen dust balance
    b, rc = a['b'], a['rho_c']; VA = -b * rc / BETA                                   # balance: beta A V_L e^{-beta phi} + b rho_c = 0 at phi = 0
    f = lambda x: -VA * math.exp(-BETA * x) + rc * math.exp(b * x); h = 1e-4
    num = (f(h) - 2 * f(0) + f(-h)) / h ** 2
    return abs(num - v) < 1e-5 * max(abs(v), 1e-6)
def _det(a):
    F = 1 + 2 * a['gamma'] * a['E'] / a['s']
    return (F * F - a['gamma'] ** 2 * a['y'] ** 2 * (a['Ex'] ** 2 + a['Ey'] ** 2) / a['s'] ** 2) / (16 * a['y'] ** 2 * a['s'] ** 2)
def _det_test(a, v):                         # independent: the determinant from the three metric entries
    F = 1 + 2 * a['gamma'] * a['E'] / a['s']; KUU = F / (4 * a['y'] ** 2); KSS = F / (4 * a['s'] ** 2)
    KUS2 = a['gamma'] ** 2 * (a['Ex'] ** 2 + a['Ey'] ** 2) / (16 * a['s'] ** 4)
    return abs(KUU * KSS - KUS2 - v) < 1e-10 * max(abs(v), 1e-12)
def _flux(a): return math.exp(a['K']) * a['KUUinv'] * a['KSSinv'] * a['b'] ** 2
def _flux_test(a, v):                        # independent: canonically normalise each field separately; the two masses must agree with each other and with v
    mU = math.exp(a['K']) * a['KSSinv'] * a['b'] ** 2 / (1 / a['KUUinv']); mS = math.exp(a['K']) * a['KUUinv'] * a['b'] ** 2 / (1 / a['KSSinv'])
    return abs(mU - mS) < 1e-10 * max(mU, 1e-12) and abs(mU - v) < 1e-10 * max(v, 1e-12)
def _growth(a): return (a['t2'] / a['t1']) ** (2 / 3)
def _growth_test(a, v):                      # independent: integrate delta'' + 2H delta' - (3/2) H^2 delta = 0, H = 2/(3t), with RK4 in ln t
    n = 4000; L = math.log(a['t2'] / a['t1']); h = L / n; d, w = 1.0, 2 / 3                                    # w = d(delta)/d ln t on the growing mode
    f = lambda d, w: (w, w - (4 / 3) * w + (2 / 3) * d)                                                        # delta_xx = delta_x - (4/3) delta_x + (2/3) delta
    for _ in range(n):
        k1 = f(d, w); k2 = f(d + h / 2 * k1[0], w + h / 2 * k1[1]); k3 = f(d + h / 2 * k2[0], w + h / 2 * k2[1]); k4 = f(d + h * k3[0], w + h * k3[1])
        d += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); w += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return abs(d - v) < 1e-6 * v

def _u(r, lo, hi, nd=3): return round(r.uniform(lo, hi), nd)
TOOLS = {
 'ufe_laplace':   ('ufe', 'A non-holomorphic Eisenstein series E_s has Laplace eigenvalue s(s-1) on the upper half-plane. Compute the eigenvalue for {x}.', _lap, _lap_test, 0.005,
                   lambda r, k: {'s': r.choice([2, 1.5] if k == 0 else [2, 1.5, 2.5, 3, 3.5, 4, 5][: 2 + 2 * k])}),
 'ufe_extremum':  ('ufe', 'Dust with density rho_c = rho* a^-3 e^(b phi) sits at an extremum V_phi + b rho_c = 0. The extremum moves as d(phi_min)/d(ln a) = 3 b rho_c / (V_phiphi + b^2 rho_c). Compute it for {x} (Vpp is V_phiphi).', _slope, _slope_test, 0.02,
                   lambda r, k: {'b': -_u(r, 0.02, 0.2 + 0.2 * k), 'rho_c': _u(r, 0.1, 2 + 2 * k), 'Vpp': _u(r, 0.2, 5)}),
 'ufe_hessian':   ('ufe', 'A 2x2 mass matrix has diagonal entries mu_e2 + 2 eta + 2 kappa Delta^2 and mu_w2 + 2 eta + 2 kappa Delta^2, and off-diagonal entries -2 eta. Compute its SMALLEST eigenvalue for {x}.', _hmin, _hmin_test, 0.02,
                   lambda r, k: {'mu_e2': _u(r, 0.2, 3), 'mu_w2': _u(r, 0.2, 3), 'eta': _u(r, 0, 1 + k), 'kappa': _u(r, 0, 1 + k), 'Delta': _u(r, 0, 1 + 0.5 * k)}),
 'ufe_thread':    ('ufe', 'At the frozen dust balance of the reverse-thread model the thread curvature is b (b + beta) rho_c with beta = 2 sqrt(2). Compute it for {x} (a negative value means a saddle).', _thread, _thread_test, 0.02,
                   lambda r, k: {'b': -_u(r, 0.02, 0.5) if k == 0 or r.random() < 0.6 else -_u(r, 3.0, 4.5), 'rho_c': _u(r, 0.1, 2 + 2 * k)}),
 'ufe_loop_det':  ('ufe', 'For K = -ln(2y) - ln(2s) + gamma E/s the Kahler metric determinant is (F^2 - gamma^2 y^2 (Ex^2 + Ey^2)/s^2) / (16 y^2 s^2) with F = 1 + 2 gamma E/s. Compute it for {x}.', _det, _det_test, 0.02,
                   lambda r, k: (lambda y, E: {'y': y, 's': _u(r, 0.6, 2 + k), 'gamma': _u(r, 0, 0.3 + 0.2 * k), 'E': E, 'Ex': _u(r, -0.5, 0.5), 'Ey': round(2 * E / y * _u(r, 0.2, 0.9), 3)})(_u(r, 0.87, 2 + k), _u(r, 2.0, 6))),
 'ufe_flux_mass': ('ufe', 'In the flux-bridge toy model every mass squared is e^K * KUUinv * KSSinv * b^2. Compute it for {x}.', _flux, _flux_test, 0.02,
                   lambda r, k: {'K': -_u(r, 0.2, 2 + k), 'KUUinv': _u(r, 1, 6 + 4 * k), 'KSSinv': _u(r, 1, 6 + 4 * k), 'b': _u(r, 0.1, 2)}),
 'ufe_growth':    ('ufe', 'In the matter era the dust density contrast grows as t^(2/3). Compute Delta(t2)/Delta(t1) for {x}.', _growth, _growth_test, 0.01,
                   lambda r, k: (lambda t1: {'t1': t1, 't2': round(t1 * _u(r, 2, 10 * 3 ** k), 2)})(_u(r, 1, 50, 1))),
}
# status, the model the relation belongs to, where in the audit it is, and what it must NOT be read as
META = {
 'ufe_laplace':   dict(status='DERIVED',     model='mathematics', source='audit section 4', not_a='reason to identify E_2 with E_{3/2}: the eigenvalues 2 and 3/4 differ'),
 'ufe_extremum':  dict(status='DERIVED',     model='coupled-dust late sector (assumed)', source='audit section 3, T1', not_a='statement that the field tracks the extremum; the CLASS comparison is BLOCKED'),
 'ufe_hessian':   dict(status='CONDITIONAL', model='five-field local ansatz (assumed)', source='audit section 3, T3', not_a='physical stability boundary: the baseline Hessian and shared action are not supplied'),
 'ufe_thread':    dict(status='CONDITIONAL', model='reverse-thread model (assumed)', source='audit section 3, T3', not_a='proof of an evolving attractor; b = -0.074 gives a saddle'),
 'ufe_loop_det':  dict(status='CONDITIONAL', model='loop-metric candidate (assumed)', source='audit section 2', not_a='positivity proof beyond this two-field truncation'),
 'ufe_flux_mass': dict(status='CONDITIONAL', model='flux-bridge toy model', source='audit section 2', not_a='flux-realisation theorem or joint action'),
 'ufe_growth':    dict(status='CONDITIONAL', model='separately assumed scalar + dust + radiation model, exact quadratic V, fixed k', source='handoff review update 25 Nov', not_a='uniform-in-k, nonlinear or quantum stability result; a generic cubic 2:1 resonance is a counterexample to broadening it'),
}
def register(engine_module):
    """Add the UFE tools to the engine. Refuses anything not DERIVED or CONDITIONAL, and anything without META."""
    for name, tool in TOOLS.items():
        m = META.get(name)
        if not m or m['status'] not in ('DERIVED', 'CONDITIONAL'): raise ValueError(f'{name}: only DERIVED or CONDITIONAL relations with a status record may become tools')
        engine_module.TOOLS[name] = tool; engine_module.META[name] = m
    return list(TOOLS)
def gates_report():
    return '\n'.join(f'  {s:8s} {k}: {t}' for s, k, t in GATES)
