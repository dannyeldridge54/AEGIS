"""PREREG_S2_FLUXCOEF"""
import sys, math, json
sys.path.insert(0, 'tools/weave_cm'); import weave_tools as W
gs = 2 / math.sqrt(3); MP = 2.435e18; C = 8e-7; w = 2 / 3; ainv = 28.9
out = {}
for c in (6, 9, 12):
    flux = c / gs; ReT = ainv - flux; x = flux / ainv; TR = x * 1.34e9
    g = W.weave_genesis({'T_R_GeV': TR}); wf = W.weave_wino({'T_R_GeV': TR}); f, lim = wf['fraction'], wf['limit']
    d0, d1 = f['0.66'] - lim['0.66'], f['1.0'] - lim['1.0']
    if d0 > 0: edge = None
    elif d1 <= 0: edge = '>=1.0'
    else: edge = math.exp(math.log(0.66) + math.log(1.0 / 0.66) * (-d0) / (d1 - d0))
    centre = (0.67 + (edge if isinstance(edge, float) else 1.0)) / 2 if edge is not None else None
    chis = {}
    if centre:
        for N in range(5, 11):
            W0 = math.exp(-2 * math.pi * ReT / N); K = math.sqrt(gs / 2) * W0 * MP / 375 / 1e3 * 4 * (2 * math.pi) ** 3 * C / w
            chi = K / centre
            if 20 <= chi <= 500: chis[N] = round(chi, 1)
    out[f'c={c}'] = dict(flux_part=flux, ReT=ReT, x=x, T_R=TR, M_N_min=g['M_N_min_GeV'], wino_f={'0.66': f['0.66'], '1.0': f['1.0']},
                         wino_window_TeV=None if edge is None else [0.67, edge], chi_for_window_centre=chis)
out['robust'] = all(v['chi_for_window_centre'] for v in out.values())
print(json.dumps(out, indent=1, default=str))
