"""JANUS tick 25: three bands x three n_s combinations (see PREREG)."""
import json, sys
data = {'CMB': (0.9682, 0.0032), 'CMB+DESI': (0.9728, 0.0029), 'P-ACT-LB2-BK18': (0.9752, 0.0030)}
bands = {'band_e': (0.970, 0.975, 5.12e-4), 'band_i': (0.970, 0.975, 5.7e-4), 'band_e_audited': (0.9717, 0.9760, 4.90e-4)}
out = {}
for b, (lo, hi, rmax) in bands.items():
    g = [lo+(hi-lo)*i/1000 for i in range(1001)]; out[b] = {'r_max': rmax, 'r_ok_0034': rmax < 0.034, 'r_ok_0038': rmax < 0.038}
    for k, (m, s) in data.items():
        f = sum(abs((x-m)/s) < 2 for x in g)/1001
        out[b][k] = dict(pulls=[(lo-m)/s, (hi-m)/s], frac=f, label='FULL' if f == 1 else ('PARTIAL' if f > 0 else 'OUT'))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for b in out:
    print(b, ' | '.join(f"{k}: {out[b][k]['label']} {out[b][k]['frac']:.0%} [{out[b][k]['pulls'][0]:+.2f},{out[b][k]['pulls'][1]:+.2f}]σ" for k in data))
