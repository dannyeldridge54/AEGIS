# PREREG L2 — Janus-LT linear growth D(z), f(z), σ8(z)/σ8(0) vs CAMB
Locked 2026-11-17 before any L2 number.
Equation (fetched, arXiv:2602.08207 Eqs. 5–7): D″ + (2 + dlnH/dlna) D′ − (3/2)Ω_m(a) D = 0 in x = ln a, Ω_m(a) =
Ω_m0 H0²/(a³H²), f = dlnD/dlna; σ8(z) = σ8 D(z)/D(0). Ω_m0 = (ω_b + ω_c)/h² (massless ν; radiation in H only);
start in matter domination at a = 1e-3 with D = a(1 + small radiation term ignored) and D′ = D (growing mode, stated).
Reference: CAMB 2.0.5 (massless ν, PPF dark energy), get_results with matter power to k = 2 h/Mpc; σ8(z) at
z ∈ {0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0}; ratio σ8(z)/σ8(0) vs D(z)/D(0); f compared with CAMB's fsigma8/sigma8 (get_fsigma8).
Cosmologies: 20 of the L0a seeded set (first 10 ΛCDM-like by setting w0 = −1, wa = 0; next 10 as drawn w0–wa).
Tests: T1 ΛCDM: |Δ(D ratio)| ≤ 2e-3 and |Δf/f| ≤ 3e-3 at all z; T2 w0–wa: report (CAMB's PPF dark-energy perturbations
and scale dependence from baryons/radiation make exact agreement impossible for a scale-independent D; report max).
Verdict L2 VALIDATED iff T1.
