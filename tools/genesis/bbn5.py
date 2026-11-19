# (c) Danny Lee Eldridge · AEGIS Community License
"""BBN v5 (lock PREREG_RD1_COULOMB): v4 + Fermi-function Coulomb correction on e-p branches."""
import math
from scipy.integrate import quad
from tools.genesis import bbn2 as B2, bbn4 as B4
ALPHA=1/137.035999
q=B2.Q/B2.ME
def F(x):
    eta=ALPHA*x/math.sqrt(x*x-1); a=2*math.pi*eta; return a/(1-math.exp(-a))
_f0=quad(lambda x:x*math.sqrt(x*x-1)*(q-x)**2*F(x),1+1e-12,q)[0]; K=1/(B2.TAU*_f0)
def rates_c(T,Tnu):
    z=B2.ME/T; zn=B2.ME/Tnu; fd=B2._fd
    def integ(sgn):
        gp=lambda x: x*math.sqrt(x*x-1)*(sgn*q-x)**2*fd(-x*z)*fd((x-sgn*q)*zn)*F(x)
        gm=lambda x: abs(x)*math.sqrt(x*x-1)*(sgn*q-x)**2*fd(-x*z)*fd((x-sgn*q)*zn)
        up=60/z+q+5
        return K*(quad(gp,1+1e-12,up,limit=200)[0]+quad(gm,-up,-1,limit=200)[0])
    return integ(1),integ(-1)
def run(**kw):
    old=B4.rates; B4.rates=rates_c
    try: return B4.run(**kw)
    finally: B4.rates=old
