"""Chronos for CubeMind (CM-NUCLEAR): one dispatcher, numbers + chart specs. Same engine as the referee-cleared Chronos."""
import math, numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chronos import T12, LAM, CHAINS, MIN, H, D, Y, needed_at_start, generator_peak, transient_ratio, solve_bateman, release_age, sn_luminosity, kilonova_luminosity
from chronos_branches import ni_mass_from_tail, ni_mass_arnett, dwd_merger_time, dwd_gw_freq, eob_activity
import chronos_a3 as A3

def _nuc(k):
    s = str(k).replace(' ', '')
    import re
    m = re.match(r'^([A-Za-z]+)-?(\d+)(m?)$', s)
    if m: s = f'{m.group(1)}-{m.group(2)}{m.group(3)}'
    for n in list(T12) + list(A3.T12x):
        if n.lower() == s.lower(): return n
    raise ValueError(f'unknown nuclide {k}; known: {", ".join(sorted(set(T12) | set(A3.T12x)))}')

def _chart(title, xl, yl, series, logy=False):
    return dict(title=title, x_label=xl, y_label=yl, logy=logy, series=[dict(name=n, x=[float(v) for v in x], y=[float(v) for v in y]) for n, x, y in series])

def half_life(a):
    n = _nuc(a['nuclide']); t = T12.get(n) or A3.T12x[n]; return dict(nuclide=n, half_life_s=t, half_life_h=t / H, half_life_d=t / D, half_life_y=t / Y)

def activity_after(a):
    n = _nuc(a['nuclide']); lam = A3.LAM[n]; A0 = float(a['A0']); t = float(a['hours']) * H
    ts = np.linspace(0, max(t * 1.5, 5 * math.log(2) / lam if t == 0 else t * 1.5), 120)
    return dict(nuclide=n, A=A0 * math.exp(-lam * t), chart=_chart(f'{n} decay', 'hours', 'activity (same unit as A0)', [(n, ts / H, A0 * np.exp(-lam * ts))]))

def make_now_for(a):
    n = _nuc(a['nuclide']); t = float(a['hours']) * H; need = float(a['A_needed']); lam = A3.LAM[n]
    ts = np.linspace(0, t, 100); make = needed_at_start(n, need, t) if n in LAM else need * math.exp(lam * t)
    return dict(nuclide=n, make_now=make, half_lives_elapsed=t * lam / math.log(2), warning='more than 10 half-lives: impractical' if t * lam / math.log(2) > 10 else None,
                chart=_chart(f'{n}: activity from now until use', 'hours from now', 'activity', [(n, ts / H, make * np.exp(-lam * ts))]))

def generator(a):
    p = _nuc(a['parent']); c = next((k for k in CHAINS if k.startswith(p + ' ') and 'generator' in k), None)
    if not c: raise ValueError(f'no generator for {p}')
    (n, br) = CHAINS[c]; lp, ld = LAM[n[0]], LAM[n[1]]; Ap = float(a.get('parent_GBq', 1.0)); tp = generator_peak(c)
    ts = np.linspace(0, min(4 * tp, 10 * T12[n[0]]), 160); N = [solve_bateman(n, br, [Ap * 1e9 / lp, 0], t) for t in ts]
    out = dict(chain=c, peak_hours=tp / H, equilibrium_ratio=transient_ratio(c),
               chart=_chart(f'{c}: ingrowth after elution', 'hours', 'GBq', [(n[0], ts / H, [lp * x[0] / 1e9 for x in N]), (n[1], ts / H, [ld * x[1] / 1e9 for x in N])]))
    if 'hours' in a:
        Nt = solve_bateman(n, br, [Ap * 1e9 / lp, 0], float(a['hours']) * H); out.update(daughter_GBq=ld * Nt[1] / 1e9, parent_GBq_then=lp * Nt[0] / 1e9)
    return out

def release_age_tool(a):
    pa, pb = str(a['pair']).split('/'); r, r0 = float(a['ratio_now']), float(a['ratio_at_release'])
    if not (0 < r < r0): raise ValueError('need 0 < ratio_now < ratio_at_release')
    y = release_age(r, r0, pa.strip(), pb.strip()); ys = np.linspace(0, y * 1.3, 120)
    lam = LAM[pa.strip()] - LAM[pb.strip()]
    return dict(years=y, days=y * 365.25, chart=_chart(f'{pa}/{pb} ratio since release', 'years', 'activity ratio', [('ratio', ys, r0 * np.exp(-lam * ys * Y))], logy=True))

def ac225_chain(a):
    A0 = float(a['Ac225_MBq_at_purification']); t = float(a.get('hours', 6)) * H
    A, _ = A3.ac225_activities(t, A0); out = dict(activities_MBq={k: float(v) for k, v in A.items() if k != 'Bi-209'})
    ts = np.linspace(1, max(t, 12 * H), 120); rows = [A3.ac225_activities(x, A0)[0] for x in ts]
    out['chart'] = _chart('Ac-225 chain ingrowth', 'hours', 'MBq', [(k, ts / H, [r[k] for r in rows]) for k in ('Ac-225', 'Bi-213', 'Pb-209')])
    if 'ac227_ratio_eob' in a and 'days_stored' in a: out['ac227_ratio_after'] = A3.ac227_fraction(float(a['days_stored']) * D, float(a['ac227_ratio_eob']))
    return out

def pu_separation_age(a):
    y = A3.pu_age(float(a['am_over_pu_activity'])); ys = np.linspace(0, max(1.5 * y, 1), 120)
    return dict(years=y, chart=_chart('Am-241/Pu-241 activity ratio since separation', 'years', 'ratio', [('Am/Pu', ys, [A3.pu_ratio(v) for v in ys])]))

def tritium(a):
    g, yrs = float(a['grams']), float(a['years']); left, he3 = A3.tritium(g, yrs); ys = np.linspace(0, max(yrs, 1) * 1.5, 100)
    return dict(left_g=left, He3_g=he3, percent_decayed=100 * (1 - left / g), chart=_chart('Tritium inventory', 'years', 'grams', [('H-3', ys, [A3.tritium(g, v)[0] for v in ys]), ('He-3', ys, [A3.tritium(g, v)[1] for v in ys])]))

def decay_heat(a):
    T = float(a['days_operated']) * D; t = float(a['hours_after_shutdown']) * H; ts = np.logspace(1, math.log10(max(t * 10, 3600 * 24 * 30)), 120)
    return dict(fraction=A3.decay_heat_way_wigner(t, T), note='Way-Wigner approximation (~factor 2 at extremes; excludes U-239/Np-239; not ANS-5.1)',
                chart=_chart('Decay heat after shutdown (Way-Wigner)', 'seconds after shutdown (log)', 'fraction of operating power', [('P/P0', np.log10(ts), [A3.decay_heat_way_wigner(v, T) for v in ts])], logy=True))

def supernova_heating(a):
    M = float(a['M_Ni_Msun']); t0 = a.get('t0_days'); t0 = None if t0 is None else float(t0); d = float(a['days']); ds = np.linspace(2, max(400, d), 200)
    return dict(erg_per_s=sn_luminosity(d * D, M, t0), note='radioactive heating; equals bolometric L near/after peak (Arnett)',
                chart=_chart(f'Ni-56 heating, {M} Msun' + ('' if t0 is None else f', t0 = {t0} d'), 'days', 'erg/s', [('heating', ds, [sn_luminosity(x * D, M, t0) for x in ds])], logy=True))

def nickel_mass(a):
    L, d = float(a['L_erg_s']), float(a['days'])
    if a.get('mode') == 'arnett': return dict(M_Ni_Msun=ni_mass_arnett(L, d * D), assumption='Arnett rule at peak, full trapping')
    t0 = a.get('t0_days'); t0 = None if t0 is None else float(t0)
    return dict(M_Ni_Msun=ni_mass_from_tail(L, d * D, t0), assumption='full trapping (Type II-P only)' if t0 is None else f'trapping t0 = {t0} d')

def white_dwarf_merger(a):
    P, m1, m2 = float(a['period_s']), float(a['m1']), float(a['m2']); Ps = np.linspace(P * 0.5, P * 3, 100)
    return dict(merger_Myr=dwd_merger_time(P, m1, m2) / Y / 1e6, f_gw_mHz=dwd_gw_freq(P) * 1e3, note='Peters 1964 point-mass coalescence (upper bound to contact)',
                chart=_chart(f'Merger time vs period ({m1}+{m2} Msun)', 'orbital period (s)', 'Myr', [('t_merge', Ps, [dwd_merger_time(p, m1, m2) / Y / 1e6 for p in Ps])], logy=True))

def kilonova_heating(a):
    M = float(a['M_ej_Msun']); d = float(a['days']); f = float(a.get('f_th', 0.5)); ds = np.linspace(0.25, max(30, d), 120)
    return dict(erg_per_s=kilonova_luminosity(d * D, M, f), note='order of magnitude (Korobkin+2012)', chart=_chart('Kilonova r-process heating', 'days', 'erg/s', [('heating', ds, [kilonova_luminosity(x * D, M, f) for x in ds])], logy=True))

def star_age(a):
    o = 10 ** float(a['log_eps_observed']); p = float(a['production_ratio'])
    g = A3.cosmo_age(o, p, 'U-238', 'Th-232', stable_ref=False) if a.get('pair') == 'U/Th' else A3.cosmo_age(o, p)
    if not g > 0: raise ValueError('observed ratio must be below the production ratio')
    return dict(age_Gyr=g, note='single r-process event; production ratio is the dominant uncertainty')

TOOLS = {'chronos_half_life': half_life, 'chronos_activity_after': activity_after, 'chronos_make_now': make_now_for, 'chronos_generator': generator,
         'chronos_release_age': release_age_tool, 'chronos_ac225': ac225_chain, 'chronos_pu_age': pu_separation_age, 'chronos_tritium': tritium,
         'chronos_decay_heat': decay_heat, 'chronos_supernova': supernova_heating, 'chronos_nickel_mass': nickel_mass,
         'chronos_wd_merger': white_dwarf_merger, 'chronos_kilonova': kilonova_heating, 'chronos_star_age': star_age}
EXAMPLES = {'chronos_half_life': '{"nuclide": "Tc-99m"}', 'chronos_activity_after': '{"nuclide": "I-131", "A0": 100, "hours": 24}',
            'chronos_make_now': '{"nuclide": "F-18", "A_needed": 370, "hours": 2.5}', 'chronos_generator': '{"parent": "Mo-99", "parent_GBq": 10, "hours": 23}',
            'chronos_release_age': '{"pair": "Cs-134/Cs-137", "ratio_now": 0.05, "ratio_at_release": 1}',
            'chronos_ac225': '{"Ac225_MBq_at_purification": 10, "hours": 6, "ac227_ratio_eob": 0.0015, "days_stored": 10}',
            'chronos_pu_age': '{"am_over_pu_activity": 0.02}', 'chronos_tritium': '{"grams": 1000, "years": 1}',
            'chronos_decay_heat': '{"days_operated": 365, "hours_after_shutdown": 24}', 'chronos_supernova': '{"M_Ni_Msun": 0.6, "days": 18, "t0_days": 35}',
            'chronos_nickel_mass': '{"L_erg_s": 1e41, "days": 200, "mode": "tail", "t0_days": 40}',
            'chronos_wd_merger': '{"period_s": 765, "m1": 0.26, "m2": 0.50}', 'chronos_kilonova': '{"M_ej_Msun": 0.05, "days": 1}',
            'chronos_star_age': '{"pair": "Th/Eu", "log_eps_observed": -0.52, "production_ratio": 0.45}'}
def run(name, args): return TOOLS[name](args)
