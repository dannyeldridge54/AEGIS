import json, math
A=16*(math.pi**2/6)/(3*1.2020569031595942)
tun=json.load(open('field_tests/results/GENESIS_DE/tuning.json'))
H0=1.0; Hinf_over_H0=2.4e-6/ (1.0/ (2.435e18/1.44e-42*1e-0) ) if False else None
# units: M_P=H0=1 in D1626 code; convert H_inf: H0 = 1.44e-42 GeV, M_P(reduced)=2.435e18 GeV -> H0/M_P = 5.9e-61
H0_MP=1.44e-42/2.435e18
out={}
for k,v in tun.items():
    beta=float(k.split('=')[1]); b=v['best_minmax']; amp=b['amp']; dln=v['window_dln']
    y=math.sqrt(A/amp); ylo=math.sqrt(A/(amp*math.exp(dln/2))); yhi=math.sqrt(A/(amp*math.exp(-dln/2)))
    P=(1/ylo-1/yhi)/(math.pi/3)
    # Q1: V = VL(1-amp_now)... VL ~ 3.2 (H0=1 units, D1628 range 2-3.3); V'' = -VL*A*beta^2*e^{-beta psi} = -VL*beta^2*amp
    VL=3.0; Vpp=VL*beta**2*amp
    # H at BBN (T~0.1 MeV): H ~ 1e-25 GeV -> /H0 = 7e16; end of inflation H=2.4e-6 M_P -> /H0 = 2.4e-6/H0_MP
    H_bbn=1e-25/1.44e-42; H_inf=2.4e-6/H0_MP
    q1={'today':Vpp, 'BBN':Vpp/H_bbn**2, 'end_inflation':Vpp/H_inf**2}
    dpsi=dln/beta; dphi_q=(2.4e-6/(2*math.pi))*math.sqrt(60)
    out[k]=dict(amp=amp,y=y,y_window=[ylo,yhi],P_window=P,Q1_meff2_over_H2=q1,window_dpsi_MP=dpsi,quantum_spread_MP=dphi_q,
        reading=('tuned' if P<0.01 else 'mild' if P<0.05 else 'natural'))
out['C_start_supported']=False if all(v['Q1_meff2_over_H2']['BBN']<1e-3 for v in out.values() if isinstance(v,dict)) else 'check'
print(json.dumps(out,indent=1)); json.dump(out,open('field_tests/results/GENESIS_DE/rc2.json','w'),indent=1)
