# PREREG PROM-6 DEVICES (23 Nov 2026 12:50 CT) — held-out test of the 0-D fusion engine on other tokamak designs
Big loom after CM-CARDS. The ITER-tuned engine (FUSION-1, PROM-1..5) is run, unchanged, on two published designs it has never seen.
These targets are OTHER CODES' predictions (POPCON/TRANSP for SPARC; the ARC design point), not measurements: code-vs-code consistency.

## Inputs (LIT)
SPARC V2 (Rodriguez-Fernandez et al., JPP 86 (2020) 865860503, Tables 1, 3): R 1.85, a 0.57, kappa 1.97, B 12.2 T, Ip 8.7 MA, H98 1.0,
  <n_e> = 0.37 n_G (vol. avg), Z_eff 1.5, n_DT/n_e 0.85, n_W/n_e 1.5e-5, POPCON point: P_fus 140 MW, Q 11.2 -> P_aux 12.5 MW, <T> 7.9 keV, P_rad 10.4 MW.
ARC (Sorbom et al., FED 100 (2015) 378, Table 1): R 3.3, a 1.13, kappa 1.84, B 9.2 T, Ip 7.8 MA, V 141 m^3, <n> 1.3e20, <T> 14 keV,
  P_fus 525 MW, P_aux 13.6 ICRF + 25 LH = 38.6 MW (Q 13.6), H98 1.8, tau_E 0.64 s. Z_eff not stated -> 1.5 ASSUMED.
EU-DEMO: EXCLUDED (the sources found give R, a, kappa, B, Ip, Z_eff 2.19, P_fus ~2 GW but not density, temperature, volume or H98).

## Engine changes (mechanical only, no refit)
- tau_ipb98 multiplied by m.get('H98', 1.0) (ITER keeps 1.0 -> unchanged).
- Geometry: V = c_V 2 pi^2 R a^2 kappa, S = c_S 4 pi^2 R a sqrt((1+kappa^2)/2), with c_V, c_S calibrated on ITER (831 m^3, 683 m^2); ARC uses its V 141.
- Profiles: ITER's pedestal shape in normalised form: n_ped/<n> and n_sep/<n> as ITER (0.708, 0.354); T_ped = 0.39 x published <T>
  (ITER ratio), T_sep 0.1 keV; alpha_n, alpha_T, rho_ped as ITER. (Published <T> enters only the profile shape; the operating T is solved.)
- Composition: Z_eff set by f_Be (low-Z proxy) after He; Ar 0; W via the OPEN-ADAS line model (SPARC n_W/n_e 1.5e-5, ARC 0); line_model 'adas';
  Ti/Te 1.0; M 2.5; He ash self-consistent (tau_He*/tau_E 5); Lux radiation correction as ITER.

## Goalposts (locked)
D1 SPARC: P_fus within +-25% of 140 MW; <T> within +-20% of 7.9 keV.
D2 ARC: P_fus within +-25% of 525 MW; tau_E within +-25% of 0.64 s; <T> within +-20% of 14 keV.
D3 can-fail: ARC with H98 1.0 instead of 1.8 must move P_fus by more than 25% (else D2 proves nothing).
D4 robustness (reported, not pass/fail): T_ped x0.7 and x1.3 spread for D1/D2.
Referee after the run; findings to DEVIATIONS before any fix; one rerun only.
