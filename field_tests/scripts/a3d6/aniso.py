import numpy as np, json, math
exec(open('field_tests/scripts/a3d6/run.py').read().split("# validation")[0])
sets=[(1,1,1,2),(1,1,2,2),(1,2,2,2),(1,1,1,3),(1,1,3,3),(1.5,)*4,(1,1,1,1.3)]
o={}
for s in sets:
    I=RN(lambda x,y,s=s: np.prod([G11(R,x,y) for R in s]),2)
    o[str(s)]=dict(I=I,V=float(np.prod(s)))
o['volume_controlled']=all(v['I']>0 for v in o.values() if v['V']>=4)
print(json.dumps(o,indent=1,default=float)); json.dump(o,open('field_tests/results/a3_d6_aniso.json','w'),indent=1,default=float)
