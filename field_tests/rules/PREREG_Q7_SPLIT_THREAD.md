# PREREG Q7 — split the quark thread (Danny 07:01: "later parts within the weave… fields 9 through 16… it continues to get split up to 16. Test that.") (locked 2026-11-20, before computing)
Postulate P-Q7: the quark thread is not one field. Up-type and down-type quarks each sit on their own modulus (τ_u, τ_d), each at a
supergravity (m,0) CP-violating minimum near ρ (arXiv:2201.02020) with its own integer class m. The family index m runs 1…16.
Prediction per m (2212.13336 convention): |ε(m)| = √3 · 0.0145/(m + 0.0625), arg ε = 50°. Formula verified by the paper only for m ≤ 7;
m = 8…16 is an EXTRAPOLATION and is labelled so.
Near-ω hierarchy with O(1) couplings (2212.13336 Eqs. 48–49): m₂/m₃ ≈ |ε|, m₁/m₃ ≈ |ε|². So each sector implies two ε targets:
 e_a = m₂/m₃ and e_b = √(m₁/m₃), from M_Z masses (Q2 inputs: u 1.29 MeV, c 0.629, t 169 GeV; d 2.80 MeV, s 55.7 MeV, b 2.794 GeV).
Rule (O(1) couplings ⇒ factor-3 tolerance, set now): a sector MATCHES class m if both e_a and e_b lie within [|ε(m)|/3, 3|ε(m)|].
 Report every matching m for up and for down.
PASS (split thread viable) if at least one m matches down AND at least one m matches up, with the down and up classes allowed to differ.
Also report, without a pass rule: which m sits closest (geometric mean of e_a, e_b) for each sector.
Disclosure: before writing this lock I estimated roughly where the sectors fall (up near |ε| ~ 3e-3, down ~ 2–3e-2). The rule is fixed now; the
script below is run once after commit. No reruns, no new tolerance.
Not evidence: up/down masses were known; this tests whether a discrete family of minima CAN host both sectors (structure).
