"""D811 (locked PREREG_D811). AI-assisted."""
import sys, mpmath as mp
sys.path.insert(0,'theory/modular')
from inflaton_ad_d790 import Ese
mp.mp.dps=30
def L(t): return -mp.log(2*mp.im(t)*abs(mp.eta(t))**4)
def dz(F,t,h=mp.mpf('1e-10')):
    gx=(F(t+h)-F(t-h))/(2*h); gy=(F(t+1j*h)-F(t-1j*h))/(2*h); return (gx-1j*gy)/2
E=lambda t: mp.mpf(Ese(float(mp.re(t)),float(mp.im(t))))
def g(t,C): return 4*mp.im(t)**2*abs(dz(L,t)+C*dz(E,t,mp.mpf('1e-6')))**2
i=mp.mpc(0,1); h=mp.mpf('1e-3')
for C in (0,1e-6,1e-4,1e-2,1):
    g0=g(i,C); gxx=(g(i+h,C)-2*g0+g(i-h,C))/h**2; gyy=(g(i+1j*h,C)-2*g0+g(i-1j*h,C))/h**2
    print(f"C={C:g}: g(i)={mp.nstr(g0,3)} g_xx={mp.nstr(gxx,8)} g_yy={mp.nstr(gyy,8)}")
