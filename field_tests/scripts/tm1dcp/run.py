import json
D={'IC19':dict(s23=0.561,bf=177,up=19,dn=20,lo3=96,hi3=422,pred=[74.3,285.7]),'IC24':dict(s23=0.470,bf=212,up=26,dn=41,lo3=124,hi3=364,pred=[97.6,262.4])}
o={}
for k,d in D.items():
    r=[]
    for p in d['pred']:
        x=p if p>=d['lo3'] else p+360
        inside=d['lo3']<=x<=d['hi3']
        dd=x-d['bf']
        if dd>=0: s1,s3=d['up'],d['hi3']-d['bf']
        else: s1,s3=d['dn'],d['bf']-d['lo3']
        a=abs(dd); pull=a/s1 if a<=s1 else 1+2*(a-s1)/(s3-s1)
        r.append(dict(pred=p,inside_3sigma=inside,approx_pull=round(pull,2)))
    o[k]=dict(branches=r,survives=any(b['inside_3sigma'] for b in r))
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/tm1_dcp.json','w'),indent=1)
