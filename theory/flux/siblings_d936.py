import math
mem=[('A',3,1),('B',4,2),('C',2,2),('D',2,4),('E',4,4)]
L=[]
for name,n,k in mem:
    p=k*math.sqrt(2/n); a=2/(3*p*p)
    for N in (50,55,60):
        ns=1-2/N; r=12*a/N**2; als=-2/N**2
        L.append(f"{name} n={n} k={k} p={p:.4f} alpha={a:.4f} N={N}: ns={ns:.4f} r={r:.2e} alpha_s={als:.2e} | SPA {(0.9684-ns)/0.0030:+.1f}sig, SPA+DESI {(0.9728-ns)/0.0027:+.1f}sig | LiteBIRD {'yes' if r>=1e-3 else 'no'}")
L.append("SERAPIS reference: alpha=1/12, p=2.8284")
open('field_tests/results/siblings_d936.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
