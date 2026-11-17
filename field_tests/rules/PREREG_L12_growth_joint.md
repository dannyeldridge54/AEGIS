# PREREG L12 — L7 (BAO + compressed CMB + Pantheon+) + DESI DR1 full-shape fσ8 ratios, w0waCDM, with a Planck A_s prior
Locked 2026-11-17 before any L12 number. Likelihood = L7's χ² (unchanged) + χ²_fσ8 + ((ln10¹⁰A_s − 3.044)/0.014)².
A_s prior: Planck 2018 VI Table 2, TT,TE,EE+lowE+lensing, ln(10¹⁰A_s) = 3.044 ± 0.014, n_s fixed at 0.9649 (same table) — APPROXIMATION: those values come
from a ΛCDM fit and are used here in w0waCDM (labelled in the result).
fσ8 data: the six DESI DR1 full-shape ratios to the DESI fiducial used in L9/L9v2 (theory/janus_lt/l9_fs8.py: rat, sig, redshifts z).
Model: fσ8(z) = f(z)·σ8·D(z)/D(0), with growth from the scale-independent equation (tools/janus_lt/growth.py form) using a matter + dark-energy E(a) without
radiation (the L9c fix), σ8 from L9c's EH98 + A_s machinery rescaled by D₀(w0wa)/D₀(ΛCDM) (both matter-dominated-normalised). Prediction = ratio to the same
machinery evaluated at the DESI/Planck fiducial (h 0.6736, ω_b 0.02237, ω_c 0.1200, ΛCDM, same A_s), so shared systematics cancel.
Free: w0, wa, h, ω_b, ω_bc, ln10¹⁰A_s (Nelder–Mead, 3 starts).
Claims: C1 joint w0 and wa each within 1 σ_L7 of L7's MAP (−0.853 ± 0.053, −0.518 ± 0.200); C2 χ²_fσ8 at the joint MAP ≤ 12.59 (6 points, 95%).
Both → GROWTH CONSISTENT WITH THE BACKGROUND FIT. Also reported: Δχ² ΛCDM vs w0waCDM (L7 alone: 7.70). Results: field_tests/results/janus_lt_l12_growth.txt.
