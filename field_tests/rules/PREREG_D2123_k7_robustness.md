# PREREG D2123: checklist item 9, robustness of the gauge-coupling-matching FAIL (ping-pong: referee R9-1…R9-3 folded in). Locked before computing.

**Primary model** (D2119): threshold reading A (consistent), reduced M_Pl, 2π normalisation. Metric: min ctrl = max|δ|/T over the matching curve (SLSQP, 40 starts, fsolve re-verification). Criterion unchanged: controlled ⇔ < 0.3.

**Running (R9-2):**
- SM 2-loop from M_Z to M_SUSY, then MSSM 2-loop up to M_s, with the standard b_i and b_ij.
- Top-Yukawa 2-loop term (SM a = (17/10, 3/2, 2); MSSM a = (26/5, 6, 4)), with y_t run at one loop from y_t(M_Z) = 0.94.
- MS-bar → DR-bar at M_SUSY: α_i⁻¹ −= C₂/(12π), with C₂ = (0, 2, 3).
- No constant term at the PS matching (DR-bar).
- Inputs: PDG α_em⁻¹ = 127.951, sin²θ_W = 0.23122, α_s = 0.1180.

**Cases:**

| Case | Running | M_SUSY | Bound | Reading | Exotics |
|---|---|---|---|---|---|
| R0 | 1-loop | (as D2119) | v_i ≥ 1 | A | — |
| R1 | 2-loop | 1 TeV | v_i ≥ 1 | A | — |
| R2 | 2-loop | 10 TeV | v_i ≥ 1 | A | — |
| R3 | 2-loop, 1 TeV | 1 TeV | v_i ≥ 1 | A | PS-vector-like exotics at M_X = M_s/100: one-loop shift −Δb_i ln(100)/2π with Δb = (4.6, 5, 4) (D2112 S2 content) |
| R4 | 2-loop | 1 TeV | **v_i ≥ ½** | A | — |
| R5 | 2-loop | 1 TeV | **v_i ≥ ¼** | A | — |
| R6 | 2-loop | 1 TeV | v_i ≥ 1 | **B** | — |

R4 and R5 are informational: v < 1 is outside geometric control. R6 is the demoted reading.

**Verdict:** item 9 = **FAIL (robust)** if R0–R3 all give min ctrl ≥ 0.3; otherwise "not robust", listing the case that crosses. R4–R6 are reported as sensitivities.
