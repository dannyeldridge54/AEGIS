# PREREG A3f — NS module re-validation after the compact.tov tolerance fix (Djl D) — locked 2026-11-17
Follows DEVIATIONS_A3f (D1) and D1090.
- F1: N4′ — SLy, log ρ_c = 14.8 / 15.0 / 15.2, common surface ρ = 1e4 g/cm³: ns.tov_tidal vs compact.tov (shipped, fixed). M and R ≤ 1e-7.
- F2: P → 0 — ns.tov_tidal(rho_surf = 1e-3) vs compact.tov(p_surf = 0), same stars: M and R ≤ 1e-6. This is the original A3a–c N4 at a looser bound, because the surface is still physically ill-conditioned there.
- F3: re-run theory/janus_astro/a0_check.py and a0s_check.py unchanged. Every check that PASSed before (results in git history) must still PASS.
A3f VALIDATED iff F1, F2 and F3. Together with A3c's N1–N3 (PASS), the NS module is then VALIDATED.
Script theory/janus_astro/a3f_check.py for F1 and F2 (written after this lock).
