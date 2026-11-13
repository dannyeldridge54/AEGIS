# PREREG TAIL-F: the full tail, with today's slope set by the heat share (Development 78b)

Locked 13 Nov 2026 under STANDING_LOCK_AUTHORITY.md, before any TAIL-F fit is run. AI-assisted.

## Model
The full supergravity tail (μ = 1, n = 125, m2 = 1): the field freezes after the cliff where the heat share f leaves
it (tail_freeze.run) and thaws on the full tail shape (tail_full_thaw.solve). Its w(z) is represented by the CPL
pair (w0, wa) fitted over z < 2, read off field_tests/results/tail_curve_table.json
(sha256 d0f6adc13fb4ff668a1a0d46fa217cf48efdc9482a478891e59badcea46e04fd), interpolated linearly in ln f. β = 0. Approximations stated: Ω_m = 0.31 fixed when building the table; CPL
stands in for the exact w(z); background + PPF only (as TOURNAMENT's W0WA).

## Data and likelihood
Exactly TOURNAMENT's FULL configuration: DESI DR2 BAO + Pantheon+ + compressed CMB (θ*, ω_b, ω_b + ω_c),
tournament.chi2("W0WA", [h, ω_b, ω_c, w0, wa], bao_desi()). Free: h, ω_b, ω_c (Nelder–Mead, TOURNAMENT's two starts and
settings). Reference: ΛCDM χ² = 1401.176 and w0wa χ² = 1394.971 (best w0 −0.872, wa −0.368) from tournament/*_FULL.json —
disclosed: these were known before this rule was written.

## Two fits
- FIXED: f = 0.13%, the computed heat share (D42; computed before this rule). Zero extra parameters.
- RANGE: f free in [0.01%, 0.25%] (the table's span; above ~0.25% the tail is too stiff to be dark energy). One parameter.

## Readings (Δ = χ² − χ²_ΛCDM)
FIXED: Δ ≤ −2 → "FULL TAIL HOLDS"; −2 < Δ < +2 → "FULL TAIL NEUTRAL"; Δ ≥ +2 → "FULL TAIL DISFAVOURED".
RANGE: best f in [0.04%, 0.25%] (inside the derived range 0.04–0.4%) → "HEAT SHARE CONSISTENT"; best f < 0.04% →
"DATA WANT LESS HEAT THAN COMPUTED". Also reported, no reading: χ²_RANGE − χ²_w0wa.

## No reruns to chase results. Fixes only through TAIL_F_DEVIATIONS.md written before any rerun.
