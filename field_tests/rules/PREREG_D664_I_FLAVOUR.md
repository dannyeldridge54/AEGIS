# PREREG D664: τ = i covariant completion with Γ2 ≅ S3 flavour multiplets — do matter parity and neutrino masses coexist?
Locked before computation, 2026-11-15. Script theory/modular/i_flavour_d664.py (reuses D597's verified Γ2 weight-2 doublet Yd verbatim); output results/i_flavour_d664.txt.
Set-up: centre matter parity (D663): odd weights for leptons, even for Higgs: k_L = k_N = 1, k_Hu = 0. η^{-2} rule: each coupling = η^{-2}·h, h a Γ2 modular form of weight Σk. Analytic: −I ∈ Γ(2), so Γ2 representations carry ρ(−I) = 1 and the centre parity is unchanged by the flavour structure.
Compute at τ = i:
(a) Weinberg operator with L a Γ2 doublet: Σk = 2 → h = weight-2 doublet Y; S3 contraction (L L)_2·Y gives M_ν ∝ A(Y) = [[Y2, Y1],[Y1, −Y2]] (D597 convention). Report Y(i), the singular values of A(Y(i)).
(b) Three generations as 2 ⊕ 1 (L3 singlet, k = 1): L3 L3 needs a weight-2 singlet (none for Γ2 → entry 0); L_doublet·L3 couples to Y via 2⊗1 → 2 contracted with Y (entries Y1, Y2 times a free coefficient b). Report the singular values of the 3×3 matrix for b ∈ {0.3, 1, 3} and whether one vanishes.
(c) Majorana mass for N as a Γ2 doublet (k_N = 1, Σk = 2): M_N ∝ A(Y(i)); report singular values (non-zero ⇒ allowed).
Verdict: non-zero rank-2 (or 3) mass matrices at i ⇒ with Γ2 doublets the τ = i covariant completion keeps both centre matter parity and neutrino masses. Any exactly vanishing eigenvalue is reported as a structural prediction (estimate-level: tree level, before corrections).
