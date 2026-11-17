# PREREG R2b — two-channel Sommerfeld with both channels open (relic stage R2b) — locked 2026-11-17
Code (written after this lock): sommerfeld.two_channel_open(M, v, Vfun, dm, tails).
- Channels (χ⁰χ⁰, χ⁺χ⁻). The χ⁺χ⁻ threshold is 2δm, and both channels are open for E = Mv²/4 > 2δm.
- Two regular solutions are integrated from r₀ (u = r e_j). At large R each channel is decomposed into incoming/outgoing waves with WKB-local k_j(R).
- The physical solution for incoming channel i has an incoming amplitude −1/(2ik_i) e^{−ik r} in channel i only.
- s_{i·} = u'(0) of that solution. Free normalisation: s = identity.
Tests (scored):
- T1: V = 0 gives s = I to 1e-6 (M = 2000, v = 0.1, 0.3).
- T2: with the off-diagonal set to 0 and dm = 0, each diagonal entry |s_ii|² equals single_channel for that channel's potential to 1e-4 (wino LO diagonal potentials, v = 0.1, 0.3).
Reported (not scored):
- T3: threshold continuity. |s_{00,00}|² from two_channel_open just above threshold (E = 1.01·2δm) vs wino_s (closed channel) just below (E = 0.99·2δm), M = 2000.
- The full wino LO s at v = 0.1, 0.3, and the resulting σv for χ⁰χ⁰ and χ⁺χ⁻ incoming.
R2b VALIDATED iff T1 and T2 pass.
