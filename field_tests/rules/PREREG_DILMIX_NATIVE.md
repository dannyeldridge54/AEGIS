# PREREG DILMIX_NATIVE — referee m1: does the DILMIX in-band result survive a native tilt (C_n·x on the raw E(τ,3/2)) instead of the C·g approximation?

Locked 2026-11-19 (08:25 CT) before computing. Danny "Djl" (current focus: referee follow-ups after the harvest).
Background: PREREG_DILMIX applied the tilt as V = P(1 + C·g), g = P/(1 − P) (declared approximation, referee m1). The physical tilt
is a correction to the potential in the raw modular variable x = λ(E(τ,3/2) − E(ρ,3/2)), i.e. V = P(x)·(1 + C_n·x), P = α x/(1+x) + (1−α)(1 − 1/(1+x)²).
Analytic map (derived before computing): 1 − P = α/(1+x) + (1−α)/(1+x)², so g = x/α · [1 + O(1/(αx))] and C·g → (C/α)·x.
Checked on the grid: g·α/x = 0.934, 0.978, 0.993 at x = 30, 100, 300 (α = 0.25); 0.984, 0.995, 0.998 (α = 0.5).
Runs (cloud, same engine/start rule/T_R = 8.94e8/λ = 1 as PREREG_DILMIX; only the tilt term changes):
  N1: α 0.25, C_n = 5.0e-6 (= 1.25e-6/0.25)    N2: α 0.5, C_n = 2.5e-6 (= 1.25e-6/0.5)
Rule: "AGREE" if |Δn_s| ≤ 0.002 and |Δr|/r ≤ 10 % against the matching C·g rows (DILMIX a0.25_C1.25e-06, a0.5_C1.25e-06); then m1 is
closed with the map C_n = C/α (and the in-band flag is re-read under the native form). Else "DISAGREE": the C·g approximation is
retired and in-band claims must be redone natively. Also report in band / near per PREREG_SMSCAN.
Expectation stated now: AGREE, with n_s slightly LOWER natively (g·α/x < 1 at finite x ⇒ C·g is the weaker tilt only if dg/dx·α < 1; sign not
certain — the slope term decides).
No reruns to chase results; fixes only via PREREG_DILMIX_NATIVE_DEVIATIONS.md written first.
