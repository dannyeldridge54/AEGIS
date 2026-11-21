# PREREG D1938 — the S–T seam test (Danny 16:50: parent equation or fundamental split? Locked 21 Nov 2026 before running; repo at b1c952d7)
Source: Conlon–Palti, arXiv:0901.4350, §5.2.1. The untwisted D3–D7 running is "gauge-group universal" (Eqs. 194, 231). Matching to the Kaplunovsky–Louis formula needs Re S → Re S − (2/9)(1/16π²) n₇ ln 𝒱, which the authors reject as non-local; they "were unable to match onto the KL field theory formula".
Test: theory/tests/d1938_seam.py, with three readings of the S–T term:
- (a) the Conlon–Palti universal D7 running;
- (b) their KL-matching dilaton shift through f_vis = T + 9S;
- (c) the raised matching scale M_X.
Each reading is the shift in Δ₃ (non-universal part only), at 𝒱 = 4.0e4.
**PASS:** all three supply Δ₃ shifts in [0.022, 0.066] (+0.044 ± 50 %). This would mean the parent-equation form fixes the seam. **FAIL** otherwise: the seam then needs a hand-added non-universal term, which reads as a fundamental split.
Field tag: S–T. Prior expectation, written before running: every term is universal on one visible stack, so FAIL.
