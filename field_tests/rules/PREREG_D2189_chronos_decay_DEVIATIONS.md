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
