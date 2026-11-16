# PREREG D976: Project H vacuum effect with the physically consistent tilt C = lambda' C0 (follows D975; complements the fixed-C lock D961)
Model: V = P3(lambda' Ehat)(1 + C Ehat), C = lambda' * C0, C0 = 1.15e-6 (so the plateau-level ramp C/lambda' equals the published fit); paper convention Ehat.
Reheating as D961: T_R = 6.7e9 GeV * lambda'^(1/4) (Gamma ∝ m ∝ sqrt(lambda'), D722 channel). N* self-consistent (nstar.py), r and n_s from ms.spectra_fast (validated for n_s, r: selftest L4e; alpha_s not reported).
Start at Ehat = 5000/lambda' (within the grid); assert Ntot >= N* + 8 (else report that lambda' cannot give N* at this C).
Runs: lambda' in {1, 0.1729, 0.05}.
PASS (fixed now): for lambda' = 0.1729: |n_s - n_s(1)| < 1e-3 and |r/r(1) - 1| < 5%. lambda' = 0.05 reported only.
Script theory/flux/projH_refitC_d976.py; output field_tests/results/projH_refitC_d976.txt.
