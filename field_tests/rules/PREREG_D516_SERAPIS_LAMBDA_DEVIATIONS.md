# D516 DEVIATIONS (written before rerunning)
D1. First run (kept as results/serapis_lambda_d516_run1.txt): V(i)/V_plateau came out 1.4e-61 (a = ½) and 3.6e-76 (a = 1) instead of the target 7.1e-111. That is a double-precision floor: j(i) − 1728
is ~1e-12 numerically, so the main term does not vanish at τ = i. Test (1) (inflation unchanged) was also not coded. The mass results are dominated by the main term and are kept, but the a = 1 value is
unreliable, because the main term is quartic there (zero curvature analytically) and the number is floor noise. Fix: evaluate at 50-digit precision with mpmath (η, E4, j, H) for V(i) and the Hessian;
add test (1) using the D515 code with the c-term included. Physics and criteria unchanged.
