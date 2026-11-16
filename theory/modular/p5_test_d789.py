"""D789 (locked PREREG_D789). AI-assisted. Colour: count 3 vs 3bar; singlet if #3 - #3bar = 0 mod 3 (only for <=3 coloured fields)."""
import itertools, math
from fractions import Fraction as F
fields={'Q':(3,F(1,6),2),'U':(-3,F(-2,3),1),'D':(-3,F(1,3),1),'L':(1,F(-1,2),2),'E':(1,F(1),1),'Hu':(1,F(1,2),2),'Hd':(1,F(-1,2),2),
        'X':(3,F(2,3),1),'Xb':(-3,F(-2,3),1)}
def gauge_ok(fs):
    col=[fields[f][0] for f in fs]; n3=col.count(3); n3b=col.count(-3)
    colour_ok=(n3-n3b)%3==0 and not (n3+n3b==2 and n3!=n3b) and not (n3+n3b==1)
    # SU(3): singlet from 3x3bar or 3x3x3 or 3bar^3; exclude 3x3 and 3bar x 3bar pairs
    if n3+n3b==2 and n3!=1: colour_ok=False
    Y=sum(fields[f][1] for f in fs); doublets=sum(1 for f in fs if fields[f][2]==2)
    return colour_ok and Y==0 and doublets%2==0
SM=['Q','U','D','L','E','Hu','Hd']
res=[]
for Q,Hu in itertools.product(range(3),repeat=2):
    if Hu==0: continue
    Hd=(-Hu)%3; L=(-Hu)%3; E=(-L-Hd)%3; U=(-Q-Hu)%3; D=(-Q-Hd)%3
    ch={'Q':Q,'U':U,'D':D,'L':L,'E':E,'Hu':Hu,'Hd':Hd}
    for q in (1,2):
        ch2=dict(ch); ch2['X']=(-q-U)%3; ch2['Xb']=(-2*D)%3
        mass_ok=(ch2['X']+ch2['Xb'])%3==0
        allowed=[]
        for k in (1,2):
            for combo in itertools.combinations_with_replacement(SM,k):
                for x in ('X','Xb'):
                    fs=(x,)+combo
                    if gauge_ok(fs) and sum(ch2[f] for f in fs)%3==0 and '·'.join(fs)!='Xb·D·D': allowed.append('·'.join(fs))  # DEVIATIONS D1
        gauge_only=[]
        for k in (1,2):
            for combo in itertools.combinations_with_replacement(SM,k):
                for x in ('X','Xb'):
                    fs=(x,)+combo
                    if gauge_ok(fs): gauge_only.append('·'.join(fs))
        res.append((Q,Hu,q,mass_ok,allowed))
        print(f"(qQ,qHu)=({Q},{Hu}) N-charge q={q}: X={ch2['X']} Xb={ch2['Xb']} mass XXb allowed={mass_ok}; gauge-allowed X-terms={gauge_only}; Z3-allowed besides P5 terms={allowed}")
good=[r for r in res if r[3] and not r[4]]
print("consistent & no extra X couplings:",[(r[0],r[1],r[2]) for r in good])
print("(3) matter parity: N odd, U odd, D odd -> N·U·X even needs X even; Xb·D·D even needs Xb even: X,Xb even (Higgs-like) -> consistent")
MP=2.435e18; H=1.66*math.sqrt(106.75)*(3e8)**2/MP
for y in (0.02,0.2):
    for M in (4.3e11,1e12): print(f"(4) y={y} M={M:.1e}: Gamma={y*y*M/(16*math.pi):.2e} GeV vs H(T_R=3e8)={H:.2e} GeV")
print("VERDICT:","P5 PASSES" if good else "P5 FAILS")
