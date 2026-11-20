# Twin slip-ladder — data sheet (living; started 2026-11-20, Danny 07:07)
Rungs: theory/quarks/LADDER_DATASHEET.csv (regenerate: `python3 theory/quarks/ladder_datasheet.py`).
Shape (same as the dual-helix twin ladder): LEFT ladder climbs to the knot ρ ((m,0) classes, CP-violating slips);
RIGHT ladder climbs to the knot i ((0,n) classes, at i); CENTRE = the arc |τ| = 1 where mixed (m,n) classes sit (Ma'at balance).
Status words: lit · formula (paper fit, m ≤ 7) · extrap · computed · derived · open · TENSION.

## Who sits where (current)
| place | occupant | source | status |
|---|---|---|---|
| knot ρ (rung ∞, or ≳ 400) | inflaton endpoint; charged leptons (Koide needs |ε| ≲ 6e-5) | D1606, D1595, D1737 | derived / computed |
| rung 8 (68%: 5–14) | up quarks (u, c, t) | D1733, D1734, D1736 | computed (chance 52%); rung position now computed, not extrapolated |
| rung 1 | down quarks (d, s, b) | D1733 | computed |
| rung 1 | ~~charged leptons~~ WITHDRAWN (a rung-1 slip breaks Koide by 8.5e-3) | D1737 | computed |
| arc (m,n) | — (position set by the ratio m:n alone) | D1736 | computed |
| knot i | neutrino modulus (P-F3), dark thread / Arthur field at rest | D1610, D1653 | derived |
| rungs 11 → ∞ (ρ side) | empty in the SM; room for hidden families | D1734 T4 | structure only |

## How the sectors interact, rung to rung
| pair | interaction | number | status |
|---|---|---|---|
| up (8) ↔ down (1) | CKM mixing = mismatch of the two rungs' matrices | best O(1): |V_us| 0.195 (0.87×), |V_cb| 0.043 (1.03×), |V_ub| 0.0011 (0.30×), J 8.9e-6 (0.29×); m_s/m_b 0.38× | computed FAIL (D1738); better than one modulus (χ² 54→39) |
| up (8–10) ↔ down (1), weight-8/6/4 model | CKM + masses | χ² 5.8; pass m_d/m_b, m_c/m_t, m_u/m_t, V_us, J; miss m_s/m_b 0.54×, V_cb 1.27×, V_ub 0.73× | computed FAIL, closest so far (D1739) |
| up (8) ↔ down (1) | strong CP: θ̄ = 0 for any rungs if weights anomaly-free | θ̄ = 0 | lit (FST) |
| down (1) ↔ charged leptons (knot) | NOT the same rung; hierarchies by different mechanisms (slip vs Z₃ numbers) | ΔQ(rung 1) = 8.5e-3 | computed (D1737) |
| quarks (ρ side) ↔ neutrinos (i) | different knots ⇒ small CKM vs large PMNS | θ_C 13° vs θ₁₂ 34° | consistent (qualitative) |
| τ_q ↔ inflation | τ_q decay dilutes, ΔN* = −⅓ ln D | m(τ_q) ≳ 2e10 GeV | computed (Q4, D1730) |
| quarks ↔ dark thread | no coupling allowed today (clocks, F1) | ζ < 3.6e-6 | bound |
| quarks ↔ wino / B→μμ | none at tree/one loop | R_μμ +0.6σ (SM) | consistent (D1726) |

## Postulates on this sheet
- P-Q9 slip ladder (D1734).
- P-Q10 twin ladder (D1735): (m,0) to ρ, (0,n) to i, (m,n) on the arc; built outward from both knots.
- P-Q11 history (D1735): rungs freeze in order as the universe cools; the knot is the far-future limit. Must NOT move today (see D1735).

## Queue (each locked first)
Q8 CKM from rungs (1, 8). Q10 Koide vs rung-1 slip. Q11 compute the SUGRA minima directly for m up to 32 and mixed (m,n) (removes the "extrap" label).
