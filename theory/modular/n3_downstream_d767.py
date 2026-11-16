"""D767 (locked PREREG_D767). AI-assisted."""
import math
k=15/(64*math.pi**6)
for N,N0,F in ((5,1,0),(3,1,6)):
    assert 3*N+N0+F==16
    Ne=N-N0; lo,hi=k*Ne/1.3e-6,k*Ne/1.0e-6
    print(f"(N,N0,N_flux)=({N},{N0},{F}) N_eff={Ne}: Im S*Im rho = {lo:.0f}-{hi:.0f}; half-unit variant {lo/2:.0f}-{hi/2:.0f}")
