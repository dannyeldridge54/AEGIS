# DEVIATIONS R1 (written before any rerun) — 2026-11-17
D1: The first run crashed (ZeroDivisionError). The log-Y formulation underflowed when LSODA probed large negative y. Numerical only; no result was produced.
Fix: integrate W = Y directly, dW/dx = −(λ/x²)(W² − Y_eq²), with the stiff Radau method from x0 = 3 (start at W = Y_eq), rtol 1e-8, atol 1e-20. Physics, inputs and criteria unchanged.
