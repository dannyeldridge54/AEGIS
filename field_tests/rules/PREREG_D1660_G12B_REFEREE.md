# PREREG_D1660_G12B_REFEREE — round-2 referee + source audit (Janus genesis G12b; locked 2026-11-19 ~23:32Z before any check)
Scope: D1653, D1654, D1655, D1657, D1658, D1659 (Janus round 2) and a SOURCE AUDIT of every genesis note D1626–D1659 (both chats) in theory/pending_docs/D72_D75_weak_spots.md.
Checks (script field_tests/scripts/janus_g/g12b_referee.py):
K-order: PREREG first commit ≤ result json first commit for each of the six; D1644/D1658 DEVIATIONS precede their rerun result (the rerun result json is the one added after the DEVIATIONS file).
K-arith: D1654 pulls recomputed from (mean, σ) = (2.86, 0.13), (2.990, 0.070) and SM 3.044; D1657 ε from Γ(e⁺e⁻) and ħ; D1659 open intervals from the band list + D1657 floor; D1658 matched |Δw₀| ≤ 0.002 for all three sets; D1655 classes from the stored distances (< 0.02 rule); D1653 R0.
K-card: g10_card_check.py CONSISTENT.
K-source (automatic flag, then read by hand): every genesis section that states an observational value or bound (patterns: N_eff, observed, bound, Planck, DESI, Y_p … ±, D/H … ±, ε ≲/≳) but carries no paper reference (arXiv number, journal ref, or named collaboration paper) in the same section is FLAGGED. Each flag is then read: "verdict-dependent" if a stated verdict rests on that unsourced number; otherwise "nit".
Pass rule: PASS if K-order, K-arith, K-card all pass and no flag is verdict-dependent. Verdict-dependent flags → FAIL; each becomes a new G-lead.
Stated limitation: same agent as most Janus notes; other chat's notes read cold.
