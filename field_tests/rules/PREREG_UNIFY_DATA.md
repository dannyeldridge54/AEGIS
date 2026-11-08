# PRE-REGISTRATION UB-2: the unified BI axion–dilaton against data

Locked 7 Nov 2026 with AI assistance, with Danny's choices ("Do the best one; if it fails make a note of the other
three"). **No UB-2 data fit has been run.** Replaces `DRAFT_PREREG_UNIFY_DATA.md` (kept).

## What is tested
One BI axion–dilaton (fixed λ = −2√(2/3), F = F_P/|φ|, F_P = 1.559, n = 3, **no cosmological constant**) doing both
the early and the late job, against real data.
- **Variant B only** (exponential dilaton, slope κ free): it passed UB-1 (D1). Variant A (derived, b = 0) failed UB-1;
  variant C (derived, W = W0 e^{bΦ}) failed UB-1b (closest miss 0.038: peak at z = 1,930, Ω_m = 0.330). Neither is fitted.
- Free beyond the standard six (A is fixed by flatness, replacing Λ): ln L, θ_i, |φ|_i, κ — **4 extra parameters**
  (w0–wa has 2; the Locked Twist + Spiral pieces together have more).
- Prior box: the UB-1 box (ln L ∈ [0, 40], θ_i ∈ [0.1, 3.0], |φ|_i ∈ [1.1, 60], κ ∈ [−3, 3]); H0 ∈ [55, 85] sampled
  directly; standard parameters as in the stored `lcdmP` fits. Starting points: the UB-1 D1 passing point (no data used).

## Engine (validated before this lock)
CAMB 2.0.5 + the two-field module `cmb-fit/ub2_camb/DarkEnergyUBField.f90` (both fields' perturbations) + Cobaya
3.6.2, driver `cmb-fit/ub2_fit.py`, background equations `theory/unify_hyperbolic_bg_ub1b.py` (= UB-1 D1).
Gates (`results/ub2_gates.json`): G1 Δχ² 0.000 vs CAMB EarlyQuintessence at the Locked Twist best fit; G2 Δχ² 0.000 vs
stored ΛCDM; G3 H(z) to 1e-6. SHA-256: ub2_fit.py `b0bbe6412b367521ef6bfa4de78217b61d23ef5420e87aa2f90bd51a0b64d968`; DarkEnergyUBField.f90 `c6b3d5a57490a9d38b306d99567dd764eacd276d79359330c171494d2939afe0`;
unify_hyperbolic_bg_ub1b.py `bea8c6b8fac66bbb1389cb5ea2909ff0dfb58d82c28cc07c938354afc9e7a974`.

## Data (option a)
Planck 2018 (low-ℓ TT/EE, plik-lite TTTEEE, lensing) + DESI DR2 BAO + one supernova set: Pantheon+, DES-Dovekie,
Union3. Runs: `ub2B`, `ub2B_dovekie`, `ub2B_union3`, bobyqa best of 4. References on the same data and engine:
`lcdmP*` and `edelockP*` (stored), `w0waP*` (3 new CAMB fits, same settings).

## Verdicts (per supernova set; SF thresholds)
- **vs ΛCDM:** BEATS if Δχ² ≤ −4 on at least 2 of 3; TIE if none ≤ −4 and none ≥ +2; otherwise MIXED.
- **vs w0–wa:** BEATS if Δχ² ≤ −2 on at least 2 of 3; COMPETITIVE if ≤ +2 on at least 2 of 3; else NOT COMPETITIVE.
  Reported with parameter counts and ΔAIC.
- **Unification:** UNIFIES if UB-2's Δχ² vs ΛCDM is within +2 of the better stored piece's (Locked Twist `edelockP*`,
  same engine; Spiral SF, AxiCLASS, vs its own ΛCDM) on at least 2 of 3 sets; otherwise DOES NOT UNIFY.
- **Reported, not verdicts:** S8 (DES Y6 penalty as S8-WL Part 1), f_peak, z_peak, w0, |φ| today, κ.
- **Failures:** a failed or non-finite fit is NO VERDICT for that set; any setting change is logged first.

## Declared follow-ups if UB-2 fails (Danny: "make a note of the other three"); each needs its own locked rule
1. **Data (b):** add ACT DR6 + SPT-3G (combined CMB), with new CAMB ΛCDM / w0–wa references on that data.
2. **Engine:** none needed (the two-field module passed every gate); a failure is not blamed on the engine.
3. **Thresholds:** no change after seeing results; a stricter or looser threshold would be a new test, not a re-score.
4. **Variants:** C (derived potential, b free) only if a new background test passes first; A stays failed.
