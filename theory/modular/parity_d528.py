"""D528: modular-centre matter parity search (locked PREREG_D528_MODULAR_PARITY). AI-assisted."""
import itertools
F=['Q','U','D','L','E','Hu','Hd']
W_ok=[('Q','Hu','U'),('Q','Hd','D'),('L','Hd','E'),('Hu','Hd'),('L','Hu','L','Hu')]
W_no=[('L','Hu'),('U','D','D'),('L','Q','D'),('L','L','E'),('Q','Q','Q','L'),('U','U','D','E'),('Q','Q','Q','Hd')]
K_no=[(('Q','Q'),('U','E')),(('Q','L'),('U','D'))]
for t in (0,1):
    print(f"convention t={t} ({'rigid' if t==0 else 'supergravity'})")
    for M in range(1,7):
        N=2*M; sols=[]
        for n in itertools.product(range(N),repeat=7):
            k=dict(zip(F,n))
            w=lambda ops:sum(k[o] for o in ops)%N
            if any(w(o)!=(t*M)%N for o in W_ok): continue
            if any(w(o)==(t*M)%N for o in W_no): continue
            if any((sum(k[o] for o in a)-sum(k[o] for o in b))%N==0 for a,b in K_no): continue
            sols.append(n)
        ex=('' if not sols else ' e.g. '+', '.join(f"{f}={x}/{M}" for f,x in zip(F,sols[0])))
        print(f"  M={M} (Z_{N}): {len(sols)} solutions{ex}")
