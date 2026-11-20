# The Weave — every connection between sectors (20 Nov 2026, Danny 09:34 "check all paths eq")

Equations are nodes; a connection is a quantity shared by equations of different sectors. Status: C computed in our tools, D derived in notes, P postulate/hosted. Built from the D-notes, no new physics.

28 equations, 63 quantities, 17 cross-sector connections; every pair of the 8 sectors is connected.

## Hubs (one number, several sectors)
| quantity | sectors | equations |
|---|---|---|
| T_R | dark, early, matter, quark | E19 tau_q cosmology; E3 N* from history; E4 reheating; E5 leptogenesis; E6 gravitino->wino |
| dilution | dark, early, quark | E19 tau_q cosmology; E3 N* from history; E9 asymmetric DM |
| tau_nu=i | early, late, lepton | E13 TM1 mixing; E15 seesaw; E25 Y-fork; E26 thread endpoint |
| eta_B | dark, late, matter | E11 BBN; E5 leptogenesis; E9 asymmetric DM |
| A | early, late | E1 inflation plateau; E22 reverse thread; E27 species scale |
| D | early, late | E1 inflation plateau; E2 r ladder; E22 reverse thread |
| m_phi | early, matter | E1 inflation plateau; E4 reheating; E5 leptogenesis |
| g_s | dark, early | E28 brane split; E4 reheating |
| tau_lep=rho | early, lepton | E12 Koide at rho; E13 TM1 mixing; E25 Y-fork |
| M_N | lepton, matter | E15 seesaw; E5 leptogenesis |
| Sum m_nu | late, lepton | E14 relic neutrinos; E15 seesaw |
| m_e | chemistry, lepton | E12 Koide at rho; E21 atoms & molecules |
| quark hierarchies | nuclear, quark | E16 quark ladder; E20 proton |
| m_p | chemistry, nuclear | E20 proton; E21 atoms & molecules |
| alpha | chemistry, late | E21 atoms & molecules; E24 alpha drift |
| Delta N_eff | dark, late | E11 BBN; E28 brane split |
| thread identity | dark, late | E24 alpha drift; E28 brane split |

## Shortest path between every pair of sectors
| from | to | steps | path | weakest link |
|---|---|---|---|---|
| early | matter | 1 | E1 inflation plateau -> m_phi -> E5 leptogenesis | E5 leptogenesis [D] |
| early | lepton | 1 | E25 Y-fork -> tau_nu=i -> E15 seesaw | E25 Y-fork [D] |
| early | quark | 1 | E3 N* from history -> T_R -> E19 tau_q cosmology | E3 N* from history [D] |
| early | nuclear | 3 | E25 Y-fork -> tau_lep=rho -> E12 Koide at rho -> m_e -> E21 atoms & molecules -> m_p -> E20 proton | E25 Y-fork [D] |
| early | chemistry | 2 | E25 Y-fork -> tau_lep=rho -> E12 Koide at rho -> m_e -> E21 atoms & molecules | E25 Y-fork [D] |
| early | dark | 1 | E3 N* from history -> T_R -> E6 gravitino->wino | E3 N* from history [D] |
| early | late | 1 | E1 inflation plateau -> D -> E22 reverse thread | E1 inflation plateau [C] |
| matter | lepton | 1 | E5 leptogenesis -> M_N -> E15 seesaw | E5 leptogenesis [D] |
| matter | quark | 1 | E5 leptogenesis -> T_R -> E19 tau_q cosmology | E5 leptogenesis [D] |
| matter | nuclear | 5 | E5 leptogenesis -> M_N -> E15 seesaw -> tau_nu=i -> E13 TM1 mixing -> tau_lep=rho -> E12 Koide at rho -> m_e -> E21 atoms & molecules -> m_p -> E20 proton | E13 TM1 mixing [P] |
| matter | chemistry | 4 | E5 leptogenesis -> M_N -> E15 seesaw -> tau_nu=i -> E13 TM1 mixing -> tau_lep=rho -> E12 Koide at rho -> m_e -> E21 atoms & molecules | E13 TM1 mixing [P] |
| matter | dark | 1 | E5 leptogenesis -> T_R -> E6 gravitino->wino | E5 leptogenesis [D] |
| matter | late | 1 | E5 leptogenesis -> eta_B -> E11 BBN | E5 leptogenesis [D] |
| lepton | quark | 2 | E15 seesaw -> M_N -> E5 leptogenesis -> T_R -> E19 tau_q cosmology | E15 seesaw [D] |
| lepton | nuclear | 2 | E12 Koide at rho -> m_e -> E21 atoms & molecules -> m_p -> E20 proton | E12 Koide at rho [D] |
| lepton | chemistry | 1 | E12 Koide at rho -> m_e -> E21 atoms & molecules | E12 Koide at rho [D] |
| lepton | dark | 2 | E15 seesaw -> M_N -> E5 leptogenesis -> T_R -> E6 gravitino->wino | E15 seesaw [D] |
| lepton | late | 1 | E15 seesaw -> Sum m_nu -> E14 relic neutrinos | E15 seesaw [D] |
| quark | nuclear | 1 | E16 quark ladder -> quark hierarchies -> E20 proton | E16 quark ladder [C] |
| quark | chemistry | 2 | E16 quark ladder -> quark hierarchies -> E20 proton -> m_p -> E21 atoms & molecules | E16 quark ladder [C] |
| quark | dark | 1 | E19 tau_q cosmology -> T_R -> E6 gravitino->wino | E6 gravitino->wino [D] |
| quark | late | 2 | E19 tau_q cosmology -> T_R -> E5 leptogenesis -> eta_B -> E11 BBN | E5 leptogenesis [D] |
| nuclear | chemistry | 1 | E20 proton -> m_p -> E21 atoms & molecules | E20 proton [C] |
| nuclear | dark | 3 | E20 proton -> m_p -> E21 atoms & molecules -> alpha -> E24 alpha drift -> thread identity -> E28 brane split | E28 brane split [P] |
| nuclear | late | 2 | E20 proton -> m_p -> E21 atoms & molecules -> alpha -> E24 alpha drift | E20 proton [C] |
| chemistry | dark | 2 | E21 atoms & molecules -> alpha -> E24 alpha drift -> thread identity -> E28 brane split | E28 brane split [P] |
| chemistry | late | 1 | E21 atoms & molecules -> alpha -> E24 alpha drift | E21 atoms & molecules [C] |
| dark | late | 1 | E9 asymmetric DM -> eta_B -> E11 BBN | E9 asymmetric DM [D] |

## Connections worth testing first (each is ONE number that must fit several places at once)
1. **D, the dimension at horizon exit**: sets r (inflation) AND the thread's slope beta (dark energy). D = 10 means r = 5.4e-4 AND alpha = 1/12 for the thread; D = 6 means r = 1.07e-3 AND alpha = 1/6. If the thread carries the same D as inflation (a postulate: the reverse thread reuses the plateau), a measured r fixes the thread tilt — a joint test of the early and late universe.
2. **T_R, the reheating temperature (1.34e9 GeV)**: feeds N* (so n_s), leptogenesis (eta_B), thermal gravitinos -> winos (dark matter), and the quark-modulus dilution. Moving it moves four sectors together.
3. **The quark-modulus mass m_tauq**: one number sets the dilution D, which shifts N* (n_s), the asymmetric dark-matter mass (m_X ∝ D) and the needed leptogenesis yield (0.87e-10 × D).
4. **The knot i**: neutrinos (TM1, seesaw), the Y-fork exit, AND the dark thread's final resting point. Same point, three roles.
5. **The plateau coefficient A = 7.30**: inflation and dark energy share it (the "reverse thread").
6. **eta_B**: leptogenesis, BBN (omega_b) and the 12.8 GeV dark-matter mass are tied by one asymmetry.
7. **alpha**: if the thread drifted it would move alpha, which moves every atomic and molecular scale (Rydberg, bond lengths) — chemistry is a clock for the thread's identity.
8. **m_e from the knot ρ**: the Koide leptons set the electron mass that sets chemistry; a slip > 6e-5 off the knot would break both Koide and (through m_e) the atomic scales.
Weakest links (P): E28 brane split (dark ↔ visible separation, thread identity), E13 TM1 (post hoc), E18 strong CP (imported), E27 species principle.

