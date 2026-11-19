import sys, json, math; sys.path.insert(0,'.')
from tools.genesis import bbn4 as B4, bbn3 as B3
o={}; r=B4.run(); v3=B3.run()
o['base']=dict(Yp=r['Yp_He'],D_H=r['D_H'],He3_H=r['He3_H'],Li_H=r['Li_H'],Be_frac=r['Be_frac'],ok=r['ok'])
o['L1']=3e-10<=r['Li_H']<=7e-10
o['L2']=dict(dYp_rel=r['Yp_He']/v3['Yp_He']-1,dDH_rel=r['D_H']/v3['D_H']-1,pass_=abs(r['Yp_He']/v3['Yp_He']-1)<0.005 and abs(r['D_H']/v3['D_H']-1)<0.005)
o['L3']=r['Be_frac']>=0.5
m=B4.run(dneff=0.3); o['M1']=dict(Li_H=m['Li_H'],rel=m['Li_H']/r['Li_H']-1,solves=abs(m['Li_H']/r['Li_H']-1)>=0.10)
# M2: rho_DM/rho_rad at T=0.07 MeV. rho_DM ∝ a^-3 ; matter-radiation equality T_eq ≈ 0.80 eV (z_eq=3400) -> ratio ≈ (T_eq/T)*(g_s factor ~1)
Teq=2.7255*8.617e-5*3402; o['M2']=dict(ratio=Teq/0.07e6,negligible=Teq/0.07e6<1e-3)
o['spite_obs']=1.6e-10; o['problem_factor']=r['Li_H']/1.6e-10
print(json.dumps(o,indent=1,default=float)); json.dump(o,open('field_tests/results/GENESIS_MATTER/li7.json','w'),indent=1,default=float)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7.5,4.8)); Y=r['Y']; T=r['T']
for i,lab,mf in [(2,'D',2),(4,'He-3',3),(5,'He-4',4),(6,'Be-7',7),(7,'Li-7',7)]: ax.loglog(T,np.maximum(mf*Y[i],1e-16),label=lab)
ax.axhline(7*1.6e-10*0.75,ls=':',c='k',lw=1,label='Li observed (Spite, mass)')
ax.invert_xaxis(); ax.set_ylim(1e-14,1); ax.set_xlabel('temperature (MeV)'); ax.set_ylabel('mass fraction'); ax.legend(fontsize=8)
ax.set_title(f"BBN v4: Li/H={r['Li_H']:.2e} vs observed 1.6e-10 (×{r['Li_H']/1.6e-10:.1f})")
fig.tight_layout(); fig.savefig('field_tests/results/GENESIS_MATTER/li7.png',dpi=110)
