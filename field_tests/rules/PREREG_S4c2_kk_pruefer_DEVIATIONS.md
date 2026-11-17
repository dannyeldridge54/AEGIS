# DEVIATIONS — PREREG_S4c2_kk_pruefer
D1 (17 Nov ~06:37Z): the first run was killed by my 500 s shell timeout after the ε = 1e-3 interval (stiff Radau near the
singular ends is slow); printed so far: θ_end(m² = 0) − π/2 = 0 and m²₁..₃ = 0.8214, 2.6732, 5.5778 at ε = 1e-3 (the V lines
were computed but only written at the end, so they were lost). Fix: rerun the SAME script with no shell timeout in the cloud
background; method, tests and tolerances unchanged.
