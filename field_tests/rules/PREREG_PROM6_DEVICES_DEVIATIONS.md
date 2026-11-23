# PROM-6 DEVIATIONS (written before any fix). Locked result stands: D1 FAIL, D2 FAIL, D3 PASS.
Referee R89 (sonnet, read-only): misses come mainly from the solved temperature root (P_fus ~ x3 over 6.4 -> 7.9 keV), a dilution proxy and
profile peaking, plus an internally inconsistent ARC target set. No code bug in the H98 multiplier.
- DEV-1 (fair, from published input) SPARC dilution: take n_DT/n_e = 0.85 as published (f_Be set to give 0.85 after He; Z_eff then follows,
  ~1.3 instead of 1.5: a Be-only proxy cannot meet both). ARC states no dilution -> unchanged (Z_eff 1.5 proxy).
- DEV-2 (fair, from published input) ARC peaking: alpha_T chosen so the engine's T0/<T> = 27/14 = 1.93 (was 1.78). SPARC states no peaking -> unchanged.
- DEV-3 (bug, negligible) negative line radiation (PRB - impurity bremsstrahlung < 0) clipped at 0 per radial point.
- DEV-4 (target, post-hoc) ARC tau_E = 0.64 s is not consistent with its own H98 1.8 + IPB98 (~1.0 s) or with W/P_loss from its own averages
  (W 114 MJ / 0.64 s = 178 MW > P_alpha + P_aux 143 MW). Reported, not used as a goal in the rerun; the locked D2 FAIL stays on the record.
- DEV-5 (diagnostic, not pass/fail) P_fus at the published <T> reported beside the solved point, to separate the T-root from the rest.
- Flag (no fix): SPARC solved point is below the L-H threshold (P_loss 19 < P_LH 33 MW): a symptom of the low T root; no L-mode branch added.
One rerun with DEV-1..3, same goalposts D1, D2 (P_fus, <T>), D3.
