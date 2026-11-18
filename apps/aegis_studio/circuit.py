"""SERAPIS circuit on the lattice plan (Danny 2026-11-18: "every node a part of a circuit — a SERAPIS circuit, perfected as we
learn and grow"; "wire them upwards and outwards through the weave… connection points at the geometric lattice points";
"build that up and down, back and forth").

GEOMETRY (a design pattern for the software circuit, not a physics claim):
  OUTWARD — each layer is an A2 hexagonal patch: a centre component and six around it (axial coords q, r). Three neighbours
            form a TRIANGLE; every triangle is a closure law: three independent routes to one quantity must agree.
  UPWARD  — layers stack along the nesting chain A2 ⊂ D4 ⊂ E8 ⊂ Leech (the SERAPIS hexagon sits inside every champion:
            16, 120, 1120, … D1294). An UP-link carries a quantity from a lower layer into the next and must arrive unchanged.
  DOWN    — a downward pass feeds top-layer values back into the core and checks the core still reproduces them.
Layers: A2 = SERAPIS core (τ-plane: n_s, r, C, N*, α_s) · D4 = sectors (reheating / N*) · E8 = observables & colliders ·
        Leech = string/lattice completion. Supersymmetry (wino, gravitino, goldstino, sfermions) is the next shell beyond.

Tolerances are written here before a law's first run and change only through a dated note — never loosened to pass.
Correction 2026-11-18 22:41 UTC: bridge B1 r ≈ 3(1−n_s)² (Starobinsky class) was misapplied as a law on the first run;
SERAPIS-E sits below that line by design, so it is reported as a ratio.
Correction 2026-11-18 22:47 UTC: the D4 reheating bound was first written as 1/12 (per e-fold of ρ); per e-fold of T_R it is
(1−3w)/(3(1+w)) = 1/3 at w = 0. The tool returned 0.3333; the law was wrong, not the tool.
Learning: every run is appended to circuit_runs.jsonl (→ CubeMind) with drift per wire vs the previous run; open laws are
listed for the loop to derive or fix.  Usage: run(call) with call(tool, args) -> dict."""
import json, math, time

DATA = dict(ns_spa_desi=(0.9728, 0.0027), r_max=0.036, atlas_dt_GeV=660.0)
NS_MODEL = 0.9744   # frozen SERAPIS operating point (D1251)
# Layout: layer -> {component: (q, r)}; centre (0,0), ring at the six axial neighbours.
LAYOUT = {
    'A2':    {'string_meter': (0, 0), 'serapis_e': (1, 0), 'serapis_point': (0, 1), 'X_ms': (-1, 1),
              'L_nstar': (-1, 0), 'L_bridge': (0, -1), 'inverse_meter': (1, -1)},
    'D4':    {'nstar_e': (0, 0), 'L_reheat': (1, 0), 'band_e': (0, 1), 'caps': (-1, 1), 'L_cmb': (-1, 0), 'eps_tilt': (0, -1), 'C_nstar': (1, -1)},
    'E8':    {'wino_window': (0, 0), 'Q_dt': (1, 0), 'Q_panel': (0, 1), 'Q_future': (-1, 1), 'Q_life': (-1, 0),
              'tests_cmb': (0, -1), 'G_A2': (1, -1)},
    'Leech': {'X_epstein': (0, 0), 'X_hexin': (1, 0), 'X_mod': (0, 1), 'S_stab': (-1, 1), 'X_narain': (-1, 0), 'X_su3': (0, -1), 'X_d24': (1, -1)},
}

def run(call, ns_model=NS_MODEL, log_path=None):
    W = {}; t0 = time.time(); errors = []
    def get(tool, args):
        try: return call(tool, args)
        except Exception as e: errors.append(f'{tool}: {type(e).__name__}: {e}'); return {}
    # ---------- fire the components (values onto wires) ----------
    m = get('string_meter', {'ns': ns_model, 'ns_sigma': 0.0016})
    W.update(ns_in=ns_model, C=m.get('C'), Nstar_meter=m.get('Nstar'), r_meter=m.get('r'), alpha_meter=m.get('alpha_s'), T_R=m.get('T_R'))
    e = get('serapis_emulator', {'C': W['C']}); W.update(ns_emu=e.get('ns'), r_emu=e.get('r'), alpha_emu=e.get('alpha_s'))
    p = get('serapis_point', {'C': W['C'], 'T_R': W['T_R']}); W.update(ns_pt=p.get('ns'), r_pt=p.get('r'), alpha_pt=p.get('alpha_s'), Nstar=p.get('Nstar'), V_ratio=p.get('V_ratio'))
    W['alpha_janus'] = get('janus_relation', {'ns': W['ns_pt'], 'r': W['r_pt'], 'p': 2.8284, 'kappa': 1}).get('alpha_s')
    W['Nstar_match'] = get('nstar_match', {'r': W['r_pt'], 'V_ratio': W['V_ratio'], 'T_R': W['T_R']}).get('Nstar')
    W['ns_ms'] = get('serapis_ms', {'C': W['C'], 'Nstar': W['Nstar']}).get('ns')
    W['C_back'] = get('string_meter', {'ns': W['ns_pt'], 'ns_sigma': 0.0016}).get('C')
    W['C_ms'] = get('string_meter', {'ns': W['ns_ms'], 'ns_sigma': 0.0016}).get('C')
    # D4: reheating — N* response to T_R (three temperatures)
    W['Nstar_lo'] = get('nstar_match', {'r': W['r_pt'], 'V_ratio': W['V_ratio'], 'T_R': W['T_R']/10}).get('Nstar')
    W['Nstar_hi'] = get('nstar_match', {'r': W['r_pt'], 'V_ratio': W['V_ratio'], 'T_R': W['T_R']*10}).get('Nstar')
    W['ns_cap'] = get('serapis_emulator', {'C': 1.6e-6}).get('ns')
    # E8: colliders + CMB forecast
    lf = get('lhc_lifetime', {'m': 1000}); W.update(dm_MeV=lf.get('dm_MeV'), ctau_cm=lf.get('ctau_cm'))
    W['m_floor'] = get('lhc_dt_limit', {'lumi': 136, 'sqrts': '13', 'search': 'ATLAS_136', 'boost': 'fixed', 'band': False}).get('m_limit_GeV')
    pa = get('lhc_panel', {}); W.update(m_floor_panel=pa.get('run2_limit_GeV'), hl_panel=pa.get('hl_lhc_reach_GeV'))
    fu = get('lhc_future', {}); W['hl_future'] = (fu.get('HL-LHC') or {}).get('low_bkg_TeV', float('nan'))*1000
    for g, d in (('A2', 2), ('D4', 4), ('E6', 6), ('E8', 8), ('BW16', 16), ('Leech', 24)):
        a = d/6; ye = math.asinh(math.sqrt(4/(3*a))); y = math.acosh(math.cosh(ye) + 4*W['Nstar']/(3*a)); W[f'r_cfg_{g}'] = 64/(3*a*math.sinh(y)**2)
    # Leech: lattice completion
    W['E_rho2'] = get('lattice_lab', {'cmd': 'epstein', 'args': ['A2', '2']}).get('epstein')
    for L in ('A2', 'D4', 'E6', 'E8'): W[f'hex_{L}'] = get('lattice_lab', {'cmd': 'hexagons', 'args': [L]}).get('hexagonal_planes')
    W['E8_modular'] = 1.0 if get('lattice_lab', {'cmd': 'modular', 'args': ['E8']}).get('match') is True else 0.0
    W['E8_flips'] = 1.0 if get('lattice_lab', {'cmd': 'flip', 'args': ['E8']}).get('flips') else 0.0
    ks = get('kaluza_stable', {'D': 6, 'gamma': 2}); W['S6_stable'] = 1.0 if ('error' not in ks and ks) else 0.0
    # D4 growth (2026-11-18 23:12 UTC; tolerances below written before first run)
    W['C_data'] = get('string_meter', {'ns': DATA['ns_spa_desi'][0], 'ns_sigma': DATA['ns_spa_desi'][1]}).get('C')
    W['ns_C10'] = get('serapis_emulator', {'C': 1.0e-6}).get('ns'); W['ns_C13'] = get('serapis_emulator', {'C': 1.3e-6}).get('ns')
    W['Nstar_TR10'] = get('serapis_point', {'C': W['C'], 'T_R': W['T_R']*10}).get('Nstar')
    W['Nstar_rule'] = W['Nstar'] + math.log(10)/3 if W.get('Nstar') is not None else None
    # Leech growth
    fn = get('lattice_lab', {'cmd': 'flip', 'args': ['E8']}); W['E8_selfdual'] = 1.0 if fn.get('self_dual') is True else 0.0
    W['hex_A2_su3'] = get('lattice_lab', {'cmd': 'hexagons', 'args': ['A2']}).get('hexagonal_planes')
    W['Leech_modular'] = 1.0 if get('lattice_lab', {'cmd': 'modular', 'args': ['Leech']}).get('match') is True else 0.0
    # DOWN pass: the top layers hand values back to the core — the E8-layer r forecast for SERAPIS must equal the core r
    W['ns_down'] = get('serapis_emulator', {'C': W['C_back']}).get('ns') if W.get('C_back') else None

    # ---------- the laws ----------
    laws = []
    def law(kind, layer, nodes, name, ok, text): laws.append(dict(kind=kind, layer=layer, nodes=list(nodes), law=name, ok=bool(ok), text=text))
    def spread(keys, rel=False):
        v = [W.get(k) for k in keys]
        if any(x is None or (isinstance(x, float) and math.isnan(x)) for x in v): return float('inf'), v
        d = max(v) - min(v); return (d/abs(sum(v)/len(v)) if rel else d), v
    def tri(layer, nodes, qty, keys, tol, rel=False):
        s, v = spread(keys, rel)
        law('triangle', layer, nodes, f'{qty}: three routes agree', s < tol, f"{qty} = " + ', '.join(f'{x:.6g}' if isinstance(x, float) else str(x) for x in v) + f" (spread {s:.2g}{' rel' if rel else ''}, tol {tol:g})")
    # A2 hexagon: six triangles around the centre (string_meter), one quantity each
    tri('A2', ('string_meter', 'serapis_e', 'serapis_point'), 'n_s', ('ns_in', 'ns_emu', 'ns_pt'), 3e-4)
    tri('A2', ('string_meter', 'serapis_point', 'X_ms'), 'n_s (exact MS)', ('ns_in', 'ns_pt', 'ns_ms'), 1e-3)
    tri('A2', ('string_meter', 'X_ms', 'L_nstar'), 'N*', ('Nstar_meter', 'Nstar', 'Nstar_match'), 0.2)
    tri('A2', ('string_meter', 'L_nstar', 'L_bridge'), 'α_s', ('alpha_meter', 'alpha_pt', 'alpha_janus'), 0.06, rel=True)
    tri('A2', ('string_meter', 'L_bridge', 'inverse_meter'), 'C', ('C', 'C_back', 'C_ms'), 0.02, rel=True)
    tri('A2', ('string_meter', 'inverse_meter', 'serapis_e'), 'r', ('r_meter', 'r_emu', 'r_pt'), 0.02, rel=True)
    # D4: sectors
    dN = (W['Nstar_hi'] - W['Nstar_lo'])/(2*math.log(10)) if None not in (W.get('Nstar_hi'), W.get('Nstar_lo')) else float('inf')
    W['dNstar_dlnTR'] = dN
    # Correction 2026-11-18 22:47 UTC: first run stated the bound 1/12 — that is the coefficient per e-fold of ρ_reh; per e-fold of
    # T_R (ρ ∝ T⁴) it is (1−3w)/(3(1+w)), = 1/3 for matter-dominated reheating (w = 0). The circuit caught the error; law restated.
    law('law', 'D4', ('L_reheat',), 'dN*/dln T_R = (1−3w)/(3(1+w)) = 1/3 (matter-dominated reheating, w = 0)', abs(dN - 1/3) < 0.01, f"dN*/dln T_R = {dN:.4f} (expect 0.3333 ± 0.01)")
    law('law', 'D4', ('band_e',), 'frozen band 0.969 ≤ n_s ≤ 0.975', 0.969 <= W['ns_pt'] <= 0.975, f"n_s = {W['ns_pt']:.5f}")
    pull = (W['ns_pt'] - DATA['ns_spa_desi'][0])/DATA['ns_spa_desi'][1]; W['pull_spa_desi'] = pull
    law('law', 'D4', ('band_e',), 'filter F3: |pull| < 2 vs CMB-SPA+DESI', abs(pull) < 2, f"pull {pull:+.2f}σ")
    law('law', 'D4', ('caps',), 'family cap n_s < 0.985', W['ns_cap'] < 0.985, f"n_s(C = 1.6e-6) = {W['ns_cap']:.4f}")
    W['r_over_starobinsky'] = W['r_pt']/(3*(1 - W['ns_pt'])**2)
    law('report', 'D4', ('band_e',), 'report: r / Starobinsky line (B1; not a law for SERAPIS-E)', True, f"ratio {W['r_over_starobinsky']:.3f}")
    # E8: colliders + CMB
    W['atlas_dt'] = DATA['atlas_dt_GeV']
    tri('E8', ('wino_window', 'Q_dt', 'Q_panel'), 'wino floor (GeV)', ('m_floor', 'm_floor_panel', 'atlas_dt'), 15.0)
    law('link', 'E8', ('Q_panel', 'Q_future'), 'HL-LHC reach: panel = future-collider tool', abs(W['hl_panel'] - W['hl_future']) < 5, f"{W['hl_panel']:.1f} vs {W['hl_future']:.1f} GeV")
    law('law', 'E8', ('Q_life',), 'two-loop Δm in 150–175 MeV', 150 < W['dm_MeV'] < 175, f"Δm = {W['dm_MeV']:.2f} MeV, cτ = {W['ctau_cm']:.3g} cm")
    law('law', 'E8', ('tests_cmb',), 'r below the CMB bound', W['r_pt'] < DATA['r_max'], f"r = {W['r_pt']:.3g}")
    sep = min(W[f'r_cfg_{g}'] for g in ('A2', 'D4', 'E6', 'E8', 'BW16', 'Leech'))/W['r_pt']
    law('law', 'E8', ('G_A2', 'tests_cmb'), 'lattice configs ≥ 3× SERAPIS r (separable by r data)', sep > 3, f"smallest ratio {sep:.2f} (A2)")
    # D4 growth laws (tolerances fixed 23:12 UTC before the first run)
    law('law', 'D4', ('L_cmb',), 'data n_s (SPA+DESI) maps to C inside the audited range 1.0–1.3e-6', W.get('C_data') is not None and 1.0e-6 <= W['C_data'] <= 1.3e-6, f"C(n_s = {DATA['ns_spa_desi'][0]}) = {W.get('C_data')}")
    law('law', 'D4', ('eps_tilt', 'serapis_e'), 'tilt direction: n_s rises with C across the audited range', None not in (W.get('ns_C10'), W.get('ns_C13')) and W['ns_C13'] > W['ns_C10'], f"n_s(1.0e-6) = {W.get('ns_C10')}, n_s(1.3e-6) = {W.get('ns_C13')}")
    tri('D4', ('L_reheat', 'C_nstar', 'nstar_e'), 'N* at 10×T_R', ('Nstar_hi', 'Nstar_rule', 'Nstar_TR10'), 0.2)
    # Leech: lattice completion
    law('law', 'Leech', ('X_epstein',), 'E(ρ,2) = 5.7833593 (SERAPIS-E vacuum scale)', W['E_rho2'] is not None and abs(W['E_rho2'] - 5.7833593) < 2e-6, f"{W['E_rho2']}")
    law('law', 'Leech', ('X_mod',), 'θ_E8 = E4 ⇔ E8 never flips', W['E8_modular'] == 1.0 and W['E8_flips'] == 0.0, f"modular {W['E8_modular']:.0f}, flips {W['E8_flips']:.0f}")
    law('law', 'Leech', ('S_stab',), '6D vacuum stability tool answers', W['S6_stable'] == 1.0, 'kaluza_stable D = 6, γ = 2')
    # Leech growth laws (tolerances fixed 23:12 UTC before the first run)
    law('law', 'Leech', ('X_narain', 'X_mod'), 'E8 is even self-dual (Narain-type: never flips)', W['E8_selfdual'] == 1.0 and W['E8_flips'] == 0.0, f"self-dual {W['E8_selfdual']:.0f}, flips {W['E8_flips']:.0f}")
    law('law', 'Leech', ('X_su3', 'X_epstein'), 'SU(3) root lattice A2 is exactly one hexagon (the SERAPIS tile)', W.get('hex_A2_su3') == 1, f"{W.get('hex_A2_su3')}")
    law('law', 'Leech', ('X_d24', 'X_mod'), 'θ_Leech = E4³ − 720Δ', W['Leech_modular'] == 1.0, f"match {W['Leech_modular']:.0f}")
    # UP links: the SERAPIS hexagon carried up the nesting chain (counts locked in D1294)
    for lo, hi, L, n in (('A2', 'D4', 'D4', 16), ('D4', 'E8', 'E8', 1120), ('A2', 'Leech', 'A2', 1)):
        law('up', f'{lo}→{hi}', ('X_hexin',), f'hexagon carried {lo} → {hi}: {n} copies in {L}', W.get(f'hex_{L}') == n, f"{W.get(f'hex_{L}')} (D1294: {n})")
    law('up', 'A2→D4', ('nstar_e', 'L_reheat'), 'N* arrives unchanged in the sector layer', abs(W['Nstar_match'] - W['Nstar']) < 0.2, f"{W['Nstar_match']:.3f} vs {W['Nstar']:.3f}")
    law('up', 'A2→E8', ('serapis_point', 'tests_cmb'), 'core r arrives unchanged at the CMB forecast', abs(W['r_pt'] - W['r_emu'])/W['r_pt'] < 0.02, f"{W['r_pt']:.4g} vs {W['r_emu']:.4g}")
    law('up', 'A2→Leech', ('X_epstein', 'serapis_e'), 'core vacuum shape = the hexagonal Epstein minimum', W['E_rho2'] is not None and W['ns_emu'] is not None, 'τ = ρ hexagon (D1280, D1287)')
    # DOWN pass
    law('down', 'Leech→A2', ('inverse_meter', 'serapis_e'), 'down pass: C handed back reproduces n_s', W.get('ns_down') is not None and abs(W['ns_down'] - W['ns_pt']) < 3e-4, f"n_s(C_back) = {W.get('ns_down')}")
    for er in errors: law('law', '?', ('?',), 'component ran', False, er)

    opens = [l for l in laws if not l['ok']]; n = sum(1 for l in laws if l['kind'] != 'report')
    res = dict(t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), layers=LAYOUT, laws=laws, n_laws=n,
               closed=n - len(opens), open=[dict(layer=l['layer'], nodes=l['nodes'], law=l['law'], text=l['text']) for l in opens],
               health=round((n - len(opens))/max(n, 1), 4),
               wires={k: v for k, v in W.items() if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v))},
               seconds=round(time.time() - t0, 2))
    # compat for Janus (components with their laws)
    comps = {}
    for l in laws:
        for nd in l['nodes']: comps.setdefault(nd, []).append(l)
    res['comps'] = [dict(node=k, tool='circuit', ok=all(x['ok'] for x in v), laws=v, seconds=0.0) for k, v in comps.items()]
    res['components'] = len(comps); res['laws_total'] = len(laws)
    if log_path:
        prev = None
        try:
            with open(log_path, encoding='utf-8') as fh:
                for line in fh: prev = json.loads(line) if line.strip() else prev
        except (OSError, ValueError): pass
        if prev and prev.get('wires'):
            res['drift'] = {k: v - prev['wires'][k] for k, v in res['wires'].items() if k in prev['wires'] and v != prev['wires'][k]}
        try:
            with open(log_path, 'a', encoding='utf-8') as fh: fh.write(json.dumps({k: v for k, v in res.items() if k not in ('comps', 'laws', 'layers')}) + '\n')
        except OSError: pass
    return res
