# PREREG D723: is φ → N2N2 (D722) a dark-radiation kill for SERAPIS-E at ρ?
Locked 2026-11-16 before computing. Script: theory/modular/n2_darkrad_d723.py. Output: field_tests/results/n2_darkrad_d723.txt.
## Inputs (fixed now)
- Γ2-doublet-only model of D720–D722: M_N = diag(M1, 0) at ρ, T_R(N2) = 6.7e8–6.7e10 GeV (D722).
- Neutrino bound: N2 + a light ν form a Dirac state of mass y_D v (v = 174 GeV); require y_D v < 0.07 eV (Σm_ν bound in constraints.yaml region) → y_D,max.
- Thermalisation: Γ_th ≈ y_D² T/(8π) vs H = 1.66 √g* T²/M_P (g* = 106.75) at T = T_R; needs y_D,th.
- Competing SM channel: D601-scaled sfermion channel, T_R,SM ≈ 30–70 GeV (D720 estimate) → Br_SM ≈ (T_R,SM/T_R,N2)².
- If N2 does not thermalise: ρ_N2/ρ_SM ≈ 1/Br_SM at reheating; ΔN_eff = (4/7)(11/4)^{4/3}·(ρ_N2/ρ_ν,one)… computed as ΔN_eff ≈ (8/7)(11/4)^{4/3} ρ_N2/ρ_γ at BBN, with entropy-dilution factor (g*s(T_BBN)/g*s(T_R))^{4/3} for the SM bath.
- Limit: ΔN_eff < 0.3 (and constraints.yaml neff row).
## Decision rule (written before running)
- KILL (for the doublet-only model) if y_D,max < y_D,th AND ΔN_eff > 0.3.
- SAFE if N2 thermalises with y_D ≤ y_D,max, or ΔN_eff < 0.3.
- If KILL: state the minimal escape (N2 mass from extra structure) as reasoning, not computed.
- Fixes only via D723_DEVIATIONS.md.
