"""JANUS tick 4: band_e (n_s 0.970-0.975, r 4.55-5.12e-4) vs end-2025 CMB(+DESI) and ACT DR6 running (see PREREG)."""
import json, sys
P = 2.8284; NS = (0.970, 0.975); R = (4.55e-4, 5.12e-4)
cmb, cmbd, rmax95, act = (0.9682, 0.0032), (0.9728, 0.0029), 0.034, (0.0062, 0.0052)
N = 1001; ns = [NS[0]+(NS[1]-NS[0])*i/(N-1) for i in range(N)]
pull = lambda v, d: (v-d[0])/d[1]
frac = lambda d: sum(abs(pull(x, d)) < 2 for x in ns)/N
al = [-P*P*r/4 for r in R]
out = dict(ns_pull_cmb_desi=[pull(NS[0], cmbd), pull(NS[1], cmbd)], ns_pull_cmb=[pull(NS[0], cmb), pull(NS[1], cmb)],
           frac_in_2sigma_cmb_desi=frac(cmbd), frac_in_2sigma_cmb=frac(cmb),
           R1='PASS' if frac(cmbd) > 0 else 'FAIL', r_max=R[1], R2='PASS' if R[1] < rmax95 else 'FAIL',
           alpha_range=al, alpha_pulls=[pull(a, act) for a in al], R3='PASS' if max(abs(pull(a, act)) for a in al) < 2 else 'FAIL')
out['verdict'] = 'PASS' if all(out[k] == 'PASS' for k in ('R1', 'R2', 'R3')) else 'FAIL'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
