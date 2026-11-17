# PREREG A2b (track X, Hyperion; manual Djl 17 Nov 06:08 CT): aligned-spin TaylorF2 phase vs LALSuite (written before running)
Code: tools/janus_astro/gw.py taylorf2_phase_spin as committed with this lock. Every coefficient copied from Khan et al. 2016 (PhenomD), arXiv:1508.07253, Appendix B (fetched 17 Nov; definitions δ = (m1 − m2)/M, χ_s = (χ1 + χ2)/2, χ_a = (χ1 − χ2)/2; φ_5 log factor [1 + log(πMf)]; φ_6 log −(6848/63) log(64πMf)). Never compared before this lock.
Reference: lalsimulation TaylorF2, phase order 7, amplitude order 0, inclination 0, PNSpinOrder set per case, aligned spins, tidal off; same comparison method as A2a (−unwrap arg h̃₊; residual after removing a + b f; band 20 Hz to 0.8 f_ISCO; Δf = 1/512 Hz).
Cases: binaries (1.4, 1.4), (10, 10), (36, 29), (5, 50) M_⊙ × spins (χ1, χ2) ∈ {(0.5, 0.5), (−0.5, 0.3), (0.9, −0.9)} (BNS uses (0.05, 0.05), (−0.05, 0.03), (0.09, −0.09) as realistic NS spins).
Scored: spin orders 3 (1.5PN spin-orbit), 4 (+ 2PN spin-spin), 5 (+ 2.5PN SO): max |residual| ≤ 1e-2 rad in every case → A2b VALIDATED.
Reported only: spin orders 6 and 7 (LAL may include 3PN spin–spin and 3.5PN spin terms absent from the PhenomD Appendix-B list; a difference there would identify such terms, not a Hyperion error).
Output field_tests/results/janus_astro_a2b.txt via theory/janus_astro/a2b_check.py. No reruns to chase; DEVIATIONS first.
