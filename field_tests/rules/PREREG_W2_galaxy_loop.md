# PREREG W2 (Djl loop (C), manual Djl 17 Nov 07:03 CT): the Galaxy loop — Star Mapper orbits ⇄ Milky Way halo ⇄ local DM density ⇄ J-factor ⇄ wino limits (written before running)
Wiring (theory/wiring/w2_galaxy_loop.py, never run before this lock): a disk-star sample (A8c3 generator, seed 11, 200 stars) → fast.orbits_fast in Hyperion's Milky Way with the halo amplitude scaled by s ∈ {0.8, 0.9, 1.0, 1.1, 1.2} → Mapper observables (median z_max, median e, median r_apo); the same halo gives ρ_⊙(s) = s·ρ_halo(R₀ = 8 kpc) → J-factor for the H.E.S.S. region (A7a geometry, r_⊙ = 8 kpc, NFW with r_s = 16 kpc as in MWPotential2014) → wino f_max(M) = f_max,ref(M)·√(J_ref/J(s)), with f_max,ref = A7b tree values 0.19, 0.24, 0.18 at M = 0.66, 1.0, 1.85 TeV and J_ref = 4.413e21 GeV² cm⁻⁵ (A7a Einasto, ρ_⊙ 0.39) → compared with SERAPIS-E's f = 0.14, 0.26, 0.67.
Tests:
W2a lossless: every wired number equals a direct call with the same inputs (ρ_⊙, J, orbit statistics): relative ≤ 1e-12.
W2b closure: the full chain run twice gives identical outputs (≤ 1e-12).
W2c joint prediction (reported): d(median z_max)/ds and d f_max/ds across s; which wino masses pass at each s; whether the Mapper observable responds measurably (change in median z_max across s vs the A8c4 orbit precision 1e-3).
Verdict: W2a and W2b PASS → wiring VALIDATED; W2c reported.
Caveats stated now: the NFW halo here is MWPotential2014's (lighter than the A7a Einasto normalisation); A7b's f_max,ref carries D735's ×2 read-off uncertainty; scaling only the halo amplitude changes v_c(R₀) away from 220 km/s (reported).
Output field_tests/results/wiring_w2.txt. No reruns to chase; DEVIATIONS first.
