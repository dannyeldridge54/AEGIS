# PREREG P1 — power toolkit 1: solar single-diode I–V + MPP, and an RC/RL transfer function
Locked 2026-11-18 07:38Z before building/testing. Label: tool / shared-numerics (standard EE; same ODE/root-find maths as Janus/Hyperion). No claim that SERAPIS yields energy technology.
Build tools/power/circuits.py:
 (a) solar single-diode model I = Iph − I0(exp((V+I·Rs)/(n·Vt)) − 1) − (V+I·Rs)/Rsh, Vt = kT/q; solve I(V) by bisection; sweep V, find MPP (Pmax, Vmp, Imp, FF).
 (b) first-order filters: rc_lowpass(f, R, C) and rl_lowpass(f, R, L) magnitude/phase; analytic |H|=1/sqrt(1+(2πf·τ)²).
Tests (pre-stated):
 T1 solar: with a datasheet-like cell set (Iph 8.8, I0 2e-10 A, n 1.3, Rs 0.3 Ω, Rsh 300 Ω, 60 cells at 25 °C) the model gives Voc 36–40 V, Isc ≈ 8.8 A, and Pmax within the module class 230–270 W; FF 0.70–0.80. (datasheet-plausible band, not a fit).
 T2 I(V) residual: the solved I at V=Vmp satisfies the diode equation to ≤1e-6 A.
 T3 RC: |H| at f = 1/(2πRC) equals 1/√2 to ≤1e-9; phase −45° to ≤1e-6°.
 T4 RL: same at its corner.
Adopt (register 'power_solar' + 'power_filter') if T1–T4 pass. Results: field_tests/results/p1_power.txt.
