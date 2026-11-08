# Theory note v3 (Zenodo, same concept record 10.5281/zenodo.23898708): plan

**Status:** prepared 8 Nov 2026; publishes only on Danny's word, as v1 and v2 did. Built from
`cubemind/zenodo/spiral_note/spiral_twist_note_v2.tex` (same sections), adding what happened 3–8 Nov.
Verdicts marked ⟨…⟩ are filled from the locked scorers' output only; nothing is written before the result exists.

## Changes from v2, section by section

1. **Status** — v2 plus: Nieh–Yan chosen over Holst (7 Nov, FP cannot yet tell them apart); width F = 1.559 from
   Nieh–Yan at the Planck length (TF-P supported); n = 3 vs n = 2 (n = 3 favoured), n = 1 ⟨deferred / result⟩.
2. **Geometry** — unchanged algebra; add the convention map to the Axiodilaton (arXiv:2512.13544): ζ = −λ/2, so our
   λ = −2√(2/3) is their no-scale √(2/3); their |ζ| ≲ 0.05 bounds the dark-matter coupling, ours is β = √(2/3)·f.
3. **Validation** — add the two-field CAMB module (λ = 0 limit matches EarlyQuintessence to 2×10⁻⁵; gates G1–G3) and
   the light-angle AxiCLASS build (code identity 2×10⁻⁸; gate G-L within 0.03).
4. **One field for both jobs** (new) — UB-1 (passes only with an extra slope), UB-1b (fails by 0.038), UB-2 against
   data (vs ΛCDM MIXED, vs w0–wa NOT COMPETITIVE, DOES NOT UNIFY), UB-P predictions locked blind (MIXED: 1, 3, 4 of 5).
   Interpretation with Giarè & Sakstein (no steeper middle phase, no drain).
5. **Weak lensing** (new) — S8-WL Part 1 (DES Y6 NLA 0.798; TATT 0.783 also stated); Part 2 full DES Y3: Locked Twist
   +1.14 PASSES, Spiral +2.57 / +3.47 / +3.99 OVER, UB-2 −0.37 / 0.00 / +0.14 PASSES; survey split (DES-driven,
   KiDS-Legacy mild); S8-J ⟨verdict, deltas, lensing cost⟩; S8-L light angle ⟨verdict, mass, penalties⟩.
6. **Quantum side** (new) — Nieh–Yan instantons give a cosine (Kaul & Sengupta), not n = 3; instanton-action target
   S ≈ 240 for the S8-L mass window; starting-angle tension (≈0.03 rad late share vs 2.4–2.8 rad early).
7. **Predictions locked before the data** — v2's list plus every rule locked since, each with its SHA-256 and time
   (PREREG_UNIFY_BG, _1B, _DATA, UB2_PREDICTIONS, S8_WL, S8_JOINT, SPIRAL_L, POWER_N1 if locked).
8. **How to falsify** — v2 plus: S8-L's mass must sit inside the Rogers et al. window and survive Lyman-α; a measured
   field-space curvature far from √(2/3) in an axion–dilaton fit with a sub-dominant axion would contradict λ.
9. **Deviations** — every deviation logged since v2 (UB-1 D1/D2/D1b-1, S8J-D1..D3, ...), at full size.

## Supplement zip
Scripts and result JSONs behind every number above (scorers, gates, fit drivers, the two engine patches), with md5s
checked against the repo before upload, as in v2.

## Before publishing (checklist)
- [ ] S8-J and S8-L scored; Part 2 reruns done or marked pending.
- [ ] All ⟨…⟩ filled from scorer output; no number typed by hand.
- [ ] PDF built and read through once.
- [ ] Danny's word to publish.
