import sys, math, cmath, json, os; sys.path.insert(0,'.')
from tools.serapis_calc.shapes import E
Ef=lambda t:E(t,1.5).real
z3=1.2020569031595942
g=lambda t:(t-1)/t
def orbit(t): return [t,g(t),g(g(t))]
def dyl(t,h=1e-6):
    return t.imag*(math.log(Ef(complex(t.real,t.imag*(1+h))))-math.log(Ef(complex(t.real,t.imag*(1-h)))))/(2*h*t.imag)
K={'K1':lambda t:t.imag**1.5,'K2':lambda t:t.imag**-0.5,'K3':lambda t:2*z3*t.imag**1.5/Ef(t),
   'K4':lambda t:dyl(t),'K5':lambda t:(2/3*dyl(t))**2}
def Neff(v): return sum(abs(x) for x in v)**2/sum(x*x for x in v)
rho=complex(0.5,math.sqrt(3)/2); out={'orbit_check':[str(x) for x in orbit(rho)]}
pts={}
for e in (0.05,0.1,0.2,0.3):
    for ph in (0,90,180,270): pts[f'rho+{e}@{ph}']=rho+e*cmath.exp(1j*math.radians(ph))
pts.update({'i':1j,'2i':2j,'5i':5j})
for name,t in pts.items():
    o=orbit(t); out[name]={k:round(Neff([f(x) for x in o]),6) for k,f in K.items()}
res={}
for k in K:
    vals=[out[n][k] for n in pts if n.startswith('rho')]
    a=all(abs(v-1.5)<=0.0015 for v in vals); b=abs(out['i'][k]-1.5)<=0.0015; c=abs(out['5i'][k]-1.5)<=0.0015
    res[k]=dict(all_eps=a,at_i=b,cusp=c,PASS=a or b or c)
out['verdict']=res
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/WEAVE_INDEX',exist_ok=True)
json.dump(out,open('field_tests/results/WEAVE_INDEX/out.json','w'),indent=1)
