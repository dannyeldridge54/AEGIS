"""The Hexagon (PREREG_HEX1): a centre engine and six node engines on one bus, in one loop.
Centre = where the fields settle + the Bloom score + the judge of postulates. Nodes = nuclear, forces, neutrinos, inflation, dark sector,
late universe. Each node reads the bus, derives with the existing tools (in-process, memoised), writes the bus, scores locally and posts
postulates. The loop sweeps the nodes until the bus settles, then judges postulates until a round accepts nothing (NULL).
Usage: python hex.py            one settled pass + board
       python hex.py --loop     settle + postulate rounds until NULL
       python hex.py --json"""
import functools, json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rings as G
AS_ENGINE = 0.11446   # D2221/D2222: Weave alpha_s(M_Z) from theory/tests/d2221_as_top.py (single source)
AEGIS = G.AEGIS; W = G.W; B = G.B
sys.path.insert(0, AEGIS)

class Bus:
    def __init__(self): self.v, self.meta, self.sweep = {}, {}, 0
    def put(self, node, key, value, label):
        self.v[key] = value; self.meta[key] = dict(node=node, label=label, sweep=self.sweep)
    def get(self, key, default=None): return self.v.get(key, default)
    def snapshot(self): return {k: v for k, v in self.v.items() if isinstance(v, (int, float, bool, str))}

def gauss_pull(x, mu, sig): return (x - mu) / sig

# ------------------------------------------------------------------ the six node engines
@functools.lru_cache(maxsize=64)
def _bbn(ombh2, dN):
    from tools.janus_astro import bbn
    return bbn.Yp(ombh2, dN), bbn.DH(ombh2, dN)

@functools.lru_cache(maxsize=64)
def _lt(h, ombh2, omch2, w0, wa):
    from tools.janus_lt.background import Cosmo
    from tools.janus_lt.growth import growth
    c = Cosmo(100 * h, ombh2, omch2, w0, wa); g = growth(c, [0.5, 1.0])
    return {z: dict(DM_Mpc=c.DM(z), H=c.H(z), f=g[z][1], D=g[z][0]) for z in (0.5, 1.0)}

@functools.lru_cache(maxsize=64)
def _wino_xsec(m_GeV):
    from tools.lhc import xsec as X
    return X.total(m_GeV, '13.6')['sum'] if 100 <= m_GeV <= 2000 else None

class Node:
    name = 'node'
    def run(self, bus): return {}
    def postulates(self, bus, knobs): return []

class Nuclear(Node):
    name = 'N1 nuclear'
    YP, DH = (0.245, 0.003), (2.547e-5, 0.025e-5)      # PDG 2024 primordial helium mass fraction, D/H
    def run(self, bus):
        a_s = bus.get('alpha_s'); obs = 0.118
        hoyle = W.weave_nuclear({'dalpha_s': a_s - obs, 'alpha_s': obs})
        Yp, DH = _bbn(bus.get('ombh2'), bus.get('dNeff'))
        from tools.janus_astro import bbn as _b
        sYp, sDH = _b.sigma(bus.get('ombh2'), bus.get('dNeff'))      # DEV-2: PRIMAT theory error in quadrature
        wb = bus.get('ombh2'); sYp = math.hypot(sYp, abs(_b.Yp(wb + 1e-4, bus.get('dNeff')) - _b.Yp(wb - 1e-4, bus.get('dNeff'))) / 2e-4 * 0.00015)   # D2222
        sDH = math.hypot(sDH, abs(_b.DH(wb + 1e-4, bus.get('dNeff')) - _b.DH(wb - 1e-4, bus.get('dNeff'))) / 2e-4 * 0.00015)   # D2221: omega_b error (Planck 0.00015)
        bus.put(self.name, 'hoyle_radius', hoyle['radius'], 'LIVE'); bus.put(self.name, 'hoyle_inside', hoyle['inside'], 'LIVE')
        bus.put(self.name, 'dmq_over_Lambda', hoyle['dmq_over_Lambda'], 'LIVE'); bus.put(self.name, 'dm_p_MeV', 'not wired (DEV-1)', 'NONE')
        bus.put(self.name, 'Yp', Yp, 'LIVE'); bus.put(self.name, 'DH', DH, 'LIVE')
        return dict(pull_Yp=(Yp - self.YP[0]) / math.hypot(self.YP[1], sYp), pull_DH=(DH - self.DH[0]) / math.hypot(self.DH[1], sDH), hoyle_inside=hoyle['inside'],
                    hoyle_note='restates the forces alpha_s tension; not independent (DEV-3)')
    def postulates(self, bus, knobs):
        if not bus.get('hoyle_inside'): return [dict(node=self.name, flag='Hoyle window left: forces node must reduce the alpha_s shift', knobs=None)]
        return []

class Forces(Node):
    name = 'N2 forces'
    def run(self, bus):
        s = bus.get('s_m32'); m_w, m_g = 0.687 * s, 4.93 * s
        a_s = AS_ENGINE * math.exp(   # D2221: engine value with MS->DR (D2220) + top decoupling (D2221); was 0.1142
            B.D['levers']['lnm32']['moves']['alpha_s'] * math.log(s))
        xs = _wino_xsec(round(m_w * 1000, 6))
        bus.put(self.name, 'm_wino_TeV', m_w, 'LINEAR'); bus.put(self.name, 'm_gluino_TeV', m_g, 'LINEAR'); bus.put(self.name, 'alpha_s', a_s, 'LINEAR')
        bus.put(self.name, 'wino_xsec_fb_13p6', xs if xs is not None else float('nan'), 'LIVE')
        bus.put(self.name, 'wino_events_3ab', xs * 3000 if xs is not None else float('nan'), 'LIVE')
        return dict(pull_alpha_s=gauss_pull(a_s, 0.118, 0.0009))
    def postulates(self, bus, knobs):
        k = B.D['levers']['lnm32']['moves']['alpha_s']; s = math.exp(math.log(0.118 / AS_ENGINE) / k) if k else None
        return [dict(node=self.name, why='zero the alpha_s pull through the m32 lever', knobs=dict(knobs, s_m32=s))] if s else []

class Neutrinos(Node):
    name = 'N3 neutrinos'
    def run(self, bus):
        r1 = G.ring1(G.S13SQ); kq = W.weave_koide({'masses': [0.51099895, 105.6583755, 1776.93]})
        bus.put(self.name, 'theta12', r1['theta12'], 'LIVE'); bus.put(self.name, 'm_bb_meV', r1['m_bb'], 'LIVE'); bus.put(self.name, 'sum_mnu', r1['sum_mnu'], 'LIVE')
        bus.put(self.name, 'koide_Q_leptons', kq['Q'], 'LIVE')
        return dict(koide_dev=kq['Q'] - 2 / 3)

class Inflation(Node):
    name = 'N4 inflation'
    def run(self, bus):
        p = G.pattern(bus.get('C'), bus.get('T_R'))
        for k in ('ns', 'r', 'running', 'Nstar'): bus.put(self.name, k, p[k], 'LIVE')
        return dict(pull_ns=gauss_pull(p['ns'], 0.9728, 0.0029))
    def postulates(self, bus, knobs):
        from scipy.optimize import minimize_scalar
        f = lambda c: gauss_pull(G.pattern(float(f'{c:.6e}'), bus.get('T_R'))['ns'], 0.9728, 0.0029) ** 2
        r = minimize_scalar(f, bounds=(1.0e-6, 1.6e-6), method='bounded', options=dict(xatol=1e-9))
        return [dict(node=self.name, why='C that puts n_s on the data', knobs=dict(knobs, C=float(f'{r.x:.6e}')))]

class Dark(Node):
    name = 'N5 dark sector'
    def run(self, bus):
        T = bus.get('T_R'); r3 = G.ring3(T)
        bus.put(self.name, 'genesis_viable', r3['genesis_viable'], 'LIVE'); bus.put(self.name, 'eps_needed', r3['eps_needed'], 'LIVE')
        bus.put(self.name, 'dNeff', 0.0, 'STORED')
        return dict(genesis_viable=r3['genesis_viable'])

class Late(Node):
    name = 'N6 late universe'
    def run(self, bus):
        lt = _lt(0.6736, bus.get('ombh2'), 0.12, -1.0, 0.0)
        for z, d in lt.items(): bus.put(self.name, f'DM_Mpc_z{z}', d['DM_Mpc'], 'LIVE'); bus.put(self.name, f'f_z{z}', d['f'], 'LIVE')
        bus.put(self.name, 'alpha_drift', 3.8e-10, 'STORED')
        return dict(sum_mnu_seen=bus.get('sum_mnu'))

NODES = [Forces(), Nuclear(), Neutrinos(), Inflation(), Dark(), Late()]

# ------------------------------------------------------------------ the centre
def centre_publish(bus, knobs):
    s = W.weave_point({})
    for k in ('alpha_inv_M12', 'M12_GeV', 'N', 'm32_GeV'): bus.put('centre', k, s[k], 'INPUT')
    for k, v in knobs.items(): bus.put('centre', k, v, 'KNOB')
    bus.put('centre', 'ombh2', 0.02237, 'INPUT')

def centre_score(bus):
    live = dict(alpha_s=bus.get('alpha_s'), n_s=bus.get('ns'),   # D2221: live engine alpha_s (was the data file's 0.1142)
                 r=bus.get('r'), running=bus.get('running'), theta12=bus.get('theta12'), m_bb=bus.get('m_bb_meV'), sum_mnu=bus.get('sum_mnu'))
    base = B.apply_levers(B.D['terms'], {'lnm32': bus.get('s_m32')})
    terms = [dict(t, ours=live[t['id']]) if t['id'] in live else t for t in base]
    return terms

def settle(knobs, max_sweeps=6):
    bus = Bus(); centre_publish(bus, knobs); local = {}; prev = None
    dNeff0 = 0.0; bus.put('centre', 'dNeff', dNeff0, 'INPUT'); bus.put('centre', 'alpha_s', AS_ENGINE, 'INPUT')
    for sw in range(1, max_sweeps + 1):
        bus.sweep = sw
        for n in NODES: local[n.name] = n.run(bus)
        snap = bus.snapshot()
        if prev is not None and all(k in prev and (v == prev[k] or (isinstance(v, float) and (math.isnan(v) and math.isnan(prev[k]) or abs(v - prev[k]) <= 1e-12 * max(1, abs(v))))) for k, v in snap.items()):
            return bus, local, sw
        prev = snap
    return bus, local, max_sweeps

COUNTED = set()   # knobs already charged (C, T_R, s_m32 are not in the Bloom's fitted list; each costs +1 the first time it moves)
ADOPTED = dict(G.ADOPTED)

def evaluate(knobs):
    bus, local, sw = settle(knobs); terms = centre_score(bus)
    moved = {k for k in knobs if knobs[k] != ADOPTED[k]}
    k_fit = sum(k['n'] for k in B.D['fitted_knobs']); lnL, tgt, N, k = B.target(terms, k_fit, len(moved))
    return dict(knobs=knobs, bus=bus, local=local, sweeps=sw, lnL=lnL, target=tgt, k=k, N=N, terms=terms)

def loop(max_rounds=6, log=print):
    cur = evaluate(dict(ADOPTED)); history = []
    for rnd in range(1, max_rounds + 1):
        posts = [p for n in NODES for p in n.postulates(cur['bus'], cur['knobs'])]
        accepted = None
        for p in posts:
            if p.get('knobs') is None: history.append(dict(round=rnd, **{k: v for k, v in p.items() if k != 'knobs'}, decision='FLAG')); continue
            trial = evaluate(p['knobs']); ok = trial['target'] > cur['target'] + 1e-9
            history.append(dict(round=rnd, node=p['node'], why=p['why'], knobs=p['knobs'], target_before=cur['target'], target_after=trial['target'],
                                lnL_after=trial['lnL'], decision='ACCEPT' if ok else 'REJECT'))
            log(f'  round {rnd}: {p["node"]}: {p["why"]} -> target {cur["target"]:.3f} -> {trial["target"]:.3f}  {"ACCEPT" if ok else "reject"}')
            if ok and (accepted is None or trial['target'] > accepted['target']): accepted = trial
        if accepted is None: log(f'  round {rnd}: NULL (nothing accepted)'); return cur, history, rnd
        cur = accepted
    return cur, history, max_rounds

def board(E):
    b = E['bus']; L = [f'Hexagon: knobs {E["knobs"]}  settled in {E["sweeps"]} sweeps  lnL {E["lnL"]:.3f}  target {E["target"]:.3f} (k={E["k"]}, N={E["N"]})']
    for n in NODES:
        keys = [k for k, m in b.meta.items() if m['node'] == n.name]
        L.append(f'  {n.name}: ' + ', '.join(f'{k}={b.v[k]:.5g}' if isinstance(b.v[k], float) else f'{k}={b.v[k]}' for k in keys) + f'   local {E["local"][n.name]}')
    return '\n'.join(L)

if __name__ == '__main__':
    t0 = time.perf_counter(); E = evaluate(dict(ADOPTED)); t1 = time.perf_counter()
    print(board(E)); print(f'pass {t1 - t0:.2f} s')
    if '--loop' in sys.argv:
        t2 = time.perf_counter(); F, H, R = loop(); print(f'loop ended after {R} rounds in {time.perf_counter() - t2:.1f} s'); print(board(F))
