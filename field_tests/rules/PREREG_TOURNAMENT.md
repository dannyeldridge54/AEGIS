# TOURNAMENT: every late-time Twist version through the same tests, and the best one that acts like ΛCDM then engages

**Status: LOCKED** on Danny's word ("Do this in cloud give me the best standard version that acts like ΛCDM then
engages", 12 Nov 2026, 16:59 CT, replying to the proposed tournament). Written and locked by Claude before any
tournament fit. AI-assisted. Cloud.

**Why.** Today FLAG-1 failed to predict DESI when DESI was held out (Test A: ΔA = +12.46), and DESI and SDSS agree
(M3). Before anything is carried forward, every late-time version of the Twist runs the same tests on the same data,
including versions that behave exactly like ΛCDM until the coupling switches on late.

**Not blind.** Known at writing: every stored result in CURRENT_MODEL.md, including M1 (compressed anchor: FLAG-1
χ² 1395.852 vs ΛCDM, Δ −5.32), Test A, M3 (the no-BAO FLAG-1 predicts DESI and SDSS worse than ΛCDM), CC, DATA-GEN.

## Likelihood (one for all)
The M1 / V1 compressed real-data anchor: Pantheon+ (analytic M), compressed CMB vector, background only, plus BAO by
configuration. Build `AxiCLASS_coupled_betabins` (gated: reproduces the coupled build to 10⁻⁷).

## Versions (k = parameters beyond ΛCDM's h, ω_b, ω_c)
| Id | Version | k |
|---|---|---|
| LCDM | ΛCDM (reference) | 0 |
| W0WA | w0–wa fluid (reference only, not a Twist version) | 2 |
| SPIRAL0 | Spiral, κ = 1, no coupling (β = 0) | 0 |
| FLAG1 | Spiral, κ = 1, constant β ∈ [0, 0.15] | 1 |
| SPIRAL | Spiral, κ free ∈ [0.1, 2], β ∈ [0, 0.15] | 2 |
| ON2 / ON1 / ON05 | **Switch-on:** κ = 1, β = 0 for z ≥ z_on, constant β_late ∈ [0, 0.15] for z < z_on, with z_on = 2, 1 or 0.5 fixed | 1 each |

The switch-on versions are the "acts like ΛCDM, then engages" family: before z_on the dark matter is uncoupled.
Choosing among three z_on values is counted as three tries.

## Configurations
- **FULL:** DESI DR2 BAO (ALL covariance).
- **NOBAO:** no BAO. Each version's NOBAO best fit then **predicts** DESI DR2 and SDSS BAO with no refit.
- **SDSS:** SDSS BAO instead of DESI: DR12 consensus z = 0.38 and 0.51 (rs_fid 147.78 Mpc; with their 4×4 covariance),
  DR16 LRG z = 0.698 and DR16 QSO z = 1.48 (their 2×2 covariances), as in DATA-GEN generation 2 without ELG, Lyα and MGS.

Fits: Nelder–Mead, best of 2 starts (the ΛCDM-partner values with β = 0.01 and 0.06; κ = 1 for SPIRAL; w0, wa =
(−0.9, −0.3) and (−0.75, −0.8) for W0WA), maxfev 1500 per start. **Gate:** LCDM and FLAG1 FULL fits reproduce M1's
full-data χ² to within 0.05; else NO VERDICT on everything.

## Scores per version (each relative to LCDM in the same configuration)
- ΔAIC_FULL = Δχ²_FULL + 2k.
- Prediction: ΔP_DESI = χ²_DESI(version, NOBAO fit) − χ²_DESI(LCDM, NOBAO fit); ΔP_SDSS likewise.
- Δ_SDSS = Δχ² in the SDSS configuration.

## Readings
- A Twist version **PREDICTS** if ΔP_DESI ≤ 0 and ΔP_SDSS ≤ 0 (it predicts both surveys at least as well as ΛCDM)
  and Δ_SDSS ≤ +1.
- **BEST STANDARD VERSION:** among Twist versions that PREDICT, the lowest ΔAIC_FULL, provided ΔAIC_FULL < 0.
- If none predicts: **NO VERSION PREDICTS**; the lowest-ΔAIC_FULL Twist version is reported as "best fit only".
- If some predict but none has ΔAIC_FULL < 0: **PREDICTS BUT NOT PREFERRED**, naming the best.
- Reported for all: every χ², parameter, and W0WA beside them for reference.

## What may not happen
No change of versions, bounds, starts, configurations or bands after any fit. No new version added to chase a reading
(a new one needs its own rule). Counted +6 in V7 (six Twist versions, the three z_on values included).

## Code
`field_tests/missing_piece/tournament.py` → `field_tests/results/tournament.json`.
