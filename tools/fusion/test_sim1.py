"""SIM-1 tests A1-A5, B1-B3, run once as locked."""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F, fusion_fast as X, sim as S
t0 = time.time(); m = F.ITER; n = m['n_avg']; EA = S.EA; rel = lambda a, b: abs(a - b) / abs(b)
op50 = X.operating_point_fast(m, EA, P_aux=50.0); op40 = X.operating_point_fast(m, EA, P_aux=40.0)
Paux = lambda t: 50.0 if t < 200 else 40.0
sol, tr = S.burn(m, n, Paux, op50['Te_avg'] * 0.98, 0.02, 400.0, t_eval=[0, 50, 100, 150, 199.9, 210, 220, 240, 260, 300, 350, 400])
at = {round(r['t'], 1): r for r in tr}; s200, s400 = at[199.9], at[400.0]
A1 = dict(P_fus=rel(s200['P_fus'], op50['P_fus']), T=rel(s200['T'], op50['Te_avg']), f_He=rel(s200['f_He'], op50['f_He']))
A2 = dict(P_fus=rel(s400['P_fus'], op40['P_fus']), T=rel(s400['T'], op40['Te_avg']), f_He=rel(s400['f_He'], op40['f_He']))
# settling time after the step: first t where P_fus within 1% of the new steady value
fine = S.burn(m, n, lambda t: 40.0, op50['Te_avg'], op50['f_He'], 200.0, t_eval=[i * 0.5 for i in range(401)])[1]
settle = next((r['t'] for r in fine if abs(r['P_fus'] / op40['P_fus'] - 1) < 0.01 and all(abs(q['P_fus'] / op40['P_fus'] - 1) < 0.01 for q in fine if q['t'] >= r['t'])), None)
A3 = {}
for k in (1.1, 0.9):
    tr3 = S.burn(m, n, lambda t: 50.0, op50['Te_avg'] * k, op50['f_He'], 200.0, t_eval=[0, 10, 50, 100, 200])[1]
    A3[f'start_x{k}'] = dict(T_end=tr3[-1]['T'], P_fus_end=tr3[-1]['P_fus'], returns=abs(tr3[-1]['P_fus'] / op50['P_fus'] - 1) < 0.01)
# A4 helium e-folding from f_He 0 at fixed operating temperature region
tr4 = S.burn(m, n, lambda t: 50.0, op50['Te_avg'], 1e-4, 200.0, t_eval=[i * 0.25 for i in range(801)])[1]
target = op50['f_He']; t63 = next(r['t'] for r in tr4 if r['f_He'] >= (1 - math.exp(-1)) * target)
A4 = dict(t63=t63, five_tauE=5 * op50['tau_E'])
W0, W1, E = tr[0]['W'], tr[-1]['W'], tr[-1]['E_net']; A5 = dict(dW=W1 - W0, integral=E, rel=abs((W1 - W0) - E) / max(abs(W1 - W0), 1e-9))
tbr = F.tbr_required(1.0, 10.0, 5.0); s, k = S.tritium_life(1.0, 10.0, tbr, 20.0)
import numpy as np
I5 = float(np.interp(5.0, s.t, s.y[0])); I, bred, burned, decayed = s.y[:, -1]
B1 = dict(TBR=tbr, I_5y=I5, rel=abs(I5 / 20 - 1)); B2 = dict(closure=abs((10 + bred - burned - decayed) - I) / I)
B3 = dict(TBR_min_hold=1 + k['lam'] * 10.0 / k['b'], I_20y=I)
r = dict(op50=dict(P_fus=op50['P_fus'], T=op50['Te_avg'], f_He=op50['f_He'], tau_E=op50['tau_E']), A1=A1, A2=A2, A2_settling_s=settle, A3=A3, A4=A4, A5=A5, B1=B1, B2=B2, B3=B3,
         seconds=round(time.time() - t0, 1))
r['verdict'] = dict(A1=max(A1.values()) <= 1e-3, A2=max(A2.values()) <= 1e-3, A5=A5['rel'] <= 1e-5, B1=B1['rel'] <= 1e-6, B2=B2['closure'] <= 1e-9)
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'sim1.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
