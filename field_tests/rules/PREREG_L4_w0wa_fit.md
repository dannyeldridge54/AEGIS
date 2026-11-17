# PREREG L4 — w0–wa from Janus-LT with DESI DR2 BAO + DESI's compressed CMB prior (data/desi/*.txt)
Locked 2026-11-17 before any L4 number.
Model: flat w0waCDM, Σm_ν = 0.06 eV (one massive state, L0c), N_eff = 3.044; parameters (w0, wa, h, ω_b, ω_bc).
θ* = r_s(z*)/D_M(z*) with z* and the drag-epoch r_d from Janus-LT's own recombination; because recombination depends on
(ω_b, ω_bc) and not on h or dark energy at the 1e-4 level, z* and z_d are tabulated on a 5×5 grid in (ω_b, ω_bc) around the
prior means (±4σ) and interpolated (cubic); the interpolation error is checked at 3 off-grid points (must be ≤ 1e-4 in z).
χ² = BAO (L3) + compressed CMB (Gaussian, A1–A2). Fits: ΛCDM (w0 = −1, wa = 0) and w0waCDM, by minimisation (Nelder–Mead,
several starts). Report best-fit (MAP) w0, wa, Δχ² = χ²_w0wa − χ²_ΛCDM, and the Laplace (Hessian) errors.
Comparison target (DESI+full-CMB, Eq. 25): w0 = −0.42 ± 0.21, wa = −1.75 ± 0.58, Δχ²_MAP = −12.5.
Pass (CONSISTENT) if |w0 − (−0.42)| ≤ 0.21 and |wa − (−1.75)| ≤ 0.58 and Δχ² within ±4 of −12.5 (compressed vs full CMB and
MAP vs posterior mean differ; tolerances set at 1σ in advance). Otherwise report as INCONSISTENT with numbers.
