# Late Twist null mirror: a +1.35 χ² offset in the field's ΛCDM limit

**When:** 1 November 2026, run beside PREREGISTRATION_EDGE_SCAN.md (locked 12:34:01).

**Code and data:** `axiclass/null_mirror.py`, `results/null_mirror_latetwist.json`.

**Method:** χ² of the Late Twist with every cosmological and calibration parameter fixed at the AxiCLASS ΛCDM (halofit)
best fit (χ² 2402.26), for fields from edge-like to deeply frozen. No fitting. In the frozen limit the field is
physically a cosmological constant, so a correct code should give χ² − χ²_ΛCDM → 0.

| F (M_Pl) | m (H₀) | m²F² | χ² − χ²_ΛCDM |
|---|---|---|---|
| 3.16 | 0.5 | 2.50 | **+0.39** |
| 10 | 0.15 | 2.25 | +1.25 |
| 30 | 0.05 | 2.25 | +1.49 |
| 100 | 0.015 | 2.25 | +1.35 |

## Finding

- **In the frozen limit the residual levels off at about +1.35 ± 0.15, not 0.** This is a numerical offset between the
  Late Twist code path (a scalar field closing the energy budget, Ω_Λ = 0) and the ΛCDM path (a true Λ).
- **A likely cause, not yet confirmed:** AxiCLASS splits the scalar field's energy into "matter" and "radiation" parts
  (ρ_m += ρ_scf − 3p_scf, ρ_r += 3p_scf), which for a frozen field (p = −ρ) gives odd bookkeeping that can enter the
  halofit non-linear step. It could also come from the shooting precision.
- **The edge-like point (+0.39) is below the frozen limit:** a slight thaw improves the fit by about 1, relative to
  the code's own Λ limit.

## Consequences (no rule changed)

- **L1 (Late Twist vs ΛCDM):**
  - As written, it compares with the ΛCDM halofit run, so the grid best of +1.15 is **FAIL**.
  - Corrected for the offset, +1.15 − 1.35 ≈ **−0.2**: a **tie** with ΛCDM (that would be INCONCLUSIVE).
  - Both readings are reported; the official verdict is the one as written.
- **L2 (vs w0–wa)** is also shifted by about +1.35 in the same direction. It is WORSE either way.
- **Coupled Twist:** C2 (coupled vs Late Twist) shares the code path, so the offset cancels. C1 and C3 (against
  ΛCDM and w0–wa) carry it, and the same note applies.
- **The DES Y5 runs** carry the same offset. The edge scan and grid are compared on equal footing, and only
  comparisons with Λ-based references need the note.

## Diagnosis (13:06, 1 November 2026): the cause is halofit

**Code and data:** `axiclass/null_mirror_nl.py`, `results/null_mirror_nl.json`. The same fixed ΛCDM parameters are
evaluated with the non-linear correction on and off, for ΛCDM and for the Late Twist. No fit.

| Point | χ² − χ²_ΛCDM, halofit on | χ² − χ²_ΛCDM, non-linear off |
|---|---|---|
| Frozen (F 100, m 0.015) | +1.354 | **+0.029** |
| Edge-like (F 3.16, m 0.5) | +0.392 | **−0.905** |

- **With the non-linear step off, the frozen limit returns to ΛCDM (+0.03).** The offset is entirely in halofit.
- **Mechanism, read in the source:**
  - `background.c` lines 505–506 and 543–544 add the field to "matter" as ρ − 3p and to "radiation" as 3p.
  - For a frozen field (p = −ρ), that puts **+4 Ω_scf into Ω_m(z)** and −3 Ω_scf into Ω_r(z).
  - `external/Halofit/halofit.c` lines 107–108 and 208–209 read exactly these Ω_m and Ω_r. At late times halofit
    therefore sees roughly Ω_m ≈ 3 and Ω_Λ ≈ −0.7, instead of 0.31 and 0.69.
  - This distorts the non-linear lensing correction, which enters the CMB lensing likelihoods.
  - The split was written for early dark energy, where the field is small at late times, so it rarely matters there.
- **The thawing point is genuinely better than Λ** by about 0.9 in the linear comparison. With the correct
  bookkeeping, a slight thaw helps.
- **Side effect:** CLASS's derived Ω_m (`Omega0_m`, also used in its printed S8) is inflated the same way for
  every Late Twist and Coupled Twist run. Use the true Ω_m from `coupled/coupled_weff.py` (Ω_b + Ω_cdm + Ω_ν), never
  CLASS's derived Ω_m, for these models.

**Status of the verdicts:** unchanged. L1 is still FAIL as written. The offset-corrected reading (≈ −0.2, a tie) now
has a confirmed cause, not only a measured size.

**A fix** (a halofit Ω_m without the scalar field) would be a code change. It must be logged as a deviation before any
rerun, and is the user's decision.
