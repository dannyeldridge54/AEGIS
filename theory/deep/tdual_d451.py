import math
n,mu,m2=124.1,1.0,4/math.pi
def lnF(x,e): return math.log(x+e)-0.5*math.log(1+x/mu)-n*(1-math.exp(-x/m2))
def lnV(x,e): return 2*lnF(x,e)-3*math.log(2*x)
xs=1.3e-4; Vd=(2/xs)**1.5
print(f"dual volume {Vd:.2e}; M_s'/M_P = {0.1**0.25*math.sqrt(math.pi/Vd):.2e} (g_s 0.1), {0.5**0.25*math.sqrt(math.pi/Vd):.2e} (0.5)")
worst=0
for e in (0.0,3.04e-7):
    for x in (xs,1.0,29.6):
        lA=(lnV(1/x,e)-lnV(x,e))/math.log(10)
        if x==xs: worst=max(worst,abs(lA))
        print(f"eps={e:.2e} x={x}: log10 A = {lA:.2f}")
print("VERDICT:", "RESCUED" if Vd>1e2 and worst<0.1 else ("DUAL FRAME CONTROLLED, F NOT MODULAR" if Vd>1e2 else "NOT RESCUED"))
