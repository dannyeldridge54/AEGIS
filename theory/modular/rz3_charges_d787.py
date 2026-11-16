"""D787 (locked PREREG_D787). AI-assisted."""
import itertools
ok_any=[]
for Q,Hu in itertools.product(range(3),repeat=2):
    Hd=(-Hu)%3; L=(-Hu)%3; E=(-L-Hd)%3; U=(-Q-Hu)%3; D=(-Q-Hd)%3
    ch={'Q':Q,'U':U,'D':D,'L':L,'E':E,'Hu':Hu,'Hd':Hd}
    ops={'UDD':['U','D','D'],'QDL':['Q','D','L'],'LLE':['L','L','E'],'QQQL':['Q','Q','Q','L'],'UUDE':['U','U','D','E'],'LHu':['L','Hu']}
    c={k:sum(ch[f] for f in v)%3 for k,v in ops.items()}
    # checks of imposed terms
    assert (Q+Hu+U)%3==0 and (Q+Hd+D)%3==0 and (L+Hd+E)%3==0 and (Hu+Hd)%3==0 and (2*L+2*Hu)%3==0 and (L+Hu)%3==0
    sm_allowed=[k for k,v in c.items() if v==0]
    pair={q:[k for k,v in c.items() if (v+q)%3==0] for q in (1,2)}
    both=bool(pair[1]) and bool(pair[2])
    triality = (c['UDD']!=0)   # baryon-number-violating ops carry charge -> B3-like
    print(f"(qQ,qHu)=({Q},{Hu}): charges {ch} | SM-allowed: {sm_allowed} | pair q=1 via {pair[1]}, q=2 via {pair[2]} | B3-like: {triality}")
    if both and 'QQQL' not in sm_allowed and 'UDD' not in sm_allowed: ok_any.append((Q,Hu))
print("Assignments satisfying R-Z3 with proton safety:",ok_any)
print("VERDICT:","R-Z3 SATISFIABLE" if ok_any else "CONFLICT/NOT SATISFIABLE")
