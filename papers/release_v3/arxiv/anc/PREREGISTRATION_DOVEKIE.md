# Pre-registration: A3 with DES-Dovekie supernovae (the bracket, ROUTE.md B1)

**Written:** 2026-11-01 09:56:48 CT. The time is from the clock, inserted by the command that hashes and commits this file. No
Dovekie fit of any model had been run.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards. Post-hoc in spirit: the Pantheon+ and
DES Y5 A3 results are known. So, like PREREGISTRATION_ROBUSTNESS.md, this cannot change the official A3 verdict
(MILD). It decides whether the DES Y5 "SURVIVES" is robust.

## Why

| Supernova set | A3 result |
|---|---|
| Pantheon+ | D = −3.65, MILD |
| DES Y5 | D = −4.70, SURVIVES |

The original DES Y5 sample has a reported calibration offset of about 0.04 mag between low and high redshift
(Efstathiou, arXiv:2408.07175). DES corrected it in the **DES-Dovekie** sample (arXiv:2511.07517).

## Runs

The same as A3 (AxiCLASS, same data, priors and settings, best of 2), with Pantheon+ replaced by `sn.desdovekie`:
`ax_spa_lcdm_dovekie`, `ax_spa_w0wa_dovekie` and `ax_spa_edelock_w0wa_dovekie`.

## Rules

**The A3 bands on D_dov = χ²(edelock_w0wa_dovekie) − χ²(w0wa_dovekie):**

| Verdict | Rule |
|---|---|
| SURVIVES | D_dov < −4 and D_dov + 4 < 0 |
| NOT NEEDED | D_dov ≥ −1 |
| MILD | in between |

**Reading:**
- **SURVIVES with Dovekie:** the early hint holds with the corrected supernovae as well as with DES Y5. It is
  supernova-dependent only against Pantheon+.
- **MILD or NOT NEEDED with Dovekie:** the DES Y5 "SURVIVES" is attributed to the uncorrected sample. **A3 is MILD with
  every current corrected set.**

**Also reported:**
- the late gain χ²(w0wa_dovekie) − χ²(lcdm_dovekie), against Pantheon+ −10.95 and DES Y5 −20.67;
- DESI DR2 with Dovekie as a reference, if a published value is found;
- H₀, f_EDE, w0 and wa for the early + late fit.

## Expectation, written in advance

- **Dovekie lands between Pantheon+ and DES Y5:** a late gain of roughly −12 to −17.
- **D_dov is most likely in the MILD band, near the −4 line.** The corrected sample removes part of what inflated DES
  Y5's late signal.
