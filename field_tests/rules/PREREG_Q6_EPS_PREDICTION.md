# PREREG Q6 — does the SUGRA (m,0) CP-violating minimum (2201.02020) land where the near-ω A4 quark fits (2212.13336) need τ? (locked 2026-11-20, before computing)
Convention (2212.13336 Eq. 34): τ = ω + ε, ω = e^{2πi/3}; u = (τ−ω)/(τ−ω²), ε ≃ i√3 u.
Prediction: u(m) = |u|min e^{−i2π/9}, |u|min = 0.0145/(m + 0.0625), m = 1..7; cross-check with the listed minima τ = −0.484+0.884i (m=1), −0.492+0.875i (m=2), −0.495+0.872i (m=3) (exact ε = τ − ω), choosing the CP image in the same quadrant as the fits.
Targets: fit A (masses only) ε = 0.03188+0.02151i; fit B (masses+CKM, real g) 0.01779+0.02926i; fit C (complex g_d) 0.00318+0.02792i; band |ε| ∈ [0.028, 0.038].
Rules (fits carry no errors, so a fixed tolerance is set now):
- MAG PASS if some m gives |ε| inside the band [0.028, 0.038].
- POINT PASS if some m gives |ε_pred − ε_fit| ≤ 0.25 |ε_fit| for fit B or C (the CKM-including fits).
- Report arg ε predicted vs fits (no pass rule; descriptive).
Overall: PREDICTION SUPPORTED only if both MAG and POINT pass. No reruns; no new m or tolerance afterwards.
