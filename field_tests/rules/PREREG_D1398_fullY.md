# PREREG D1398 — the full universal threshold Y as the plateau function (D1397 rescue) through the SERAPIS pipeline

Locked 2026-11-18 before computing (Danny "Djl", P3 hunt).

Model (KKPR + D1394 structure, constant uplift p = 0): L(U) = s + Y(T,U)/16π², Re T = 0, path Re U = ½, kinetic n = 1 (pipeline default).
Y by its two large-modulus expansions (exponential corrections dropped; C¹-matched at U₂ = T₂ to 0.1% — checked before locking):
  U₂ ≤ T₂: Y = 6πT₂ + (90/π³)E(U,2)/T₂;   U₂ > T₂: Y = 6πU₂ + (90/π³)E(iT₂,2)/U₂.
V ∝ (1 − L_ρ/L)(1 + C·κ(L − L_ρ)) is produced by the unchanged pipeline with E_paper → κ·L (κ = 10) and λ = 1/(κL_ρ)
(e/(e+1) = 1 − L_ρ/L; tilt C·e/λ = Cκ(L − L_ρ); κ only moves the pipeline's start point inside its y-grid).
Scan: T₂ ∈ {4, 16}, s = 1, C ∈ {0, 1e-4, 1e-3}; T_R = 8.94e8. Engine pipeline.predict (exact spectra).
Report n_s, r, α_s, N* per run and whether in the frozen band (n_s 0.969–0.975, r 4.55–5.7e-4).
Also report y* (Im U at horizon exit) to check the chamber used at horizon exit.
Rule: "full-Y plateau viable (scan)" if ≥ 1 run in band; else "not viable on this scan" with the closest point recorded. Also
check: the vacuum of L is at ρ (L(ρ) < L(i)) — stated, computed in script.
No reruns to chase results; fixes only via PREREG_D1398_DEVIATIONS.md written first.
