import math
z=lambda x:(math.atan(x/10)-math.atan(x/400))/math.pi-0.3728
k=math.sqrt(2/3)  # d/dphi = k x d/dx
def g(x,a):  # dV/V
    return a*abs(z(x))
def d1(f,x,h=1e-4): return k*x*(f(x*(1+h))-f(x*(1-h)))/(2*x*h)
def d2(f,x): return d1(lambda y:d1(f,y),x)
eps0=0.0046/16; out=[]
for ms in (0.1,1.0):
  for cH in (1,3):
    a=cH/3*ms**2
    f=lambda x:g(x,a)
    x=1.3e-4
    s=d1(f,x); de=0.5*s**2+math.sqrt(2*eps0)*abs(s); dn=d2(f,x)
    dns=2*dn-6*de; dr=16*de
    mx=max(f(10**(-5+5*i/200)) for i in range(201))
    out.append((ms,cH,dns,dr,mx))
    print(f"Ms/MP={ms} cH={cH}: dV/V*={f(x):.3e} dns={dns:.2e} dr={dr:.2e} max dV/V(x<=1)={mx:.3e}")
ok=all(abs(o[2])<1e-4 and abs(o[3])<1e-4 and o[4]<0.01 for o in out if o[0]==1.0)
print("VERDICT:", "SAFE" if ok else ("SAFE IF M_s <= 0.1 M_P" if all(abs(o[2])<1e-4 and abs(o[3])<1e-4 and o[4]<0.01 for o in out if o[0]==0.1) else "DISTURBS"))
