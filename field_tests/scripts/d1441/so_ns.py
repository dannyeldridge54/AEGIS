import json
c,s=0.9682,0.002; o=dict(D='D1441',tension_A1=(0.974393-c)/s,tension_NA12=(0.97462-c)/s,ratio=2.8e-3/2.0e-3)
o['D1437_SO']='conservative' if o['ratio']>1 else 'optimistic'; o['SO_alone_3sigma']=min(o['tension_A1'],o['tension_NA12'])>=3
json.dump(o,open('field_tests/results/D1441_so_ns_check.json','w'),indent=1); print(o)
