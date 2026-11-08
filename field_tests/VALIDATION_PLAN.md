# Validation plan (added 8 Nov 2026 at Danny's request)

Goal (Danny): not just beat ΛCDM, but map the equation as fully as possible, then test it in as many independent ways
as we can. Every item below is **planned**, not locked. Each gets its own locked rule before it touches data. Order:
after today's S8-J, S8-L and the bracket.

| Order | ID | What it checks | Where / cost |
|---|---|---|---|
| 1 | MAP | The Twist's full action, every term marked **derived / chosen / fitted** | cloud, paper work |
| 2 | V-PRED | Numbers locked now for DESI DR3, Euclid, Rubin, Simons Observatory (strongest test) | cloud, cheap |
| 3 | V-ALPHA | Constants of nature do not drift (dilaton touches only dark matter; separates us from the Axiodilaton) | cloud, cheap |
| 3 | V-GW | Gravity waves travel at light speed (GW170817) | cloud, cheap |
| 3 | V-BBN | No extra radiation in the first minutes (N_eff, D/H, helium) | cloud, cheap |
| 3 | V-BIREF | CMB polarisation twist stays within Planck/ACT limits | cloud, cheap |
| 3 | V-FIFTH | Dark-matter-only fifth force vs galaxies and clusters | cloud, cheap |
| 4 | V-FS8 | Growth rate fσ8 from galaxy motions (DESI, BOSS) | PC fits |
| 4 | V-CLUSTER | S8 from cluster counts (eROSITA, SPT) | PC fits |
| 4 | V-CODE | Same headline numbers in CLASS and CAMB | cloud + PC |
| 5 | V-LYA | Lyman-α cutoff of the light angle (only if S8-L works) | after S8-L |

Also open from the quantum-side list (`theory/QUANTUM_SIDE_NOTES_2026-11-08.md`): instanton height (the angle's
mass), origin of n = 3, the starting-angle conflict, Holst mixing before the next FP test. The n = 1 test stays
deferred (both engines hang).

## Status after the first pass (8 Nov, 10 AM; details in the Claude doc "The Twist equation map")
- MAP: **done (first version)**. 5 derived, 1 derived in kind, 4 chosen, 5 fitted.
- V-GW: passes by construction (Einstein–Cartan + Nieh–Yan reduces to GR; theory audit E). Rule only needs to record it.
- V-ALPHA: Twist predicts no drift at tree level; limits gathered (ESPRESSO 1.3 ± 1.4 ppm; clocks (1.0 ± 1.1)e-18/yr).
- V-FIFTH: Twist force ratio 2β² ≈ 0.4% vs Sagittarius-stream bound ≈ 4% (β_KK < 0.2). Must first state whether the
  coupling acts on all dark matter (as fitted) or only on the 5% angle share at full strength.
- V-BBN: early field frozen at BBN; estimate negligible. Rule should compute it from the stored fits.
- V-BIREF: already done 2 Nov (B4): the Twist does not explain the measured 0.24°; EXCLUDED as an explanation.
- V-FS8: GH (2 Nov) NEUTRAL for older fits; redo for the Spiral and S8-J/S8-L fits.
- V-PRED: 2 Nov locks cover the Late and Coupled Twist only. **Gap: lock predictions for the Spiral + Locked Twist (and
  S8-J/S8-L once scored) before DESI DR3 (not out) and Euclid DR1 cosmology (mid-2027).**
- V-CLUSTER, V-LYA, V-CODE: not started (V-CODE partly covered by existing mirrors).

## Per-step folders (8 Nov)
Prep, data collected and to-do for each scheduled step: `field_tests/validation/V1..V5_*.md`; running log `field_tests/validation/DATA_LOG.md` (each check-in appends what it finds).

## Credibility items added 8 Nov (priority by expected referee impact)
| Priority | ID | Item | Cost | Status |
|---|---|---|---|---|
| 1 | V1 | Locked predictions for DESI DR3 (before release) | cloud, cheap | scheduled today 16:47 |
| 2 | V6 | Full posteriors (MCMC) and Bayesian evidence (MCEvidence/PolyChord) | PC, ~2–4 days | plan written |
| 3 | V7 | Programme-wide look-elsewhere correction (local vs global σ) | cloud, cheap | plan written; inventory base = ledger |
| 4 | V9 | Pre-registration ledger with hash verification | cloud, cheap | **built**: 50 files verified, 72 verdicts |
| 5 | V8 | One-command reproducibility package | cloud + PC export | plan written |
| 6 | V5 | Instanton height (derived mass) | theory | scheduled 12 Nov |
Wording: `field_tests/WORDING_STANDARD.md` applies to all write-ups.
