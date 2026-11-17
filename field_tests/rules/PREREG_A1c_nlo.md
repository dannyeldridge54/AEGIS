# PREREG A1c — NLO wino potential: reproduce the 2.419 TeV resonance (Djl A) — locked 2026-11-17
Source: Beneke, Szafron, Urban 2020 (arXiv:2009.00640), Eqs. 2.8, 3.14, 3.18, 3.25, 3.26 as recorded in PREP_A (14:20 UTC entry). Their LO resonance 2.282 TeV was reproduced in A1b (2.2855).
Code (written after this lock): tools/janus_astro/sommerfeld_nlo.py. It is wino_s with V_{00,+−} += δV_{00→+−} (3.25) and V_{+−,+−} += δV_{+−→+−} (3.26). Inputs as A1b.
PRIMARY convention: δV_{00→+−} added to the matrix entry as is. Alternative, reported only: ×√2.
Peak finder as A1b (σv_tot ∝ (2s₀² + 2√2 s₀s₁ + 3s₁²)/M², v = 1e-6), scan [2.25, 2.65] TeV.
- T0 (sanity, scored): with the NLO terms switched off, the code returns A1b's 2.2855 TeV to 1e-4.
- T1 (scored): primary NLO peak within 1% of 2.419 TeV.
A1c VALIDATED iff T0 and T1. If T1 fails, report both conventions and stop; no tuning. Fixes only via DEVIATIONS.
Reported: the NLO CMB band shift for D1081/D1087 (a real computation if T1 passes).
