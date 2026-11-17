# PREREG A2a (track X): Janus-Astro TaylorF2 phase (to 3.5PN, non-spinning) vs LALSuite (written before running)
Code: tools/janus_astro/gw.py taylorf2_phase as committed with this lock (coefficients typed from Buonanno et al. 2009 Table I; not yet compared with anything).
Reference: lalsimulation SimInspiralChooseFDWaveform, approximant TaylorF2, zero spins, zero tides, inclination 0, amplitude order 0, phase order O ∈ {4, 7} (set via LALDict PNPhaseOrder), deltaF = 1/512 Hz, f_min = 20 Hz.
Comparison: Ψ_LAL = ∓unwrap(arg h̃₊) on f ∈ [20 Hz, 0.8 f_ISCO] (f_ISCO = c³/(6^{3/2} π G M)); the sign is the one that gives the smaller residual (conventions differ between codes; a wrong sign gives residuals of order the full phase, so the choice is not a tuning). Residual = Ψ_ours − Ψ_LAL minus its least-squares fit a + b f (removes t_c and φ_c). Binaries (m1, m2)/M_⊙: (1.4, 1.4), (10, 10), (36, 29), (5, 50).
Pass: max |residual| ≤ 1e-2 rad for every binary at both orders → A2a VALIDATED; otherwise name the failing cases. Fixes only via DEVIATIONS written first; no reruns to chase.
Script theory/janus_astro/a2a_check.py; output field_tests/results/janus_astro_a2a.txt.
