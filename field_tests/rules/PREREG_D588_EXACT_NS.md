# PREREG D588: exact background + Mukhanov–Sasaki n_s and r (follows the D587 self-check failure), locked before computing

Models (along Re τ = 0, α = 1/3, φ = ln(y)/√2):
- two-term SERAPIS with ε = 1.0e-4 and 1.3e-4;
- HS-Kairos (ε = 0, p = 2).

Background:
- Exact φ″ + (3 − ε₁)(φ′ + V_φ/V) = 0 in e-folds, from y = 80 (slow-roll initial velocity), to ε₁ = 1.
- N* is counted EXACTLY back from the end. Values: N* ∈ {49, 51} (the D578/D581 range).

Perturbations:
- R″ + (3 − ε₁ + ε₂)R′ + (k/aH)²R = 0 and h″ + (3 − ε₁)h′ + (k/aH)²h = 0.
- Bunch–Davies initial conditions at k/aH = 200. Evaluate when k/aH = 1e-3.
- P_R = k³|R|²/2π² and P_t = 8k³|v_t|²/(2π²a²), with h = 2v_t/a (two polarisations).
- n_s from ln P_R at k*·e^{±0.05}; r = P_t/P_R at k*.
- Validation: the code must reproduce the analytic α = 1/3 attractor trend (n_s within 0.002 of 1 − 2/N* for HS-Kairos).

Report per model and N*:
- exact y*; MS n_s and r;
- the old slow-roll-count values at the same nominal N* (D575/D581 code) and the difference;
- σ vs SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027).
D588 numbers supersede the slow-roll-count numbers for all FUTURE use. Earlier locked notes are not edited; this is a correction note. Fixes go in PREREG_D588_DEVIATIONS.md, written first.
