# Pre-registration: the Coupled Twist (Late Twist + dark-matter coupling)

**Written:** 2026-11-01 08:10 CT (time from the clock).
- The Late Twist rerun (`ax_spa_latetwist`) was running, and its result file did not exist.
- No coupled-model code exists yet, so no coupled fit has been run.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards. Deviations go in
PREREGISTRATION_SPT3G_DEVIATIONS.md.

## What is already known (disclosed)

- **The stalled first Late Twist run**, and the corner probe, which showed χ² ≈ ΛCDM + 0.4 near F = 0.54–3.2 M_Pl.
- **The literature:** coupled quintessence and coupled axion dark sectors can produce DESI's apparent phantom crossing.
  Khoury, Lin & Trodden arXiv:2607.16191 report Δχ² −14.48 on CMB + DESI DR2 + DES-Dovekie; see also
  arXiv:2604.08449, 2606.21826 and 2608.05032. This test is **not a new mechanism**. It checks whether *our* field,
  with its natural potential, does it on our data.
- **The coupling is not torsion-specific.** The torsion-native axial coupling vanishes for conserved charge
  (UFE_MATH_SHEET §6), so the coupling used here is the standard conformal one.
- **A correction to my own earlier wording:** I said the coupling's natural size could be "tied to the field's F".
  Nothing in the minimal theory derives such a tie, so none is tested. The only parameter-free torsion choice is test C5.

## Model

- **Field:** as the Late Twist. V = Λ⁴[1 − cos(φ/F)], it is all of the dark energy (no Λ), and the starting angle is
  fixed by closure.
- **Coupling:** cold dark matter only (baryons uncoupled, so no fifth force on ordinary matter). The mass is
  m_c(φ) = m_c,0 · exp(β φ / M_Pl), where M_Pl is the reduced Planck mass.
- **Background equations:**
  - ρ̇_c + 3Hρ_c = +(β/M_Pl) φ̇ ρ_c
  - φ̈ + 3Hφ̇ + V_φ = −(β/M_Pl) ρ_c

  These are the trace-coupling equations of UFE_MATH_SHEET §6, with T_c = −ρ_c.
- **Perturbations:** the standard linear coupled-quintessence equations (Amendola 2000), in the synchronous gauge
  that CLASS uses.

| Free | Prior |
|---|---|
| log10(F / M_Pl) | uniform in [−1.3, 0.5] (as the Late Twist) |
| log10(m / H₀) | uniform in [−0.5, 1.5] (as the Late Twist) |
| β | uniform in [−0.15, 0.15] |

That is **3 extra settings** over ΛCDM.

**Engine and settings:**
- AxiCLASS with the coupling added; halofit (as the Late Twist deviation).
- Same data and calibration priors as PREREGISTRATION_LATE_TWIST.md.
- Bobyqa, best of 4, cosmological references at the AxiCLASS ΛCDM halofit best fit, the minimiser guard for
  non-finite points, and β reference 0 ± 0.02.
- **Run name:** `ax_spa_coupledtwist`.

## Validation gates (all must pass before any coupled fit counts)

| Gate | Requirement |
|---|---|
| V1 | With β = 0, χ² equals the uncoupled Late Twist at the same parameter point to within 0.05 |
| V2 | Total energy is conserved: Σρ continuity holds to 10⁻⁴ over 0 < z < 10⁴ |
| V3 | The φ-matter-dominated era (field kinetic, V negligible) reaches Ω_φ = 2β²/3 (Amendola 2000) to within 5% for β = 0.1 |
| V4 | The sign check: β > 0 makes ρ_c fall faster than a⁻³ while φ̇ > 0, as the equations require |

If a gate fails, the code is fixed and **all gates rerun**. Each attempt is logged.

## Rules

**C1, against ΛCDM:**
- Δχ² = χ²(coupled) − χ²(ax_spa_lcdm_halofit); ΔAIC = Δχ² + 6.
- **PASS:** Δχ² < −6. **FAIL:** Δχ² ≥ 0. **INCONCLUSIVE:** in between.

**C2, is the coupling needed:**
- D_c = χ²(coupled) − χ²(ax_spa_latetwist, the approved rerun).
- **NEEDED:** D_c < −4. **NOT NEEDED:** D_c ≥ −1. **MILD:** in between.

**C3, against w0–wa:**
- ΔAIC = χ²(coupled) − χ²(ax_spa_w0wa_halofit) + 2.
- **PREFERRED:** ΔAIC < −2. **AS GOOD AS:** \|ΔAIC\| ≤ 2. **WORSE:** ΔAIC > 2.

**C4, apparent phantom crossing:**
- Effective dark energy as an observer assuming ordinary dark matter would infer it:
  ρ_DE,eff = ρ_φ + ρ_c − ρ_c,0 a⁻³, and w_eff from its continuity equation.
- **CROSSES** if w_eff < −1 anywhere in 0.3 < z < 2 at the best fit. **DOES NOT** otherwise.

**C5, the torsion-natural coupling (the one parameter-free torsion choice):**
- If dark matter couples through the canonical twist variable with the construction's own scale
  s = √(3/2) M_Pl, i.e. m_c ∝ exp(±φ/s), then **|β| = M_Pl/s = √(2/3) = 0.816**.
- One fit with |β| fixed at 0.816 (the sign giving the lower χ²), everything else free.
- **SURVIVES** if its Δχ² against ΛCDM is below 0. **EXCLUDED** otherwise.
- **Expectation, written in advance: EXCLUDED.** Coupled-quintessence bounds are typically \|β\| ≲ 0.05–0.1, and this
  value lies far outside the C1–C4 prior.

**Reported beside the verdicts:** best-fit β with an approximate interval from a 5-point β profile (β = −0.1, −0.05, 0,
0.05, 0.1), plus H₀, S8, σ8, w_eff(z) and the χ² split by data set.

## Order

1. Write the coupling into AxiCLASS on a separate copy; the original stays untouched.
2. Pass gates V1–V4, with the gate results committed.
3. Run C1–C4 (one fit), C5 (one fit) and the β profile (5 fits).
4. Apply the rules as written, run the scales checkpoint (SCALES_CHECKPOINT.md), and report.

**Cost:** writing and validating the code is likely a day of work; the fits take about 4–8 hours of CPU. Nothing here
starts until the current runs finish, and the author decides when.

## What would count

| Outcome | Meaning |
|---|---|
| C1 PASS + C2 NEEDED + C4 CROSSES | The twist field, coupled to dark matter, reproduces DESI's apparent phantom behaviour with a healthy field. Strong for the "one field, late role" picture, but not for torsion specifically |
| C2 NOT NEEDED | The plain Late Twist suffices, or nothing does |
| C5 SURVIVES | Against the expectation: the only parameter-free torsion coupling fits. That would be the first torsion-specific success, and would need independent checks |
