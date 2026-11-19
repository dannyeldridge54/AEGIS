import json, mpmath as mp
mp.mp.dps=30
A=2*mp.zeta(4); B=1-mp.mpf('5.783341757348703'); D=mp.pi*mp.zeta(3); Cc=mp.euler+mp.log(2)-2
def V(phi,Cr):
    y=mp.e**(mp.sqrt(2)*phi); E1=A*y*y+B+D/y; return (1-1/E1)*(1+Cr*(E1-1))
def flows(phi,Cr):
    d=[mp.diff(lambda p: V(p,Cr),phi,n) for n in range(6)]
    Vp=d[1]/d[0]
    ev1=Vp**2/2
    ev2f=lambda p: 2*((mp.diff(lambda q:V(q,Cr),p,1)/V(p,Cr))**2-mp.diff(lambda q:V(q,Cr),p,2)/V(p,Cr))
    ev2=ev2f(phi); dev2=mp.diff(ev2f,phi); ev3=-dev2*Vp/ev2
    ev3f=lambda p: -mp.diff(ev2f,p)*(mp.diff(lambda q:V(q,Cr),p,1)/V(p,Cr))/ev2f(p)
    ev4=-mp.diff(ev3f,phi)*Vp/ev3
    return ev1,ev2,ev3,ev4,d
def obs(phi,Cr):
    ev1,ev2,ev3,ev4,d=flows(phi,Cr)
    e1=ev1*(1-ev2/3); e2=ev2*(1-ev2/6-ev3/3); e3=ev3*(1-ev2/3-ev4/3); e4=ev4
    ns=1-2*e1-e2-(3+2*Cc)*e1*e2-2*e1**2-Cc*e2*e3; r=16*e1*(1+Cc*e2)
    a2=-(1+e1)*(2*e1*e2+e2*e3)-(3+2*Cc)*e1*e2*(e2+e3)-4*e1**2*e2-Cc*e2*e3*(e3+e4)
    V0=d[0]; eps=0.5*(d[1]/V0)**2; eta=d[2]/V0; xi=d[1]*d[3]/V0**2
    first=dict(ns=1-6*eps+2*eta,r=16*eps,a=16*eps*eta-24*eps**2-2*xi)
    return ns,r,a2,first

corners={'K1':(1.0e-6,'0.972710','4.38906e-4','-9.1099e-4'),'K2':(1.3e-6,'0.974828','4.89722e-4','-1.0144e-3')}
out={'D':'D1443','corners':{}}
for k,(C0,ns0,r0,a0) in corners.items():
    NS,R,AEX=mp.mpf(ns0),mp.mpf(r0),mp.mpf(a0)
    F=lambda c6,phi: (lambda o:[o[0]-NS,(o[1]-R)*1000])(obs(phi,c6*mp.mpf('1e-6')))
    s=mp.findroot(F,(mp.mpf(C0*1e6),mp.log(mp.mpf('14.6'))/mp.sqrt(2)),tol=1e-18)
    ns,r,a,f=obs(s[1],s[0]*mp.mpf('1e-6'))
    Cr=float(s[0])*1e-6; ok=abs(Cr/C0-1)<0.1
    out['corners'][k]=dict(C_solved=Cr,C_corner=C0,impl_ok=ok,y_star=float(mp.e**(mp.sqrt(2)*s[1])),alpha=float(a),alpha_exact=float(AEX),err=float(a/AEX-1))
    print(k,out['corners'][k],flush=True)
c=out['corners']
out['verdict']='no result' if not all(v['impl_ok'] for v in c.values()) else ('PASS' if max(abs(v['err']) for v in c.values())<0.005 else 'FAIL')
json.dump(out,open('field_tests/results/D1443_box_corners.json','w'),indent=1); print(out['verdict'])
