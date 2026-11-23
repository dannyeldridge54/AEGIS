# N12 DEVIATIONS (written before the rerun). Locked run: C1 FAIL, C2 FAIL. Referee R101 (sonnet): both are TEST errors, not physics.
- DEV-1 (my lock algebra) C1 expectation omitted the pump recirculation: dP_net = dM * P_n * (eta_th (1+f_pump) - f_pump) = 14.3277 MW (code 14.32769).
- DEV-2 (my test call) 'hold' was computed as tbr_required(1,10,1e6) = 1.0201, which is the TBR to reach 2 I0 eventually. Hold: dI/dt = 0 ->
  TBR = 1 + lambda I0 / b = 1.0101 (the locked 1.010). coverage_min recomputed with it (1.0101/1.021 = 0.989).
- Notes: M from a Pb-Li sphere applied to a DEMO plant (eta_th, f_pump calibrated at M 1.2387); P_net 4.9 MW at Q_e 1.02 is inside model
  uncertainty (sign not robust); M omits divertor/port losses; TBR omits burn fraction and residence times. The idealised TBR margin is ~1%.
