# PREREG NA1 — node audit, phase 1: the SERAPIS-E chain (serapis_e → nstar_e → band_e, caps), recomputed through the Janus app on Danny's PC
Locked 2026-11-17 20:10 CT before any NA1 number. Purpose (Danny 20:05 CT): map every current node with an arithmetic/derivation recheck; phase 1 = the frozen
SERAPIS-E band, because every downstream node leans on it. No fixes during the audit; mismatches are recorded and flagged on the ladder.
Frozen claims under test (PREREG_D693_SERAPIS_E_FROZEN, D693/D725/D962): n_s 0.970–0.975; r (4.55–5.12)e-4; α_s −(9.4–10.6)e-4; for C = (1.0–1.3)e-6 and N* 48.4–49.9;
corrected N* bracket (nstar_e, D979): 49.7–50.5. Family caps (D675/D677): n_s ≤ 0.985, r ≤ 8.3e-4.
Method: Janus core spectra3 (validated D1218/D1228; |Δn_s| vs exact ≈ 3e-6) on the unchanged pipeline potential, run LIVE in the Janus desktop app via the link
(scan command), at C/1.15e-6 ∈ {0.8696, 1.0, 1.1304} (= C 1.0, 1.15, 1.3 e-6) × N* ∈ {48.4, 49.15, 49.9, 50.5}. Cross-check: the same points from the cloud knob grid
are not used (grid nodes differ); instead the PC values for C ×1.0 are compared to the cloud Janus run of the same code (expect ≤ 3e-7 in n_s, cf. the exe self-test).
Verdicts per claim: CONSISTENT if every audited point at N* 48.4–49.9 lies in the frozen n_s, r, α_s ranges within the Janus accuracy (n_s ±1e-5, r ±1 %, α_s ±2 %);
MISMATCH otherwise (value and size recorded). Separately reported: the same at the corrected N* 49.9–50.5 edge (inside or outside the frozen band), and caps.
