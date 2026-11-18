# PREREG C10 — 3-parameter Milky Way refit to Eilers+2019: disc-amplitude factor f_d plus NFW (ρ_s, r_s) with r_s bounded to 10–25 kpc — locked 2026-11-18, before code or run
Follow-up to C9 (D1210), where the halo-only refit needed r_s ≈ 3 kpc.
- Data and errors as C9: 32 points with R ≤ 20.78 kpc, statistical σ. A 2%-floor variant is reported.
- Model: v_c² = f_d·v²(McMillan17 DiskSCF component [0]: stellar discs + gas) + v²(SCF bulge [2], fixed) + v²_NFW(ρ_s, r_s).
- Bounds: f_d ∈ [0.5, 1.5]; r_s ∈ [10, 25] kpc (typical Milky Way halo range, labelled prior); ρ_s free (positive).
- scipy least_squares; start at f_d = 1 and the McMillan17 NFW values.
Scored:
- Q1: χ²/dof < 2 (statistical errors).
- Q2: dv_c/dR(8.178) < 0.
- Q3: no parameter sits on a bound (|p − bound| > 1% of the range). Otherwise the fit is "prior-limited", reported as such.
Reported: f_d; ρ_s; r_s; v_c, Ω and κ at 8.178 with Horta+2026 pulls; ρ_DM☉.
If Q1–Q3 all pass, it becomes a candidate Mapper potential. Adoption would be a separate locked step; there is no code change here.
