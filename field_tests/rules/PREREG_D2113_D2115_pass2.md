# PREREG D2113–D2115: settle loop, pass 2. Fixes the D2112 open items. Locked before computing.

## D2113: P2-only rescan
- Same class and filters as D2111, but with the convention fixed to **P2** (settled by D2112 K4). Code: z2z6p_scan_p2.py, a copy of the D2111 scan with every P1 replaced by P2, writing to z2z6p_scanP2_*.json.
- **Control:** the Table 27 visible triple must be found.
- **Report:** raw, distinct-by-cycle and distinct-spectra counts. Does uniqueness (1 spectrum up to L↔R) survive?

## D2114: K7 scale tension with full one-loop thresholds
- **Setup:** one-loop MSSM couplings from M_Z (α_s(M_Z) = 0.1180), matched at M_s. Matching rules, stated as an ASSUMPTION: 4π/g² = Re f_tree + Re δf; α₃ = α₄; α₂ = α_b; α₁⁻¹ = (2/5)α₄⁻¹ + (3/5)α_c⁻¹.
- **Tree level:** T = R/(4g_s), with R = √(v₁v₂v₃)/(2π²√3)^{3/2}. M_s = M_Pl·g_s/√(4π v₁v₂v₃), using reduced M_Pl = 2.435e18 GeV; the non-reduced value is a variant.
- **Thresholds:** the asymptotic linear forms (paper: valid from v ≈ 1). Variant A uses the paper's asymptotes. Variant B is the same, but with the b, c v₃ slope −1/48π from our exact evaluation (D2112 K6).
- **(i) Isotropic L/R (v₁ = v₂):** α_b = α_c, so M_s is fixed by the data through α₁⁻¹ = 0.4α₃⁻¹ + 0.6α₂⁻¹. This leaves 3 equations in (v, v₃, g_s). PASS if there is a solution with all v_i ≥ 1 and 0 < g_s < 1.
- **(ii) General (v₁, v₂, v₃, g_s):** a 1-parameter family (scanned over v₃). Existence PASS on the same criteria. This is a FIT, not a prediction.
- **Control flag:** max|δ_x|/T > 0.3 means the one-loop terms are not small, so control is questionable.

## D2115: PS breaking route (logic check)
- The paper (around line 1452) says brane recombination or splitting needs deformation moduli, which are the adjoint multiplets.
- **Check:** do Tables 28/29 contain any adjoints (aa, cc sectors) for the stacks a and c? Are there any (4,1,2)-type Higgs fields? If there are no adjoints and no such Higgs, then **OBSTRUCTED perturbatively**. Any remaining routes are listed as OPEN (non-perturbative, or recombination with the hidden d, which has 4 adjoints).

No reruns to chase. Fixes go in DEVIATIONS.
