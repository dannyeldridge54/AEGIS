"""JANUS tick 16: D1234 N*(T_R) line, MSSM shift, extrapolated to the band_e_audited T_R window (see PREREG)."""
import json, math, sys
s = 50.642 - 49.878
N = lambda TR: 49.878 + s*math.log10(TR/3e8) - 0.063
lo, hi = N(5.46e8), N(1.65e10)
d = [lo-50.07, hi-51.22]
out = dict(slope_per_decade=s, ln10_over_3=math.log(10)/3, N_lo=lo, N_hi=hi, box=[50.07, 51.22], diffs=d,
           verdict='same chain' if max(map(abs, d)) < 0.10 else ('conflict' if max(map(abs, d)) > 0.20 else 'unclear'))
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
