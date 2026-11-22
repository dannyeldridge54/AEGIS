# D2088 DEVIATIONS (written before any rerun)

**Run 1: the control FAILED.** With one-loop RGEs, λ crosses zero at 9.15e7 GeV, outside the locked window [3e8, 3e11]. Its tan β results (1.7–1.9) are **void**, not scored, and kept here as a record only.

**Fix:** add two-loop terms (convention V = λ|H|⁴; m_h² = 2λv²), with k = 1/16π²:
- **Gauge:** the full SM two-loop matrix b_ij, as in tools/seed/twoloop.py, plus top-Yukawa pieces −(17/10, 3/2, 2)y_t² in GUT normalisation (g′² = (3/5)g₁²).
- **β_yt⁽²⁾ (leading only):** y_t k²[−12y_t⁴ + 36g₃²y_t² − 108g₃⁴ + 6λ² − 12λy_t²]
- **β_λ⁽²⁾ (leading only):** k²[−312λ³ − 144λ²y_t² − 3λy_t⁴ + 30y_t⁶ − 32g₃²y_t⁴ + 80g₃²λy_t²]

**Stated:** the electroweak-gauge cross terms in β_yt⁽²⁾ and β_λ⁽²⁾ are dropped. They are subleading; the control window tests whether this is adequate.

**Rules unchanged:** the same control window; if it fails again, stop, and give the literature reading only.
