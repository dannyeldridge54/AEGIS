# PREREG D2088: does m_h = 125.1 GeV allow the D2087 GM branch (m₃/₂ = M_S ≈ 124–156 TeV, μ = c·m₃/₂, c ≈ 1, tan β = 1.5–4)? Locked before computing.

**Formulas (textbook):**
- **Boundary at M_S (high-scale SUSY, 1407.4081 form):** λ(M_S) = ¼(g² + g′²)cos²2β + (3y_t⁴/8π²)(x_t² − x_t⁴/12), with x_t = X_t/M_S and X_t = A_t − μ cot β. Here A_t = 0 (the AMSB A-term is loop-suppressed), μ = c·M_S, so x_t = −c cot β. **Stated simplification:** the 1-loop threshold only, all scalars at M_S, and the light winos and gluino are ignored in the λ running.
- **Running:** SM one-loop RGEs for (g′, g, g₃, y_t, λ) between m_t and M_S (Machacek–Vaughn), with m_h² = 2λv², v = 246 GeV.
- **Boundary at m_t (Buttazzo et al. 1307.3536, MS-bar):** g′ = 0.3583, g = 0.6478, g₃ = 1.1666, y_t = 0.9369, λ(m_t) = 0.12604 for m_h = 125.1.
- **Theory error:** one-loop running and the 1-loop threshold are counted as ±1.5 GeV in m_h, i.e. ±0.0030 on λ(m_t), propagated to the tan β band.

**Control (must pass):** with these RGEs, λ crosses zero at μ ∈ [3e8, 3e11] GeV (the literature instability scale is ~1e10–1e11).

**Test:** for M_S ∈ {124, 145, 156} TeV (the D2087 points) and c ∈ {0.953, 1, 1.047}:
- find the tan β with λ_run(M_S) = λ_boundary(tan β), within the ±1.5 GeV band;
- compare it with the D2087 feasible tan β at each M_S: 124 → 1.5, 145 → 3, 156 → 4.

**Verdict:**
- **CONSISTENT** if the D2087 tan β lies inside the m_h-allowed band at ≥ 1 of the three points;
- else **TENSION**.

**Note:** tan β = 1 at the boundary (BIM Eq. 72) gives cos 2β = 0, so the tree-level λ is 0. That case is reported too.
