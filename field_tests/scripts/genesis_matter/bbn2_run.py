import sys, json, time; sys.path.insert(0,'.')
from tools.genesis import bbn2 as B
t0=time.time(); out={}
r=B.run(); out['base']=dict(Yp=r['Yp_He'],D_H=r['D_H'],ok=r['ok'])
out['P1']=0.235<=r['Yp_He']<=0.260
sp=[B.run(dd_scale=s)['Yp_He'] for s in (0.1,10)]; out['dd_x0.1_x10']=sp; out['spread']=max(sp+[r['Yp_He']])-min(sp+[r['Yp_He']]); out['P2']=out['spread']<=0.01
r3=B.run(dneff=0.3); out['dYp_dNeff']=(r3['Yp_He']-r['Yp_He'])/0.3; out['P3']=0.008<=out['dYp_dNeff']<=0.018
out['seconds']=time.time()-t0
print(json.dumps(out,indent=1,default=float))
import os; os.makedirs('field_tests/results/GENESIS_MATTER',exist_ok=True)
json.dump(out,open('field_tests/results/GENESIS_MATTER/bbn2.json','w'),indent=1,default=float)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,a=plt.subplots(figsize=(7,4.5)); a.loglog(r['T'],r['Yn'],label='free neutrons'); a.loglog(r['T'],np.maximum(r['Yd'],1e-12),label='deuterium'); a.loglog(r['T'],np.maximum(r['YHe'],1e-12),label='helium-4 (mass)')
a.invert_xaxis(); a.set_ylim(1e-8,1); a.set_xlabel('temperature (MeV)'); a.legend(); a.set_title(f"BBN v2: Y_p = {r['Yp_He']:.4f} (obs 0.245)")
fig.tight_layout(); fig.savefig('field_tests/results/GENESIS_MATTER/bbn2.png',dpi=110)
