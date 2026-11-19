import json, mpmath as mp
mp.mp.dps=40
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
NS,R,AEX=mp.mpf('0.974393'),mp.mpf('4.82095e-4'),mp.mpf('-9.9814e-4')
def solve(order):
    def F(c6,phi):
        ns,r,a,f=obs(phi,c6*mp.mpf('1e-6'))
        if order==1: ns,r=f['ns'],f['r']
        return [ns-NS,(r-R)*1000]
    sol=mp.findroot(F,(mp.mpf('1.255'),mp.log(mp.mpf('14.8'))/mp.sqrt(2)),tol=1e-24)
    return sol
s1=solve(1); ns,r,a,f=obs(s1[1],s1[0]*mp.mpf('1e-6')); a1=f['a']
s2=solve(2); ns2,r2,a2,f2=obs(s2[1],s2[0]*mp.mpf('1e-6'))
check=abs(a1/mp.mpf('-1.0114e-3')-1)
out=dict(D='D1442',first_order_alpha=float(a1),impl_check_vs_D1415=float(check),
 second=dict(C=float(s2[0]*1e-6),y_star=float(mp.e**(mp.sqrt(2)*s2[1])),ns=float(ns2),r=float(r2),alpha=float(a2),err=float(a2/AEX-1)))
out['verdict']='no result (impl check)' if check>1e-3 else ('PASS' if abs(out['second']['err'])<0.01 else 'FAIL')
json.dump(out,open('field_tests/results/D1442_rho_second_order.json','w'),indent=1); print(json.dumps(out,indent=1))
