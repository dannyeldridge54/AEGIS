# PREREG D2259 — UFE engine stages 2-4: exact numbers, symbolic re-derivation, contradiction finder (locked 25 Nov 2026)

**Object.** The local agents' final derivation audit, `bridge/REPORTS/UFE_final_copilot_2026-11-25.md` at AEGIS commit 1fa03d92, and their
handoff value E_rho(3/2, full lattice) = 8.89274510039729. This run checks the audit's algebra and numbers. It tests no theory against data.
**Script.** `tools/field_engine/ufe_stages.py`, written after this lock, run once. Output `field_tests/results/d2259_ufe_stages.json`.

## Stage 2 — exact numbers (code only, no models)
| ID | Check | Pass rule |
|---|---|---|
| N1 | E_{3/2}(rho), full lattice, Chowla-Selberg (`serapis_calc.shapes.E`) vs the agents' 8.89274510039729 | relative difference <= 1e-9 |
| N2 | The same value from a direct lattice sum inside radius R = 400 plus the continuum tail 2 pi y^(s-1) R^(2-2s)/(2s-2) | relative difference from N1's value <= 1e-3 |
| N3 | E_2(rho): Chowla-Selberg vs direct sum (R = 400, same tail) | relative difference <= 1e-5 |
| N4 | Normalisation: shapes.E(U,s) = 2 zeta(2s) x eisenstein.E_fourier(x,y,s) at rho and at 0.2+1.1i, s = 2 | relative difference <= 1e-8 |
| N5 | rho is a critical point: \|grad E_s(rho)\| / E_s(rho) for s = 2 and 3/2 (central differences, h = 1e-4) | <= 1e-6 |
| N6 | Laplace eigenvalue y^2 (E_xx + E_yy)/E at 0.2+1.1i: 2 for s = 2, 3/4 for s = 3/2 | absolute difference <= 1e-4 |
| N7 | Isotropy at rho: y^2 E_xx / E = 1 (s = 2) and 3/8 (s = 3/2); E_xy = 0 | <= 1e-4 |
| N8 | SERAPIS-E mass: 2 y^2 V_xx at rho for V = V0 z(1 + C z)/(1 + z), V0 = 1, C = 8e-7, equals 2 E_2(rho) | relative difference <= 1e-4 |
| N9 | YFORK2 mass in units of V_inf: (16/9) (y^2 E_xx/E)^2 at rho for s = 3/2 equals 1/4 | absolute difference <= 1e-4 |
A failed N-check is reported as FAIL with both numbers. No tolerance is changed afterwards.

## Stage 3 — symbolic re-derivation (sympy)
Each item REPRODUCES only if the difference between the audit's expression and the re-derived one simplifies to exactly 0. Otherwise it is
listed as DISCREPANCY with the residual. Items: S1 moving-extremum slope; S2 dust scaling rho_{c,N} = (-3 + b phi_N) rho_c; S3 loop-metric
entries K_UU, K_SS, K_US and the determinant, using y^2 (E_xx + E_yy) = 2E; S4 the determinant bound when \|grad E\| = 2E/y;
S5 the eta-kappa modulus block; S6 the reverse-thread modulus block; S7 the thread curvature b(b + beta) rho_c at the dust balance;
S8 the flux-bridge V_2 from W_2 and the mass e^K K^UU K^SS \|b\|^2 at a = 0; S9 the YFORK2 field equations from its Lagrangian;
S10 the radiation oscillator: conformal-time and cosmic-time forms equivalent under d/d eta = a d/dt; S11 the roots of
C(lambda) = lambda^4 (lambda+1)(3 lambda - 2)/3 equal the matter-era growth exponents; S12 the v3/v4 normalisation factor 9/4.

## Stage 4 — contradiction finder
Each sector and bridge declares the value it requires for named quantities. The finder groups by quantity and reports any group whose values
differ by more than 1e-6 relative. **Pass rule for the finder itself:** it must report, without being told, the three disagreements the audit
found by hand: (a) V_w/(V0 E_2(rho)) = 32 (loop candidate's 2:1 tuning) vs 8 (flux-bridge match); (b) the shape-function Laplace eigenvalue
2 (SERAPIS-E) vs 3/4 (Weave, YFORK2); (c) the Weave gauge coefficient: the source text "9 Re S" at rho gives 4.5, the source number is 7.79.
Any further disagreement it reports is listed as NEW and sent to the bridge; it is not a claim about physics.

## Not in scope
No scans, fits or data. No run on language models. Stage 7 (perturbation system) is not built here.
