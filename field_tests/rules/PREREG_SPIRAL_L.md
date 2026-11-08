# Pre-registration S8-L: the Spiral with a light angle (weak-lensing option 4)

**Locked:** 8 Nov 2026, time in `PREREG_SPIRAL_L.md.sha256` (UTC), by Claude at Danny's request ("Start them", answering
whether to lock as drafted). AI-assisted. No S8-L fit exists at lock.

**Not blind on lensing, stated plainly.** We know the Spiral's lensing problem (S8-WL Parts 1 and 2), and the engine check
(`cmb-fit/axiclass/ula/ula_check_ax_spa_spiraltwist_nlfix.json`, no data) shows that a light share lowers S8: by −0.003
at log10 a_c = −5 and −0.035 at −4.5 (Pantheon+ Spiral point). No fit to any data has been run with this model.

## Question
If the BI angle's share of dark matter is an ultralight field (as an axion naturally is), does it fix the Spiral's
weak-lensing problem without losing its win over ΛCDM? Lensing is **not** in the fit: it is a prediction checked after.

## Model (fixed)
- The SF Spiral exactly (`PREREGISTRATION_SPIRAL_FIT.md`: κ, β_eff, same priors, data, engine settings, best of 4), with
  one change: the angle share **f = β_eff/0.816** of the dark matter (tied, not free) is an ultralight field, uncoupled:
  AxiCLASS's pheno_axion fluid, n = 1 (w → 0 after onset, sound speed c_s² = k²/(k² + 4a²m²)), frozen before onset,
  Θ_i = 0.1. The rest, (1 − f), is the coupled dark matter as in SF.
- **One new free parameter:** the onset scale factor, log10 a_c ∈ [−6, −3.5] (mass ≈ 10⁻²³ to 10⁻²⁷ eV; the heavy end
  behaves like ordinary dark matter). The mass in eV is reported.
- Engine: `cmb-fit/axiclass/ula/` (build_ula.sh = AxiCLASS_coupled_nlfix + patch_ula.py, two edits that change no
  physics equation: HALOFIT takes dark-energy w from the scalar field; omega_fld is accepted for the fluid density).
  Fitter: `spiral_l_fit.py` (wraps the SF fitter). Runs `spiralL`, `spiralL_dovekie`, `spiralL_union3` (PC).

## Gate (before any fit)
G-L: with the light share forced to 10⁻⁷, the full fitter on the new build reproduces each stored SF χ² within 0.1
(`python spiral_l_fit.py gate_pc` → `results/spiral_l_gate_pc.json`). Cloud code check already done: σ8 equal to
2×10⁻⁸. If G-L fails: no fits, no verdict.

## Verdicts (per SN set; same data as SF)
- **Against ΛCDM:** χ²(S8-L) − χ²(ΛCDM halofit): BEATS if ≤ −4 on at least 2 of 3; TIE if none ≤ −4 and none ≥ +2;
  otherwise MIXED.
- **Lensing (the point of the test):** DES Y6 S8 penalty vs ΛCDM at the best fit, as S8-WL Part 1 (P ≤ 2 passes).
  **LENSING FIXED** if P ≤ 2 on at least 2 of 3 **and** S8-L still BEATS ΛCDM; **TRADE-OFF** if P ≤ 2 on 2 of 3 but
  not BEATS; **NOT FIXED** otherwise.
- **Reported, not verdicts:** χ²(S8-L) − χ²(SF) with ΔAIC (+1 parameter); mass in eV; S8; the full DES Y3 Δ_WL
  (S8-WL Part 2 pipeline) at the best fits.
- **Failures:** a failed or non-finite fit is NO VERDICT for that set; any settings change is logged first.

## Choices made at lock
1. Light share tied to the angle: f = β_eff/0.816 (no extra fraction parameter).
2. Mass range: log10 a_c ∈ [−6, −3.5].
