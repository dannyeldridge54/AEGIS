# PREREG D1381 — mixed unshifted+shifted sectors: does S0 + c·Sa keep an interior minimum at a hexagon point? (D1380 caveat)

Locked 2026-11-18 before computing (Danny "Djl", P3 hunt).

Identity used (derived now, checked numerically in the script at 3 points to 1e-6 against direct sums N = 300):
  Σ_{m even} = E(U/2,2)/4,  Σ_{m odd} = E(U,2) − E(U/2,2)/4  ⇒  F_c(U) ≡ S0 + c·Sa = (1 − c)·E(U,2) + (c/2)·E(U/2,2)
  (E via tools/serapis_calc/shapes.py, Chowla–Selberg). F_c is Γ₀(2)-type invariant (T-periodicity 1 lost? no: U/2 → U/2 + ½,
  so period 2 in x; box covers x ∈ [−1, 1]).
c ∈ {0 (control), −1, −0.5, 0.5, 1}. Grid x ∈ [−1, 1] step 0.01, y ∈ [0.2, 3] step 0.01; refine minimum with Nelder–Mead.
Gate: c = 0 must give min value 5.7834 ± 2e-3 at a point γ(ρ), γ ∈ SL(2,Z) (y ∈ {√3/2, √3/6, …}, x ∈ ½ + Z or ±½ for y = √3/6).
Rule per c: "interior minimum" if the refined min is not on the box edge (y = 0.2 or 3, x = ±1 excluded as periodic copy);
"hexagon kept" if it is within 2e-3 of an SL(2,Z) image of ρ; else record location ("vacuum moves") or "runaway".
No reruns to chase results; fixes only via PREREG_D1381_DEVIATIONS.md written first.
