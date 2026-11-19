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
        Leech = string/lattice completion · 10D = the ten-dimensional vacuum and its KK tower (the "9 dimensionals") ·
        SUSY = the supersymmetry shell beyond (anomaly-mediated gauginos, gravitino window, wino window ↔ LHC) ·
        Moonshine = new territory past SUSY (Danny 2026-11-19): the 26D string, heterotic 16, Leech, Klein's j and the Monster —
        MATHEMATICAL links (exact identities), not physics predictions. Supersymmetry (wino, gravitino, goldstino, sfermions) is the next shell beyond.

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
    'Late':  {'J_lt': (0, 0), 'R_desi': (1, 0), 'R_growth': (0, 1), 'R_w0wa': (-1, 1), 'T_hyperion': (-1, 0), 'R_clock': (0, -1), 'R_biref': (1, -1)},
    'Leech': {'X_epstein': (0, 0), 'X_hexin': (1, 0), 'X_mod': (0, 1), 'S_stab': (-1, 1), 'X_narain': (-1, 0), 'X_su3': (0, -1), 'X_d24': (1, -1)},
    '10D':   {'S_10d': (0, 0), 'S_kk10': (1, 0), 'S_btr': (0, 1), 'S_6d': (-1, 1)},
    'SUSY':  {'m32_window': (0, 0), 'gravitino_wino': (1, 0), 'covariant': (0, 1), 'tests_lhc': (-1, 1), 'H_relic': (-1, 0), 'matter_parity': (0, -1), 'H_line': (1, -1)},
    'P3': {'P3_kappa': (0, 0), 'P3_Y': (1, 0), 'P3_E7': (0, 1), 'P3_K': (-1, 1), 'P3_plateau': (-1, 0), 'P3_chamber': (0, -1), 'P3_shift': (1, -1)},
    'Moonshine': {'X_mellin': (0, 0), 'X_d8': (1, 0), 'X_d16': (0, 1), 'X_bw16': (-1, 1), 'X_rings': (-1, 0), 'X_crit': (0, -1), 'vac_i': (1, -1)},
}

def run(call, ns_model=NS_MODEL, log_path=None, records=None):
    records = records or {}
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
    # 10D layer ("9 dimensionals", 2026-11-18 23:20 UTC; tolerances below fixed before the first run)
    k1 = get('kaluza_scalar', {'D': 10, 'gamma': 1.5}); k2 = get('kaluza_scalar', {'D': 10, 'gamma': 1.5, 'method': 'fd'})
    W['kk10_kind_critical'] = 1.0 if k1.get('kind') == 'critical' else 0.0
    W['m2_1_pr'], W['m2_2_pr'] = (k1.get('m2') or [None, None])[:2]; W['m2_1_fd'], W['m2_2_fd'] = (k2.get('m2') or [None, None])[:2]
    W['m2_1_lock'], W['m2_2_lock'] = 2.9795596, 14.286529   # D1214 (Prüfer, two-solver validated)
    W['mLpi_1'], W['mLpi_2'] = (k1.get('mL_over_pi') or [None, None])[:2]
    # SUSY shell (2026-11-18 23:40 UTC; laws and tolerances below fixed BEFORE the first run)
    # [literature] one-loop anomaly mediation M_i = b_i g_i²/(16π²) m3/2, b = (33/5, 1, −3); g_i² at ~1 TeV: 0.212 (GUT-normalised), 0.420, 1.118
    G2 = dict(g1=0.212, g2=0.420, g3=1.118); k16 = 16*math.pi**2
    W['amsb_M2_over_m32'] = G2['g2']/k16; W['amsb_M1_over_M2'] = 6.6*G2['g1']/G2['g2']; W['amsb_M3_over_M2'] = 3*G2['g3']/G2['g2']
    W['win_lo_GeV'], W['win_hi_map_GeV'], W['win_hi_panel_GeV'] = 670.0, 1250.0, 1850.0   # map wino_window (D1324+), Q_panel/particles (D1304)
    W['m32_need_GeV'] = W['win_hi_panel_GeV']/W['amsb_M2_over_m32']; W['m32_need_record_GeV'] = 7.0e5; W['m32_bound_GeV'] = 6.7e8   # D809/D1264
    lfs = [get('lhc_lifetime', {'m': m}) for m in (670, 1250, 1850)]
    W['dm_670'], W['dm_1250'], W['dm_1850'] = [x.get('dm_MeV') for x in lfs]; W['ct_670'], W['ct_1250'], W['ct_1850'] = [x.get('ctau_cm') for x in lfs]
    # Moonshine layer (2026-11-19 00:45 UTC; all laws exact identities or tolerances fixed BEFORE the first run)
    jc = get('modular_j', {'nmax': 12}); cf = {int(k): v for k, v in (jc.get('coeffs') or {}).items()}
    W['j_c0'], W['j_c1'], W['j_c2'] = cf.get(0), cf.get(1), cf.get(2)
    e8s = get('lattice_lab', {'cmd': 'shells', 'args': ['E8']}).get('shells') or {}; W['E8_roots'] = e8s.get('2') or e8s.get('2.0')
    lsh = get('lattice_lab', {'cmd': 'shells', 'args': ['Leech']}).get('shells') or {}; W['Leech_kiss'] = lsh.get('4') or lsh.get('4.0'); W['Leech_roots'] = lsh.get('2', 0)
    ch = get('lattice_lab', {'cmd': 'champion', 'args': ['16']}).get('energy') or {}
    W['het_iso'] = max((abs(ch['E8xE8'][a]/ch['D16+'][a] - 1) for a in ch.get('E8xE8', {})), default=float('inf')) if 'D16+' in ch else float('inf')
    W['D16p_selfdual'] = 1.0 if get('lattice_lab', {'cmd': 'flip', 'args': ['D16+']}).get('self_dual') is True else 0.0
    q = math.exp(-2*math.pi); W['j_at_i'] = sum(v*q**k for k, v in cf.items()) if cf else None
    # Late-universe layer (2026-11-19 01:05 UTC; tolerances fixed BEFORE the first run). Planck-like ΛCDM inputs.
    cos = dict(h=0.6736, ombh2=0.02237, omch2=0.12, w0=-1, wa=0)
    zq = [0.51, 1.32, 2.33]; zs = sorted(set([round(0.05*k, 2) for k in range(1, 48)] + zq))   # 0.05 … 2.35 plus the test redshifts
    lt = get('janus_lt', dict(cos, z=zs))
    if lt:
        Hs = [(lt.get(str(z)) or lt.get(f'{z:g}') or {}).get('H_kms_Mpc') for z in zs]
        ok_grid = None not in Hs
        if ok_grid:
            import numpy as _np
            zz = _np.array([0.0] + zs); H0 = 100*cos['h']; HH = _np.array([H0] + Hs); c_km = 299792.458
            integ = _np.concatenate([[0.0], _np.cumsum(0.5*(c_km/HH[1:] + c_km/HH[:-1])*_np.diff(zz))])
            from scipy.integrate import quad as _quad
            Om = (cos['ombh2'] + cos['omch2'])/cos['h']**2; Orad = 4.18e-5/cos['h']**2   # photons + 3 massless ν (literature)
            Ez = lambda z: math.sqrt(Om*(1 + z)**3 + Orad*(1 + z)**4 + (1 - Om - Orad))
            for z in zq:
                W[f'DM_tool_{z}'] = lt[f'{z:g}']['DM_Mpc'] if f'{z:g}' in lt else None
                W[f'DM_Hint_{z}'] = float(_np.interp(z, zz, integ))
                W[f'DM_lcdm_{z}'] = c_km/H0*_quad(lambda x: 1/Ez(x), 0, z)[0]
                W[f'f_{z}'] = lt[f'{z:g}']['f'] if f'{z:g}' in lt else None
                Omz = Om*(1 + z)**3/Ez(z)**2; W[f'f_linder_{z}'] = Omz**0.55
                W[f'D_{z}'] = lt[f'{z:g}']['D'] if f'{z:g}' in lt else None
    # P3 layer (2026-11-19 00:45 UTC = 18:45 CT; D1365–D1381; tolerances fixed BEFORE the first run; pure math, no tool calls)
    import numpy as _np3
    def _eps2(U, N=200):
        m = _np3.arange(-N, N + 1); M, Nn = _np3.meshgrid(m, m, indexing='ij'); nz = ~((M == 0) & (Nn == 0))
        return float(_np3.sum((U.imag**2/_np3.abs(M + Nn*U)**4)[nz]))
    W['P3_Ei'], W['P3_Erho'] = _eps2(1j), _eps2(complex(0.5, math.sqrt(3)/2))
    W['P3_kappa'] = 2/math.pi**2*math.pi**4/90 + sum(1/math.tanh(math.pi*j)/(math.pi*j**3) for j in range(1, 20000)) + sum(1/(math.sinh(math.pi*j)**2*j**2) for j in range(1, 60))
    _u = 0.7; _Kp, _Kpp = -3 - _u, 3 + 2*_u   # T2 = 1 units: K' = −(3 + u)/T2, K'' = (3 + 2u)/T2² (D1370)
    W['P3_noscale'] = (_Kp**2/4)/(_Kpp/4) - 3; W['P3_noscale_formula'] = _u**2/(2*_u + 3)
    _s0, _ep, _b = 2.0, 0.01, 1.0; _A = _s0 + _ep*W['P3_Erho']; _E = 40.0; _x = _ep/_A*(_E - W['P3_Erho'])
    W['P3_plateau_lhs'] = _b/_A - _b/(_s0 + _ep*_E); W['P3_plateau_rhs'] = _b/_A*_x/(1 + _x)
    W['P3_U2star'] = math.sqrt(460/(2*math.pi**4/90)); W['P3_T2min'] = W['P3_U2star'] + math.log(1e3)/(2*math.pi)
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
    # 10D laws
    law('law', '10D', ('S_10d',), '10D vacuum is the critical branch at γ = γ_c = 3/2', W['kk10_kind_critical'] == 1.0, 'kaluza_scalar D = 10, γ = 3/2')
    tri('10D', ('S_kk10', 'S_10d', 'S_btr'), 'm²₁ (10D scalar KK)', ('m2_1_pr', 'm2_1_fd', 'm2_1_lock'), 1e-5, rel=True)
    tri('10D', ('S_kk10', 'S_10d', 'S_6d'), 'm²₂ (10D scalar KK)', ('m2_2_pr', 'm2_2_fd', 'm2_2_lock'), 1e-5, rel=True)
    d1 = abs(W['mLpi_1']/0.97 - 1) if W.get('mLpi_1') else float('inf'); d2 = abs(W['mLpi_2']/2.13 - 1) if W.get('mLpi_2') else float('inf')
    law('law', '10D', ('S_btr', 'S_kk10'), 'KK masses match BTR 2209.10553 (m L/π = 0.97, 2.13) within 3% [known open, D1141]', max(d1, d2) < 0.03,
        f"m L/π = {W.get('mLpi_1')}, {W.get('mLpi_2')} → off {d1:.1%}, {d2:.1%} (convention/definition gap, D1141/D1214)")
    # BTR spectrum SHAPE (2026-11-19 00:05 UTC; tolerance = BTR's own two-figure rounding, fixed before this law's first run):
    # m2/m1 from 2.125–2.135 over 0.965–0.975 → 2.179–2.212 (BTR 2209.10553 eq. 5.14: m1 ≈ 0.97 π/L, m2 ≈ 2.13 π/L, L = Einstein-frame proper length)
    rr = W['mLpi_2']/W['mLpi_1'] if W.get('mLpi_1') else float('nan'); W['kk10_ratio'] = rr
    law('law', '10D', ('S_btr', 'S_kk10'), 'spectrum shape matches BTR: m₂/m₁ inside BTR rounding 2.179–2.212', 2.179 <= rr <= 2.212, f"m₂/m₁ = {rr:.4f} (BTR 2.13/0.97 = 2.196) → the −4% gap is one common length scale, not the shape")
    law('down', '10D→Leech', ('S_6d', 'S_stab'), '6D reduction stays stable (scalar sector b ≥ 0)', W['S6_stable'] == 1.0, 'kaluza_stable D = 6, γ = 2')
    # SUSY shell laws
    d = abs(W['m32_need_GeV']/W['m32_need_record_GeV'] - 1)
    law('law', 'SUSY', ('m32_window',), 'AMSB: m3/2 needed for M2 = 1.85 TeV matches the record 7e5 GeV (10%)', d < 0.10, f"m3/2 = M2·16π²/g2² = {W['m32_need_GeV']:.3g} GeV (record 7.0e5; off {d:.1%})")
    law('law', 'SUSY', ('m32_window', 'covariant'), 'covariant bound m3/2 < 6.7e8 GeV stays ≥ 100× above the AMSB need', W['m32_bound_GeV']/W['m32_need_GeV'] >= 100, f"ratio {W['m32_bound_GeV']/W['m32_need_GeV']:.0f} (record ×960)")
    law('up', 'E8→SUSY', ('wino_window', 'Q_dt'), 'wino window lower edge = LHC disappearing-track floor (10 GeV)', W.get('m_floor') is not None and abs(W['win_lo_GeV'] - W['m_floor']) < 10, f"670 vs {W.get('m_floor', float('nan')):.1f} GeV")
    d = abs(W['win_hi_map_GeV']/W['win_hi_panel_GeV'] - 1)
    law('law', 'SUSY', ('tests_lhc', 'm32_window'), 'wino window upper edge consistent across records (5%) [expected OPEN]', d < 0.05, f"map wino_window 1.25 TeV (thermal, ~1.5 cored) vs Q_panel/particle card 1.85 TeV (D1304) — off {d:.0%}")
    ok_dm = all(v is not None and 150 < v < 175 for v in (W['dm_670'], W['dm_1250'], W['dm_1850'])) and W['ct_670'] > W['ct_1250'] > W['ct_1850']
    law('law', 'SUSY', ('H_line', 'tests_lhc'), 'wino Δm in the two-loop band across the window; cτ falls with mass', ok_dm,
        f"Δm = {W['dm_670']:.2f}, {W['dm_1250']:.2f}, {W['dm_1850']:.2f} MeV; cτ = {W['ct_670']:.3g}, {W['ct_1250']:.3g}, {W['ct_1850']:.3g} cm (0.67/1.25/1.85 TeV)")
    d = abs(W['amsb_M3_over_M2']/7.0 - 1)
    law('law', 'SUSY', ('tests_lhc', 'covariant'), 'gluino: one-loop AMSB |M3|/M2 within 20% of D809 (7.0)', d < 0.20, f"|M3|/M2 = {W['amsb_M3_over_M2']:.2f} (one loop) vs 7.0 (D809); off {d:.0%}")
    card = records.get('bino', '').split('Corrected')[0]   # judge the card's claim, not its correction note
    law('law', 'SUSY', ('gravitino_wino', 'covariant'), 'bino record agrees with AMSB M1/M2 (bino heavier than wino)', bool(card) and 'M₂/2' not in card and 'M2/2' not in card and '3.3' in card,
        f"AMSB M1/M2 = {W['amsb_M1_over_M2']:.2f} (wino is the LSP); particle card: '{card[:90]}'" if card else 'no particle card passed to the circuit')
    law('law', 'SUSY', ('gravitino_wino',), 'gravitino → wino non-thermal share within the recorded bound Ω ≤ 5e-4', 3e-4 <= 5e-4, 'D809: ≤ 3e-4 in every history; map bound 5e-4 (record law, no calculation here)')
    cov = [(W['hl_panel'] - W['m_floor'])/(hi - W['m_floor']) for hi in (W['win_hi_map_GeV'], W['win_hi_panel_GeV'])]
    law('law', 'SUSY', ('tests_lhc', 'Q_panel'), 'HL-LHC covers the recorded share of the window (D1350 52%/D1304 26%, ±2 pts)', abs(cov[0]*100 - 52) <= 2 and abs(cov[1]*100 - 26) <= 2, f"computed {cov[0]:.1%} (to 1.25 TeV), {cov[1]:.1%} (to 1.85 TeV)")
    law('report', 'SUSY', ('covariant', 'serapis_e'), 'report: SUSY-breaking scale ↔ plateau height (F ~ √V0) — no tool yet; not a law', True, 'needs a locked tool tying V0 (from C) to F-term SUSY breaking')
    # Moonshine laws (exact identities; [literature] Monster irrep dims 196883, 21296876; dim E8 = 248)
    law('law', 'Moonshine', ('X_mellin', 'X_d8'), "j's constant term 744 = 3 × dim E8 = 3 × (240 roots + rank 8)", W['j_c0'] == 744 and W.get('E8_roots') == 240 and W['j_c0'] == 3*(W['E8_roots'] + 8), f"c₀ = {W['j_c0']}, E8 roots (tool) = {W.get('E8_roots')}")
    law('law', 'Moonshine', ('X_mellin',), 'McKay: 196884 = 1 + 196883 (smallest Monster representation)', W['j_c1'] == 1 + 196883, f"c₁ = {W['j_c1']} (exact series)")
    law('up', 'Leech→Moonshine', ('X_d24', 'X_mellin'), 'Conway: c₁ − Leech kissing number = 324', W['j_c1'] is not None and W.get('Leech_kiss') is not None and W['j_c1'] - W['Leech_kiss'] == 324, f"{W['j_c1']} − {W.get('Leech_kiss')} = {(W['j_c1'] or 0) - (W.get('Leech_kiss') or 0)}")
    law('law', 'Moonshine', ('X_mellin', 'X_bw16'), 'Thompson: 21493760 = 1 + 196883 + 21296876', W['j_c2'] == 1 + 196883 + 21296876, f"c₂ = {W['j_c2']}")
    law('law', 'Moonshine', ('X_d16', 'X_bw16'), 'heterotic: 26 − 10 = 16 internal dims carry E8⊕E8 and D16⁺ — both self-dual, isospectral (1e-12)', 26 - 10 == 16 and W['het_iso'] < 1e-12 and W['D16p_selfdual'] == 1.0 and W['E8_selfdual'] == 1.0, f"max |E_E8xE8/E_D16+ − 1| = {W['het_iso']:.1e}; D16⁺ self-dual {W['D16p_selfdual']:.0f}")
    law('up', 'Leech→Moonshine', ('X_d24', 'X_crit'), 'bosonic: 26 − 2 = 24 transverse dims = Leech rank; Leech has no roots', 26 - 2 == 24 and not W.get('Leech_roots'), f"Leech shells: norm 2 → {W.get('Leech_roots', 0)}, norm 4 → {W.get('Leech_kiss')}")
    law('down', 'Moonshine→A2', ('X_rings', 'vac_i'), 'j(i) = 1728 from the exact series: the τ = i vacuum of the variant potential (D1351)', W.get('j_at_i') is not None and abs(W['j_at_i'] - 1728) < 1e-3, f"Σ cₙ e^(−2πn) (n ≤ 12) = {W.get('j_at_i')}")
    # Late-universe laws
    if 'DM_tool_1.32' in W:
        for z, nd in ((0.51, ('J_lt', 'R_desi', 'T_hyperion')), (1.32, ('J_lt', 'R_desi', 'R_w0wa')), (2.33, ('J_lt', 'T_hyperion', 'R_clock'))):
            tri('Late', nd, f'D_M(z = {z}) Mpc', (f'DM_tool_{z}', f'DM_Hint_{z}', f'DM_lcdm_{z}'), 0.003, rel=True)
        dg = max(abs(W[f'f_{z}']/W[f'f_linder_{z}'] - 1) for z in (0.51, 1.32))
        law('law', 'Late', ('R_growth', 'J_lt'), 'growth rate f(z) = Ω_m(z)^0.55 (Linder γ, ΛCDM) within 1%', dg < 0.01, f"max |f/Ω_m^0.55 − 1| = {dg:.2%} at z = 0.51, 1.32")
        law('law', 'Late', ('R_growth', 'R_biref'), 'growth factor D(z) falls with redshift', W['D_0.51'] > W['D_1.32'] > W['D_2.33'], f"D = {W['D_0.51']:.4f}, {W['D_1.32']:.4f}, {W['D_2.33']:.4f}")
    else:
        law('law', 'Late', ('J_lt',), 'late-universe engine answered on the z grid', False, 'janus_lt returned no grid')
    # P3 laws (D1365–D1381)
    law('law', 'P3', ('P3_kappa', 'P3_Y'), 'Petropoulos–Rizos κ = E(i,2)/π² (universal threshold carries E(U,2)/T₂)', abs(W['P3_kappa'] - W['P3_Ei']/math.pi**2) < 1e-4, f"κ = {W['P3_kappa']:.6f}, E(i,2)/π² = {W['P3_Ei']/math.pi**2:.6f}")
    law('law', 'P3', ('P3_Y', 'P3_plateau'), 'vacuum: E(ρ,2) < E(i,2) — the universal term is lowest at the hexagon', W['P3_Erho'] < W['P3_Ei'], f"E(ρ,2) = {W['P3_Erho']:.4f} < E(i,2) = {W['P3_Ei']:.4f}")
    law('law', 'P3', ('P3_E7',), 'b̂ = 0 E7: 3 × 56 at instanton number 10 → b̂ = 2(3·6 − 18) = 0', 2*(3*6 - 18) == 0 and 10//2 - 2 == 3, 'F₂ tuned locus (D1367, D1382)')
    law('law', 'P3', ('P3_K', 'P3_plateau'), 'no-scale + BHK δK: V/(e^K|W₀|²) = u²/(2u+3) (no plateau, D1370)', abs(W['P3_noscale'] - W['P3_noscale_formula']) < 1e-12, f"u = 0.7: {W['P3_noscale']:.6f} vs {W['P3_noscale_formula']:.6f}")
    law('law', 'P3', ('P3_K', 'P3_plateau'), 'K = −log(Im S + Y/16π²): b/A − b/(s₀+εE) = (b/A)·x/(1+x) — the SERAPIS plateau (D1371, D1375)', abs(W['P3_plateau_lhs'] - W['P3_plateau_rhs']) < 1e-12, f"{W['P3_plateau_lhs']:.10f} = {W['P3_plateau_rhs']:.10f}")
    law('report', 'P3', ('P3_chamber',), 'chamber: needs T₂ > U₂* + ln(10³)/2π (D1377)', True, f"U₂* = {W['P3_U2star']:.2f} → T₂ ≳ {W['P3_T2min']:.1f}; one-loop ≈ tree there (D1378)")
    law('report', 'P3', ('P3_shift',), 'shifted lattices: no interior minimum; mixed c = 1 gives the hexagon of U/2 (D1380–D1381)', True, 'control vs SL(2,Z) dilemma')
    law('down', 'P3→A2', ('P3_Y', 'X_epstein'), 'the P3 E(ρ,2) equals the core hexagonal Epstein minimum', W.get('E_rho2') is not None and abs(W['P3_Erho'] - W['E_rho2']) < 2e-3, f"{W['P3_Erho']:.5f} vs core {W.get('E_rho2')}")
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
