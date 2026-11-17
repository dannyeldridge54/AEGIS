# PREREG L8 — Janus-LT self-consistency with the Planck 2018 distance priors (Chen, Huang & Wang 2019)
Locked 2026-11-17 before any L8 number. Source (fetched, ar5iv 1808.05724): l_A = (1+z*)πD_A(z*)/r_s(z*) (Eq. 1), R = (1+z*)D_A(z*)√(Ω_m H0²)/c
(Eq. 2); Table 1 (TT,TE,EE+lowE, flat ΛCDM): R = 1.7502 ± 0.0046, l_A = 301.471 ± 0.0895, ω_b = 0.02236 ± 0.00015 (n_s dropped —
background only), correlations R–l_A 0.46, R–ω_b −0.66, l_A–ω_b −0.33. z* by Hu–Sugiyama with g₁ prefactor as printed in the TEXT
(0.0738) — the paper's code listing says 0.0783; both are run and reported (z* option "HS-text", "HS-code"); also Janus-LT's own
recombination z* (τ = 1, Recomb) as option "own".
Fit: flat ΛCDM, mν = 0.06 eV (one massive state), N_eff 3.044, free (h, ω_b, ω_c); minimise χ² for each z* option.
Claim (self-consistency: a ΛCDM fit to a prior derived from ΛCDM must sit near its centre): for "HS-code" (the code the
authors ran) χ²_min ≤ 1 → CONSISTENT, else INCONSISTENT. Other options and the fitted h, Ω_m reported only.
Results: field_tests/results/janus_lt_l8_priors.txt.
