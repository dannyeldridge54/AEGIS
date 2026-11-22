# PREREG D2036: two referee checks on UFE v4 (written before computing)
The inputs are taken as written in WEAVE_UNIFIED_EQUATION v4 §2–3:
- f_vis = T_vis + 9S;
- W ⊃ A e^{−2πT_vis/6}, so the visible cycle is the KKLT-stabilised cycle;
- x = at = 21.10;
- m₃/₂ = 2.58e5 GeV;
- Minkowski vacuum (uplifted);
- V∞^{1/4} = 4.9e15 GeV.

## Check M (mirage mediation)
- **Rule** (Choi–Falkowski–Nilles–Olechowski, hep-th/0503216, eq. for D7 gauge fields with f = T): in an uplifted KKLT vacuum, F^T/(T+T̄) ≈ (n_t/2)·m₃/₂/(at). Take n_t = 2 (anti-D3) as the reference. The pure-AMSB wino is M₂ = (g₂²/16π²)·m₃/₂, with g₂² = 0.42.
- **Verdict rule:**
  - if the modulus piece exceeds the pure-AMSB wino by more than ×2 → **FAIL** of the pure-AMSB assumption. The wino/gluino chain must be recomputed with mixed modulus–anomaly (mirage) masses.
  - between ×0.5 and ×2 → **MIXED**;
  - below ×0.5 → **PASS**.
- **Escape clause, recorded in advance:** a PASS also follows if v4 states an uplift or sector that makes F^T_vis = 0 at leading order. A search of the v4 text decides this.

## Check K (Kallosh–Linde)
- **Rule** (hep-th/0411011): with a KKLT barrier ~ m₃/₂, the volume is stable during inflation only if H_inf ≲ m₃/₂ (within ×10), unless v4 contains a separate heavy stabiliser (as in the D586 mechanism of two-term SERAPIS).
- Here H_inf = V∞^{1/2}/(√3 M_P).
- **Verdict rule:**
  - H/m₃/₂ ≤ 10 → **PASS**;
  - otherwise **FAIL as written**, unless v4's W or V contains a heavy stabiliser. A search of the v4 text decides this.
