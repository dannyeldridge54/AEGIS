"""D809 (locked PREREG_D809). Pradler-Steffen thermal gravitino yield. AI-assisted."""
import math
MZ=91.19; ainv0=(59.0,29.6,8.5); b=(33/5,1,-3)
y=(0.653e-12,1.604e-12,4.276e-12); k=(1.266,1.312,1.271)
def g(i,T): ai=ainv0[i]-b[i]/(2*math.pi)*math.log(T/MZ); return math.sqrt(4*math.pi/ai)
def Y(T,M=(0,0,0),m32=2.5e5):
    return sum(y[i]*g(i,T)**2*(1+M[i]**2/(3*m32**2))*math.log(k[i]/g(i,T)) for i in range(3))*T/1e10
print(f"(D) K4: Y(1e10)={Y(1e10):.3e} vs old fit 1.9e-12 (ratio {Y(1e10)/1.9e-12:.2f}); g_i(1e10)={[round(g(i,1e10),3) for i in range(3)]}")
for M2,M3,m32 in ((670,4700,2.5e5),(1850,13000,7e5)):
    M=(M2/2.0*0.9,M2,M3)  # bino ~ M2/2 order; irrelevant (M<<m32)
    print(f"-- M2={M2} GeV, M3={M3} GeV, m3/2={m32:.1e}: goldstino term max {(M3/m32)**2/3:.1e}")
    for T in (1e6,3e6): yv=Y(T,M,m32); print(f"(A) tau=i T_R={T:.0e}: Y={yv:.2e} (old {1.9e-12*T/1e10:.2e}), Omega_nth={2.74e8*M2*yv:.2e}")
    for TR in (3e8,3e9):
        for T2 in (1e5,1e6,140,1100):
            yv=Y(TR,M,m32)*T2/TR; tag='B frozen' if T2>=1e5 else 'C self-dil'
            print(f"({tag}) T_R={TR:.0e} T2={T2:.0e}: Y={yv:.2e}, Omega_nth={2.74e8*M2*yv:.2e}")
