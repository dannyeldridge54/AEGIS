"""D664 (locked PREREG_D664_I_FLAVOUR). AI-assisted."""
import cmath, math, numpy as np
src=open('theory/modular/s3_flavour_d597.py').read().splitlines()
exec("\n".join(src[1:5]))   # imports, sig, E2, Yd (verbatim from D597)
A=lambda Y:np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
y=Yd(1j)
print("Y(i) =",np.round(y,6))
sv=np.linalg.svd(A(y),compute_uv=False); print("(a) Weinberg 2x2 singular values:",np.round(sv,6))
for b in (0.3,1.0,3.0):
    M=np.zeros((3,3),complex); M[:2,:2]=A(y); M[0,2]=M[2,0]=b*y[0]; M[1,2]=M[2,1]=b*y[1]; M[2,2]=0
    s=np.linalg.svd(M,compute_uv=False); print(f"(b) 2+1, b={b}: singular values {np.round(s,6)}; min/max = {s[-1]/s[0]:.3e}")
sv=np.linalg.svd(A(y),compute_uv=False); print("(c) Majorana N doublet singular values:",np.round(sv,6))
