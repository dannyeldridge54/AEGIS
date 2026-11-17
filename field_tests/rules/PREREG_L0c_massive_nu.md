# PREREG L0c — massive neutrinos in Janus-LT's H(z) vs CAMB (follows D1006/D1012)
Locked 2026-11-17 before any L0c number.
Source (fetched, Komatsu et al. 2011, WMAP7, arXiv:1001.4538 Sec. 3.3): ρ_ν(a) = 0.2271 N_eff ρ_γ(a) f(m_ν a/T_ν0) (Eq. 24),
f(y) = (120/(7π⁴)) ∫₀^∞ x²√(x² + y²)/(e^x + 1) dx (Eq. 25, used exactly by quadrature, NOT the Eq. 26 fit),
T_ν0 = (4/11)^{1/3} T_CMB. Implementation: CAMB's default single massive eigenstate (num_massive_neutrinos = 1,
mass Σm_ν) carrying N_eff/3 of the neutrino density, the rest massless: ρ_ν = 0.2271 ρ_γ [ (2N_eff/3) + (N_eff/3) f(Σm_ν a/kT_ν0) ].
(The N_eff/3 share for the massive state is my reading of CAMB's degeneracy convention; the test checks it.)
Ω_ν today enters the closure Ω_DE = 1 − Ω_m − Ω_γ − Ω_ν(a=1).
Test: same 50 seeded cosmologies (L0a), each at Σm_ν ∈ {0.06, 0.15, 0.30} eV (150 cases), CAMB 2.0.5 mnu=Σm_ν,
num_massive_neutrinos = 1, nnu = 3.044. T1: max |ΔH/H| and |ΔD_M/D_M| at z ∈ {0.1, 0.3, 0.51, 0.71, 0.93, 1.32, 2.33, 1100}
≤ 1e-4 → VALIDATED; ≤ 1e-3 PARTIAL; else NOT VALIDATED (L0a's scale). T2 (report): r_d with CAMB's zdrag (route 2), and
with our own recombination (L0b2 route 1).
