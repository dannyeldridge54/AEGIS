# PREREG C4 — MWPotential2014 halo M200 vs Bird+2022 NFW fits (Djl C) — locked 2026-11-17
Data (quoted in D1093, arXiv:2207.08839 Table 2): M200 = 0.55 (+0.15/−0.11) e12 M_⊙ (KG Jeans) and 1.00 (+0.67/−0.33) e12 (BHB Jeans).
Assumed definition: 200 × critical density. This is a labelled assumption; the definition is not quoted.
Model: galpy NFWPotential.mvir(H = 67.66, overdens = 200, wrtcrit = True, ro = 8, vo = 220) for the MWPotential2014 halo with amplitude s ∈ {0.8, 1.0, 1.2, 1.5}. Halo only; disk and bulge are excluded (they add ~6e10 M_⊙, reported).
Pull uses the asymmetric error on the relevant side. CONSISTENT if |pull| ≤ 2 for both, TENSION if ≤ 3, else EXCLUDED.
Script theory/wiring/c4_m200.py (written after this lock).
