import sys, json; sys.path.insert(0,'.')
from tools.genesis import bbn4 as B4, bbn5 as B5, bbn2 as B2
v4=B4.run(); v5=B5.run()
o=dict(v4=dict(Yp=v4['Yp_He'],D_H=v4['D_H'],Li=v4['Li_H']),v5=dict(Yp=v5['Yp_He'],D_H=v5['D_H'],Li=v5['Li_H']),
  dYp_coulomb=v5['Yp_He']-v4['Yp_He'],dDH_rel=v5['D_H']/v4['D_H']-1,
  rates_1MeV_born=B2.rates(1.0,1.0),rates_1MeV_coul=B5.rates_c(1.0,1.0))
o['pass_Yp']=0.244<=v5['Yp_He']<=0.250; o['pass_DH']=abs(o['dDH_rel'])<0.03
print(json.dumps(o,indent=1,default=float)); json.dump(o,open('field_tests/results/GENESIS_MATTER/rd1.json','w'),indent=1,default=float)
