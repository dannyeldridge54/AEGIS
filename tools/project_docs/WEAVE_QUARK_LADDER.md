# The Weave — quark sector and the twin slip-ladder (20 Nov 2026, D1726–D1740)
Supplements WEAVE_FULL_EQUATION §5. Correction to §5: "their fit τ_q = 1/8 + i" is one model's fit, not a universal location (D1729).

## Summary (honest status: quarks HOSTED and CONSISTENT, NOT PREDICTED)
| step | test (locked) | result |
|---|---|---|
| Q1 | inflaton endpoint ρ as the quark modulus | FAIL: leftover offset ~1600× too small (D1727) |
| — | dark thread as the quark modulus | FAIL: would make quark masses drift today (clocks, F1) and rests at a CP-symmetric point (D1619) |
| Q2 | Koide (δ = 2/9) for quarks | FAIL: Q(u,c,t) 0.887, Q(d,s,b) 0.742 (D1728) |
| Q3 | anomaly-free modular quark models predictive? | FIT-ONLY: 15–22 parameters for 8–10 observables; θ̄ = 0 structure survives (D1729) |
| Q4 | heavy τ_q vs early universe | PASS: m(τ_q) ≳ 2e10 GeV (≳ 8e8 if displaced 0.1 M_P) (D1730) |
| Q5 | what holds τ_q | SUGRA (m,0) minima just off ρ, CP-violating (lit 2201.02020) (D1731) |
| Q6 | zero-parameter ε vs quark fits | FAIL: |ε| 0.024 vs needed 0.028–0.038 (D1732) |
| Q7 | split thread: up and down on different rungs | PASS (structure): down rung 1, up rung ~8 (D1733) |
| Q9 | slip ladder from two anchors | map: rung 1 down, rung 8 up (chance 52%), neutrinos off-ladder at i (D1734) |
| Q11 | compute minima directly | formula holds to ~1% up to m = 32; mixed (m,n) on the arc, set by m:n (D1736); independently confirmed by root finding to <1e-5 (D1740) |
| Q10 | charged leptons on rung 1? | NO: slip breaks Koide by 8.5e-3; leptons at the knot (or rung ≳ 400) (D1737) |
| Q8 | CKM, original model, split rungs | FAIL; χ² 54 → 39 vs one modulus; V_cb and up masses fixed (D1738) |
| Q12 | CKM, weight-8/6/4 model (chosen after Q8), split rungs | FAIL but closest: χ² 5.8 (one modulus 20.4), all couplings O(1); misses m_s/m_b 0.54×, V_cb 1.27×, V_ub 0.73× (D1739) |

## The twin slip-ladder (P-Q9/P-Q10/P-Q11)
- Left ladder → knot ρ: SUGRA classes (m,0), |ε_m| ≈ 0.0251/(m + 1/16), arg ≈ 50°, CP-violating. Rung 1: down quarks. Rung 8 (–13): up quarks. Rungs ≳ 400 or the knot: charged leptons (Koide). Rungs 11 → ∞: empty in the SM.
- Right ladder → knot i: (0,n) classes sit exactly at i. Neutrino modulus and the dark thread rest here.
- Centre: mixed (m,n) classes on the arc |τ| = 1, CP-conserving, position set by m:n alone.
- History reading (P-Q11): rungs freeze in the early universe; the knots are far-future attractors; nothing moves along the ladder today (clock bounds).
- Hierarchies by two mechanisms: quarks by slip distance; leptons by symmetry numbers at the knot (√2, 2/9).
- Independent literature cross-check: 2212.13336's own two-moduli fit puts ε_d near rung 1 and ε_u ≈ rung 13 (not a prediction).

## Open
The down sector wants a larger slip than rung 1 (m_s/m_b low in both models); the residual misses in V_cb and V_ub; what selects the classes m; why the weights are anomaly-free.
Data sheet: repo theory/quarks/LADDER_DATASHEET.md + .csv. Weave Control has a Quarks level.

## The ladder equation (D1741) — frozen predictions (PREREG_LADDER_PREDICTIONS, 20 Nov 2026)
    ε_m = 0.0251·e^{i50°}/(m + 1/16)
    rung-m family:  m₂/m₃ ≃ κ₂ε_m,  m₁/m₃ ≃ κ₁ε_m²  (κ O(1))
    two families:   g_a/g_b = (m_b + 1/16)/(m_a + 1/16)   (equal-coefficient limit)
| # | prediction | today | how it is scored |
|---|---|---|---|
| L1 | up quarks on rung 8: g_u/g_d = 0.1318 (rung 9 would be 0.1172) | 0.1276 ± 0.0060 (0.7σ) | future quark masses with σ ≤ 0.0049 |
| L2 | no Koide for quarks; leptons never follow slip scaling | holds (D1728, D1737) | any new precision masses |
| L3 | any new modular fermion family sits on an integer rung: m₂/m₃ ∈ [ε_m/3, 3ε_m]; free rungs 2–7, ≥ 11 | — | a dark-sector family, if found |
| L4 | θ̄ = 0 exactly | |θ̄| < 1e-10 | neutron EDM |
