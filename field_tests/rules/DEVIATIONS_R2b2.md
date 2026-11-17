# DEVIATIONS R2b2 — written after the FAIL, before any further computation (2026-11-17)
Result as locked: S(0.99) = 3.94, S(1.01) = 36.2, jump 8.2 → FAIL. The scored result stands.
Hypothesis (physics, not code):
- The closed χ⁺χ⁻ channel has an attractive Coulomb tail −α/r.
- So below 2δm there is an infinite Rydberg tower of quasi-bound χ⁺χ⁻ states (Feshbach resonances in χ⁰χ⁰ → SM).
- Their energies are E_n ≈ 2δm − μα²/(2n_eff²), with μ = M/2. With n_eff = n − (quantum defect): 1 − x_n ≈ M α²/(8δm n_eff²) = 0.0917/n_eff² at M = 2000.
- Then σv below threshold swings between resonance peaks and troughs. Pointwise continuity is NOT expected.
- Only the resonance-averaged σv joins the above-threshold value (Gailitis–Damburg).
- So the locked 20% pointwise criterion was ill-posed. That is my error in the lock, not a code fix.
Diagnostic D1 (no change to any code; scored only as a diagnosis):
- Scan S(x) at 600 points uniform in n_eff = sqrt(0.0917/(1−x)) on [1.2, 8], closed side as locked.
- Find the local maxima.
- The Rydberg diagnosis is SUPPORTED iff (a) and (b) both hold:
  - (a) there are ≥4 maxima with n_eff > 2;
  - (b) the spacing of consecutive maxima in n_eff is 1.00 ± 0.10 for every pair with n_eff > 3.
- Otherwise the diagnosis FAILS, and the jump is treated as a code fault (normalisation or asymptotics) to chase next.
- No rerun of the scored test either way.
