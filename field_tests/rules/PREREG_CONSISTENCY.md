# CONSISTENCY: does one coupling explain both expansion and growth?

**Status: LOCKED** on Danny's word ("schedule them all to set automatically in q", 12 Nov 2026, 14:17 CT, asking for every pending test to be queued to run). Draft text below unchanged except this line. Drafted, written 12 Nov 2026 at Danny's request ("Yes", 13:21 CT, to "draft the consistency test as a rule
for your lock, to run after β(z)"). It becomes LOCKED only on Danny's word, and runs only after PREREG_BETAZ.md is
scored. AI-assisted. Cloud.

**Why.** In FLAG-1 one coupling β does two jobs: it changes the expansion history (BAO, supernovae, CMB distances) and
adds the fifth force that changes the growth of structure (fσ8, E_G). A data quirk in distances would not also show
up in growth. If β measured from expansion alone and β measured from growth alone agree, that is strong evidence for
the coupling; if they disagree, the expansion signal comes from something else.

**Not blind, and the expected reach, stated now.** Known at writing: V3 (DESI DR1 full-shape fσ8: both models
consistent, χ² ≈ 5 for 6 points), M2 (E_G: no discrimination), the frozen E_G forecast, and that FLAG-1's E_G is about
4.8% above ΛCDM. Today's growth data are loose (fσ8 errors 5–10% per tracer, E_G about 17%), so β from growth is
expected to be poorly measured and the likely reading is CONSISTENT with a wide error. The test is built now so that
DESI DR3 full-shape and future E_G data can be scored the same way.

## Build
`AxiCLASS_coupled_betabins`, with the growth equations also using β(z) (12 Nov). **Gate (done before this draft):**
with all β equal, P_cb(k = 0.02 and 0.1 Mpc⁻¹, z = 0, 0.5, 1.5) and σ8 match the original coupled build to 2×10⁻⁶
relative; with β varying, growth changes as expected (σ8 0.7990 → 0.8007 for β_a = 0.03).

## β from expansion
The constant-β FLAG-1 fit on the compressed DR2 anchor (`betaz/const_dr2.json`, from PREREG_BETAZ.md): β_exp with its
Hessian error (finite differences, step 0.005).

## β from growth
Background held at the expansion fit's h, ω_b, ω_c; only β is free, β ∈ [0, 0.15] (the early-universe coupling is
held at its fitted value, so the CMB is not refitted). Data, growth only:
- DESI DR1 full-shape fσ_s8, six tracers, with the SELFCHECK V3 conversion (D2: EH98 no-wiggle primary) and its
  diagonal errors;
- ACT DR6 × BOSS E_G, two points, as in MISSING-PIECE M2.
β_grow and its error from a 1-D scan (Δχ² = 1), in steps of 0.0025.

## Readings
- **ONE COUPLING EXPLAINS BOTH:** |β_grow − β_exp| ≤ 2σ_comb, and σ_grow < 0.04 (growth actually constrains β).
- **CONSISTENT BUT UNCONSTRAINED:** |β_grow − β_exp| ≤ 2σ_comb, and σ_grow ≥ 0.04.
- **TENSION:** 2σ_comb < |β_grow − β_exp| ≤ 3σ_comb. **INCONSISTENT:** beyond 3σ_comb.
- σ_comb is the two errors in quadrature; the two fits share no data, so they are treated as independent.
- Also reported: the growth-data precision that would make σ_grow < 0.01 (a 2.5σ test of β = 0.041 from growth alone).

## What may not happen
No change of data, conversion, bounds, scan or bands after any number. Counted +1 in V7.

## Code
To be written after the lock (`field_tests/missing_piece/consistency.py`), reusing `v3_desi_fs.py` and `m2_eg.py` methods.
