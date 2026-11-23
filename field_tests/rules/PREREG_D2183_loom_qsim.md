# PREREG D2183 — Loom quantum-lattice simulator (TOOL): spin-1 Bose–Hubbard digital twin built on the Loom node/compass engine
Locked 2026-11-23 06:22 CT before building. Danny 06:18 "Build one based off our engine make it better than hers".
Honest frame (stated now): a classical computer cannot beat a cold-atom quantum simulator at large size (Hilbert space grows exponentially). "Better" here means: a fast, checked digital twin that (a) does exact quantum dynamics at small size, (b) does mean-field dynamics at any size, and (c) adds what a lab does not get for free — the Loom compass (sensitivity of every observable to every dial) and a node-balance readout. It is for planning and interpreting experiments, not replacing them.
Build tools/qsim/loom_qsim.py:
 Q1 exact spin-1 single-mode (SMA) dynamics in the M=0 sector: H = (c/2N)[(2N0−1)(N−N0) + 2(a1†a−1†a0a0 + h.c.)] − q N0 (q = quadratic Zeeman); ρ0(t) = <N0>/N.
 Q2 mean-field spin-1 lattice (L sites, hopping J, spin coupling c, q), RK4 on ζ_{i,m}.
 Q3 exact scalar Bose–Hubbard chain (L sites, N bosons, periodic), H = −J Σ(b_i†b_{i+1}+h.c.) + (U/2) Σ n_i(n_i−1).
 Q4 Loom compass: finite-difference Jacobian of observables (ρ0 period/amplitude, spin-mixing frequency, ground energy) vs dials (c, q, J, U) + a balance readout (which dial dominates each node).
Validation (pre-stated; tool adopted only if all pass):
 V1 Q3 at U=0: ground energy = −2JN (all bosons in k=0), |err| < 1e-9.
 V2 Q3 at J=0, N=L (unit filling): ground energy 0 and first gap = U (Mott), |err| < 1e-9.
 V3 Q1 vs Q2 (single site): for N = 2000, ρ0(t) from exact and mean-field agree to < 0.02 over the first oscillation (mean-field is the large-N limit), starting from ρ0 = 0.5 with a small phase offset.
 V4 Q2 conserves total atom number and energy to < 1e-6 relative over the run.
 V5 Q1 total-spin sector check: H commutes with N and M (built in M=0); Hermiticity error < 1e-12.
Then (not a test of any physics claim): run the compass on the sodium (antiferromagnetic, c > 0) case relevant to the OSU apparatus.

## Addendum 1 (2026-11-23 06:24 CT, after V1–V5 passed, before the lens pass) — lenses, as with the emulator
Danny 06:19 "examine it through lenses like with emulator". Compass fix already applied (period by interpolated crossings, eps 1e-2; the first compass print had a grid-quantised period and is void — validation unaffected).
L1 LENS SVD: Jacobian of 6 observables [period, amplitude, mean ρ0, quantum break time t_b (exact vs mean-field |Δρ0| > 0.02), BH ground energy E0, BH gap] vs 6 dials [c, q, ρ0_init, φ_init, J, U] (log-derivatives); report singular values and the effective lens rank (σ_i/σ_1 > 1e-2) — how many independent knobs the experiment really has.
L2 EMULATOR LENS: quadratic surrogate of (period, amplitude) on a 7×7 grid in (c, q) around the sodium point (c=1, q in 0.1–0.6); leave-one-out error and speed-up vs the RK4 twin. Pass if LOO max relative error < 2% away from the separatrix.
L3 SCALE LENS: t_b vs N for N = 250…8000; fit t_b ∝ N^a and ∝ ln N; report which form fits (the known result for this model is t_b ∝ ln N for unstable/near-separatrix and ∝ √N-type for stable orbits; we report what we get, labelled).
