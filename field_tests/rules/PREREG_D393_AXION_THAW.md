# PREREG D393 — Twist-2 sector II: can one thawing axion give DESI's w0, wa AND the birefringence angle? (locked 13:30 CT 14 Nov 2026)

Script: theory/twist2/axion_thaw_d393.py. Model: canonical axion, V = L4 (1 + cos(φ/f)), plus matter (Ω_m = 0.31) and radiation
(Ω_r = 9.1×10⁻⁵), flat, M_P = H0 = 1; start a = 10⁻⁴ at rest at φ = θ_i f; L4 shot so H(a = 1) = 1. Grid: f ∈ {0.1, 0.3, 1} M_P,
θ_i ∈ {0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}. Outputs: CPL fit (w0, wa) of w(a) over a ∈ [1/3, 1]; Ω_DE; Δθ between z = 1089 and
today; β = 0.42° (c_γ/2π)|Δθ| for c_γ ∈ {1, 10, 20} (relation from arXiv:2504.17638).
Targets (arXiv:2511.22512 CPL, CMB+DESI+SNe): PantheonPlus w0 = −0.833 ± 0.055, wa = −0.65 ± 0.20; DESY5 w0 = −0.749 ± 0.057,
wa = −0.88 (+0.23/−0.19). Birefringence: β = 0.261 ± 0.061° (Planck+ACT naive combination, 2504.17638).
Statistic and reading:
- PASS(PantheonPlus) if some grid point has w0 within 1σ AND wa within 2σ of the PantheonPlus values AND, at that point, β for some
  c_γ ∈ {1, 10, 20} lies within 2σ of 0.261°. Same test reported for DESY5.
- PARTIAL if w0 and wa pass but no c_γ in the set gives β (i.e. birefringence needs a non-listed coupling).
- FAIL otherwise; report the closest point and which quantity fails (expected risk: thawing fields give wa ≈ −1.6 (1 + w0), shallower
  than the CPL fits).
Cross-sector: does not test n_s, matter genesis or the decay-constant obstacle (D392); f is taken as given (alignment assumed).
Not a likelihood fit; grid comparison only. No reruns; fixes via a DEVIATIONS file written first.
