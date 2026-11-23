import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
d = F.N210808; R = F.hs_radius_um(d['V_um3']); pd = F.hs_pressure_Gbar(d['Y_MJ'], d['T_keV'], d['tau_ps'], d['V_um3'])
I1 = dict(p_derived=pd, published=d['p_Gbar'], err=d['p_err'], pull=(pd - d['p_Gbar']) / d['p_err'], pass_=abs(pd - d['p_Gbar']) <= d['p_err'])
I2 = dict(R_um=R, G_LC_published_p=F.G_LC(d['p_Gbar'], R), G_LC_derived_p=F.G_LC(pd, R)); I2['pass_'] = I2['G_LC_published_p'] > 1
I3 = dict(ratio=F.alpha_fraction(d['Y_MJ'], d['E_hs_kJ'])); I3['pass_'] = I3['ratio'] > 1.4
I4 = dict(gain=d['Y_MJ'] / d['E_laser_MJ']); I4['pass_'] = abs(I4['gain'] - 0.72) < 0.01
p_tau = F.hs_pressure_Gbar(d['Y_MJ'], d['T_keV'], d['tau_ps'] * 1.1, d['V_um3']); p_V = F.hs_pressure_Gbar(d['Y_MJ'], d['T_keV'], d['tau_ps'], d['V_um3'] * 1.1)
I5 = dict(ratio_tau=p_tau / pd, ratio_V=p_V / pd, expected=1 / math.sqrt(1.1)); I5['pass_'] = abs(I5['ratio_tau'] - I5['expected']) < 1e-12 and abs(I5['ratio_V'] - I5['expected']) < 1e-12
extra = dict(Y_ign_MJ_example_M0p2_rhoR0p44=F.Y_ign_MJ(0.2, 0.44))
r = dict(I1=I1, I2=I2, I3=I3, I4=I4, I5=I5, extra=extra)
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom4.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
