# PREREG TK2 — SERAPIS late universe through the upgraded Hyperion / Janus-LT (U4): DESI DR2 BAO + DESI compressed CMB
Locked before running. Method = L4/L5 exactly (theory/janus_lt/l4_w0wa.py, l5_serapis_late.py: 5×5 (ω_b, ω_bc) recombination grid with bicubic interpolation, Nelder–Mead over (h, ω_b, ω_bc), same data files), now with U4's recombination.
SERAPIS late universe = ΛCDM with Σm_ν = 0.05878 eV (NuFIT 6.0 NO floor, D1234). Comparison model: w0waCDM with the same Σm_ν.
T1 reproduction: ΛCDM χ² at Σm_ν 0.05878 within 0.05 of L5's 15.32 (at 0.0587).
T2 report: Δχ² = χ²(w0wa) − χ²(SERAPIS ΛCDM) and its Gaussian-equivalent significance for 2 extra parameters; (w0, wa) MAP. No pass/fail on T2 (consistency report; data predate the freeze).
T3 speed: whole script ≤ 120 s (L4/L5 took ~240 s).
Results: field_tests/results/tk2_serapis_late.txt.
