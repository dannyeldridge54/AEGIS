# PREREG SIM-1 — time-dependent simulations on the fusion engine (locked before build/run), 2026-11-23 12:45 CT
Danny 11:27: "get all the way through the derivations, testing, and then run simulations."
SIM-A 0-D burn dynamics (ITER 500 MW machine, fast S3 path): state = thermal energy W and helium ion count N_He; density held by
  fuelling; T_e from W by inverting W(T) at fixed n and f_He. dW/dt = P_alpha + P_aux - C3 P_rad,core - W/tau_E(P_L);
  dN_He/dt = S_alpha - N_He/(5 tau_E). Integrator: scipy solve_ivp (LSODA), rtol 1e-8.
  A1 steady state of the ODE (t = 200 s) equals operating_point to rel 1e-3 in P_fus, T, f_He.
  A2 step P_aux 50 -> 40 MW at t = 200 s: the new steady state equals operating_point(P_aux = 40) to rel 1e-3; report the settling time.
  A3 thermal stability: start at T x 1.1 and x 0.9: report whether the burn returns to the operating point (stable) or runs away.
  A4 helium ash e-folding time reported vs 5 tau_E.
  A5 energy bookkeeping: W(t1) - W(t0) = integral of (sources - losses) dt to rel 1e-5.
SIM-B tritium inventory over plant life (S5 + Chronos half-life): dI/dt = (TBR - 1) b - lambda I, 1 GW, I0 = 10 kg, 20 years.
  B1 with TBR from tbr_required(1 GW, 10 kg, 5 y), I(5 y) = 20 kg to rel 1e-6. B2 mass bookkeeping closes to rel 1e-9.
  B3 report the minimum TBR that keeps the inventory from falling (lambda I0 / b).
Fails recorded as failed-as-locked; DEVIATIONS first; one rerun. Simulations go to the referee.
