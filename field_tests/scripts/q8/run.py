import math, json
gs=106.75; MP=1.22e19; c=1.66*math.sqrt(gs)/MP
Mmax=math.sqrt(1.34e9/c); Mmin=math.sqrt(130/c)
lo,hi=max(Mmin,1.25e10),min(Mmax,2.5e12)
o=dict(M_window=[Mmin,Mmax],N_window=[1.25e10,2.5e12],overlap=[lo,hi] if lo<hi else None)
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/q8_portal.json','w'),indent=1)
