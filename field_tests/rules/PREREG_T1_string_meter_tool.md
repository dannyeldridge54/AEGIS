# PREREG T1 — toolkit: `string_meter` registry tool (inverse string meter as a callable tool)
Locked 2026-11-18 05:01Z before building/testing. Source: PW6 (D1268) exact table at T_R 7.389e8 GeV, MSSM g*.
Tool: tools/serapis_calc/meter.py → meter(ns, ns_sigma=None, T_R=7.389e8, exact=False): log-interpolates C and P = Im S·Im ρ (and linear r, α_s, N*) in the PW6 table (n_s 0.970–0.978); exact=True (or T_R ≠ 7.389e8, or n_s outside the table) runs the PW6 secant with predict_fast; with ns_sigma returns the P interval from n_s ± σ; N_eff = 4, C = 15·4/(64π⁶ P).
Registry: cubemind aegis_tools/registry.py TOOLS['string_meter'].
Tests (pre-stated): T1 table points reproduce PW6 exactly (|ΔP/P| < 1e-6); T2 at n_s 0.973 and 0.975 the interpolated P agrees with an exact secant inversion to ≤ 1 %; T3 registry call returns in ≤ 5 s (table path); T4 ns_sigma = 0.0016 at 0.9744 gives a P interval consistent with PW5's ±14 % (within a factor 1.5 of 14 %).
Adopt if T1–T3 pass. Results: field_tests/results/t1_string_meter.txt.
