"""Fusion engine for CubeMind (CM-FUSION): one dispatcher, numbers (+ chart specs where useful). Same validated engine (FUSION-1, PROM-1..5)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F
import fusion_fast as X
EA = F.two_body_split('DT')[1]
MACH = dict(ITER=F.ITER, ITER_400=F.ITER_400)

def _chart(title, xl, yl, series, logy=False):
    return dict(title=title, x_label=xl, y_label=yl, logy=logy, series=[dict(name=n, x=[float(v) for v in x], y=[float(v) for v in y]) for n, x, y in series])

def sigmav(a):
    r = a.get('reaction', 'DT'); T = float(a['T_keV']); Ts = [10 ** (i / 20) for i in range(0, 41)]
    return dict(reaction=r, T_keV=T, sigmav_cm3_s=F.sigmav(r, T),
                chart=_chart(f'{r} reactivity (Bosch-Hale)', 'T (keV)', '<sigma v> (cm^3/s)', [(r, Ts, [F.sigmav(r, t) for t in Ts])], logy=True))
def q_value(a):
    r = a.get('reaction', 'DT'); out = dict(reaction=r, Q_MeV=F.q_value(r))
    if r == 'DT': En, Ea = F.two_body_split('DT'); out.update(E_n_MeV=En, E_alpha_MeV=Ea)
    return out
def ignition(a):
    T, ntt = F.ignition_min(EA); return dict(T_min_keV=T, nTtau_min=ntt, T_ideal_keV=F.ideal_ignition_T(EA), units='keV s m^-3')
def operating_point(a):
    m = MACH[a.get('machine', 'ITER')]; op = X.operating_point_fast(m, EA, n_avg=a.get('n_avg'), P_aux=a.get('P_aux'))
    if op is None: return dict(error='no hot operating point')
    return {k: op[k] for k in ('P_fus', 'Q', 'tau_E', 'Te_avg', 'Ti_avg', 'W_MJ', 'beta_N', 'f_He', 'f_G', 'P_loss', 'P_LH', 'P_rad')}
def plant(a):
    p = F.plant(float(a['P_fus']), float(a['P_aux']), dict(F.PLANT_DEMO, **{k: a[k] for k in ('eta_wp', 'P_other', 'eta_th') if k in a}))
    return {k: p[k] for k in ('P_th', 'P_gross', 'P_recirc', 'P_net', 'Q_e', 'M')}
def nif_pressure(a):
    p = F.hs_pressure_Gbar(float(a['Y_MJ']), float(a['T_keV']), float(a['tau_ps']), float(a['V_um3'])); R = F.hs_radius_um(float(a['V_um3']))
    return dict(p_Gbar=p, R_um=R, G_LC_proxy=F.G_LC(p, R))
def gamow(a):
    g = F.gamow(int(a['Z1']), int(a['Z2']), float(a['mu_u']), T_K=a.get('T_K'), kT_keV=a.get('kT_keV')); return dict(E0_keV=g['E0_keV'], width_keV=g['width_keV'])
def tritium_burn(a):
    P = float(a.get('P_GW', 1.0)); return dict(T_kg_per_fpy=F.burn_kg_per_GWfpy('T') * P, Li6_kg_per_fpy=F.burn_kg_per_GWfpy('Li6') * P, D_kg_per_fpy=F.burn_kg_per_GWfpy('D') * P)
def tbr(a): return dict(TBR=F.tbr_required(float(a['P_GW']), float(a['inventory_kg']), float(a['doubling_years'])))
def burn_fraction(a): return dict(Phi=F.burn_fraction(float(a['rhoR'])))
def element_cooling(a):
    import adas as A
    el = a['element'].lower(); T = float(a['T_keV']); ne = float(a.get('ne_m3', 1e20))
    return dict(element=el, T_keV=T, L_line_W_m3=A.L_line(el, ne, T), L_imp_W_m3=A.L_imp(el, ne, T), mean_charge=float(sum(i * f for i, f in enumerate(A.fractions(el, ne, T)))))
def nuclide(a):
    import nuclide_pulse as P
    Z, A, iso = P.key(a['name']); rows = [r for r in P.parse() if r['Z'] == Z and r['A'] == A and (r['iso'] > 0) == iso]
    if not rows: return dict(error=f'{a["name"]} not in NUBASE2020')
    r = rows[0]; return dict(name=a['name'], mass_excess_keV=r['me_keV'], half_life_s=r['t12_s'], stable=r['stable'], decay=r['modes'])

TOOLS = {'fusion_sigmav': sigmav, 'fusion_q_value': q_value, 'fusion_ignition': ignition, 'fusion_operating_point': operating_point,
         'fusion_plant': plant, 'fusion_nif_pressure': nif_pressure, 'fusion_gamow': gamow, 'fusion_tritium_burn': tritium_burn,
         'fusion_tbr': tbr, 'fusion_burn_fraction': burn_fraction, 'element_cooling': element_cooling, 'nuclide_lookup': nuclide}
EXAMPLES = {'fusion_sigmav': '{"reaction": "DT", "T_keV": 10}', 'fusion_q_value': '{"reaction": "DT"}', 'fusion_ignition': '{}',
            'fusion_operating_point': '{"machine": "ITER"}', 'fusion_plant': '{"P_fus": 500, "P_aux": 50}',
            'fusion_nif_pressure': '{"Y_MJ": 1.37, "T_keV": 10.9, "tau_ps": 89, "V_um3": 640000}', 'fusion_gamow': '{"Z1": 1, "Z2": 1, "mu_u": 0.5036, "T_K": 15000000}',
            'fusion_tritium_burn': '{"P_GW": 1}', 'fusion_tbr': '{"P_GW": 1, "inventory_kg": 10, "doubling_years": 5}', 'fusion_burn_fraction': '{"rhoR": 3}',
            'element_cooling': '{"element": "Ar", "T_keV": 1.0}', 'nuclide_lookup': '{"name": "Pu-241"}'}
def run(name, args): return TOOLS[name](args)
