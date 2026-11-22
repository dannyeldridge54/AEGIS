# Loom engine loop: engineering notes (D2027, 22 Nov 2026)
**Danny 00:58:** "One basic setup that can handle a whole bunch of different things … one for an outward build, the other for pulling inward or compressing."

## The one setup: description length
- **Every domain reports bits.**
  - **Inward, the Forge:** bits = 8 × compressed bytes. This is an online, prequential code.
  - **Outward, the Bloom:** bits = −lnL/ln2 + (k/2)·log₂N. This is a two-part code: the data given the theory, plus the theory's fitted knobs.
- **This is the minimum description length (MDL) principle.** It is established mathematics (Rissanen; Grünwald's tutorial, math/0406077). BIC is its large-N form.
- **Same rule both ways.** The same Centre tunes either domain. A knob stays only if it shortens the total description on held-out data. The Forge's −0.38% and the Bloom's "lnL − BIC" are the same kind of number.
- **Code:** `tools/loom/loom_engine.py`, with `BloomDomain` and `ForgeDomain` (the Forge adapter is not run while the Forge is paused).

## Engine optimisation ladder (to null)
| rung | change | wall time per Bloom run | gain |
|---|---|---|---|
| 0 | pure-Python bootstrap, 20k toys | ~0.13 s | — |
| 1 | numpy-vectorised toys | ~0.15 s | none: the numpy import (63 ms) ate the gain |
| 2 | exact χ² survival function (regularised upper gamma); toys only with `--toys` | **0.032 s** | ×4 |
| 3 | what remains is Python start-up (~25 ms) | — | **NULL**: under 5% is possible. Stop. |

Cross-check: exact p = 8.35e-4; toys p = 8.5e-4; the dof-4 closed form gives 8.34e-4 at χ² = 18.87.

## Improvements found while building
1. **Step size per knob.** loomcore's octave/fifth (×2, ×1.5) cannot move a theory value that needs ×1.033. Each domain now gives its own step ladder (Bloom: ×1.1 → 1.03 → 1.01 → 1.003).
   - Free α_s what-if: 30.3 → 19.5 bits even after its knob cost. A tuned seam "pays", so the label rule (**FIT**, never derived) is what protects us, not the penalty.
2. **Prequential = post-lock evidence.** Online coding (the Forge) scores each byte before it is seen. For the Bloom that means each dataset is scored only after its prediction is locked: gap E1, strict evidence.
   - Next: every term gets `locked` and `released` dates, and the Bloom reports a prequential description length over post-lock terms (currently 0 terms).
3. **The theory-error lens** (GAMBIT practice: float the theory errors and test sensitivity). The α_s failure is ladder-unconverged (see D2026).
4. **The Jacobian lens** (still owed): the rank-1 link Δ₃ → m₃/₂ → wino, so a T1 move also prices T2.

## Lenses: how much fits one setup (broad search)
Anything that can be written as "data + model → bits" plugs in:
- **Ramsey:** bits = log₂(remaining search cases), or a certificate length. Closing a case = describing it in 0 bits beyond the proof.
- **CubeMind:** curriculum items are scored by how much they shorten its description of the data. This is the "understanding is compression" view (arXiv 2407.07723).
- **Mersenne:** a trial-factor depth vs the bits it removes from candidate space.
- Bits-back / variational coding (arXiv 1901.04866) is the bridge to latent-variable models: the theory's hidden fields would cost bits only for what they explain.

## Compressor sidebar (saved for when the Forge resumes; none tested)
- From cmix-obias:
  - a byte-LSTM mixer;
  - a PPMd prior gated at g = 0.15;
  - an offline-trained correction head (23 kB);
  - PGO + LTO builds.
- From StateSMix: entropy-adaptive weighting (scale by model confidence); bounded linear probing.
- From GLN: halfspace-gated weight sets. loomz19's HG is a first try; at 200 kB it was worse (+0.14%), so test it on the 3 MB rung.
- D2025 is locked and waiting (SKIP + RCTX; −0.38% on the sanity slice).
