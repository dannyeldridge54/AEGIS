# D2113–D2115 DEVIATIONS (written before the rerun)

**D2114 crash:** fsolve stepped to a negative v, giving a math domain error in sqrt. Nothing was printed (output only happens at the end).

**Fix:** solve in log-variables (v = e^u) so that v stays positive. This is solver robustness only; the equations, inputs and criteria are unchanged. The isotropic existence criterion is also clarified to match the PREREG wording "solution exists": a sign change of the α₁ residual between adjacent v₃ grid points, refined by bisection.
