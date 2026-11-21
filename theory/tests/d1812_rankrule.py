import math, json
sv, N = 20.15, 6; sd = 2 * N / N * sv
aD = 1 / (sd + (4 / 3) / (2 * math.pi) * math.log(1.06e16 / 12.8))
Vreq = 1e5 * (3.9e-4 / 1.66e-6) ** 2
out = dict(sigma_d=sd, in_window=36.9 <= sd <= 40.6, alphaD_12GeV=aD, V_required=Vreq, V_visible=7.5e4, ratio=Vreq / 7.5e4)
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1812_rankrule.json', 'w'), indent=1)
