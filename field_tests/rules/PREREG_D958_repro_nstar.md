# PREREG D958: independent reproduction of the SERAPIS-E N* brackets (D719) with tools/serapis_calc levels 3, 4, 6 (selftest must pass)
Model: SERAPIS-E, paper convention (E(U,2) = BHK lattice sum), C = 1.15e-6 (as D719). N* solved self-consistently: N* = matching(r(N*), V*/V_end, T_R) with r from exact MS (D719 used first-order slow roll for r and V*/V_end; same matching equation, tools/serapis_calc/nstar.py, itself checked against D719 to 0.01).
T_R = 1e4, 1e6, 1e7, 1e8, 1e10 GeV. Reference D719: N* = 46.29, 47.81, 48.58, 49.34, 50.87.
PASS (fixed now): |N* - ref| <= 0.10 at every T_R (allows the known exact-vs-slow-roll r difference of 2-3%, which moves N* by ~0.01). Also report exact n_s at each N*.
FAIL otherwise: record; trace; DEVIATIONS before any rerun.
Script theory/flux/repro_nstar_d958.py; output field_tests/results/repro_nstar_d958.txt.
