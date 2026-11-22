# D2113–D2115 DEVIATIONS (written before the rerun)

**D2114 crash:** fsolve stepped to a negative v, giving a math domain error in sqrt. Nothing was printed (output only happens at the end).

**Fix:** solve in log-variables (v = e^u) so that v stays positive. This is solver robustness only; the equations, inputs and criteria are unchanged. The isotropic existence criterion is also clarified to match the PREREG wording "solution exists": a sign change of the α₁ residual between adjacent v₃ grid points, refined by bisection.

**Addendum (before the rerun):** a second domain error. M_s underflowed to 0 at extreme solver steps, so log(M_s/M_Z) failed. **Fix:** catch the overflow and underflow and return a large residual, which repels the solver. Robustness only; nothing printed.
