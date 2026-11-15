"""D529: Ibanez-Ross anomaly check of D528 parity solutions (locked PREREG_D529_PARITY_ANOMALY). AI-assisted."""
import itertools
from fractions import Fraction as Fr
F=['Q','U','D','L','E','Hu','Hd']
W_ok=[('Q','Hu','U'),('Q','Hd','D'),('L','Hd','E'),('Hu','Hd'),('L','Hu','L','Hu')]
W_no=[('L','Hu'),('U','D','D'),('L','Q','D'),('L','L','E'),('Q','Q','Q','L'),('U','U','D','E'),('Q','Q','Q','Hd')]
K_no=[(('Q','Q'),('U','E')),(('Q','L'),('U','D'))]
for t in (0,1):
    for M in (2,3,4):
        N=2*M; tot=0; ok=[]
        if t==1 and M%2: print(f"t={t} M={M}: not an R-symmetry assignment"); continue
        for n in itertools.product(range(N),repeat=7):
            k=dict(zip(F,n)); w=lambda o:sum(k[x] for x in o)%N
            if any(w(o)!=(t*M)%N for o in W_ok) or any(w(o)==(t*M)%N for o in W_no): continue
            if any((sum(k[x] for x in a)-sum(k[x] for x in b))%N==0 for a,b in K_no): continue
            tot+=1; g=Fr(M,2) if t else 0; q={f:Fr(k[f])-(Fr(M,2) if t else 0) for f in F}
            A3=3*Fr(1,2)*(2*q['Q']+q['U']+q['D'])+3*g
            A2=3*Fr(1,2)*(3*q['Q']+q['L'])+Fr(1,2)*(q['Hu']+q['Hd'])+2*g
            if (A3-A2)%Fr(N,2)==0: ok.append((n,A3,A2))
        ex='' if not ok else f" e.g. {dict(zip(F,ok[0][0]))} A3={ok[0][1]} A2={ok[0][2]}"
        print(f"t={t} M={M} (Z_{N}): {len(ok)}/{tot} pass{ex}")
