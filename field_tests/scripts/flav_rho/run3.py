import sys, math, json, os; sys.path.insert(0,'.')
import numpy as np
from tools.serapis_calc.shapes import E
out={}
Ef=lambda t:E(t,1.5).real
def V0(t,h=1e-5):
    x,y=t.real,t.imag
    L=lambda a,b:math.log(Ef(complex(a,b)))
    dy=(L(x,y+h)-L(x,y-h))/(2*h); dx=(L(x+h,y)-L(x-h,y))/(2*h)
    return (4/9)*y*y*(dx*dx+dy*dy)
for nm,t in [('i',1j),('rho',complex(.5,math.sqrt(3)/2))]:
    out['V0_'+nm]=V0(t); out['V0_'+nm+'_nbhd']=[V0(t+d) for d in (1e-3,-1e-3,1e-3j,-1e-3j)]
w=np.exp(2j*np.pi/3)
S=np.array([[-1,2,2],[2,-1,2],[2,2,-1]])/3; T=np.diag([1,w,w**2])
out['checks']=dict(S2=float(np.abs(S@S-np.eye(3)).max()),T3=float(np.abs(np.linalg.matrix_power(T,3)-np.eye(3)).max()),ST3=float(np.abs(np.linalg.matrix_power(S@T,3)-np.eye(3)).max()))
ev,VST=np.linalg.eig(S@T)
es,VS=np.linalg.eigh(S); vplus=VS[:,np.argmax(es)]
c=np.abs(VST.conj().T@vplus)**2
out['ST_eigs']=[str(np.round(e,6)) for e in ev]; out['c']=sorted([float(x) for x in c],reverse=True)
s13=0.02195; c13=1-s13
tm2=1/(3*c13); tm1=1-2/(3*c13)
pull=lambda v:(v-0.307)/(0.012 if v>0.307 else 0.011)
out['TM2_s12']=tm2; out['TM2_pull']=pull(tm2); out['TM1_s12']=tm1; out['TM1_pull']=pull(tm1)
# Koide delta vs Q/3
import mpmath as mp
me,mm=0.51099895,105.6583755
for lab,mt in [('belle2',1777.09),('pdg',1776.93)]:
    s=[mp.sqrt(me),mp.sqrt(mm),mp.sqrt(mt)];mu=sum(s)/3;Q=float(sum(x*x for x in s)/sum(s)**2)
    A=mp.sqrt(2*(sum(x*x for x in s)/(3*mu*mu)-1));d=float(mp.acos((s[2]/mu-1)/A))
    out['delta_vs_Q3_'+lab]=dict(delta=d,Q_over_3=Q/3,diff=d-Q/3)
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/FLAV_RHO',exist_ok=True)
json.dump(out,open('field_tests/results/FLAV_RHO/run3.json','w'),indent=1)
