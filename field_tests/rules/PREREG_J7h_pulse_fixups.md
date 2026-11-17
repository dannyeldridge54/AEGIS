# PREREG J7h — the 6 models listed in J7f by my own driver/parameter choices, rerun into pulses 1–3
Locked 2026-11-17 before any J7h number. Same method, claims and reporting as PREREG_J7f (pulse 1) and PREREG_J7g (pulses 2–3).
(i) GMLFI (2, 1, 0.01), NCLI (1e-4, 0.18, 2), RPQTI (10, 0.01, −0.01): J7f's "compile fail" was my generated driver's Fortran
line truncation (j7g's drivers compile them with -ffree-line-length-none) — same parameters, flag added.
(ii) CNBI α = 1e-2 (its *main.f90 line 154; α = 0.1 gave only 14.5 e-folds); KMIII ν = 1e6 → α = ν^{5/3}, β = ν^{2/3}
(its *main.f90 parameterisation; α = β = 1 hit ASPIC's Lambert-branch STOP); HI ξ = 20000 rerun with a 300 s ASPIC timeout
(J7f's 60 s timed out). Results go to field_tests/results/janus_j7h*.part.jsonl and are reported as their own lines and
merged into the pulse totals in the pulse D-notes (stating which points came from J7h).
