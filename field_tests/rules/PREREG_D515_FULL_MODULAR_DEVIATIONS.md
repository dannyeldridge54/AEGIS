# D515 DEVIATIONS (written before rerunning)
D1. The first run crashed before any output (OverflowError: |j| ~ e^{2π Im τ} overflows for Im τ ≳ 100). Fix: evaluate ln V in log form on the imaginary axis,
ln|j| = 2πy + ln|1 + 744q + 196884q² + 21493760q³| (q = e^{−2πy}) for y ≥ 1.5 and the direct q-series below; ln|η| = −πy/12 + Σ ln|1 − qⁿ|. Same function; no physics change.
