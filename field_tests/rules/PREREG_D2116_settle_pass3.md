# PREREG D2116: settle loop, pass 3 (closing). Locked before computing.

**D2116a: D2114 dense check.** The D2114 solver grid skipped 300 < v₃ < 1e4. Re-solve the same equations, variants A/B and reduced/non-reduced M_Pl, on 120 log-spaced v₃ values in [10, 1e6], with multiple seeds. The criteria are **unchanged**:
- existence = v_i ≥ 1 and 0 < g_s < 1;
- control = max|δ|/T < 0.3;
- isotropic = a genuine root of the α₁ residual on a single continuous branch (|residual| < 0.05 after bisection on that branch).
Verdict: K7 resolved under perturbative control, yes or no.

**D2116b: K11 ΔN_eff estimate (ESTIMATE).** The 6 massless hidden SU(2)_d × SU(2)_e gauge bosons give g = 12. Use ΔN_eff = (4/7)·g·(10.75/g*s(T_dec))^{4/3}, with decoupling at M_s and g*s = 228.75 (MSSM) as a lower bound on g*s (more states only lower ΔN_eff). Compare with the Planck 2018 + BAO 95% bound N_eff = 2.99 ± 0.34, so ΔN_eff ≲ 0.3.

**D2116c: K-theory / FI check (literature).** grep p.tex for K-theory and FI/D-term statements about this model. Record as found, or as NOT VERIFIED.

**Closing rule:** after D2116, every K item must be PASS / FAIL / OBSTRUCTED / FLAG / ESTIMATE with evidence. Then write the paper. No reruns to change a verdict.
