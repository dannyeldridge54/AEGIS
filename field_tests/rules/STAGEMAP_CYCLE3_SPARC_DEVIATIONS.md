# STAGE MAP cycle 3 (SPARC) - DEVIATIONS (written after referee R107, before the one rerun)
Run 1 (commit 4e9c0f3a): cfspopcon 9.0.1 SPARC_PRD with our ADAS-built radas files -> 115.9 MW, Q 12.78, <Te> 9.14 keV, n 2.5e20 (their own
regression file: 115.8 MW, Q 12.74, same cell). Our engine at that cell: P_fus 89.4 MW (-23%), required P_aux 14.4 MW. Scored as written: B.L4 OUT.

Referee R107 (sonnet, read-only, /tmp/ref3):
- GOALPOST (DEV-1): the lock's "140 MW / Q~11 / 7.3 keV" is NOT what cfspopcon's own PRD point gives (116 MW / Q 12.7 / 9.14 keV with THEIR
  atomic data). The literal reproduction clause fails; its premise ("then our atomic data is at fault") is refuted by their own regression. The
  clause stays FAILED on the record; it is not redefined. Atomic-data agreement at the point: Q/P_fus 0.1%, P_rad +13%, P_SOL/P_LH 1.008 vs 1.040,
  W mean charge 53.4 vs 58.4 (coronal), edge Ar concentration +41% (our equilibrium_* = coronal copies; does not feed P_fus/P_in).
- LIKE-WITH-LIKE (DEV-2): our "required P_aux" = P_heat - P_alpha includes ohmic. Primary comparison is therefore against their absorbed + ohmic
  = 7.0979 + 1.194 = 8.29 MW (run 1: +73%); absorbed-only and launched reported alongside. Hard-coded 7.0908 corrected to 7.0979.
- BUG (DEV-3, harness): the SPARC dict was built for n_avg 3.1e20 / 7.3 keV (n_ped 2.7e20 fixed, T_ped 0.39*7.3, shape targets at 7.3 keV).
  Evaluated at 2.5e20 the density profile is hollow (n0/<n> 0.97, pedestal above average). Fix, decided here before rerunning: rebuild the SPARC
  dict at their (n, T) with the SAME recipe PROM-8 used at its own point - n_ped = (2.7/3.1) n, n_sep scaled by n/3.1e20, T_ped = 0.39 T,
  then T7.shape(S, 1.3, 2.5, T) (density peaking 1.3 and temperature peaking 2.5 exactly as locked in PROM-8; no other change). n_pk 1.5 (their
  regression value) is NOT used for scoring; reported only as a side number.
- Harness hygiene (DEV-4): the engine script reads the cfspopcon point from the repo results file, not /tmp.
- DESIGN noted, not fixed: tau_E agreement (+2%) partly cancels a +5.6% volume difference (20.9 vs 19.79 m3); P_aux miss is leveraged by the
  alpha deficit.
Scoring rule for the rerun (fixed now): P_fus and P_aux(vs absorbed+ohmic) both within +-25% -> EDGE, not IN (R107: the pedestal rebuild is a
degree of freedom the lock did not name; the reproduction clause also failed). Otherwise OUT.
