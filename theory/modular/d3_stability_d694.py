"""D694 (locked PREREG_D694). AI-assisted."""
import numpy as np, math
M=60; n,m=np.meshgrid(np.arange(-M,M+1),np.arange(-M,M+1)); mask=~((n==0)&(m==0)); n=n[mask]; m=m[mask]
def E2(U,a4,a5): return U.imag**2*np.sum(np.cos(2*np.pi*(n*a5-m*a4))/np.abs(n+m*U)**4)
def g(U,a4,a5): return 256*E2(U,a4,a5)-16*E2(U,2*a4,2*a5)
for U in (complex(0.5,math.sqrt(3)/2),complex(0.5,14)):
    print(f"U={U}")
    for A0 in ((0,0),(0.5,0),(0,0.5),(0.5,0.5)):
        g0=g(U,*A0); row=[]
        for d in ((1,0),(0,1)):
            row.append(' '.join(f"{g(U,A0[0]+t*d[0],A0[1]+t*d[1])-g0:+.3e}" for t in (0.01,0.03,0.1)))
        print(f"  A0={A0}: g0={g0:.4f} | d_a4: {row[0]} | d_a5: {row[1]}")
