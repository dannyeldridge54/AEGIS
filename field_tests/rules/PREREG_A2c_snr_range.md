# PREREG A2c (track X, Hyperion; manual Djl 17 Nov 05:59 CT): GW amplitude, SNR, horizon and BNS range vs LALSuite (written before running)
Code: tools/janus_astro/gw.py amplitude0 / snr_opt / horizon as committed with this lock (never run before it). Referee: lalsimulation (LAL 8.0.1.1) TaylorF2 waveforms and its noise PSDs.
Tests:
B1 amplitude: |h̃₊| from SimInspiralChooseFDWaveform TaylorF2 (amplitude order 0, phase order 7, inclination 0, distance 100 Mpc, zero spins) vs amplitude0 at f = 20, 50, 100, 300 Hz for (1.4, 1.4), (10, 10), (36, 29) M_⊙ (below 0.8 f_ISCO): relative ≤ 1e-6.
B2 SNR integration: snr_opt (log trapezoid, 20,000 points) vs scipy quad of the same integrand for aLIGO175MpcT1800545, (1.4, 1.4) at 100 Mpc, 10 Hz to f_ISCO: relative ≤ 1e-4.
B3 BNS range: (1.4, 1.4) M_⊙, SNR 8, 10 Hz to f_ISCO (1570.6 Hz), range = horizon / 2.2648 (Finn–Chernoff), no cosmological redshift; vs the range in each PSD's name: aLIGO140MpcT1800545 → 140, aLIGO175MpcT1800545 → 175, KAGRA25MpcT1800545 → 25, KAGRA80MpcT1800545 → 80, KAGRA128MpcT1800545 → 128 Mpc: relative ≤ 5e-2 (the T1800545 ranges are rounded and may include redshift; stated).
Pass B1–B3 → A2c VALIDATED.
Reported: BNS horizon and range for AdV O4 (T1800545), A+ design (T1800042), Einstein Telescope (P1600143) and Cosmic Explorer (P1600143) — the no-redshift Euclidean numbers, flagged as underestimating nothing but overstating the true range for ET/CE where redshift matters.
Output field_tests/results/janus_astro_a2c.txt via theory/janus_astro/a2c_check.py. No reruns to chase; DEVIATIONS first.
