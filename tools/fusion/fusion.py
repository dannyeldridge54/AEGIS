"""Fusion engine (PREREG_FUSION1). Goal at the top: net electricity from D-T fusion. Sections are child engines on one bus.
Units: T in keV, <sigma v> in cm^3/s (Bosch-Hale) and m^3/s where noted, n in m^-3, energies in MeV or J as labelled."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from net import Bus, Engine, settle, tree

# ------------------------------------------------------------------ constants (CODATA 2018 / AME 2020 atomic masses in u)
U_MEV = 931.49410242; MEV_J = 1.602176634e-13; KEV_J = 1.602176634e-16; ALPHA_FS = 7.2973525693e-3; YEAR = 3.15576e7; NA = 6.02214076e23
M = dict(n=1.00866491595, H1=1.00782503223, D=2.01410177812, T=3.01604928132, He3=3.01602932197, He4=4.00260325413)
ME_U = 5.48579909065e-4          # electron mass in u (for nuclear masses)
def nuc(k, Z): return M[k] - Z * ME_U   # nuclear mass (electron binding neglected, < 30 eV)

# ------------------------------------------------------------------ S1 reactions
BH = {  # Bosch & Hale, Nucl. Fusion 32 (1992) 611: BG [keV^1/2], mrc2 [keV], C1..C7; valid 0.2-100 keV (D-He3 0.5-190 keV)
    'DT':   dict(BG=34.3827, mrc2=1124656.0, C=(1.17302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3, 1.35000e-2, -1.06750e-4, 1.36600e-5), src='listing (tokamak_neutron_source)'),
    'DDn':  dict(BG=31.3970, mrc2=937814.0, C=(5.43360e-12, 5.85778e-3, 7.68222e-3, 0.0, -2.96400e-6, 0.0, 0.0), src='listing (tokamak_neutron_source)'),
    'DDp':  dict(BG=31.3970, mrc2=937814.0, C=(5.65718e-12, 3.41267e-3, 1.99167e-3, 0.0, 1.05060e-5, 0.0, 0.0), src='listing (tokamak_neutron_source)'),
    'DHe3': dict(BG=68.7508, mrc2=1124572.0, C=(5.51036e-10, 6.41918e-3, -2.02896e-3, -1.91080e-5, 1.35776e-4, 0.0, 0.0), src='as recalled (flagged)'),
}
def sigmav(reaction, T_keV):
    """Bosch-Hale thermal reactivity <sigma v> in cm^3/s for a Maxwellian at ion temperature T (keV)."""
    p = BH[reaction]; C1, C2, C3, C4, C5, C6, C7 = p['C']; T = T_keV
    theta = T / (1 - T * (C2 + T * (C4 + T * C6)) / (1 + T * (C3 + T * (C5 + T * C7))))
    xi = (p['BG'] ** 2 / (4 * theta)) ** (1 / 3)
    return C1 * theta * math.sqrt(xi / (p['mrc2'] * T ** 3)) * math.exp(-3 * xi)

REACTIONS = {  # (reactants, products) with atomic masses (electrons balance)
    'DT': (('D', 'T'), ('He4', 'n')), 'DDn': (('D', 'D'), ('He3', 'n')), 'DDp': (('D', 'D'), ('T', 'H1')), 'DHe3': (('D', 'He3'), ('He4', 'H1'))}
def q_value(r):
    a, b = REACTIONS[r]; return (sum(M[x] for x in a) - sum(M[x] for x in b)) * U_MEV

def two_body_split(r, relativistic=True):
    """Kinetic energies of the two products for reactants at rest (the thermal energy is neglected). Returns (E_light, E_heavy) in MeV
    as (product 2, product 1) of the reaction tuple's products."""
    Z = dict(n=0, H1=1, D=1, T=1, He3=2, He4=2)
    (p1, p2) = REACTIONS[r][1]; m1, m2 = nuc(p1, Z[p1]) * U_MEV, nuc(p2, Z[p2]) * U_MEV; Q = q_value(r)
    if not relativistic: return Q * m1 / (m1 + m2), Q * m2 / (m1 + m2)
    W = m1 + m2 + Q; E2 = (W * W + m2 * m2 - m1 * m1) / (2 * W) - m2; return E2, Q - E2

# ------------------------------------------------------------------ S7 stars: the Gamow peak
K_B_KEV = 8.617333262e-8   # keV per K
def gamow(Z1, Z2, mu_u, T_K=None, kT_keV=None):
    """Gamow peak E0 = (b kT / 2)^(2/3), b = pi alpha Z1 Z2 sqrt(2 mu c^2); width Delta = 4 sqrt(E0 kT / 3). keV."""
    kT = kT_keV if kT_keV is not None else K_B_KEV * T_K
    b = math.pi * ALPHA_FS * Z1 * Z2 * math.sqrt(2 * mu_u * U_MEV * 1000.0)     # keV^1/2
    E0 = (b * kT / 2) ** (2 / 3); return dict(E0_keV=E0, width_keV=4 * math.sqrt(E0 * kT / 3), b_keV_half=b, kT_keV=kT)

# ------------------------------------------------------------------ engines
class Reactions(Engine):
    name = 'S1 reactions'
    def run(self, bus):
        for r in BH: bus.put(self.name, f'Q_{r}_MeV', q_value(r), 'LIVE', 'MeV')
        En, Ea = two_body_split('DT'); bus.put(self.name, 'E_n_DT_MeV', En, 'LIVE', 'MeV'); bus.put(self.name, 'E_alpha_DT_MeV', Ea, 'LIVE', 'MeV')
        for T in (1, 10, 20, 50, 100): bus.put(self.name, f'sv_DT_{T}keV', sigmav('DT', T), 'LIVE', 'cm^3/s')
        return dict(n_share=En / q_value('DT'))

class Stars(Engine):
    name = 'S7 stars'
    def run(self, bus):
        mu_pp = nuc('H1', 1) / 2; g = gamow(1, 1, mu_pp, T_K=15.7e6)
        mu_dt = nuc('D', 1) * nuc('T', 1) / (nuc('D', 1) + nuc('T', 1)); gd = gamow(1, 1, mu_dt, kT_keV=10.0)
        bus.put(self.name, 'gamow_pp_sun_E0_keV', g['E0_keV'], 'LIVE', 'keV'); bus.put(self.name, 'gamow_pp_sun_width_keV', g['width_keV'], 'LIVE', 'keV')
        bus.put(self.name, 'gamow_DT_10keV_E0_keV', gd['E0_keV'], 'LIVE', 'keV')
        return dict(pp=g, dt=gd)

class Fusion(Engine):
    name = 'FUSION (goal: net electricity from D-T)'

def build(sections=None):
    secs = sections or [Reactions(), Stars()]
    return Fusion(secs)

if __name__ == '__main__':
    root = build(); bus = Bus(); sw = settle(root, bus)
    print('\n'.join(tree(root))); print(f'settled in {sw} sweeps')
    for k, v in bus.v.items(): print(f'  {k:28s} {v:.6g} {bus.meta[k]["unit"]}' if isinstance(v, float) else f'  {k} {v}')
