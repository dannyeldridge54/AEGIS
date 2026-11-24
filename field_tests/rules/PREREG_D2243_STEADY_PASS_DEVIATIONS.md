# D2243 DEVIATIONS (written after referee R111, before any result was read; run 1 stopped mid-run, output not read)
DEV-1 (F1 BLOCKER): L-H was judged on P_loss = P_alpha + P_aux - 0.6 P_rad_core (pedestal/confinement convention, rad_C3),
  while exhaust used Psep = P_alpha + P_aux - P_rad_core. Fix: one Psep everywhere; H-mode access judged as f_LH = Psep / P_LH
  (EU-DEMO definition, Siccinio et al.) with margins 1.3 (R13) and 1.2 (R12, now literature-consistent).
DEV-2 (F2 BLOCKER): negative Psep could pass E2, Psep/R and (via the Lengyel clamp max(Psep,1)) seeding. Fix: Psep < 1 MW is a
  violation ('Psep_low') in every rule set.
DEV-3 (F3 MAJOR): Psep/R <= 17 was in the lock but not in the violation set. Fix: add 'PsepR' = Psep/R/17 - 1.
DEV-4 (F4 MAJOR): wording - R12 was a mixed convention; resolved by DEV-1.
DEV-5 (F5 MAJOR, SUSPECTED): synchrotron is ~64% of alpha power at R9 B9 and is all counted as core radiation. Not fixed (no
  verified reference in hand); the result will report P_synch / P_alpha for best/nearest points and carry the flag.
DEV-6 (F6 MINOR): grid with fixed blanket has 57,600 points; 5000 samples = 8.7%.
DEV-7 (F7 MINOR): impurity fixed-point iterations 2 -> 5.
Control: the unpatched D2241 engine must still reproduce P_net 1004.5 MW, violations [LH] at the D2241 eta10 R8B8 point.
CONSEQUENCE FOR EARLIER NOTES (to be recorded as D2243a): D2236-D2241 judged L-H on the lenient P_loss; any earlier point that
"passed L-H" must be re-read under f_LH = Psep/P_LH.
One rerun.
