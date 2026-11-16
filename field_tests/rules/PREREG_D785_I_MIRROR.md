# PREREG D785: the residual-symmetry check at τ = i (mirror of D777–D780)
Locked 2026-11-16 before computing. Script: theory/modular/i_mirror_d785.py. Output: field_tests/results/i_mirror_d785.txt.
Γ₂ ≅ S₃ weight-2 doublet from the q-series (S₃ basis of 1803.10391; from memory, checked by K4): Y₁ = 1/8 + 3q + 3q² + 12q³ + 3q⁴ + 18q⁵, Y₂ = √3·q^{1/2}(1 + 4q + 6q² + 8q³ + 13q⁴), q = e^{2πiτ}.
K4: at ρ, Y₂/Y₁ = i within 1e-3 (D720's direction).
At τ = i, with the same weight-2-only structures as D777:
- M_R = [[A(Y), cY], [cYᵀ, 0]], c ∈ {0.6, 1, 3};
- M_D = [[A(Y), βY], [γYᵀ, 0]], with complex β, γ on the D777 grid.
Report:
(a) the singular values of M_R, and whether the inflaton's decay pair (the degenerate pair, D725/D727) is present;
(b) the coupling of each heavy Takagi eigenstate to leptons: the column norms of M_D·U_R (U_R Takagi of M_R), min/max over the grid;
(c) the light spectrum: the fraction of grid points with an exactly degenerate pair (relative gap < 1e-9), and the NO/IO counts as in D777.
Decision:
- τ = i is UNAFFECTED if (b) shows non-zero couplings for every heavy state AND (c) shows non-degenerate spectra with some NO/IO points.
- Otherwise CORRECTION.
