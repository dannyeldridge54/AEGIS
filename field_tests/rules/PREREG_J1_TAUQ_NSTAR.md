# PREREG J1 — wire the τ_q dilution joint into the inflation level (Danny 20 Nov 11:46 "Yes", after D1750)
Locked BEFORE the code change and before any number is computed.

## What changes
The Weave Control engine computes the τ_q dilution D (quark level, D1730: D = T_R φ0²/(6 T_dec), T_R 1.34e9 GeV) but the
inflation level ignores it. After this change run() adds a JOINT block to the inflation level, computed from both levels:
- dN* = −ln(D)/3 (standard; same formula as weave_basic dNstar)
- N*_eff = N*_inf + dN*, where N*_inf is the N* the inflation level used
- r_joint = r_inf · (N*_inf / N*_eff)²   (plateau scaling r ∝ N⁻², D1588; the tilt factor is held fixed — label E)
- ns_shift_if_not_refit = −2·dN*/N*_inf² ... sign: n_s = 1 − 2/N ⇒ Δn_s = 2·dN*/N*² (negative for dN* < 0); for serapis_* n_s is FITTED, so this is reported as the re-tuning the fit must absorb, not a prediction.
- pull: r_joint vs the stored r bounds (same constraint set the inflation level already uses).

## What does NOT change
- The inflation level's own outputs (ns, r, alpha_s) and its status stay exactly as they are (locked results untouched).
  The joint is a separate block with its own status 'joint_status' (pass if r_joint passes the same r bounds and
  the quark-level τ_q window passes; else FAIL). The evidence atlas is NOT changed by this prereg.
- No tolerance is loosened. No reruns to chase a value.

## Pass criteria for the code change (checked once)
1. At DEFAULTS the joint block exists, dN* equals weave_basic dNstar(D) to 1e-12, and r_joint/r_inf = (N*/N*_eff)² to 1e-12.
2. With D = 1 (τ_q mass 5e12 GeV) r_joint = r_inf exactly.
3. All existing tests still pass (15) plus one new test for 1–2.
The numbers at DEFAULTS are reported as they come out (label E), whatever they are.
