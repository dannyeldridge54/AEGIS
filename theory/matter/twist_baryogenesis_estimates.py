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

# ---- Development 3 (12 Nov): the gravitino (K3) ----
# Thermal gravitino yield, Pradler & Steffen style fit as quoted in arXiv:0804.3745 (valid 1e5-1e12 GeV; extrapolated):
def Y32(TR):
    t = TR / 1e8; L = math.log(t)
    return 2.3e-14 * t * (1 + 0.015 * L - 0.0009 * L * L)      # transverse part; longitudinal part adds for light m_3/2
TR = T_eq
print(f"D3: gravitino yield at T_RH = {TR:.0e} GeV: Y ~ {Y32(TR):.1e} (lower bound; extrapolated past 1e12 GeV)")
# each decaying gravitino leaves one lightest superpartner (if R-parity holds): Omega h^2 ~ 2.7e8 (m/GeV) Y
mmax = 0.12 / (2.7e8 * Y32(TR))
print(f"D3: a stable lightest superpartner from those decays must be lighter than ~{mmax:.2f} GeV to not overfill dark matter")

# ---- Development 4 (12 Nov): where the early speed comes from ----
# Needed speed relative to the natural scale H*M_P at T_F, and back at reheating if the angle rolls freely since then
# (phidot ~ a^-3, H ~ a^-2 in radiation, so phidot/(H M_P) ~ 1/a ~ T).
HF = H(T_eq)
r_F = phidot_F / (HF * MP)
print(f"D4: H(T_F) = {HF:.1e} GeV; needed phidot/(H M_P) at T_F = {r_F:.1e} (kinetic share {r_F**2/6:.1e})")
for TRH in (1e14, 1e15):
    print(f"D4: same, at reheating T_RH = {TRH:.0e} GeV: phidot/(H M_P) = {r_F * TRH / T_eq:.2f}")
# Hyperbolic field space (lambda = -2 sqrt(2/3), fixed): the angle's momentum a^3 e^{lambda sigma/M_P} thetadot is
# conserved (shift symmetry), so a dilaton excursion d_sigma rescales the angle speed by e^{-lambda d_sigma}.
lam = -2 * math.sqrt(2 / 3)
for ds in (0.5, 1.0, 2.0):
    print(f"D4: dilaton excursion {ds} M_P after inflation changes the angle speed by x{math.exp(-lam * ds):.1f}")

# ---- Development 5 (12 Nov): the neutrino-mass link ----
# The lepton-number process (Weinberg operator) rate grows with sum m_i^2, so heavier neutrinos lower the freeze-out
# temperature T_F (and with it the gravitino pressure). dm21^2 = 7.4e-5, dm31^2 = 2.5e-3 eV^2.
def TF(masses_eV):
    s2 = sum((m * 1e-9) ** 2 for m in masses_eV)
    return 1.66 * math.sqrt(gs) * 4 * math.pi ** 3 * v ** 4 / (3 * MPL * s2)
cases = {"normal, lightest 0 (sum 0.059 eV)": [0, 0.0086, 0.050],
         "inverted, lightest 0 (sum 0.10 eV)": [0, 0.0492, 0.050],
         "degenerate, sum 0.15 eV": [0.05, 0.05, 0.05],
         "degenerate, sum 0.30 eV": [0.1, 0.1, 0.1]}
for k, m in cases.items():
    print(f"D5: {k}: T_F ~ {TF(m):.1e} GeV")
