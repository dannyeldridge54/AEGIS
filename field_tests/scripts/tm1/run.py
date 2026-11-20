import math, json
s13=0.02195; o={}
tm1=(1-3*s13)/(3*(1-s13)); tm2=1/(3*(1-s13))
for lab,v in (('TM1',tm1),('TM2',tm2)):
    o[lab]=dict(s12=v,dev_JUNO=(v-0.3092)/0.0087,dev_comb=(v-0.3084)/0.0070)
s=math.sqrt(s13)
for s23 in (0.561,0.470):
    t=math.asin(math.sqrt(s23)); cot2=1/math.tan(2*t)
    c1=-cot2*(1-5*s13)/(2*math.sqrt(2)*s*math.sqrt(1-3*s13))
    c2=cot2*(1-2*s13)/(s*math.sqrt(2-3*s13))
    f=lambda c:(math.degrees(math.acos(c)),360-math.degrees(math.acos(c))) if abs(c)<=1 else None
    o[f'dCP_s23={s23}']=dict(TM1=f(c1),TM2=f(c2),cos_TM1=c1,cos_TM2=c2)
o['TM2_regression_ok']=abs(o['dCP_s23=0.561']['TM2'][1]-235.6)<0.5 or abs(o['dCP_s23=0.561']['TM2'][0]-124.9)<0.5
o['TM1_survives']=abs(o['TM1']['dev_JUNO'])<=3 and abs(o['TM1']['dev_comb'])<=3
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/tm1_juno.json','w'),indent=1)
