import math
f=lambda x:(math.atan(x/10)-math.atan(x/400))/math.pi; C=-f(29.6); z=lambda x:f(x)+C
k=math.sqrt(2/3); eps0=0.0046/16; xs=1.3e-4
def d1(F,x,h=1e-4): return k*x*(F(x*(1+h))-F(x*(1-h)))/(2*x*h)
Vol=lambda x:(2*x)**1.5
ctl=False
for gs in (0.1,0.5):
    ms2=lambda x:gs**0.5*math.pi/Vol(x)
    print(f"g_s={gs}: Vol(x*)={Vol(xs):.2e}, M_s/M_P(x*)={math.sqrt(ms2(xs)):.2e}")
    if Vol(xs)<1 or ms2(xs)>1: ctl=True
    for cH in (1,3):
        F=lambda x:cH/3*abs(z(x))*ms2(x)
        s=d1(F,xs); de=0.5*s*s+math.sqrt(2*eps0)*abs(s); dn=d1(lambda y:d1(F,y),xs)
        print(f"  c_H={cH}: dV/V={F(xs):.2e} dn_s={2*dn-6*de:.2e} dr={16*de:.2e}")
print("VERDICT:", "OUTSIDE CONTROL" if ctl else "see numbers")
