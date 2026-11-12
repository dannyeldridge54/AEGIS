# TOURNAMENT deviations (PREREG_TOURNAMENT.md is locked and unchanged)

## D1 (12 Nov 2026, before any tournament fit): switch-on versions use β = 0.001, not exactly 0, before z_on
In the β(z) build, CLASS's closure (shooting) solver fails whenever the early coupling is exactly 0 while a late bin is
non-zero (tested: fails at 0 and 1e-6; works at 0.001 with either closure guess). The switch-on versions (ON2, ON1,
ON05) therefore use β = 0.001 before z_on. That adds a dark-matter force of 2β² = 2×10⁻⁶ of gravity before z_on,
negligible against everything measured; the versions still act like ΛCDM until the coupling switches on. Found while
testing the code, before any fit was run; nothing else changes.
