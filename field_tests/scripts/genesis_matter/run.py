import json, os, math, numpy as np, sys
sys.path.insert(0,'.')
from tools.genesis import genesis as G
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
eta=G.eta_from_obh2(); out={'eta':eta}
out['T1']={str(s):G.dm_mass(sharing=s) for s in (1/3,0.5,1,2,3)}
b=G.bbn(eta); out['T2']=dict(Yp=b['Yp'],TD_MeV=b['TD'],tD_s=b['tD'],pass_=0.235<=b['Yp']<=0.260)
zr=G.recombination_z(eta); out['T3']=dict(z=zr,pass_=1250<=zr<=1500)
xi=(0.3/7.4)**0.25; dn=G.mirror_dneff(xi); b2=G.bbn(eta,dneff=dn)
out['T4']=dict(xi_max=xi,dneff=dn,Yp_shift=b2['Yp']-b['Yp'],viable=xi>0.3)
print(json.dumps(out,indent=1,default=float))
os.makedirs('field_tests/results/GENESIS_MATTER',exist_ok=True)
json.dump(out,open('field_tests/results/GENESIS_MATTER/out.json','w'),indent=1,default=float)
fig,ax=plt.subplots(2,2,figsize=(11,8))
a=ax[0,0]; a.semilogx(b['T'],b['Xn'],label='neutron fraction'); a.axvline(b['TD'],ls='--',c='gray'); a.invert_xaxis()
a.set_xlabel('temperature (MeV)'); a.set_title(f"BBN [toy]: Y_p = {b['Yp']:.3f} (obs 0.245)"); a.legend()
a=ax[0,1]; zz=np.linspace(900,2000,200); a.plot(zz,[G.saha_xe(z,eta) for z in zz]); a.axvline(zr,ls='--',c='gray')
a.set_xlabel('redshift z'); a.set_ylabel('ionized fraction'); a.set_title(f'Recombination [Saha toy]: z = {zr:.0f}'); a.invert_xaxis()
a=ax[1,0]; s=np.geomspace(0.25,4,100); a.loglog(s,[G.dm_mass(sharing=v) for v in s]); a.axvline(1,ls='--',c='gray')
a.set_xlabel('sharing n_DM/n_B'); a.set_ylabel('dark-baryon mass (GeV)'); a.set_title('P-M: one asymmetry → m_DM (5.0 GeV at equal)')
a=ax[1,1]; xs=np.linspace(0,1,100); a.plot(xs,G.mirror_dneff(xs)); a.axhline(0.3,ls='--',c='r'); a.set_ylim(0,2)
a.set_xlabel('mirror temperature ratio ξ'); a.set_ylabel('ΔN_eff'); a.set_title(f'P-M constraint: ξ < {xi:.2f}')
fig.suptitle('Weave matter genesis — one asymmetry, then the element ladder'); fig.tight_layout()
fig.savefig('field_tests/results/GENESIS_MATTER/genesis.png',dpi=110)
G.sonify('field_tests/results/GENESIS_MATTER/ladder.wav')
