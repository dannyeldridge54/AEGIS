import json
UL={'SO':99e-4,'SO+SPHEREx':98e-4,'S4':34e-4,'S4+SPHEREx':33e-4,'LiteBIRD':0.98e-4,'LiteBIRD+S4(l>200)':0.98e-4,'LiteBIRD+S4+CHIME+SPHEREx':0.97e-4}
R={'band_min':4.55e-4,'A1_exact':4.82095e-4,'NA12_exact':4.8335e-4,'band_max':5.7e-4}
out={}
for s,u in UL.items():
    out[s]={'UL95':u,'sigma_onesided':u/1.645,'sigma_twosided':u/1.96,
            'S_onesided':{k:r/(u/1.645) for k,r in R.items()},'S_twosided':{k:r/(u/1.96) for k,r in R.items()}}
for s,v in out.items(): print(f"{s:28s} S(4.55e-4) {v['S_onesided']['band_min']:6.2f}-{v['S_twosided']['band_min']:6.2f}  S(5.7e-4) {v['S_onesided']['band_max']:6.2f}-{v['S_twosided']['band_max']:6.2f}")
json.dump({'D':'D1438','r':R,'surveys':out},open('field_tests/results/D1438_r_floor.json','w'),indent=1)
