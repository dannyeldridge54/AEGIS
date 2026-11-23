# N1 DEVIATIONS (written before the rerun). Locked run: B1-B4 PASS.
Referee R93 (sonnet, read-only; 4 seeds in /tmp): physics sound, pass real, caveats:
- DEV-1 statistics: shift residual seed-to-seed sd 1.5% / 0.45% / 0.27% at 5 / 10 / 20 keV (heavy-tailed weights); FWHM 0.23 / 0.12 / 0.05%.
  Rerun: 8 seeds x 2e6, report mean +- sd; claims limited to that precision.
- DEV-2 width definition: Ballabio's FWHM may be moment-based or a true half-maximum; rerun also measures the direct half-maximum width from a
  weighted histogram (1 keV bins) and reports both.
- Notes: B2 is nearly insensitive to the reactivity weighting (tests kinematics + Maxwellians); B4 nearly tautological (same mass formula);
  B3 is the real can-fail. exp overflow at E floor harmless (sigma -> 0). JSON bool cast cosmetic.
