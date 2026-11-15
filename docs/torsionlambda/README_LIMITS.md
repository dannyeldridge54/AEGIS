## What TorsionΛ can and cannot be used for (audit of v0.2.0, 15 Nov 2026)

TorsionΛ is a **pre-simulation consistency checker and teaching tool**. It is not an observationally validated
cosmology. An audit (AEGIS note D715, pre-registered; script and numbers in the AEGIS repository) found:

- **β is degenerate with Ω_m.** In the background, E²(z) = Ω_r(1+z)⁴ + Ω_m(1+β)(1+z)³ + λ, so β only rescales the
  matter density. Distances, BAO and the CMB shift parameter cannot tell (β, Ω_m) from (0, Ω_m(1+β)).
- **Normalisation.** With λ held fixed, E(0) ≠ 1 when β ≠ 0 (E(0) = 1.030 at β = 0.192). Set λ = 1 − Ω_r − Ω_m(1+β).
- **Shift parameter.** `cmb-observables.ts` uses √Ω_m with the bare Ω_m; it should use Ω_m(1+β). At β = 0.192 this changes R by about 26σ.
- **The H₀ = 72.95, β = 0.192 parameterisation is excluded** by the Planck 2018 compressed priors: R = 1.780 (+6.6σ),
  ℓ_A = 294.7 (−75σ). A ΛCDM-like background cannot raise H₀ to 73 and keep the CMB acoustic scale; TorsionΛ as coded does not evade that.
- **Validated:** at β = 0 the toolkit reproduces ΛCDM (R = 1.7497, ℓ_A = 301.45 against Planck's 1.7502 and 301.47).

Use it for: exploring how background changes propagate to distances, growth and CMB compressed observables;
screening parameter ranges before running Boltzmann codes. Do not use it to claim evidence for torsion or a
resolution of the Hubble tension.
