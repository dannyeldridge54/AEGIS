# D2189 Amendment A2 (written before any code), 2026-11-23 ~08:55 CT
Danny: full workup of each person, catalogue it in the engine, set goalposts on their newest work and execute them.
Workup sources (fetched 08:45-08:55): Baron et al. arXiv:2507.18753 (JWST SN 2024ggi, PHOENIX); Kilic et al. arXiv:2507.12655
(white dwarf merger remnants, warm DQs); OU College of Pharmacy cyclotron (GE PETtrace 890, OU news 2026-03-05); Benton
(OSU radiation physics lab: SpaceTED, aviation dosimetry); Xu (OU, radiocesium monitoring); Dai (OU, GRBs; newest paper not
yet identified, so his branch is labelled generic GRB-SN).
New branches (same engine) and locked tests:
B-Baron  Ni-56 mass from a radioactive-tail luminosity: M_Ni = L(t) / [eps(t) * trapping(t)] (inverse of A1 model).
         T7: round-trip L -> M_Ni -> L exact to 1e-12 for t = 50..400 d, with and without trapping.
B-Dai    Arnett-rule Ni-56 from a GRB-SN peak: M_Ni = L_peak / eps(t_rise) (full trapping).
         T8 (report only): M_Ni for the GRB-SN mean peak L = 9.42e42 erg/s (arXiv:2506.22914) at t_rise = 13 d; literature
         GRB-SNe typically 0.1-0.5 Msun (stated as context, not a pass/fail).
B-Kilic  Double-white-dwarf GW clock: Peters (1964) circular-orbit merger time t = (5/256) c^5 a^4 / (G^3 m1 m2 (m1+m2)),
         a from Kepler's law; GW frequency 2/P.
         T9: SDSS J0651+2844 (P = 765 s, m1 = 0.26, m2 = 0.50 Msun; Brown et al. 2011) merger time within 0.7-1.2 Myr
         (published ~0.9 Myr).
B-Awasthi Cyclotron production planner: A_EOB = A_sat (1 - exp(-lambda t_irr)) with the saturation activity A_sat entered
         by the user (no cross sections), then decay through synthesis, QC and transport.
         T10: after exactly two half-lives of irradiation the fraction of saturation is 0.75 to 1e-12.
B-Benton dose: still deferred (needs vetted dose coefficients); his open problem is catalogued, not computed.
