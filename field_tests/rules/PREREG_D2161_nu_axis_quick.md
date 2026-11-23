# PREREG D2161: quick test of the unequal-neutrino axis (locked 22 Nov 2026 23:06 CT, before running)
Danny 23:04: "can we get it tested before 12". Full PR4 refits take ~1 h and both machines are busy, so this is the fast version.
Question: does giving LCDM the Weave's neutrino setting (3 normal-ordered states, sum 0.0587 eV) instead of the standard single 0.06 eV state move LCDM's best chi2?
Tool: the referee's independent compressed fit (field_tests/weave_lcdm/referee_indep/fit.py: compressed Planck CMB 4-vector + DESI DR2 BAO + DES-Dovekie, Nelder-Mead, 2 starts), unchanged except one new model kind 'Lnu' = 'L' with mnu 0.0587, 3 massive, normal hierarchy.
Run once each: L and Lnu.
Rule: delta = chi2(Lnu) - chi2(L). |delta| < 0.5 -> the neutrino axis is CLOSED (negligible for the W-vs-L verdicts); otherwise delta is carried as a systematic on every PR4 dchi2 and a full PR4 refit is queued.
Limitation stated now: compressed CMB is far weaker than PR4 on lensing/high-l, where neutrino mass enters; a small delta here bounds the background effect only.
