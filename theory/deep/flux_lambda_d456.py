import math
from scipy.optimize import brentq
f=lambda x,m,n:(math.atan(x/m)-math.atan(x/n))/math.pi
c=-f(29.6,10,400); small=[]
for m,n in ((10,400),(9,400),(11,400),(10,399),(10,401)):
    try: xe=brentq(lambda x:f(x,m,n)+c,1,63)
    except ValueError: print(f"({m},{n}): no root in [1,63]"); continue
    dl=(xe/29.6)**-0.97-1
    if (m,n)!=(10,400): small.append(abs(dl))
    print(f"({m},{n}): x_E={xe:.4f}, dLambda/Lambda={dl:+.3%}")
s=min(small); print("smallest step", f"{s:.3%}", "VERDICT:", "FINE" if s<0.01 else ("COARSE" if s>0.1 else "INTERMEDIATE"))
