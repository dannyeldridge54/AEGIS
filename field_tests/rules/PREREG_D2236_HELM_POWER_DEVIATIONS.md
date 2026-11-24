# D2236 DEVIATIONS (after referee, before the one rerun). Run 1 is NOT reportable (referee: BLOCKER on P_sep).
- DEV-1 (BLOCKER, bug): P_sep must be P_alpha + P_aux - P_rad_core. Run 1 used P_loss - P_rad_core where the engine's P_loss already
  subtracts 0.6 P_rad_core (the C3 factor), so it removed 1.6 P_rad_core (hence negative P_sep/R). Fixed.
- DEV-2 (control): the lock's "control = +4.9 MW" was incompatible with its own new P_sep/R limit. Reported now: the old-rule ITER optimum
  (goal_dials_fast, +4.88 MW, referee-reproduced) AND its corrected P_sep/R (25.5 MW/m, so it fails the new limit) - not a pass.
- DEV-3 (radiation): the fixed P_line input scaled as s^3 g^2 is an assumption; an ADAS line-radiation variant (line_model 'adas' with the
  machine's own Be/Ar/He fractions) is reported side by side.
- DEV-4 (grid edge): P_aux set extended down: {10, 20, 30, 40, 50, 60, 73, 100} MW.
- DEV-5 (lock violation): TBR hold check added at each point: computed TBR 1.021 must exceed hold = 1 + lambda I0 / b (I0 = 10 kg, b = burn
  at that P_fus).
- DEV-6 (sources): wall load <= 2.0 MW/m^2 (average, on plasma surface S) has no verified source; P_sep/R <= 17 MW/m likely EU-DEMO (Wenninger
  2015) but not verified. Both kept unchanged and marked UNVERIFIED in the report.
- DEV-7 (plant): P_other sensitivity: 100 MW fixed (locked) and 100 MW x S/S_ITER (scaled), both reported.
Nothing else changes (knob grid, other limits, objective).
