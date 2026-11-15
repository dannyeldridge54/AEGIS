import math
MP,gs,g,xE=2.435e18,106.75,0.7,29.6; c=math.sqrt(2/3)
zp=(10/(100+xE**2)-400/(160000+xE**2))/math.pi      # dzeta/dx at x_E (M_s^2)
dp=0.1145*math.exp(-(8.44-6)); T=1.5e11/MP
H=math.sqrt(math.pi**2*gs/90)*T**2                     # M_P units
KE=0.5*(H*dp)**2                                       # M_P^4
d1=-0.019733; xip=-d1/(2*xE**2)
print(f"zeta'(x_E)={zp:.4e} M_s^2; arrival dphi/dN={dp:.4f}; H={H:.3e} M_P; KE={KE:.3e} M_P^4; D437 slope {xip:.4e}")
res={}
for ms in (0.01,0.1):
    k=zp*ms**2                                         # dxi/dx in M_P^2
    dx=math.sqrt(2*KE)/(g*k)
    R=k/xip
    res[ms]=(dx<1e-2,R>=1)
    print(f"M_s/M_P={ms}: penetration dx={dx:.3e} ({'PASS' if dx<1e-2 else 'FAIL'}); slope ratio R={R:.3f} ({'PASS' if R>=1 else 'FAIL'})")
msR=math.sqrt(xip/zp); print(f"M_s for R=1: {msR:.4f} M_P")
a,b=res[0.1]
print("VERDICT:", "CAPTURES" if a and b else (f"CAPTURES IF M_s >= {msR:.3f} M_P" if a else "NO CAPTURE"))
