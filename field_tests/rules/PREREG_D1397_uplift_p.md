# PREREG D1397 — physical λ and the uplift exponent p through the full SERAPIS pipeline (D1375, D1396)

Locked 2026-11-18 before computing (Danny "Djl", P3 hunt).

Physical frame (D1375/D1377): ε = 90/(16π⁵T₂), T₂ = 16, s = 2 ⇒ L_ρ = s + εE(ρ,2), λ_phys = ε/L_ρ = 5.7225e-4 (computed in script).
Plateau family (D1396): P_p(x) = [(1 + x)^{1−p} − 1]/(1 + x), x = λ(E(U,2) − E(ρ,2)); P_0 = x/(1+x) (SERAPIS-E).
Implementation: pipeline.build is used unchanged except that its E-grid x is mapped to g(x) = P_p/(1 − P_p), so the pipeline's
g/(1+g) equals P_p exactly; the tilt factor then reads (1 + C·g/λ) instead of (1 + C·x/λ) — identical for p = 0, an O(p·x)
relative change of the tilt term for p > 0 (declared approximation). C is the D698 rescaling C_phys = 1.25e-6/λ_phys (a = 1/λ
absorbed into C). T_R = 8.94e8. Engine: pipeline.predict (exact spectra), one shared E-grid.
Runs: R0 = (λ = 1, C = 1.25e-6, p = 0) [control = serapis_point]; R1 = (λ_phys, C_phys, p = 0); R2 = (λ_phys, C_phys, p = 0.25);
R3 = (λ_phys, C_phys, p = 0.5).
Gate G0: R0 must give n_s = 0.97446 ± 2e-4, r = 4.81e-4 ± 2%; else nothing else is read.
Questions/rules: (a) R1 in band (n_s 0.969–0.975, r 4.55–5.7e-4)? "physical λ viable at the D698-rescaled C" if yes; if no,
record (D698's λ-degeneracy fails at physical λ because x* is not ≫ 1). (b) For p = 0.25, 0.5: in band? Largest tested p in band
is recorded as "p allowed up to ≥ that value (at fixed C)". No refits. No reruns to chase results; fixes only via
PREREG_D1397_DEVIATIONS.md written first.
