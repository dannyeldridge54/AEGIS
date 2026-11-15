"""D551 (locked PREREG_D551_VACUUM_I_SELECTION). Reuses D528/D529 search. AI-assisted."""
import itertools
from fractions import Fraction as Fr
F=['Q','U','D','L','E','Hu','Hd']
W_ok=[('Q','Hu','U'),('Q','Hd','D'),('L','Hd','E'),('Hu','Hd'),('L','Hu','L','Hu')]
W_no=[('L','Hu'),('U','D','D'),('L','Q','D'),('L','L','E'),('Q','Q','Q','L'),('U','U','D','E'),('Q','Q','Q','Hd')]
K_no=[(('Q','Q'),('U','E')),(('Q','L'),('U','D'))]
t=1
for M in (2,4):
    N=2*M; passing=[]
    for n in itertools.product(range(N),repeat=7):
        k=dict(zip(F,n)); w=lambda o:sum(k[x] for x in o)%N
        if any(w(o)!=(t*M)%N for o in W_ok) or any(w(o)==(t*M)%N for o in W_no): continue
        if any((sum(k[x] for x in a)-sum(k[x] for x in b))%N==0 for a,b in K_no): continue
        g=Fr(M,2); q={f:Fr(k[f])-g for f in F}
        A3=3*Fr(1,2)*(2*q['Q']+q['U']+q['D'])+3*g; A2=3*Fr(1,2)*(3*q['Q']+q['L'])+Fr(1,2)*(q['Hu']+q['Hd'])+2*g
        if (A3-A2)%Fr(N,2)==0: passing.append(n)
    ok=0; ex=None
    for n in passing:
        for lift in itertools.product((0,2),repeat=7):
            kw={f:Fr(x,M)+l for f,x,l in zip(F,n,lift)}
            kys=[sum(kw[x] for x in o)-1 for o in W_ok]
            if all(ky.denominator==1 and ky>=0 and ky%4==0 for ky in kys):
                ok+=1; ex=ex or (n,lift,[int(x) for x in kys]); break
    print(f"Z_{N}^R: {ok}/{len(passing)} anomaly-passing assignments admit a lift with all required couplings nonzero at tau=i"+(f"; e.g. n={ex[0]} lift={ex[1]} k_Y={ex[2]}" if ex else ""))
