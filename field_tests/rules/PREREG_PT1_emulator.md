# PREREG PT1 — repurpose our data: a fast SERAPIS-E emulator (n_s, r, α_s from the tilt C) at the leptogenesis T_R
Locked 2026-11-18 07:45Z before computing. Label: tool (a surrogate fit to our own locked outputs; scored against predict_fast). Repurposes the PW6 exact table (D1268, 5 points over C) which were produced by predict_fast (Janus N* + U1b exact MS) at T_R 7.389e8 GeV, MSSM g*.
Build tools/serapis_calc/emulator.py: fit quadratics n_s(u), ln r(u), α_s(u) with u = ln(C/1.25e-6), from the 5 PW6 points; emulate(C) returns n_s, r, α_s instantly.
Tests (pre-stated), leave-one-out over the 5 points (refit on 4, predict the 5th):
 T1 max |Δn_s| ≤ 2e-4; T2 max |Δr/r| ≤ 2%; T3 max |Δα_s| ≤ 5e-5; T4 emulate() runtime ≤ 1 ms/call.
Adopt (register 'serapis_emulator', fixed T_R = 7.389e8) if T1–T4 pass; label it an interpolant valid only on C 1.0–1.6e-6 at that T_R. 2-D (C,T_R) emulator = a later PT pass (needs a T_R grid from predict_fast). Results: field_tests/results/pt1_emulator.txt.
