# DEVIATIONS for PREREG D1937 (written 21 Nov 2026 before the one rerun of the targeting step)
**Bug.** The σ_vis bisection bracket [19.5, 20.15] never reaches the wino bound. A larger σ means a smaller m₃/₂ and a lighter wino, and the wino is above 660 GeV across the whole bracket. So the result "σ at bound = 20.15" just returns the bracket end.
**Fix.** The bracket becomes [20.15, 20.40]; at 20.40 m₃/₂ drops by about e^{−20·0.0123}, putting the wino near 0.53 TeV, below 660. Only the targeting step is rerun. The Jacobian (run 1) is unaffected and kept.
