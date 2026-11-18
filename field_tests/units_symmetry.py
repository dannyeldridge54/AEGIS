"""D1295 (locked): automorphism orders of 2D lattices; units of Z[i], Z[omega]; symmetry => zero gradient."""
import sys, math, cmath, numpy as np; sys.path.insert(0,'tools/lattice'); import lattice_lab as LL
for name in ('tau=0.17+1.31i','tau=2i','tau=0.5+1.4i','square','hex'):
    print('P1', name, LL.automorphisms(name)['automorphisms'])
# units: elements of norm 1 in Z[i] and Z[omega]
ui=[(a,b) for a in range(-2,3) for b in range(-2,3) if a*a+b*b==1]
w=cmath.exp(2j*math.pi/3); uw=[(a,b) for a in range(-2,3) for b in range(-2,3) if abs(abs(a+b*w)-1)<1e-12]
print('P2 units Z[i]:',len(ui),' units Z[omega]:',len(uw),' -> 2x =',2*len(ui),2*len(uw))
for a in (0.5,1.0,2.0):
    h=1e-5; out=[]
    for x,y in ((0.0,1.0),(0.5,math.sqrt(3)/2),(0.0,2.0)):
        gx=(LL._E2d(x+h,y,a)-LL._E2d(x-h,y,a))/(2*h); gy=(LL._E2d(x,y+h,a)-LL._E2d(x,y-h,a))/(2*h); out.append(f"({x},{y:.3f}) |grad|={math.hypot(gx,gy):.2e}")
    print('P3 alpha',a,' | '.join(out))
