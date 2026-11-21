# PREREG D1950 — Mirror-Loom test 1: posterior fix for the modulus displacement off the knot ρ, and its mirror off i (locked 21 Nov 2026 BEFORE any research or computation of this tick; repo at bf14ac0f)
Agent: MIRROR-LOOM (independent test of the method; D-numbers D1950–D1969). Danny 14:35: "take it past the 3-point posteriors … continue the mirror method of SERAPIS itself."

## Need (declared; coordinator correction received before this lock)
Needed |δτ| = |ε| = |τ − ρ| = **0.0457** (down quarks; leptons ≈ 0.044), per D1894b. The superseded value 0.090 (D1895/D1908) is reported as a secondary line only. Planning knowledge declared: the main Loom's readings 1e-5 / 0.010–0.075 / 0.024–0.2 (2206.04313, 2304.14437, 2310.15604) and its D1908a INDETERMINATE.

## Bearings (selection rule fixed here)
- A bearing is a source (paper, framework or code path) that reports a displacement of a modulus from an elliptic fixed point (ω/ρ for the main test, i for the mirror) PRODUCED by a stabilisation/uplift/radiative mechanism. Values that data fits REQUIRE are needs, not bearings, and are excluded (they may be listed as context).
- Every source I open that meets the rule is included (no dropping after reading). Minimum 5, maximum 8 per side. Each source must be opened this tick.
- Likelihood per bearing: Gaussian in x = log10|δτ|, centre = log-centre (geometric mean) of the reported range (or the single reported value), σ = max(half-width of the reported range in dex, 0.20 dex); a single "typical/preferred" value with no range gets σ = 0.50 dex. **σ ×2 if the framework is not IIB with magnetised D7-branes on a toroidal orbifold** (heterotic, bottom-up, F-theory generic, etc.).
- Prior: uniform in x on [−7, 0].

## Combiners (all three reported)
1. Gaussian product (posterior Gaussian in x).
2. Student-t (ν = 3) product, evaluated on a grid.
3. **PRIMARY: good-or-bad mixture**: each bearing is good with prior probability 0.8 (likelihood as above) or bad (uniform on [−7, 0]). Report each bearing's posterior good-probability.
Per combiner: posterior median, 68 % and 95 % equal-tail intervals. Weights: inverse-variance fractions (Gaussian) and good-probabilities (mixture).
Consistency: χ² of the bearings about the Gaussian weighted mean (dof N−1, p-value); Bayes factor BF = Z(one common value) / Z(each its own value), same prior.

## Verdict (same bars as the Loom)
On the PRIMARY median m: **PASS** if 0.0457 is within ×1.5 of m; **PARTIAL** if within ×3; **FAIL** otherwise. Also report whether 0.0457 lies in the 68 % / 95 % interval. If the Gaussian or Student-t combiner gives a different category, the verdict is labelled **FRAGILE** (reported, not changed). 3-point fix compared: the main Loom's log-centres 1e-5 / 0.027 / 0.069 → median 0.027.

## Mirror (SERAPIS twin ladder; counts only if both sides pass at the centre)
Mirror quantity: the displacement δ_i of the dark-cycle/thread modulus off τ = i produced by the same class of mechanisms (near-i bearings, same rules). Mirror need: the Z₂ protection of α at i (D1853) needs the field within d < 4.2e-3 M_P of the knot; with K = −n ln(−i(τ−τ̄)) at Im τ = 1 the canonical distance is d = √(n/2)|δτ|, so **|δ_i| < 5.9e-3 (n = 1, the D1902 thread factor)** (3.4e-3 for n = 3, reported).
Mirror verdict on the primary posterior median of δ_i: PASS if ≤ 5.9e-3; PARTIAL if ≤ ×3 above; FAIL otherwise. If fewer than 5 near-i bearings are found, the mirror uses those found and is labelled THIN.
Centre balance: test 1 COUNTS only if forward and mirror both PASS. A universal mechanism that must move ρ by ~0.05 and i by < 0.006 is recorded as a **tension** whatever the separate verdicts.
Script and results: field_tests/mirror/. Notes: theory/pending_docs/LOOM_MIRROR_NOTES.md. Tolerances never loosened; no reruns to chase.
