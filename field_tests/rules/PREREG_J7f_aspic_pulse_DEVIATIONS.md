# DEVIATIONS — PREREG_J7f_aspic_pulse
D1 (17 Nov ~06:45Z, before any Janus/exact number was produced): the start-point search scanned candidates from the FAR end
of the grid first, where the exact background needs > 4000 e-folds and each try runs to Nmax — the first model had not
finished after 2 min of CPU. Killed with no output. Fix: scan outward from ASPIC's x*(60) (nearest first) and take the first
start with ≥ 75 e-folds; everything else unchanged.
