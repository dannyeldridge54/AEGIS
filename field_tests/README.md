# Field tests: everything left to complete the field

Set up 7 Nov 2026 (AI-assisted). Every test here has its pass/fail rule **locked before its data**; this folder only
runs and scores them. Nothing in it changes a rule, a prior or a run setting.

| Test | Question | Runs | Where |
|---|---|---|---|
| **TF-P** | Does the derived Nieh–Yan F = 1.559 M_Pl fit? | 3 (Union3 blind) | PC, AxiCLASS |
| **SF** | Does the effective Spiral Twist beat ΛCDM or match w0–wa? (gate passed: 0.08 ≤ 1.0) | 3 | PC, AxiCLASS |
| **TF** | The two heuristic F values, √(3/2) and √6 | 6 | PC, AxiCLASS |
| **FP** | Fingerprint (Holst) vs plain cosine (Nieh–Yan): tests the coupling choice | 2 + build + regression gate | PC, AxiCLASS (Fingerprint build) |
| **S8WL** | Full weak-lensing likelihoods (DES Y3, KiDS-Legacy) instead of the S8 penalty | per survey | PC, CosmoSIS; **draft rule, lock first** |
| **N2** | Potential power: n = 3 vs 2 vs 4 (`edelockP_n2_deep`) | 1 | cloud, CAMB (Kronos) |
| **BR** | Knockout bracket, stage 1: 6 variants (then stages 2–3 as the rule says) | 6+ | cloud, CAMB (Kronos) |

`TESTS.json` lists every run name and rule file. `STATUS.md` (written by `score.py`) shows where each stands.

## On the PC

- **Start now and schedule nightly:** double-click `SCHEDULE_FIELD_TESTS.bat`. It builds and checks the Fingerprint code, then starts the 14 AxiCLASS runs (12 + 2 Fingerprint; about
  2–3 hours on 16 cores, 7 lanes) and adds a nightly 01:13 resume. Finished runs are skipped, so re-runs are safe.
- **Just run once:** `RUN_FIELD_TESTS.bat` (add `--push` to publish results to the `field-results` branch).
- **Order:** Union3 first (the blind sample), then DES Y5 and Pantheon+; TF-P before TF.
- **Scoring:** `python field_tests/score.py` at any time. It calls the locked scorers in `scorers/` (copies of the
  release scorers, changed only to read `$TWIST_RESULTS`; original hashes in `scorers/ORIGINAL_SHA256.txt`).

## FP: rebuilt 7 Nov

**Now runnable.** `torsion_shape/patch_sinh.py`, `build_sinh.sh`, `regress_sinh.py` (the rule's every-digit check, a gate) and
`fp_fit.py` (fits `fp_cosine` and `fp_sinh` identically; `fp_fit.py score` applies the rule). `run_pc.sh` builds and checks it
automatically before the lanes start. Deviations: `torsion_shape/FP_DEVIATIONS.md` (the rule's reference number came from a
withdrawn, unconverged run, so the plain cosine is refitted on the same engine).

Original note:

The `axion_sinh_x0` AxiCLASS option behind the Fingerprint (`PREREGISTRATION_SINH.md`) is not in any repository. To
run FP: re-add the option to the potential (V, dV, ddV) using g(d) = s[sinh((d+φ₀)/s) − sinh(φ₀/s)]/cosh(φ₀/s),
s = √(3/2), x₀ = arsinh(1/γ₀) = 2.1445 fixed; confirm that with the option off it reproduces the current build to every
printed digit (the rule's own regression check); then fit Planck 2018 + DESI DR2 + Pantheon+ and compare with the
plain-cosine reference χ²_eff 2427.80 as the rule states. Log the rebuild as a deviation (code re-implemented, rule
unchanged).

## In the cloud (Kronos)

N2 and the bracket use the CAMB pipeline and run in the cloud chat; their results land in
`aegis-Kronos-syndyr/data/fits/refit5/` and are scored by `research/refit/tournament.py` and `bracket.py`.
