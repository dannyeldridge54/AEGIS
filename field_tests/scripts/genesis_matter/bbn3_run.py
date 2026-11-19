import sys, json, math; sys.path.insert(0,'.')
from tools.genesis import bbn3 as B
o={}; r=B.run(); o['base']=dict(Yp=r['Yp_He'],D_H=r['D_H'],He3_H=r['He3_H'],ok=r['ok'])
o['P1']=0.235<=r['Yp_He']<=0.260; o['P2']=1.5e-5<=r['D_H']<=4.0e-5; o['P3']=0.5e-5<=r['He3_H']<=2.0e-5
lo=B.run(s=0.8); hi=B.run(s=1.2); ys=[lo['Yp_He'],r['Yp_He'],hi['Yp_He']]
o['P4']=dict(Yp=ys,spread=max(ys)-min(ys),DH=[lo['D_H'],hi['D_H']],pass_=max(ys)-min(ys)<=0.003)
a=B.run(eta=6.127e-10*0.9); b=B.run(eta=6.127e-10*1.1); sl=(math.log(b['D_H'])-math.log(a['D_H']))/(math.log(1.1)-math.log(0.9))
o['P5']=dict(slope=sl,pass_=-1.9<=sl<=-1.3)
m=B.run(dneff=0.3); o['mirror_dNeff0.3']=dict(dYp=m['Yp_He']-r['Yp_He'],DH=m['D_H'],dYp_dNeff=(m['Yp_He']-r['Yp_He'])/0.3)
print(json.dumps(o,indent=1,default=float)); json.dump(o,open('field_tests/results/GENESIS_MATTER/bbn3.json','w'),indent=1,default=float)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7.5,4.8)); Y=r['Y']; T=r['T']
for i,lab,mf in [(0,'n',1),(2,'D',2),(3,'T (tritium)',3),(4,'He-3',3),(5,'He-4',4)]: ax.loglog(T,np.maximum(mf*Y[i],1e-14),label=lab)
ax.invert_xaxis(); ax.set_ylim(1e-12,1); ax.set_xlabel('temperature (MeV)'); ax.set_ylabel('mass fraction'); ax.legend(fontsize=8)
ax.set_title(f"BBN v3: Y_p={r['Yp_He']:.4f}, D/H={r['D_H']:.2e}, He3/H={r['He3_H']:.1e}")
fig.tight_layout(); fig.savefig('field_tests/results/GENESIS_MATTER/bbn3.png',dpi=110)
