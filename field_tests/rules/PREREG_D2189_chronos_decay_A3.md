# D2189 Amendment A3 (written before any code), 2026-11-23 ~08:50 CT
One pass, five new branches on the same engine, then one referee ping-pong covering A2 + A3 + the DEV fixes.
B-Ac225 (medicine): Ac-225 -> Fr-221 -> At-217 -> Bi-213 -> {Po-213 (97.8%) | Tl-209 (2.2%)} -> Pb-209 -> Bi-209.
  Data (NuDat/ENSDF): Ac-225 9.920 d, Fr-221 4.801 min, At-217 32.6 ms, Bi-213 45.61 min, Po-213 3.72 us, Tl-209 2.162 min,
  Pb-209 3.234 h. Ac-227 impurity (21.772 y) grows-in fraction vs storage time for a given Ac-227/Ac-225 activity ratio at
  end of bombardment (user input; literature ~0.1-0.2% for accelerator Ac-225, stated as context).
  T11: Bi-213 reaches >99% of transient equilibrium with Ac-225 by 6 h from pure Ac-225 (literature: ~5-6 h); branching
  sums conserve atoms to 1e-12 in the matrix solver.
B-PuAge (safeguards): time since Pu separation from the measured Am-241/Pu-241 activity (or atom) ratio, assuming Am-241 = 0 at
  separation. T12: forward/inverse round trip to 1e-9 at 1, 10, 50 y.
B-Tritium (fusion): T-3 inventory decay (12.32 y) and He-3 ingrowth; fraction lost per year. T13: annual decay fraction
  5.47% +/- 0.05% (1 - 2^(-1/12.32)).
B-DecayHeat (energy/waste): Way-Wigner approximation P/P0 = 0.0622 [t^-0.2 - (t+T)^-0.2] (t, T in s), labelled
  approximate (+/- ~factor 2 at very short and very long times; not ANS-5.1). T14 (report): P/P0 at 1 h, 1 d, 1 y after 1 y
  of operation; textbook order ~1.3%, ~0.5%, ~0.02-0.05% stated as context.
B-Cosmochron (nucleosynthesis): age from observed log eps(Th/Eu) or (U/Th) with a user-supplied production ratio; default
  production ranges taken from the literature and shown. Data: Th-232 1.40e10 y, U-238 4.468e9 y.
  T15: forward/inverse round trip exact; report the age for the CS31082-001 U/Th example only if the published log(U/Th)
  and production ratio are quoted with source, else skip.
Dose (Benton) and the m_bb -> half-life converter stay out of this pass (need vetted coefficients / matrix elements).
