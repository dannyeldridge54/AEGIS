import sys, math, json, os; sys.path.insert(0,'.')
import numpy as np
from scipy.optimize import minimize
from tools.serapis_calc.shapes import E, log_eta
Ef=lambda x,y,s=1.5:float(E(complex(x,y),s).real)
def V0(x,y,h=1e-6):
    L=lambda a,b:math.log(Ef(a,b)); dx=(L(x+h,y)-L(x-h,y))/(2*h); dy=(L(x,y+h)-L(x,y-h))/(2*h); return (4/9)*y*y*(dx*dx+dy*dy)
Fr=lambda x,y:math.sqrt(y)*math.exp(2*log_eta(complex(x,y)).real); F0=Fr(0,1)
Gr=lambda x,y:Ef(x,y,2.0); G0=Gr(0,1)
W={'F':lambda x,y:Fr(x,y)/F0,'G':lambda x,y:Gr(x,y)/G0}
def hess(f,x,y,h=1e-4):
    fxx=(f(x+h,y)-2*f(x,y)+f(x-h,y))/h**2; fyy=(f(x,y+h)-2*f(x,y)+f(x,y-h))/h**2
    fxy=(f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4*h*h); return np.array([[fxx,fxy],[fxy,fyy]])
H0=hess(V0,0,1); out={'H_V0':H0.tolist()}
rx,ry=0.5,math.sqrt(3)/2
for wn,sg in [('F',1),('G',1),('G',-1)]:
    w=W[wn]; HW=hess(w,0,1); key=f'{wn}{"+" if sg>0 else "-"}'
    mineig=lambda k:np.linalg.eigvalsh(H0+sg*k*HW).min()
    res=dict(H_W=HW.tolist())
    hi=1.0
    while mineig(hi)>0 and hi<1e6: hi*=2
    if mineig(hi)>0: res['class']='NO-SPLIT'; out[key]=res; continue
    lo=0.0
    for _ in range(80):
        m=(lo+hi)/2
        if mineig(m)>0: lo=m
        else: hi=m
    kc=(lo+hi)/2; ev,evec=np.linalg.eigh(H0+sg*kc*HW); d=evec[:,0]; res['kappa_c']=kc; res['unstable_dir']=d.tolist()
    rows=[]
    for r in (1.001,1.01,1.1,1.5):
        k=r*kc; f=lambda p:V0(p[0],p[1])+sg*k*w(p[0],p[1]) if p[1]>0.2 else 1e9
        st=[0+1e-3*d[0],1+1e-3*d[1]]
        o=minimize(f,st,method='Nelder-Mead',options=dict(xatol=1e-10,fatol=1e-15,maxiter=6000))
        x,y=o.x; t=complex(x,y); u=abs((t-1j)/(t+1j))
        rows.append(dict(r=r,x=float(x),y=float(y),abs_u=float(u),on_CP=bool(abs(x)<1e-5 or abs(abs(t)-1)<1e-5 or abs(abs(x)-0.5)<1e-5),V_min_minus_V_rho=float(o.fun-(V0(rx,ry)+sg*k*w(rx,ry)))))
    res['rows']=rows
    us=[q['abs_u'] for q in rows]
    sup=us[0]<0.05 and all(us[i]<=us[i+1]+1e-9 for i in range(3)) and all(q['V_min_minus_V_rho']<0 for q in rows)
    res['class']='SUPERCRITICAL' if sup else 'FIRST-ORDER/OTHER'
    out[key]=res
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/IOFFSET',exist_ok=True); json.dump(out,open('field_tests/results/IOFFSET/out2.json','w'),indent=1)
