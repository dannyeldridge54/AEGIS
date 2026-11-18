<!-- AEGIS-FP BFB33SNZEGHGNTLI · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J6 — Janus two-field level: δN n_s, r, f_NL^local (validation lock)

Locked 2026-11-17 (before any J6 code is run). Track J, goal J6.

## Method (fixed)
- Background: tools/serapis_calc/multifield.run (flat field space, e-fold time, end at ε_H=1).
- Slow-roll initial velocities on the flat initial slice; N(φ_a) = e-folds from the slice to ε_H=1.
- δN by central finite differences of N in field space (step h, Richardson pair h and h/2):
  P_ζ = (H*/2π)² Σ N_a², n_s − 1 = −2ε* + 2 N_a N_b V_ab /(3H*² ... ) taken from a FETCHED source,
  r = 8/(Σ N_a²), (6/5) f_NL = N_a N_b N_ab /(Σ N_a²)².
  All formulas to be fetched (Lyth–Rodriguez / Vernizzi–Wands astro-ph/0603799) and quoted with
  equation numbers in the code header before running. No formula from memory.

## Tests and pass criteria (fixed)
T1 single-field limit (V=½m²φ², χ spectator with zero gradient direction removed): n_s, r agree with
   janus_calc.core second-order values to |Δn_s| < 2e-4, |Δr|/r < 1e-3.
T2 equal-mass two-field (V=½m²(φ²+χ²)): result independent of angle on the initial circle to < 1e-4 (n_s)
   and f_NL equals the single-field value to |Δf_NL| < 0.01.
T3 Vernizzi–Wands analytic δN for V=½m_φ²φ²+½m_χ²χ², mass ratio m_χ/m_φ = 9, at the initial
   condition used in that paper's figure (taken from the fetched paper): numeric f_NL within 5 % or
   within 0.02 absolute (whichever larger) of their analytic sum-separable expression.
T4 Richardson self-consistency: h vs h/2 differ by < 1e-3 relative in N_a, < 1e-2 relative in f_NL.

Verdict: VALIDATED if T1–T4 all pass; otherwise NOT VALIDATED (recorded as is; fixes only via
PREREG_J6_two_field_deltaN_DEVIATIONS.md written before any rerun).
Runtime budget < 10 min in the cloud; else queued for the PC.
