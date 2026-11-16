# PREREG D878: inflaton channel ratio b at ρ from the D725 2⊕1 couplings
Locked before computing, 2026-11-16.
Identification [derived, D780]: the exactly degenerate light pair is the Z₃-charged Dirac pair (N_n: q, N₃: −q); the heavy state is N_Y (charge 0). The two Z₃-allowed channels are LL (= φ → N_nN_n, ΔB = +2 under baryon triality) and HL (= φ → N_Y N₃, ΔB = −1).
Code: D725's script (tr_2p1_d725.py) verbatim for couplings, masses and widths, with the per-channel widths Γ_LL (sum over light-light entries) and Γ_HL (sum over heavy-light entries) printed separately; c ∈ {0.3, 1, 3}, M_heavy ∈ {1e12, 1e13, 5e13} where open.
Output: b = Γ_LL/(Γ_LL + Γ_HL), f = |3b − 1|.
Verdict rule: the D877 route is NATURAL for a case if f ∈ [1.4e-4, 1.1e-2] (D877's required range) without tuning c or M; "needs tuning" if f lies outside that range in all open cases; report the c needed for f = 1e-3 if it exists.
Prediction (pre-stated): b is not near 1/3 generically (f = O(0.1–1)); no structure enforces b = 1/3.
