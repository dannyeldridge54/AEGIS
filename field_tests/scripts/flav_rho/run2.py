import sys, math, json, os; sys.path.insert(0,'.')
from tools.serapis_calc.shapes import E
out={}
Ef=lambda t:E(t,1.5).real
rho=complex(0.5,math.sqrt(3)/2)
def V(t,C=8e-7,h=1e-5):
    y=t.imag; L=lambda yy:math.log(Ef(complex(t.real,yy)))
    yd=y*(L(y*(1+h))-L(y*(1-h)))/(2*h*y)
    Lx=lambda xx:math.log(Ef(complex(xx,y))); xd=(Lx(t.real+h)-Lx(t.real-h))/(2*h)
    V0=(4/9)*(yd**2 + (y*xd)**2)   # |∇lnE|² with metric 2y²(dx²+dy²)·(1/2)... = (4/9)y²(∂x²+∂y²)lnE·
    return V0*(1+C*(Ef(t)-Ef(rho)))
out['V_rho']=V(rho)
for d in (1e-3,1e-3j,-1e-3,-1e-3j): out[f'V_rho+{d}']=V(rho+d)
# (2) TBM vs NuFIT 6.0 NO IC19
nf={'s12':(0.307,0.012,0.011),'s13':(0.02195,0.00054,0.00058),'s23':(0.561,0.012,0.015)}
tbm={'s12':1/3,'s13':0.0,'s23':0.5}
pulls={}
for k,(b,up,dn) in nf.items():
    v=tbm[k]; pulls[k]=(v-b)/(up if v>b else dn)
pulls['s23_IC24']=(0.5-0.470)/0.017
out['TBM_pulls']=pulls; out['TBM_pass']=all(abs(p)<3 for k,p in pulls.items() if k!='s23_IC24')
# (3) theta = pi
r={}
for z in (0.45,0.47,0.49):
    r[z]=math.sqrt(math.sqrt(1-4*z/(1+z)**2))
out['mpi_ratio_theta_pi']=r; out['theta_pi_pass']=all(v>0.95 for v in r.values())
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/FLAV_RHO',exist_ok=True)
json.dump(out,open('field_tests/results/FLAV_RHO/run2.json','w'),indent=1,default=str)
