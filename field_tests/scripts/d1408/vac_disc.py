"""JANUS tick 7: Δα_s between the vacua at equal (n_s, r) via the any-kappa closed form (see PREREG)."""
import json, math, sys
P = 2.8284
rho = lambda ns, r: P*math.sqrt(r/2)/(1-ns)
a = lambda ns, r, k: -0.5*(1-ns)**2*rho(ns, r)*(1+k*(rho(ns, r)-1))
G = [(0.970+0.006*i/40, 4.4e-4+1.3e-4*j/40) for i in range(41) for j in range(41)]
D = [a(n, r, 0.5)-a(n, r, 1.0) for n, r in G]
best1 = 0.0017/2
err = max(max(0.034*abs(a(n, r, 1.0)), 0.108*abs(a(n, r, 0.5))) for n, r in G)
closed_chk = max(abs((a(n, r, 0.5)-a(n, r, 1.0))/(0.25*(1-n)**2*rho(n, r)*(rho(n, r)-1))-1) for n, r in G)
out = dict(delta_alpha_range=[min(D), max(D)], best_forecast_1sigma=best1, max_sigma_separation=max(D)/best1,
           max_relation_error=err, closed_form_check=closed_chk,
           verdict='REVIVE' if (max(D) >= 2*best1 and max(D) > err) else 'still killed')
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
