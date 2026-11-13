## Development 65 — The tail's bend does not help w_a (13 Nov 08:35)

**Idea tested.** With β = 0 (D64), can the real tail's bend (flat, then bending onto slope √(2/3), D43) make dark energy change faster and deepen w_a? Background calculation (radiation + matter + field from rest, Ω_DE = 0.69, CPL fit z < 2). Check: the pure-exponential limit gives w₀ −0.900, w_a −0.145, matching the CLASS PURE-TWIST predictions and the Scherrer–Sen thawing formula (a first version of the script had the kinetic energy too large by 3 in the w and Ω formulas; caught by this check, fixed before any use).

| start relative to the bend | w₀ | w_a | slope seen today |
|---|---|---|---|
| far before (flat part) | −1.000 | 0.000 | 0.04 × √(2/3) |
| at the bend | −0.974 | −0.039 | 0.52 × √(2/3) |
| past the bend | −0.928 | −0.105 | 0.86 × √(2/3) |
| far past (pure exponential) | −0.900 | −0.145 | 1.00 × √(2/3) |

**Reading.** No. The bend only brings w closer to −1. For β = 0 the pure exponential is the most dark energy can evolve: the theory's own prediction is **w_a between 0 and about −0.15** (w₀ ≥ −0.90). This is a sharper statement than the locked ceiling (−0.40, which also covers coupled versions). Crossroads: A. accept it (taken: it is what the theory says); B. a steeper slope κ > √(2/3) — excluded, the 3 fixes κ; C. a coupling — excluded by D64. If DESI DR3 confirms w_a ≲ −0.3, the β = 0 Twist is in trouble well before the −0.40 ceiling. Code: theory/darkenergy/tail_bend_wa.py.
