# PREREG A3e — NS radius-mismatch diagnostic (Djl D; follows D1086) — locked 2026-11-17
Hypothesis, from reading the code before running: compact.tov hard-codes atol_P = P_c·1e-16. For SLy at log ρ_c = 15.0, P_c ~ 1e34–1e35 Pa, which gives atol_P ~ 1e18–1e19 Pa. That is comparable to the surface pressure p_surf(ρ = 1e4) = 1.33e18 Pa (D1086), so compact.tov's P is uncontrolled near the surface and its event radius is imprecise. ns.tov_tidal uses atol_P = P_c·1e-30, effectively relative-only. This also explains why log ρ_c = 14.8 (lower P_c) agreed better.
Diagnostic (no pass/fail on the module; a hypothesis test):
- Re-run compact.tov's exact RHS with solve_ivp and atol_P = P_c·1e-30 (all else identical), for SLy log ρ_c = 14.8, 15.0, 15.2, at the common surface p_surf = P(1e4 g/cm³).
- Print: atol_P/p_surf; event R, P and ρ at the event, for ns, compact (as shipped) and compact (tight atol).
HYPOTHESIS CONFIRMED iff the tight-atol |R/R_ns − 1| ≤ 1e-8 at all three, while the shipped version stays ≥ 1e-6 at 15.0 and 15.2.
If confirmed, a fix to compact.tov's default atol goes through a DEVIATIONS file plus a re-lock of N4′ (A3f). It is not done in this run.
Script theory/janus_astro/a3e_diag.py (written after this lock).
