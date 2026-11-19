import json, math
s13,ss13=0.02195,0.00056
tm2=1/(3*(1-s13)); stm2=abs(1/(3*(1-s13-ss13))-tm2)
J,sJ=0.3092,0.0087; N,sN=0.307,0.012
w=[1/sJ**2,1/sN**2]; C=(J*w[0]+N*w[1])/sum(w); sC=1/math.sqrt(sum(w))
o=dict(TM2=tm2,TM2_err=stm2,dev_JUNO_sigma=(tm2-J)/math.hypot(sJ,stm2),dev_comb_sigma=(tm2-C)/math.hypot(sC,stm2),comb=C,comb_err=sC)
o['exact_TM2_survives']=abs(o['dev_JUNO_sigma'])<=3; o['shift_needed_to_comb']=C-tm2
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/rb5_juno.json','w'),indent=1)
