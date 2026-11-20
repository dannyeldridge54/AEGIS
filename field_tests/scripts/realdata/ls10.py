import json
src=open('field_tests/scripts/realdata/cmb.py').read().split("c0,x=fit('lcdm'")[0]; exec(src)
c,x=fit('ls',[[0.304,0.687,0.0222,s] for s in (2.4,3,5,8)],B3+[(0.3,10)])
o=dict(chi2=c,x=x,d=c-1650.3800547143892,vs_thread=(c-1650.3800547143892)-(-4.835376192902686))
o['beats_thread']=o['vs_thread']<-2
print(json.dumps(o,indent=1)); json.dump(o,open('/home/claude/aegis/field_tests/results/realdata_ls10.json','w'),indent=1)
