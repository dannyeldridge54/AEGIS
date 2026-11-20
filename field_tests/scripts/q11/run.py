import math, json
mX=12.8; mn=0.939; mu=mX*mn/(mX+mn); a=1/137.036; ZA=54/131
GeV2cm2=0.3894e-27; GeV2cm3s=GeV2cm2*2.998e10
aD=math.sqrt(5e-26/GeV2cm3s*mX**2/math.pi)
def sig(eps,m): return 16*math.pi*a*aD*eps**2*mu**2*ZA**2/m**4*GeV2cm2
o=dict(alpha_D_min=aD,eps_max={})
for lim in (1e-47,1e-45):
    o['eps_max'][str(lim)]={str(m):math.sqrt(lim/sig(1,m)) for m in (0.3,1,5)}
o['dim_strip_survives_optimistic']=all(v>1e-11 for v in o['eps_max']['1e-47'].values())
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/q11_dd.json','w'),indent=1)
