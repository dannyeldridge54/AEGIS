# PROM-4 after R87 (no MAJOR, 3 MINOR) — wording and labels; no code change needed for the verdicts
- I1 is a CONSISTENCY check, not an independent validation: the published 569 Gbar was inferred by a 0-D/1-D hot-spot prescription
  (PRL Ref. 94) from the same yield, burn width, volume and temperature; the engine re-implements that inference (545 Gbar, -4%).
- The sphere-from-volume radius (53.5 um) is a lower-bound proxy for the paper's burn-weighted R; G_LC 1.45/1.39 are labelled "proxy".
- Derived-pressure uncertainty from the volume alone: 516-580 Gbar; with T_DD (8.94 keV) instead of T_DT: 575 Gbar.
- I5 (sqrt scaling) only checks the code against itself; it cannot fail except by a coding bug — labelled so; future F2 sensitivity
  checks must test something the change actually affects.
