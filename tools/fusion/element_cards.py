"""CM-CARDS: one card per element (Z = 0 neutron, 1..118) joining mendeleev (periodic/atomic/thermal/geo data), NUBASE2020 (every
known nuclide) with binding energy per nucleon from the AME2020 mass excess, and the OPEN-ADAS cooling table where catalogued."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nuclide_pulse as P
ME_H, ME_N = 7288.971064, 8071.318062     # keV, AME2020 mass excesses of 1H and n
YEAR = 31557600.0
FIELDS = ['atomic_weight', 'atomic_weight_uncertainty', 'block', 'period', 'group_id', 'density', 'melting_point', 'boiling_point',
          'fusion_heat', 'evaporation_heat', 'specific_heat_capacity', 'molar_heat_capacity', 'thermal_conductivity', 'lattice_structure',
          'lattice_constant', 'atomic_radius', 'covalent_radius_pyykko', 'vdw_radius', 'metallic_radius', 'en_pauling', 'en_allen',
          'electron_affinity', 'dipole_polarizability', 'abundance_crust', 'abundance_sea', 'is_radioactive', 'is_monoisotopic',
          'geochemical_class', 'goldschmidt_class', 'discoverers', 'discovery_year', 'discovery_location', 'name_origin', 'uses', 'sources',
          'cas', 'price_per_kg', 'description']

def _clean(v):
    if v is None: return None
    if isinstance(v, float): return None if math.isnan(v) else v
    if isinstance(v, (int, str, bool)): return v
    try: return float(v)
    except Exception: return str(v)

def nuclide_rows(rows, Z, sym='n'):
    out = []
    for r in sorted((r for r in rows if r['Z'] == Z), key=lambda r: (r['A'], r['iso'])):
        A = r['A']; N = A - Z; be = (Z * ME_H + N * ME_N - r['me_keV']) / A / 1000.0 if (r['iso'] == 0 and A > 1) else None
        t = r['t12_s']
        out.append(dict(name=f"{sym}-{A}" + ('m' * min(r['iso'], 1) + (str(r['iso']) if r['iso'] > 1 else '') if r['iso'] else ''),
                        A=A, N=N, isomer=r['iso'], mass_excess_keV=r['me_keV'], mass_excess_estimated=r['me_est'],
                        BE_per_A_MeV=be, half_life_s=t, half_life_y=(t / YEAR if t else None), stable=r['stable'],
                        decay_or_abundance=r['modes']))
    return out

def build(path_out=None):
    from mendeleev.fetch import fetch_table
    import mendeleev
    T = fetch_table('elements').set_index('atomic_number')
    IE = fetch_table('ionizationenergies'); OX = fetch_table('oxidationstates'); ISO = fetch_table('isotopes'); PT = fetch_table('phasetransitions')
    rows = P.parse()
    try: adas = json.load(open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'element_catalog.json')))['elements']
    except Exception: adas = {}
    adas_by_Z = {v['Z']: (k, v) for k, v in adas.items()}
    cards = {}
    n0 = nuclide_rows(rows, 0)
    cards['n'] = dict(Z=0, symbol='n', name='neutron', nuclides=n0, n_nuclides=len(n0), sources={'nuclides': 'NUBASE2020'})
    for Z in range(1, 119):
        t = T.loc[Z]; sym = t['symbol']
        import re as _re; raw = t['electronic_configuration']; ec = ' '.join((p + '1') if _re.fullmatch(r'\d+[spdfg]', p) else p for p in raw.split())  # DEV-2
        c = dict(Z=Z, symbol=sym, name=t['name'], electron_configuration=ec, electron_configuration_raw=raw)
        c.update({f: _clean(t.get(f)) for f in FIELDS if f in t.index})
        ie = IE[IE['atomic_number'] == Z].sort_values('ion_charge')
        c['ionization_energies_eV'] = {int(d) + 1: _clean(v) for d, v in zip(ie['ion_charge'], ie['ionization_energy'])}
        pt = PT[PT['atomic_number'] == Z]
        if len(pt):
            p0 = pt.iloc[0]
            for f in ('melting_point', 'boiling_point', 'critical_temperature', 'critical_pressure', 'triple_point_temperature', 'triple_point_pressure'): c[f] = _clean(p0[f])
        c['nuclear_spin_moments'] = {f"{sym}-{int(r.mass_number)}": dict(spin=_clean(r.spin), parity=_clean(r.parity), g_factor=_clean(r.g_factor), Q_barn=_clean(r.quadrupole_moment)) for r in ISO[ISO['atomic_number'] == Z].itertuples() if _clean(r.abundance)}
        ox = OX[OX['atomic_number'] == Z]
        c['oxidation_states'] = sorted(int(v) for v in ox['oxidation_state'])
        iso = ISO[ISO['atomic_number'] == Z]
        c['natural_abundance_pct'] = {f"{sym}-{int(a)}": _clean(ab) for a, ab in zip(iso['mass_number'], iso['abundance']) if _clean(ab)}
        nu = nuclide_rows(rows, Z, sym); c['nuclides'] = nu; c['n_nuclides'] = len(nu)
        gs = [x for x in nu if x['isomer'] == 0]
        st = [x for x in gs if x['stable']]
        c['n_stable'] = len(st); c['A_range'] = [min(x['A'] for x in gs), max(x['A'] for x in gs)] if gs else None
        longest = max((x for x in gs if not x['stable'] and x['half_life_s']), key=lambda x: x['half_life_s'], default=None)
        c['longest_lived_radioactive'] = (dict(name=longest['name'], half_life_y=longest['half_life_y']) if longest else None)
        be = [x for x in gs if x['BE_per_A_MeV'] is not None and not x['mass_excess_estimated']]
        c['max_BE_per_A'] = (lambda x: dict(name=x['name'], MeV=x['BE_per_A_MeV']))(max(be, key=lambda x: x['BE_per_A_MeV'])) if be else None
        if Z in adas_by_Z:
            k, v = adas_by_Z[Z]; tab = v['table'].get('1e+20', [])
            c['adas_cooling'] = dict(status=v['status'], n_e_m3=1e20, points=[dict(T_keV=p['T_keV'], mean_z=p['mean_z'], L_line_W_m3=p['L_line'],
                                     L_rb_W_m3=p['L_rb']) for p in tab[::4]], note='coronal; L per impurity ion per electron')
        c['sources'] = {'atomic/thermal/geo': f'mendeleev {mendeleev.__version__}', 'nuclides': 'NUBASE2020 (Kondev et al. 2021) via pynucastro',
                        'BE_per_A': 'computed from AME2020 mass excess: (Z*7288.971 + N*8071.318 - ME)/A keV', 'cooling': 'OPEN-ADAS ADF11' if Z in adas_by_Z else None}
        cards[sym] = c
    if path_out:
        with open(path_out, 'w') as f: json.dump(dict(meta=dict(n_cards=len(cards), n_nuclides=sum(c['n_nuclides'] for c in cards.values()),
                                                            built='2026-11-23', lock='PREREG_CM_CARDS'), cards=cards), f, separators=(',', ':'))
    return cards

def summary(c, max_nuclides=12):
    """Text breakdown CubeMind reads (memory record / prompt card)."""
    if c['Z'] == 0: return 'neutron: ' + '; '.join(f"{x['name']} t1/2 {x['half_life_s']} s" for x in c['nuclides'][:3])
    ie = {int(k): v for k, v in c['ionization_energies_eV'].items()}; gs = [x for x in c['nuclides'] if x['isomer'] == 0]
    keep = [x for x in gs if x['stable']] + sorted((x for x in gs if not x['stable'] and x['half_life_s']), key=lambda x: -x['half_life_s'])
    nl = '; '.join(f"{x['name']} " + ('stable' if x['stable'] else f"t1/2 {x['half_life_s']:.4g} s") + (f", B/A {x['BE_per_A_MeV']:.4f} MeV" if x['BE_per_A_MeV'] else '')
                   for x in keep[:max_nuclides])
    s = (f"ELEMENT CARD {c['name']} ({c['symbol']}, Z={c['Z']}): weight {c.get('atomic_weight')}, config {c['electron_configuration']}, block {c.get('block')}, "
         f"period {c.get('period')}, group {c.get('group_id')}; IE1..3 {[ie.get(i) for i in (1, 2, 3)]} eV, {len(ie)} ionization energies known; "
         f"oxidation states {c['oxidation_states']}; density {c.get('density')} g/cm3, melt {c.get('melting_point')} K, boil {c.get('boiling_point')} K; "
         f"electronegativity (Pauling) {c.get('en_pauling')}; crust abundance {c.get('abundance_crust')} mg/kg; natural isotopes {c['natural_abundance_pct']}; "
         f"{c['n_nuclides']} known nuclides (A {c['A_range']}), {c['n_stable']} stable; longest-lived radioactive {c['longest_lived_radioactive']}; "
         f"max binding/A {c['max_BE_per_A']}. Nuclides: {nl}.")
    if c.get('adas_cooling'): s += ' ADAS mean charge at n_e 1e20: ' + ', '.join(f"{p['T_keV']:.3g} keV -> {p['mean_z']:.2f}" for p in c['adas_cooling']['points'])
    return s + ' [sources: mendeleev, NUBASE2020/AME2020' + (', OPEN-ADAS' if c.get('adas_cooling') else '') + ']'

if __name__ == '__main__':
    out = os.path.join(HERE, 'element_cards.json'); cards = build(out); print(len(cards), os.path.getsize(out))
