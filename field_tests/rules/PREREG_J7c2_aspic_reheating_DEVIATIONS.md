# DEVIATIONS — PREREG_J7c2_aspic_reheating
D1 (before any output): first run crashed (math domain error) because the Janus root bracket [20, 90] e-folds exceeded
the background's total e-folds (≥ 75) for model 1. Fix: upper bracket min(90, N_total − 1). No method change.
