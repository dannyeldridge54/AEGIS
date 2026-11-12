"""Order-of-magnitude estimates for matter formation from the Twist (spontaneous leptogenesis through the axial-torsion
coupling). Natural units, GeV. Hypothesis-stage arithmetic, not a fit. AI-assisted.
Mechanism: L ⊃ c_A (∂_μ φ / M_P) J_A^μ (axial torsion sourced by the Barbero–Immirzi field couples to the fermion axial
current, Einstein–Cartan) -> chemical potential mu = c_A phidot / M_P. With lepton number violated in equilibrium
(Weinberg operator, set by neutrino masses), an asymmetry n_L/s ~ (15 / (4 pi^2 g*)) * g_L * mu/T freezes at T_F;
sphalerons convert B = (28/79)(B - L)."""
import math
MP = 2.435e18                 # reduced Planck mass, GeV
MPL = 1.221e19                # Planck mass, GeV
gs = 106.75
target = 8.7e-11              # n_B / s (Planck + BBN; eta_10 = 6.1)
H = lambda T: 1.66 * math.sqrt(gs) * T * T / MPL
s = lambda T: 2 * math.pi ** 2 / 45 * gs * T ** 3

def nB_over_s(mu_over_T, gL=3):          # 3 lepton doublet families, order-one coefficients absorbed
    return (28 / 79) * (15 / (4 * math.pi ** 2 * gs)) * gL * mu_over_T

need = target / nB_over_s(1.0)
print(f"required mu/T at freeze-out: {need:.2e}")

# K1: today's ultralight field, frozen by Hubble friction at T ~ 130 GeV (sphaleron decoupling)
m = 1e-26 * 1e-9              # eV -> GeV
F = (4 / math.pi) * math.sqrt(1.5) * MP
for T in (130.0,):
    phidot = m * m * F / (5 * H(T))     # radiation era slow roll, theta ~ 1
    print(f"K1 T={T:.0f} GeV: phidot={phidot:.1e} GeV^2, mu/T={phidot / MP / T:.1e}, shortfall factor ~1e{math.log10(need / (phidot / MP / T)):.0f}")

# K2: fast early roll; L-violation (Weinberg operator) in equilibrium above T_eq
v = 174.0; msum2 = 0.05e-9 ** 2 + 0.0086e-9 ** 2   # normal ordering, lightest ~0
T_eq = 1.66 * math.sqrt(gs) * 4 * math.pi ** 3 * v ** 4 / (3 * MPL * msum2)
print(f"K2: Weinberg-operator equilibrium above T_F ~ {T_eq:.1e} GeV")
phidot_need = need * T_eq * MP
rho_kin, rho_rad = phidot_need ** 2 / 2, math.pi ** 2 / 30 * gs * T_eq ** 4
print(f"K2: needed phidot ~ {phidot_need:.1e} GeV^2; kinetic/radiation at T_F = {rho_kin / rho_rad:.1e} (falls as T^2 afterwards)")
print(f"K2: same ratio at BBN (1 MeV): {rho_kin / rho_rad * (1e-3 / T_eq) ** 2:.1e}")
# K3: gravitino (N = 1 supergravity) needs T_RH >= T_F
print(f"K3: needs reheating T_RH >= {T_eq:.0e} GeV; usual gravitino bound T_RH <~ 1e9-1e10 GeV unless m_3/2 >~ 10-100 TeV")


# ---- Development 1 (12 Nov): the coupling is derived, not fitted ----
# Calcagni & Mercuri 2009 (arXiv:0903.4407, Eqs. 20-22) and Mercuri 2009 (arXiv:0902.2764, Eq. 11): with the Nieh-Yan
# term, integrating out torsion leaves a canonical BI field phi with  -sqrt(3 pi G) * d_mu(phi) * J_A^mu.
# In reduced Planck units sqrt(3 pi G) = sqrt(3/8) / M_P, so c_A = sqrt(3/8) = 0.612 (no free parameter).
cA = math.sqrt(3 / 8)
phidot_F = need * T_eq * MP / cA
print(f"D1: c_A = sqrt(3/8) = {cA:.3f}; needed phidot at T_F: {phidot_F:.1e} GeV^2")
# A freely rolling field (kination-like) slows as phidot ~ a^-3 ~ T^3. Field travel after T_F:
dphi = phidot_F * MPL / (1.66 * math.sqrt(gs) * T_eq ** 2)
F_twist = (4 / math.pi) * math.sqrt(1.5) * MP
print(f"D1: field travel after T_F: {dphi:.1e} GeV = {dphi / MP:.1e} M_P = {dphi / F_twist:.1e} rad of the Twist angle")
for TRH in (1e14, 1e15):
    print(f"D1: if rolling freely since T_RH = {TRH:.0e} GeV: travel ~ {dphi * TRH / T_eq / MP:.1e} M_P")
