import sys, math, mpmath as mp
sys.path.insert(0,'theory/modular')
from inflaton_ad_d790 import Ese
mp.mp.dps=30
def Dl(x,y):
    t=mp.mpc(x,y); q=mp.exp(2j*mp.pi*t); eta=mp.exp(1j*mp.pi*t/12)*mp.qp(q); return float(-mp.log(y*abs(eta)**4))
h=1e-4; r3=math.sqrt(3)/2
for name,f in (("E(tau,2)",Ese),("Delta",Dl)):
    f0=f(0,1); fxx=(f(h,1)-2*f0+f(-h,1))/h**2; fyy=(f(0,1+h)-2*f0+f(0,1-h))/h**2
    print(f"{name}: f_xx(i)={fxx:.5e} f_yy(i)={fyy:.5e} saddle={fxx*fyy<0}; f(i)-f(rho)={f0-f(0.5,r3):.5e}")
