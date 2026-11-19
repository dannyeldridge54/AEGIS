# PREREG D1380 — where do parity-shifted Epstein sums have their minima? (P3 dilemma, D1379 option ii)

Locked 2026-11-18 before computing (Danny "Djl", P3 hunt).

Sums (U = x + iy, s = 2, all over integer pairs (m,n) ≠ (0,0) unless stated):
  S0 = Σ' y²/|m+nU|⁴                      (= E(U,2), control; must give min at ρ = e^{iπ/3}, E = 5.78336)
  Sa = Σ' (−1)^m y²/|m+nU|⁴
  Sb = Σ' (−1)^n y²/|m+nU|⁴
  Sc = Σ' (−1)^{m+n} y²/|m+nU|⁴
  Sh = Σ_{m∈Z+½, n∈Z} y²/|m+nU|⁴          (half-shifted momentum lattice)
Method: truncated sums |m|,|n| ≤ 60 on a grid x ∈ [−0.5, 0.5] (step 0.0125), y ∈ [0.15, 3] (step 0.0125); the grid minimum is refined
with Nelder–Mead at |m|,|n| ≤ 300. Report the global minimum point and value of each sum in the box, and the value at ρ.
Gate: S0 must have its minimum at ρ (|U − ρ| < 2e-3 or its x → −x image) and value 5.7834 ± 2e-3; else nothing else is read.
Rule: a shifted sum "keeps the hexagon" if its box minimum lies within 2e-3 of ρ, ρ − 1 or −ρ̄ ... i.e. of any point
γ(ρ), γ ∈ SL(2,Z), inside the box; otherwise "vacuum moves" and the minimum location is recorded. A sum unbounded below
in the box (minimum on the box edge y = 0.15) is reported as "no interior minimum".
No reruns to chase results; fixes only via PREREG_D1380_DEVIATIONS.md written first.
