# PREREG D592: adiabatic suppression of dilaton oscillations through the end of SERAPIS inflation (toy), locked before computing

Background (units M_P = 1, V₀ = 1): the canonical inflaton φ, with v(φ) the two-term SERAPIS potential (ε = 1e-4, D588 functions), symmetric about τ = i (v(φ) = v(|φ|), since y → 1/y). Integrated in cosmic time together with H² = (½φ̇² + v)/3.

Dilaton toy: Ÿ + 3HẎ + m²(Y − d) = 0, with a Hubble-induced shift d(t) = c·v(φ(t))/m², c = 1. This is the standard Hubble-induced linear term ∝ V_inf.

Start: 3 e-folds before the end of inflation, with Y = d and Ẏ = ḋ (tracking). Run to 1.5 e-folds after the end (ε_H = 1).

Scan: m/H_end-of-inflation ∈ {10, 30, 100}.

Measure at the final time:
- the free-oscillation energy E_Y = ½(Ẏ − ḋ)² + ½m²(Y − d)²;
- f_Y = E_Y/ρ_φ;
- f_track = ½m²d²/ρ_φ (the forced part, which follows φ).
Report f_Y versus m/H and an empirical fit (exponential or power law).

Compare with the D591 requirement, f_Y ≲ 4e-11 after including the ~180× stiff-phase growth, i.e. f_Y(1.5 e-folds) ≲ 2e-13 (estimate).

Caveats fixed now: c = 1 is a toy normalisation, and the result scales as c². No tuning after seeing results; fixes go in PREREG_D592_DEVIATIONS.md, written first.
