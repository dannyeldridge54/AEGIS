# PREREG A7a (track X, AEGIS application): exact J-factors for the H.E.S.S. inner-Galaxy region; upgrade of D735's profile dependence for SERAPIS-E's wino (written before running)
Request: Danny 17 Nov 05:26 CT: "Develop it like we did Janus, use our best data from AEGIS".
Code: tools/janus_astro/jfactor.py as committed with this lock (no J value computed before this lock).
Region (H.E.S.S. 2018 line search, 1805.05741, as recalled — reported, and to be checked against the paper before any public statement): cone of 1° radius around the GC with |b| < 0.3° excluded. Observer r_⊙ = 8.5 kpc, ρ_⊙ = 0.39 GeV/cm³ for every profile.
Profiles: Einasto (r_s = 20 kpc, α = 0.17; the H.E.S.S. reference), NFW (r_s = 20 kpc), Burkert (r₀ = 12.67 kpc), Einasto with a constant-density core r_c = 1 kpc and r_c = 3 kpc (ρ(r < r_c) = ρ(r_c)).
Tests:
T1 two routes (A: (l, b) grid; B: polar about the GC) agree for every profile: relative ≤ 1e-3 → J values VALIDATED.
T2 normalisation: ρ(r_⊙) = 0.39 exactly for every profile (≤ 1e-12).
Application [estimate, not pass/fail]: ON-region signal ∝ f² J, so the line limit on the wino fraction scales as f_max,X = f_max,Ein × √(J_Ein/J_X). Using D735's f_max,Ein (0.16 at 0.66 TeV, 0.24 at 1.0 TeV, 0.44 at 1.85 TeV) and SERAPIS-E's predicted f (0.14, 0.26, 0.67), report PASS/FAIL per profile and mass. Stated caveat in advance: H.E.S.S. subtracts a background measured in OFF regions; for cored profiles the OFF region also contains signal, so the true weakening is LARGER than √(J_Ein/J_X) — the ON-only numbers are conservative bounds on the weakening.
Literature comparison (reported only, not scored): any J value quoted for this region in 1805.05741.
Script theory/janus_astro/a7a_check.py; output field_tests/results/janus_astro_a7a.txt. No reruns to chase; fixes via DEVIATIONS first.
