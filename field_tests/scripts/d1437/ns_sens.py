import json, sys
C = 0.9682; P = {'rho_A1': 0.974393, 'tau_i': 0.97462}
F = {'SO': 5.6, 'SO+DESI': 4.5, 'SO+SPHEREx': 1.6, 'S4': 5.9, 'S4+DESI': 4.8, 'S4+CHIME': 3.0, 'S4+SPHEREx': 1.7,
     'S4+CHIME+DESI+SPHEREx': 1.5, 'LiteBIRD+S4(l>200)': 3.7, 'LiteBIRD+CHIME+SPHEREx': 1.2}
out = {'needed_sigma1': {k: (v-C)/3 for k, v in P.items()}, 'tension': {}}
for s, v in F.items():
    s1 = v*1e-3/2; out['tension'][s] = {k: (p-C)/s1 for k, p in P.items()}
out['reach_3sigma'] = [s for s, t in out['tension'].items() if min(t.values()) >= 3]
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print('needed', out['needed_sigma1']); [print(s, {k: round(v, 1) for k, v in t.items()}) for s, t in out['tension'].items()]; print('>=3σ:', out['reach_3sigma'])
