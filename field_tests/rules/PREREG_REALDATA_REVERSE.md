# PREREG_REALDATA_REVERSE — "reverse everything": reversed versions of the Weave thread on the same real data (locked D1693, 2026-11-20 01:20 UTC)
Danny 19:11: "Make a model based off ours" / "Try to reverse everything".
Same data and likelihood as PREREG_REALDATA_NEG (imported, unchanged). Each reversal is a one-line change to the Weave thread M2:
- R1 FLIPPED PLATEAU (reverse the sign of the step): V = V_Λ(1 + 7.30e^{−βφ}). The field rolls DOWN onto the plateau from above, so w leaves −1 and then FREEZES back toward −1 (the reverse of thawing). Params: Ω_m, amp.
- R2 REVERSED ROLL (reverse the direction): the original V, but the field starts with an initial velocity pointing UPHILL (toward the plateau): it climbs, slows and freezes. Params: Ω_m, amp, initial kinetic fraction k_i ∈ [0, 0.9] of the field's energy at a = 10⁻³.
- R3 REVERSED TIME ORDER of the thread's history: the thread's best-fit w(a) from D1692, reflected as w_R3(a) = w_D1692(a_mirror), with a_mirror = 1/3 + 1 − a over a ∈ [1/3, 1] and w = w(a = 1/3) before that. Params: Ω_m only (shape fixed from D1692). NOTE: R3 uses D1692's fitted shape, so it is post-hoc by construction; reported, not scored as a prediction.
β = 2√2 throughout. Reported: χ²_min and Δχ² versus ΛCDM (1645.33) and versus the Weave thread (1638.32).
Reading set in advance: a reversed model "BEATS ours" if Δχ² < −2 versus the thread at equal or fewer parameters (R1, R3); R2 has one more parameter, so it needs < −2.3.
Script: field_tests/scripts/realdata/reverse.py (background).
