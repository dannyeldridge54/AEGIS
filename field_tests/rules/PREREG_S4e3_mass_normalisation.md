# PREREG S4e3 — mass-normalisation convention check vs BTR eq. 5.14 (large list 12)

Locked 2026-11-17 before any computation. Label: POST-HOC convention search (target values are known: S4e gave m L/π = 0.9318, 2.0403 with BC D; BTR quote 0.97, 2.13).

## Fact used
Under a constant shift A → A + a of the warp factor (fixed y), J = e^{B−A} and the z coordinate rescale, the η-frame eigenvalue scales as m² → e^{2a} m², L = ∫e^B dy is unchanged, so m L scales by e^{a}. Hence m L/π depends on how the warp factor is normalised. Equivalently a mode with η-mass m has local proper mass m e^{−A(y_ref)} if e^{A} is set to 1 at y_ref.

## Conventions (fixed list, no additions after results)
- C0: A exactly as in theory/strings/s4e_scalar_masses.py (BTR §3 form, no shift) — reproduces S4e.
- C1: e^{A} = 1 at the maximum of A on the interval.
- C2: e^{A} = 1 at the proper-length midpoint (∫e^B dy = L/2).
- C3: 9D-Planck weighting: shift so that (1/L)∫ e^{(D−2)A} e^{B} dy = 1.
Each convention: m L/π → (m L/π)_C0 × e^{−A_ref}, with A_ref computed numerically on the same cutoffs (ξ from 1e-4 to 8) as S4e; BC D only (the BC that S4e matched in ratio).

## Pass rule
A convention MATCHES if |m1 L/π − 0.97| ≤ 0.01 AND |m2 L/π − 2.13| ≤ 0.01 (2-sig-fig rounding plus slack).
Verdicts: exactly one match → "CONVENTION IDENTIFIED (post-hoc, consistent)"; more than one → "AMBIGUOUS"; none → "NOT EXPLAINED by these conventions".
S4e's recorded verdict (NOT VALIDATED vs BTR) is unchanged in all cases; this test only informs which convention to state when quoting our 6D masses.
No reruns to chase a match; fixes only via DEVIATIONS written first.
