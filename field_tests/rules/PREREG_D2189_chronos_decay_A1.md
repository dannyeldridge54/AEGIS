# D2189 Amendment A1 (written before any code), 2026-11-23 ~08:45 CT
Danny: fold the chosen professors into one nuclear rung. Added branches (same decay engine):
- Supernovae (OU, Dr. E. Baron; Dr. M. Kilic's double white dwarfs as SN Ia progenitors): Ni-56 -> Co-56 -> Fe-56 radioactive
  heating, L(t) = M_Ni [(e_Ni - e_Co) exp(-t/tau_Ni) + e_Co exp(-t/tau_Co)] (Nadyozhin 1994), with e_Ni, e_Co COMPUTED from
  Q-values (Ni-56 1.75 MeV, Co-56 3.73 MeV incl. positron kinetic + annihilation energy, neutrinos excluded) and half-lives;
  optional gamma-ray escape with trapping timescale t0 (deposition 1 - exp(-t0^2/t^2), Jeffery 1999 / Wygoda 2019 form).
- Kilonovae / GRB-associated mergers (OU, Dr. X. Dai): r-process specific heating, power law
  eps(t) ~ 1e10 (t/1 d)^-1.3 erg/g/s (Metzger et al. 2010 order of magnitude) with thermalisation efficiency as a free knob;
  labelled order-of-magnitude.
Added locked tests:
T5: computed e_Ni = 3.9e10 and e_Co = 6.8e9 erg/g/s (Nadyozhin 1994) to within 3%.
T6: full-trapping L at t = 18 d for M_Ni = 0.6 Msun within 1.1-1.5e43 erg/s (Arnett-rule SN Ia peak scale).
Dose (Benton) stays deferred to v2 (needs vetted dose coefficients; stated in the tool).
