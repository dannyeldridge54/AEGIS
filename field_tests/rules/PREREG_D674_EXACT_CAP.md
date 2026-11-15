# PREREG D674: exact family-wide cap from the string bound (Danny "Deeper" 11:41 CT)
Locked before computation, 2026-11-15. Script theory/modular/exact_cap_d674.py; output results/exact_cap_d674.txt.
Using the exact MS code (running_d632.py lines 1–41 verbatim): for N* ∈ {46.08, 49.21} (D602 bracket ends) find ε such that the exact horizon-exit y* = 25.00 (secant/bisection on ε, start from the D673 closed-form ε ≈ 1.98e-4, tolerance |y* − 25| < 0.01). At that ε compute n_s, r, α_s with the D632 five-point stencil. These are the maximal n_s and r of home-safe SERAPIS at τ = i over all ε (n_s and r increase monotonically with ε along the Janus curve, D673).
Report ε_max, n_s,max, r_max, α_s at the cap. If ε_max lies above the D602 window (1.6e-4), state so: the window is set by the n_s data cut, the cap by the string bound.
This cap will be frozen as a forward prediction in a separate lock (D675) only after this computation; no tuning.
