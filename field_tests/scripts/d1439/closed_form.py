import json, math
NS,R,AEX,B=0.974393,4.82095e-4,-9.9814e-4,1-5.783341757348703
d=json.load(open('field_tests/results/D1415_rho_offset_relation.json'))
aB=d['B_only']['alpha']; aP=d['pure_plateau']['alpha']
rho=2*math.sqrt(2)*math.sqrt(R/2)/(1-NS); t=(rho-1)/(rho+1); w=(1-NS)/(16*(1-t))
pp=4*w*(1-t); off=-6*B*w/(1+t); a=-2*R*(1+pp+off)
out=dict(D='D1439',rho=rho,t=t,w=w,plateau_piece=pp,offset_piece=off,alpha_cf=a,alpha_B_only=aB,alpha_pure_num=aP,
 cf_pure=-2*R*(1+pp),err_vs_Bonly=a/aB-1,err_vs_A1=a/AEX-1,err_pure_cf_vs_pure_num=(-2*R*(1+pp))/aP-1)
out['test_a']='VALID' if abs(out['err_vs_Bonly'])<0.003 else 'NOT VALID'
out['test_b']='PASS' if abs(out['err_vs_A1'])<0.01 else 'FAIL'
json.dump(out,open('field_tests/results/D1439_rho_closed_form.json','w'),indent=1); print(json.dumps(out,indent=1))
