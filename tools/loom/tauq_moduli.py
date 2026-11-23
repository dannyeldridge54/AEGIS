"""D2140: tau_q moduli cosmology (dilution, moduli-induced gravitinos -> winos with re-annihilation). PREREG_D2140."""
import json, math, statistics
MP = 2.435e18; MPf = 1.2209e19; TR = 1.34e9; m32 = 2.6e5; tau32 = 1.4e-3; mw = 700.0; hbar = 6.582e-25
GEV2_TO_CM3S = 1.167e-17
def Td(m): G = m**3/(4*math.pi*MP**2); return (90/(math.pi**2*106.75))**0.25*math.sqrt(G*MP)
gs = 10.75; t = tau32/hbar; T32 = math.sqrt(0.301*MPf/math.sqrt(gs)/t)
H32 = 1.66*math.sqrt(gs)*T32**2/MPf; s32 = 2*math.pi**2/45*gs*T32**3
out = dict(T_3half_GeV=T32, rows=[])
for m in (2e10, 1e11):
    td = Td(m); D = TR/(6*td)
    for Brn, Br in (('0.01', 0.01), ('0.1', 0.1), ('(m32/m)^2', (m32/m)**2)):
        Y32 = 2*Br*0.75*td/m*min(1.0, D)
        oms = []
        for sv in (2.5e-25, 1e-24, 3e-24):
            Ycap = H32/(s32*sv/GEV2_TO_CM3S); Y = min(Y32, Ycap); oms.append(2.744e8*mw*Y)
        out['rows'].append(dict(m=m, T_d=td, D=D, Br=Brn, Y32=Y32, Omega_h2=oms, Omega_med=statistics.median(oms)))
# phi0 needed so that generic Br=0.01 passes at m=2e10 (D < 1 regime: yield scales as D ~ phi0^2)
td = Td(2e10); Y_need = 0.036/(2.744e8*mw)
Dneed = Y_need/(2*0.01*0.75*td/2e10); out['phi0_needed_for_generic_Br'] = math.sqrt(6*td*Dneed/TR) if Dneed < 1 else None
r = [x for x in out['rows'] if x['m'] == 2e10]
gen = [x for x in r if x['Br'] == '0.01'][0]['Omega_med']; sup = [x for x in r if x['Br'] == '(m32/m)^2'][0]['Omega_med']
out['a_dilution_verdict'] = 'PASS' if r[0]['D'] <= 1e3 else 'FAIL'
out['b_verdict'] = 'PASS' if gen <= 0.036 else ('CONDITIONAL' if sup <= 0.036 else 'FAIL')
print(json.dumps(out, indent=1, default=float)); json.dump(out, open('field_tests/results/d2140_tauq_moduli.json', 'w'), indent=1)
