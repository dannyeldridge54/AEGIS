# D2189 DEVIATIONS (written before fixes), 2026-11-23 ~09:00 CT
Referee R77: T1-T6 pass; half-lives within 0.5% except Sr-90; branchings, Bateman, generator formulas, release clock,
Q-values and trapping form verified. Defects -> fixes:
DEV-1 (major): Co-56 positron KE (0.12 MeV of 3.73) is deposited locally: L = L_Ni f + L_Co [(1 - 0.12/3.73) f + 0.12/3.73].
DEV-2 (major): "L" renamed "radioactive heating (deposition) rate"; note: equals bolometric L near and after peak
  (Arnett's rule); no diffusion modelled. Applies to SN and kilonova tabs and the A2 inversions (tail inversion is valid
  on the tail; Arnett inversion at peak by construction).
DEV-3 (major, presentation): the Lantern stays the header (Danny's standing wish) but starts collapsed in Chronos.
DEV-4 (minor): kilonova citation -> Korobkin et al. 2012 / Metzger 2019 (Living Rev.); note constant f_th (Barnes+2016).
DEV-5 (minor): Sr-90 half-life 28.79 -> 28.91 y (NuDat current).
DEV-6 (minor): I-131/Cs-137 clock: no default ratio; "enter your site-specific release ratio" (Fukushima ~10-100; <~3 months).
DEV-7 (minor): pharmacy warning when t > 10 half-lives; O-15 and Rb-82 removed from the make-ahead list.
DEV-8 (minor): energy tab normalised to 1 Bq of parent at t = 0, axis labelled.
DEV-9 (minor): t0 <= 0 means full escape, labelled.
T1-T6 and the A2 tests are rerun after the fixes as a check (T6 is full trapping and unaffected by DEV-1).

## Round 2 (R78), written before the fixes, ~09:00 CT: 1 major, 5 minor
DEV-10 (major): ni_mass_from_tail requires t0_days explicitly; full trapping labelled "Type II-P / full-trapping only"; the
  example is reported with t0 = 40 d (SN Ia) and with full trapping.
DEV-11: I-131/Cs-137 pair clears the release ratio and shows "—" until entered.
DEV-12: J0651 masses cited to Hermes et al. 2012; result labelled "Peters point-mass coalescence (upper bound; Brown et al.
  2011: ~0.9 Myr to contact)". T9 window unchanged (passes as locked).
DEV-13: cosmochronometry UI: log-eps input (ratio = 10^log), U/Th option, note "0.1 dex = 4.65 Gyr for Th/Eu; single-event
  assumption", negative-age guard.
DEV-14: Way-Wigner note adds "excludes U-239/Np-239 heating".
DEV-15: "Ac-225 activity at purification"; show Ac-225 at t; tritium line gives He-3 mass via the mass ratio.

DEV-16 (R78b minor, written before the fix): switching the cosmochronometry pair resets defaults (U/Th: observed -0.94 dex, production 0.57; Th/Eu: -0.52, 0.45) and the production label.

R78b verdict: NULL (all of DEV-10..15 verified).
