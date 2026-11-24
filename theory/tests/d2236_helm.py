"""D2236 (PREREG_D2236_HELM_POWER): steer R and B; per machine optimise dials; locked hard limits; report P_net and the binding limit."""
import json, math, sys, os
sys.path.insert(0, 'tools/fusion'); import fusion as F, fusion_fast as X
EA = F.two_body_split('DT')[1]; I0 = F.ITER; PIN = dict(F.PLANT_DEMO, M=1.161); SHARE = F.two_body_split('DT')[0] / F.q_value('DT')
nG0 = I0['Ip'] / (math.pi * I0['a'] ** 2)
def machine(R, B):
    s = R / I0['R']; a = I0['a'] * s; Ip = I0['Ip'] * (B / I0['B']) * s; nG = Ip / (math.pi * a ** 2); g = nG / nG0
    m = dict(I0, R=R, a=a, B=B, Ip=Ip, V=I0['V'] * s ** 3, S=I0['S'] * s ** 2, n_ped=I0['n_ped'] * g, n_sep=I0['n_sep'] * g, n_avg=I0['n_avg'] * g,
             P_line=I0['P_line'] * s ** 3 * g ** 2)
    return m
def dials(m):
    best = None; why = {}
    nG = m['Ip'] / (math.pi * m['a'] ** 2) * 1e20
    for Pa in (30.0, 40.0, 50.0, 60.0, 73.0, 100.0):
        for i in range(21):
            n = nG * (0.6 + 0.4 * i / 20)
            try: op = X.operating_point_fast(m, EA, n_avg=n, P_aux=Pa)
            except Exception: op = None
            if op is None: why['no_solution'] = why.get('no_solution', 0) + 1; continue
            Pn = op['P_fus'] * SHARE; wl = Pn / m['S']; psep = (op['P_loss'] - op['P_rad_core']) / m['R']
            fails = [k for k, bad in (('greenwald', op['f_G'] > m['fG_max']), ('beta_N', op['beta_N'] > 2.8), ('L-H', op['P_loss'] < 1.3 * op['P_LH']),
                                      ('wall_load', wl > 2.0), ('Psep/R', psep > 17.0)) if bad]
            for k in fails: why[k] = why.get(k, 0) + 1
            if fails: continue
            pl = F.plant(op['P_fus'], Pa, PIN)
            if best is None or pl['P_net'] > best['P_net']:
                best = dict(P_net=pl['P_net'], Q_e=pl['Q_e'], P_fus=op['P_fus'], Q=op['Q'], P_aux=Pa, n_over_nG=n / nG, f_G=op['f_G'], beta_N=op['beta_N'],
                            lh=op['P_loss'] / op['P_LH'], wall_load=wl, Psep_R=psep)
    return best, why
out = []
for R in (6.2, 7.0, 8.0, 9.0):
    for B in (5.3, 6.0, 7.0, 8.0, 9.0):
        m = machine(R, B); a = m['a']; Bcoil = B * R / (R - a - 1.2)
        best, why = dials(m)
        if best:
            near = {k: v for k, v in (('f_G/0.94', best['f_G'] / 0.94), ('beta_N/2.8', best['beta_N'] / 2.8), ('1.3/LH', 1.3 / best['lh']),
                                      ('wall/2', best['wall_load'] / 2.0), ('Psep_R/17', best['Psep_R'] / 17))}
            best['binding'] = max(near, key=near.get)
        out.append(dict(R=R, B=B, Ip=m['Ip'], B_coil=Bcoil, nb3sn_ok=Bcoil <= 12, hts_ok=Bcoil <= 20, best=best, rejections=why))
        b = best or {}
        print(R, B, f"Ip {m['Ip']:.1f} Bcoil {Bcoil:.1f}", 'P_net', round(b.get('P_net', float('nan')), 1), 'P_fus', round(b.get('P_fus', float('nan')), 0), 'Q', round(b.get('Q', float('nan')), 1), b.get('binding'), flush=True)
def top(cls): c = [o for o in out if o[cls] and o['best']]; return max(c, key=lambda o: o['best']['P_net']) if c else None
res = dict(control_ITER=next(o for o in out if o['R'] == 6.2 and o['B'] == 5.3)['best'], best_nb3sn=top('nb3sn_ok'), best_hts=top('hts_ok'), machines=out)
json.dump(res, open('field_tests/results/d2236_helm.json', 'w'), indent=1, default=float)
print('BEST Nb3Sn', {k: res['best_nb3sn'][k] for k in ('R', 'B')}, res['best_nb3sn']['best']); print('BEST HTS', {k: res['best_hts'][k] for k in ('R', 'B')}, res['best_hts']['best'])
