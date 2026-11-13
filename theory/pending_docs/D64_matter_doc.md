## Development 64 — The theory wants β = 0: the small coupling is not explained (13 Nov 08:25)

**Question.** The headline late-time fit (K816) needs a dark-matter coupling β ≈ 0.03. Can the base theory give it?

**Calculation.** In the code, m_DM ∝ e^{βφ}. In no-scale supergravity a matter field's mass depends on the size x through its modular weight n: m ∝ x^{n − 3/2}, i.e. β = √(2/3)(n − 3/2).

| modular weight n | β |
|---|---|
| 0 | −1.22 |
| 1 | −0.41 |
| **3/2 (or a sequestered sector)** | **0** |
| 2 | +0.41 |
| 3 | +1.22 |

The fitted β = 0.030–0.034 needs n = 1.537–1.542 — not a natural weight. Natural values give either β = 0 or |β| ≥ 0.41, and the large ones are excluded by the data.

**A second, stronger argument.** D58 made the dark matter a fermion that interacts *only through gravity*. Any dependence of its mass on the twist field is a non-gravitational coupling, so gravity-only dark matter means **β = 0 exactly**.

**Crossroads.**
- **A. Theory's own prediction: PURE-TWIST (β = 0).** Consistent with gravity-only dark matter; zero extra parameters; PREFERRED on the compressed likelihood, −3.85 on full Planck PR4, HOLDS on DES-Dovekie, STRAINED on DES Y5 and Union3.
- **B. K816 (β ≈ 0.03 fitted).** Holds on DES Y5 and Union3, but the coupling has no origin in the theory and contradicts gravity-only dark matter.
- **C. Look for a mechanism for small β** (e.g. a loop-induced coupling, or the dark matter's mass coming partly from a sector with weight near 3/2). Open; nothing found.

**Route taken: A for the theory, with B reported as the data's preference.** Why: a prediction must come from the theory, and the theory as built gives β = 0. This revises D61: K816 is not the theory's headline; it is a phenomenological extension that the supernova data mildly prefer (by 1.6–2.0 in χ² over PURE-TWIST, for one extra parameter). Stated plainly: if future data demand β ≈ 0.03, the dark-matter sector of the Twist needs rethinking. Code: theory/darkenergy/beta_origin.py.
