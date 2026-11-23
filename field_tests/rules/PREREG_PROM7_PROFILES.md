# PREREG PROM-7 PROFILES (23 Nov 2026 13:05 CT) — Prometheus cycle 5: published profile peaking as INPUTS (SPARC, ARC)
Target: the PROM-6 transfer gap (D2200). Hints: tools/fusion/hints/cycle5.json (20, sourced).
Key reading (H11): ARC's 525 MW is a PRESCRIBED-profile result (confinement not used in its 0-D scoping); SPARC's POPCON point used H98 1.0.
## Change (inputs only, no refit)
The pedestal profile basis keeps its form; for these machines alpha_n and alpha_T are solved so the engine's n0/<n> and T0/<T> equal the
published peaking (volume averages):
 SPARC: n0/<n> 1.3 (H1), T0/<T> 2.5 (H2), n_ped 2.7e20 (H6), f_DT 0.85 (D2200 DEV-1), Ti/Te 1, H98 1.0, P_aux 12.5 MW.
 ARC: n0 1.75 / <n> 1.3 (H12), T0 27 / <T> 13.9 (H14), Ti = Te (H15), Z_eff 1.2 via f_Be (H16), P_aux 38.6 MW.
Pedestal temperatures as PROM-6 (0.39 <T>) unless the peaking cannot be met, in which case T_ped is lowered and that is reported.
## Goalposts (locked)
P1 prescribed-profile fusion power (no power balance), at the published averages + peaking: SPARC within +-20% of 140 MW; ARC within +-20% of 525 MW.
P2 SPARC power balance with the P1 profile shape, H98 1.0: P_fus within +-25% of 140 MW and <T> within +-20% of 7.9 keV (re-test of D1).
P3 (reported) ARC: the H98 our power balance needs to hold the published point (P_loss = P_alpha + P_aux - 0.6 P_rad,core; W/tau): compare ARC's 1.8.
C1 can-fail: P1 with the PROM-6 shapes must differ from P1 by more than 15% for each machine (else the peaking input does nothing).
C2 ITER-400 held-out unchanged (389.5 MW, 3.41 s).
Referee after; DEVIATIONS before any fix; one rerun.
