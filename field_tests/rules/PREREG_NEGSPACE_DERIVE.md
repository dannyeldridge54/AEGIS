# PREREG_NEGSPACE_DERIVE (D1716) — does the Weave produce "negative space" (a sign-switching effective Λ) by itself?
Locked 19 Nov 2026 20:55 CT before computing. Danny: "Negative space derivation review populate make and derive it".
Idea: in the coupled thread (b < 0, φ rising) dark matter LOSES mass, ρ_c(a) = ρ_c* (a*/a)³ e^{b(φ−φ*)}. A standard analysis fixes ω_c from the CMB (at z* = 1090) and calls everything else "dark energy":
  ρ_DE,eff(a) = ρ_φ(a) + [ρ_c(a) − ρ_c*(a*/a)³].
The bracket is negative and grows as a⁻³ into the past, so ρ_DE,eff can be NEGATIVE at high z and positive today: a derived ΛsCDM-like switch.
Input: the validated CLASS coupled background (D1713, amp 1.83, b = −0.074, the D1710 point; no refit), file out_c_00_background.dat.
Outputs: z† where ρ_DE,eff = 0 (if any; count sign changes); depth r3 = ρ_DE,eff(z=3)/ρ_DE,eff(0); same for the uncoupled thread (control: must have NO switch).
Pass rules (fixed now):
- DERIVED: exactly one sign change, at 1.5 ≤ z† ≤ 3.2 (the range spanned by our real-data ΛsCDM fits, z† = 2.37–2.64, D1692/D1695, and the literature's ≈ 1.7–2.5), and the control has none.
- SHAPE MATCH (extra): −3 ≤ r3 ≤ −0.3 (ΛsCDM has r3 = −1).
- Otherwise: NOT DERIVED, recorded as such.
No refit, no change of point after seeing the result.
