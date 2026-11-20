"""Every connection in the Weave: equations as nodes, quantities they share as edges (Danny 20 Nov 09:34 "check all paths eq").
A connection = a quantity that appears in two equations of different sectors. A path = a chain of shared quantities.
Status of each equation: C computed in our tools, D derived in notes, P postulate/hosted, O open. Built from the D-notes; no new physics."""
import itertools, json, collections

EQ = {  # id: (sector, status, short form, inputs, outputs)
 'E1 inflation plateau': ('early', 'C', 'V(tau1)=Vinf(1-A e^(-beta_D psi)), A=16zeta(2)/3zeta(3)=7.30', ['A', 'D', 'C_tilt', 'N*'], ['n_s', 'r', 'alpha_s', 'H_inf', 'm_phi']),
 'E2 r ladder': ('early', 'C', 'r_D = r_10*8/(D-2)', ['D'], ['r']),
 'E3 N* from history': ('early', 'D', 'N* = f(T_R, V_end, dilution)', ['T_R', 'dilution'], ['N*']),
 'E4 reheating': ('early', 'D', 'T_R from inflaton decay to D3 gauge fields', ['m_phi', 'g_s'], ['T_R']),
 'E25 Y-fork': ('early', 'D', 'end of inflation: ridge at x=1/2; slow moduli drain to i (69%)', ['tau1 path'], ['tau_nu=i', 'tau_lep=rho']),
 'E27 species scale': ('early', 'P', 'V0 ~ |grad ln Lambda_sp|^2 (Zhinu)', ['Lambda_sp'], ['A']),
 'E5 leptogenesis': ('matter', 'D', 'eta_B from heavy-neutrino decay', ['T_R', 'm_phi', 'M_N'], ['eta_B']),
 'E15 seesaw': ('lepton', 'D', 'm_nu = m_D^2 / M_N', ['M_N', 'tau_nu=i'], ['Sum m_nu', 'm_nu masses']),
 'E12 Koide at rho': ('lepton', 'D', 'sqrt(M_l) circulant from residual Z3 at rho: Q=2/3, delta=2/9 (emp.)', ['tau_lep=rho'], ['m_e', 'm_mu', 'm_tau']),
 'E13 TM1 mixing': ('lepton', 'P', 'lepton at rho, nu at i -> TM1 (post hoc), sum rule for delta_CP', ['tau_lep=rho', 'tau_nu=i'], ['sin2theta12', 'delta_CP']),
 'E14 relic neutrinos': ('late', 'C', 'f_nu, P(k) suppression, 336/cm3', ['Sum m_nu'], ['f_nu', 'S8']),
 'E16 quark ladder': ('quark', 'C', 'eps_m = 0.0251 e^(i50)/(m+1/16)', ['SUGRA class m', 'tau_q'], ['quark hierarchies', 'eps_m']),
 'E17 CKM': ('quark', 'C', 'V = U_uL^+ U_dL from rungs 1 and ~8', ['eps_m', 'couplings kappa'], ['CKM', 'J']),
 'E18 strong CP': ('quark', 'P', 'anomaly-free weights -> theta-bar = 0', ['modular weights'], ['theta-bar']),
 'E19 tau_q cosmology': ('quark', 'C', 'D = T_R phi0^2/(6 T_dec); dN* = -ln(D)/3', ['m_tauq', 'T_R', 'phi0'], ['dilution']),
 'E20 proton': ('nuclear', 'C', 'dm_p = sigma_piN dm/m + sigma_s dms/ms', ['quark hierarchies'], ['m_p']),
 'E21 atoms & molecules': ('chemistry', 'C', 'Ry = mu alpha^2/2, a0 = 1/(m_e alpha), vib ~ mu^-1/2', ['m_e', 'm_p', 'alpha'], ['Rydberg', 'bond lengths', 'spectra']),
 'E6 gravitino->wino': ('dark', 'D', 'thermal gravitinos at T_R decay to winos', ['T_R', 'm_wino'], ['wino abundance']),
 'E7 gamma line': ('dark', 'C', 'f_max = sqrt(limit/(sigma v R J/J_b))', ['m_wino', 'wino abundance'], ['line flux']),
 'E8 colliders': ('dark', 'C', 'sigma(pp->chargino pairs), disappearing tracks', ['m_wino'], ['LHC reach']),
 'E9 asymmetric DM': ('dark', 'D', 'm_X from the same asymmetry: Omega_DM/Omega_b ~ 5.4', ['eta_B', 'dilution'], ['m_X=12.8 GeV']),
 'E10 dark photon': ('dark', 'D', 'A\' clears X antiparticles; window 0.3-5 GeV', ['m_X=12.8 GeV'], ['dark photon window']),
 'E11 BBN': ('late', 'C', 'Y_p, D/H from omega_b, Delta N_eff', ['eta_B', 'Delta N_eff'], ['Y_p', 'D/H', 'Li7']),
 'E22 reverse thread': ('late', 'C', 'V = V_L(1 - A e^(-beta phi)), beta from D', ['A', 'D', 'V_L'], ['w0', 'wa', 'dphi']),
 'E23 coupling & negative space': ('late', 'C', '(1+z_dag)^3 = Om_phi/[Om_c(e^{|b|dphi}-1)]', ['b', 'dphi'], ['z_dag', 'DM mass loss', 'S8']),
 'E24 alpha drift': ('late', 'C', 'dln(alpha) = zeta dphi, zeta_1loop = 5.7e-3', ['dphi', 'thread identity'], ['alpha drift', 'alpha']),
 'E26 thread endpoint': ('late', 'D', 'thread comes to rest at i', ['tau_thread'], ['tau_nu=i']),
 'E28 brane split': ('dark', 'P', 'visible on D3, dark on unfluxed D7: Delta N_eff ~ 0', ['g_s'], ['Delta N_eff', 'thread identity']),
}
SECTOR_ORDER = ['early', 'matter', 'lepton', 'quark', 'nuclear', 'chemistry', 'dark', 'late']


def graph():
    q2e = collections.defaultdict(set)
    for e, (_, _, _, ins, outs) in EQ.items():
        for q in ins + outs: q2e[q].add(e)
    return q2e


def shared():
    """Quantities used by equations in two or more sectors (the cross-sector connections)."""
    q2e = graph(); out = []
    for q, es in q2e.items():
        secs = sorted({EQ[e][0] for e in es})
        if len(secs) >= 2: out.append((q, secs, sorted(es)))
    return sorted(out, key=lambda t: -len(t[1]))


def path(a, b):
    """Shortest chain of shared quantities from equation/quantity a to b (BFS on the bipartite graph)."""
    q2e = graph(); adj = collections.defaultdict(set)
    for q, es in q2e.items():
        for e in es: adj[q].add(e); adj[e].add(q)
    pick = lambda x: [n for n in adj if n.lower() == x.lower()] or [n for n in adj if x.lower() in n.lower()]
    start = pick(a); goal = set(pick(b))
    if not start or not goal: return None
    prev = {s: None for s in start}; dq = collections.deque(start)
    while dq:
        n = dq.popleft()
        if n in goal:
            p = [];
            while n is not None: p.append(n); n = prev[n]
            return p[::-1]
        for m in adj[n]:
            if m not in prev: prev[m] = n; dq.append(m)
    return None


def sector_matrix():
    """For every pair of sectors, the shortest equation path between them and its weakest link status."""
    rows = []; rank = {'C': 3, 'D': 2, 'P': 1, 'O': 0}
    for s1, s2 in itertools.combinations(SECTOR_ORDER, 2):
        best = None
        for e1 in [e for e in EQ if EQ[e][0] == s1]:
            for e2 in [e for e in EQ if EQ[e][0] == s2]:
                p = path(e1, e2)
                if p and (best is None or len(p) < len(best)): best = p
        if best:
            eqs = [n for n in best if n in EQ]; weak = min(eqs, key=lambda e: rank[EQ[e][1]])
            rows.append(dict(a=s1, b=s2, steps=len(eqs) - 1, path=' -> '.join(best), weakest=f'{weak} [{EQ[weak][1]}]'))
        else:
            rows.append(dict(a=s1, b=s2, steps=None, path='NO CONNECTION', weakest=''))
    return rows


def weave_paths(a):
    """Tool: {"from": "...", "to": "..."} -> shortest path; {} -> shared quantities + sector matrix."""
    if a.get('from') and a.get('to'):
        p = path(a['from'], a['to']); return dict(path=p, label='structure (from the notes)')
    return dict(shared=[dict(q=q, sectors=s, equations=e) for q, s, e in shared()], matrix=sector_matrix(), label='structure (from the notes)')


if __name__ == '__main__':
    S = shared(); M = sector_matrix()
    print(f'{len(EQ)} equations, {len(graph())} quantities, {len(S)} cross-sector connections')
    for q, s, e in S: print(f'  {q:22s} {"/".join(s):28s} {"; ".join(e)}')
    none = [r for r in M if r['steps'] is None]
    print(f'{len(M)} sector pairs; unconnected: {[(r["a"], r["b"]) for r in none]}')
    for r in M: print(f"  {r['a']:9s}-{r['b']:9s} {r['steps']}  weakest {r['weakest']}")
