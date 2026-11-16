# Exactness audit of papers/v3/serapis_v3.tex (A2; D812, 16 Nov 2026)
Method key: MS = exact Mukhanov–Sasaki via spectra() (exact_ns_d588 family); SR1 = first-order slow roll (1−6ε+2η, 16ε); A = analytic/closed form; I = interpolated; E = estimate.

| # | Paper number | Source | Method | Status |
|---|---|---|---|---|
| 1 | Kairos n_s 0.959–0.961, r 3.3–3.7e-4 | D637 | MS | ok |
| 2 | Chronos n_s 0.970–0.975, r 4.8–5.7e-4 (frozen, lock D605) | D602 → D605 | SR1 (lock) | frozen as locked; MS consistency via D642 at N* 46–49; ok as a frozen number |
| 3 | Chronos α_s −(8.8–10.2)e-4 | D642 | MS | ok |
| 4 | Consistency relation "~2%" (abstract) / 11–13% bias | D635, D639 | A vs MS | ok (bias-removed form) |
| 5 | Caps n_s ≤ 0.9836/0.9844, r ≤ 8.2/8.3e-4 | D674, D676 | MS | ok |
| 6 | Strip width ≤ 21% | D678 | MS | ok |
| 7 | β_s −(3.0–4.6)e-5 | D666 | MS | ok |
| 8 | Chronos at corrected T_R: n_s 0.9720–0.9765, r 4.6–4.9e-4 | D729 | SR1 | **FLAG: recompute MS** |
| 9 | "meets the band only for ε ≈ 1.40–1.46e-4", n_s 0.974–0.975 | D729 | I of SR1 | **FLAG (after 8)** |
| 10 | instant reheating → n_s ≈ 0.976–0.98, y* > 25 | — | E | flag: low priority (an argument, not a prediction) |
| 11 | SERAPIS-ρ n_s 0.969–0.972, r 4.6–5.1e-4 (frozen, lock D615) | D613 | SR1 (lock) | frozen as locked; **FLAG: MS consistency check** |
| 12 | SERAPIS-ρ α_s −(8.5–9.5)e-4 | D634 | MS | ok |
| 13 | ρ doublet-only n_s 0.9735–0.9749 | D722 | ? (not verified) | **FLAG: check method** |
| 14 | ρ 2⊕1: n_s 0.9729–0.9736, r 4.66–4.75e-4 | D725/D814 | MS (D814) | ok |
| 15 | SERAPIS-E at n_s 0.970, r 4.75e-4; untilted 0.961 / 3.6e-4 | D692 | MS | ok |
| 16 | SERAPIS-E frozen band (lock D693) | D692/D693 | MS | ok |
| 17 | F-term-tilt alternative n_s 0.968–0.973, α_s −(2.4–4.5)e-3 | D684 | SR1 | flag: low priority (rejected candidate) |
| 18 | Log-derivative plateau | D758 | SR1 | to be retired (queue 8) |
| 19 | Self-diluted ρ: n_s 0.967–0.970, r 5.1–5.6e-4 | D781/D793 | SR1 (was MISLABELLED "exact spectra") | MS done D813: 0.9664–0.9699, r 5.20–5.66e-4 ✓ |
| 20 | "Detecting r ≈ 5e-4 requires σ(r) ~ 1e-4, beyond planned experiments" | — | — | **FLAG: inconsistent with prediction_sheet (LiteBIRD σ(r) ≈ 5e-5 optimistic → ~10σ); check the literature** |

Priority for recomputation (one per tick, locked, MS via spectra()): 19 → 14 → 8/9 → 11 → 13 → 20 (literature) → 17/10.
