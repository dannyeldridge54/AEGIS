# PREREG D896 (R2.2b): ρ lepton-sector lift ε with the corrected m_ν₁ target (D880a/D895)
Locked before computing, 2026-11-16.
Reason: D895 corrected ρ's LH_u AD window to m_ν₁ = 2e-11–9e-10 eV (D880's 4e-9–7e-8 eV was wrong). D883's lift ε was bisected to the old window's middle (1.7e-8 eV); D883's script and result stay unchanged as a record.
Method: identical to PREREG_D883 (model, seed 883, 20,000 draws, coupling and mass priors, pass window for Δm²₂₁/Δm²₃₁, scale fit) in a copied script theory/modular/rho_osc_d896.py; only the bisection target changes, to m_ν₁ = √(2e-11·9e-10) = 1.34e-10 eV. Also report the ε range covering the whole window (ε at 2e-11 and at 9e-10 eV, medians).
Verdict rule (same as D883): "natural" if pass fraction ≥ 1% and median ε in [1e-4, 1e-2]; "tuned" otherwise.
Prediction (pre-stated): pass fraction 3.5% (unchanged, it does not depend on the target); median ε ≈ 1.6e-4 (scaling ε ∝ √m_ν₁ from D883), i.e. "natural" at the lower edge.
