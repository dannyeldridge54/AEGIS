# PREREG D2039: the known-issues battery, every goalpost set before running, then tuned live by hand-on knobs (Centre)
**The model:** a one-loop estimate, theory/tests/d2039_battery.py.
- Gaugino masses: M_a = g_a²[M₀/g_G² + b_a m₃/₂/16π²], with M₀ = sq·(n_t/2)·m₃/₂/at, at = 21.10.
- α_s = 1/[1/(0.1142 + 0.0864(Δ₃ + 0.094)) + δ_thr], where δ_thr comes from the gluino and wino thresholds relative to v4 (D2037 formula).
- Approximation, stated in advance: m₃/₂ enters only through the gaugino thresholds, not through the full D1937 Jacobian.
- m_T = boost · a²A e^{−x} M_P/√(2σ); H_inf = 5.69e12 GeV.

## Goalposts (all must pass)
| id | issue | goalpost |
|---|---|---|
| G1 | α_s miss | \|z_PDG\| ≤ 2 |
| G2 | mirage leak (D2036 M) | M₀ / (AMSB wino) ≤ 0.5 |
| G3 | Kallosh–Linde (D2036 K) | m_T / H_inf ≥ 0.1 |
| G4 | wino | 0.670 ≤ M₂ ≤ 0.70 TeV (LHC; the v4 T_R-box bar) |
| G5 | gluino | ≥ 2.25 TeV |
| G6 | knob honesty | each knob moved off its v4 value is a fitted knob (FIT). NAILED requires 0 moved |

**Knobs (5, at most 9):**
- `m32` (× multiplier on m₃/₂);
- `d3` (Δ₃, the seam);
- `sq` (fraction of F^T_vis reaching the gauginos: 1 = KKLT as written);
- `nt` (uplift: 2 = anti-D3);
- `boost` (extra stabiliser factor on m_T: 1 = none).

**Cost** = Σ (goalpost violation in σ-units)² + ½ ln N per moved knob (N = 21).

**Read-out:** the knob point the Centre reaches; which goalposts pass; which knobs had to move. Moved knobs name the physics still to be derived.

**Data-only issues** (no knob; listed for B3/B14): the δ_CP source conflict, the running conflict, the Σm_ν FC limit, θ₁₂ at +1σ, the tadpole red flag, g_s > 1.
