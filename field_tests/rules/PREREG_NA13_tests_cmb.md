# PREREG NA13 — tests_cmb: re-derive D751/D752 discriminant arithmetic and update it to the audited predictions
Locked before computing. Inputs (fetched values recorded in D751/D749a/D752): σ(n_s) = 0.0016 (SO+SPHEREx), 0.0012 (best combination), 2212.04115 Table 5 (σ reading);
attractor n_s = 1 − 2/N*; long-kination attractor cap 0.9677 (D752); LiteBIRD σ(r) ≈ 5e-5 optimistic (D749a), requirement δr < 1e-3.
1. Reproduce D751: (0.970 − n_s,att(55))/σ = 4.0 / 5.3; vs N* = 60: 2.1 (±0.05).
2. Audited lower edges: SERAPIS-E box (PW1) n_s ≥ 0.97169; τ = i (NA12) n_s ≈ 0.9746. Report separations from attractor N* 55, 60 and from the kination cap 0.9677.
3. r detectability (optimistic LiteBIRD): r_min/σ(r) for SERAPIS-E box (4.378e-4) and τ = i (4.83e-4).
Verdict: reproduction PASS if 1 holds; 2–3 reported as the updated node value.
Results: field_tests/results/na13_tests_cmb.txt.
