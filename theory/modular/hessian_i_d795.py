import mpmath as mp
mp.mp.dps=40
eps=mp.mpf('1.45e-4')
def V(t):
    a=abs(1728*mp.kleinj(t)-1728)
    I=mp.log(1+a**2/1728**2)/(4*mp.pi); I1=mp.log(1+a/1728)/(4*mp.pi)
    return I**2/(I**2+1)+eps*I1
t0=mp.mpc(0,1)
for h in (mp.mpf('1e-3'),mp.mpf('1e-4')):
    Vxx=(V(t0+h)-2*V(t0)+V(t0-h))/h**2
    Vyy=(V(t0+1j*h)-2*V(t0)+V(t0-1j*h))/h**2
    print(f"h={float(h):.0e}: Vxx={float(Vxx):.6e} Vyy={float(Vyy):.6e} R={float(Vxx/Vyy):.8f}")
A={}
for d in (0.01,0.03,0.1):
    vals=[V(t0+d*mp.expj(2*mp.pi*k/72)) for k in range(72)]
    m=sum(vals)/72; A[d]=float((max(vals)-min(vals))/m); print(f"delta={d}: A={A[d]:.3e}")
print(f"A(0.1)/A(0.03)={A[0.1]/A[0.03]:.2f}")
