# PREREG NA3 — node audit phase 3: reheat_rho (T_R at ρ) and its inputs, re-derived
Locked before computing. Sources: D689 (line "d²V/dφ² = 11.57 V0 ⇒ m_φ ≈ 2.2e13 GeV"), D725 (theory/modular/tr_2p1_d725.py, results tr_2p1_d725.txt).
## A. Inflaton mass at ρ (SERAPIS-E pipeline, n = 1, C = 1.15e-6)
d²v/dφ² at the ρ minimum in units of V0 (v = V/V0, V0 = plateau height), by finite differences on E_paper directly (not the spline). PASS if within 1% of 11.57.
m_φ = sqrt(11.57-equivalent · V0)/M_P with V0 from A_s = 2.1e-9 and r, n at N* = 50 (Janus core): V* = (3π²/2) A_s r M_P⁴, V0 = V*/v(φ*). PASS if within 5% of 2.2e13 GeV.
## B. Arithmetic reproduction of D725's T_R
Independent re-evaluation of Γ and T_R = (90/π²g*)^{1/4} √(Γ M_P) (g* = 106.75) from the couplings and masses printed in tr_2p1_d725.txt, same formulas (Γ_ii = g²m(1−4x²)^{3/2}/16π, Γ_ij = g²m√λ(1−(x_i+x_j)²)/8π). PASS if all 7 open rows reproduce within 1% (printed g has 3 digits).
## C. Kinetic normalisation consistency
D725 line 14 converts δ(Im τ) to the canonical inflaton with can = y√(2/3), i.e. K = −3 ln(2 Im τ). SERAPIS-E's pipeline uses n = 1 (φ = √(1/2) ln y ⇒ dy/dφ = y√2).
Test: the canonical factor used by D725 equals the one of the model whose N* it feeds (nstar_e, SERAPIS-E). CONSISTENT if equal. If not: report T_R rescaled with the model's factor (g × √3 ⇒ Γ × 3, T_R × √3, and m_φ as found in A), and the N* window from it with NA2's self-consistent code. FLAG reheat_rho and nstar_e (ripple) if |ΔN*| > 0.05.
No change to frozen predictions (post-hoc). No reruns to chase; fixes via PREREG_NA3_DEVIATIONS.md first. Results: field_tests/results/na3_reheat_rho.txt.
