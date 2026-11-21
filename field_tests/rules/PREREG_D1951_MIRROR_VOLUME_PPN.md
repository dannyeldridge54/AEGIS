# PREREG D1951 — Mirror-Loom test 2: posterior fix for the volume-direction thread vs the PPN/fifth-force bound, and its early-universe mirror (locked 21 Nov 2026 BEFORE any research or computation of this tick; repo at bf14ac0f)
Agent: MIRROR-LOOM. Planning knowledge declared: D1906 (β = −0.354), D1906a (DEF α = √2β = 0.50 ⇒ γ − 1 = −0.40), Cassini (2.1 ± 2.3)e-5.

## Part (a): the bound on γ − 1
Bearings: every independent PPN-γ measurement I open (Cassini Shapiro delay, VLBI light deflection, planetary ephemerides INPOP/EPM, MESSENGER/BepiColombo, Gaia/Hipparcos astrometry, others). Minimum 5, maximum 8; include all opened. Gaussian in γ − 1 with the stated 1σ (systematics added in quadrature when stated); no ×2 inflation (framework = PPN, matches). Combiners: Gaussian product, Student-t (ν = 3), PRIMARY good-or-bad mixture (good prior 0.8, bad = uniform on ±1e-2), on a flat prior on [−1e-2, +1e-2]. Report median, 68/95 % intervals, χ²/p, BF(common vs separate), weights. Bound B95 = max(|lower|, |upper|) of the primary 95 % interval.

## Part (b): the coupling of the volume direction
Bearings on the DEF coupling α (matter-scalar coupling, γ − 1 = −2α²/(1+α²)) of a rolling Kähler modulus that changes the total volume: this repo's D1906/D1906a computation and literature values for volume / no-scale / LVS / axio-dilaton moduli (minimum 5 including the repo's, maximum 8). Gaussian in α with σ = 20 % when the source states a single value for its own model; ×2 when the model is not the Weave's (one torus factor, K = −ln(T+T̄), IIB). Same three combiners, flat prior α ∈ [0, 2]. Predicted γ − 1 from the primary α posterior (median and 95 % interval).
Verdict: **PASS** if the predicted |γ − 1| (median) ≤ B95; **PARTIAL** if ≤ 3·B95; **FAIL** otherwise. FRAGILE label as in D1950.

## Mirror (the visible-sector volume modulus in the early universe)
If the thread is the volume direction, every particle mass in Planck units scales as 𝒱^{−1/2}, so between BBN and today G m² changed by Δ ln(G m²) = 2·(β)·Δφ with Δφ the thread excursion since z* (0.64 M_P, D1853; a thawing field is frozen at BBN, so this is also the excursion since BBN). Mirror bound: the BBN (and, if found, CMB) bound on G_early/G_0 from sources opened this tick (≥ 1; flagged THIN if < 3). Mirror PASS if |Δ ln(G m²)| ≤ the 95 % bound; PARTIAL ≤ 3×; FAIL otherwise. Also reported (no verdict): the Kallosh–Linde requirement that the visible volume modulus be heavier than H_inf, versus a thread mass ~ H₀.
Centre balance: the volume thread COUNTS only if part (b) vs (a) and the mirror both PASS.
Script and results: field_tests/mirror/. No reruns to chase; tolerances never loosened.
