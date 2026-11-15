import math
MP=2.435e18; xs=1.3e-4
L=[(0.5,2.660e14,0.025),(1.0,1.613e14,0.066),(2.0,5.936e13,0.480),(3.0,2.186e13,3.091),(4.0,8.170e12,12.653),
   (5.0,3.524e12,22.826),(6.0,1.714e12,27.178),(8.0,2.391e11,29.452),(11.0,1.191e10,29.806)]
mk=lambda a:min(MP/(a*x)/T for _,T,x in L); msr=lambda a:min(MP*(a*x)**-0.75/T for _,T,x in L)
for a in (1,1000,3846,17852):
    print(f"a={a}: min m_KK/T={mk(a):.2f}, min M_s/T={msr(a):.1f}, V(x*)={(2*a*xs)**1.5:.2f}")
res={}
for k in (3,10):
    am=mk(1)/k; V=(2*am*xs)**1.5; res[k]=V
    print(f"k={k}: a_max={am:.0f}, V(x*) at a_max={V:.2f}")
print("VERDICT:", "COMPATIBLE" if res[10]>=1 else ("MARGINAL" if res[3]>=1 else "TENSION"))
