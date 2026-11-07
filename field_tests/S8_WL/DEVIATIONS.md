# S8-WL deviations (append-only)

- **2026-11-07, Part 1, implementation (rule unchanged):** S8 = σ8 √(Ωm/0.3) uses Ωm = (ω_b + ω_c + ω_ν)/h² for every
  fit. AxiCLASS's own `Omega_m` output counts a dark-energy scalar field as matter (the B0 bug, `cmb-fit/axiclass/nlfix/
  BUG_REPORT.md`) and reads 2.89 for the Spiral; for the CAMB fits both ways agree (Locked Twist 0.3002 = 0.3002).
- **Caveat reported with Part 1:** the coupled build (Spiral) closes on its actual H(0), up to 0.6% from the input h
  (theory note, closure caveat), so the Spiral's S8 carries up to ~0.005 uncertainty. It does not change any reading.
