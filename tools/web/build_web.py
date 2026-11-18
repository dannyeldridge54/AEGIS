"""AEGIS web: one graph of the twin-ladder strings, the theory map, the Janus fast/exact pairs and the SERAPIS string sector.
Every edge cites the D-note (or source) that backs it. Output: docs/web/web.json (read by the Web artifact and by waves.py).
Curated links are labelled source='curated' (my reading of the D-notes); theory-map dependencies come from theory/map/map.yaml unchanged."""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
m = yaml.safe_load(open(ROOT / 'theory/map/map.yaml', encoding='utf-8'))
N = {}; E = []
def node(i, label, lane, status='computed', refs='', info=''): N[i] = dict(id=i, label=label, lane=lane, status=status, refs=refs, info=info)
def edge(s, t, kind, sign=1, ref='', verdict='', source='curated'): E.append(dict(s=s, t=t, kind=kind, sign=sign, ref=ref, verdict=verdict, source=source))
# --- theory map (unchanged source) ---
for n in m['nodes']:
    node(n['id'], n['title'], 'theory', n['status'], ', '.join((n.get('d') or [])[-3:]), n.get('note', ''))
for n in m['nodes']:
    for d in n.get('depends') or []:
        edge(d, n['id'], 'depends', -1 if N[n['id']]['status'] in ('killed',) else 1, 'theory/map/map.yaml', n['status'], 'map.yaml')
# --- LEFT string: early universe ---
node('L_cmb', 'CMB data: n_s, r, α_s (CMB-SPA n_s 0.9684±0.0030; r < 0.036)', 'left', 'literature', 'twin-ladder F3')
node('L_bridge', 'Twist-era bridges B1 r−3(1−n_s)², B2 α_s+½(1−n_s)² — NOT SERAPIS nulls (); SERAPIS null = Janus relation', 'left', 'corrected', 'twin-ladder B1/B2, ')
node('L_nstar', 'N* (left hand-off)', 'left', 'computed', 'D1148, D1176')
node('L_reheat', 'Reheating / kination duration', 'left', 'computed', 'J7c2 D1008')
for a, b, ref in (('L_cmb', 'janus', 'Janus relation α_s(n_s, r)'), ('L_cmb', 'L_bridge', 'twin-ladder'), ('L_bridge', 'janus', 'B1/B2 null tests'),
                  ('janus', 'band_i', 'map'), ('janus', 'band_e', 'map'), ('L_nstar', 'nstar_i', 'map'), ('L_nstar', 'nstar_e', 'map'),
                  ('L_reheat', 'reheat_i', 'map'), ('L_reheat', 'reheat_rho', 'map'), ('L_reheat', 'L_nstar', 'ΔN* from reheating')):
    edge(a, b, 'string', 1, ref)
edge('band_e', 'L_cmb', 'string', 1, 'band 0.970–0.975 vs CMB-SPA 0.9684±0.0030 (+SPA+DESI 0.9728)', '~1σ from SPA, inside SPA+DESI')
# --- RIGHT string: late universe ---
node('R_desi', 'DESI DR2 BAO + Pantheon+ SN + CMB θ*', 'right', 'literature', 'D1028, D1029')
node('R_w0wa', 'w0–wa: w0 −0.853±0.053, wa −0.518±0.200 (L7)', 'right', 'computed', 'D1029, D1200, D1205, D1213')
node('R_growth', 'Growth fσ8 (DESI DR1): consistent, χ² 3.76/6', 'right', 'computed', 'D1213')
node('R_clock', 'Clocks / α-drift / EP (filter F1)', 'right', 'literature', 'D400')
node('R_biref', 'Birefringence β bridge', 'right', 'estimate', 'D403, D404')
for a, b, ref, v in (('R_desi', 'R_w0wa', 'D1029', 'Δχ²_ΛCDM ≈ 7.7'), ('R_w0wa', 'R_growth', 'D1213', 'consistent'), ('R_w0wa', 'R_clock', 'clock bridge', ''),
                     ('R_w0wa', 'R_biref', 'birefringence bridge', ''), ('R_desi', 'mnu', 'Σm_ν', ''), ('R_growth', 'halo_profile', 'structure', ''),
                     ('wino_window', 'tests_lhc', 'map', '')):
    edge(a, b, 'string', 1, ref, v)
# --- CENTRE: shared quantities ---
node('C_nstar', 'Shared N*: SERAPIS-E 50.1–51.3 (ρ), τ=i 50.40–50.45 (audited)', 'centre', 'corrected', 'D1235, D1247, '); node('C_dm', 'Shared DM mass ∝ dilution D', 'centre', 'estimate', 'twin-ladder')
node('C_lepto', 'Shared leptogenesis yield 0.87e-10 × D', 'centre', 'estimate', 'twin-ladder'); node('C_D', 'Dilution D ≤ 1e3 (F2)', 'centre', 'estimate', 'D394, D406')
for a, b in (('L_nstar', 'C_nstar'), ('C_nstar', 'R_w0wa'), ('C_D', 'C_nstar'), ('C_D', 'C_dm'), ('C_D', 'C_lepto'), ('C_dm', 'wino_window'),
             ('C_lepto', 'lepto_i'), ('C_lepto', 'lepto_rho'), ('C_dm', 'darkrad_rho')):
    edge(a, b, 'centre', 1, 'twin-ladder shared quantity')
# --- JANUS pairs (fast face ↔ exact/independent face) ---
for i, l, st, r in (('J_core', 'Janus single-field (janus-jit)', 'computed', 'D1228'), ('X_ms', 'Exact MS (ms-jit)', 'computed', 'D1225'),
                    ('X_aspic', 'ASPIC (slow-roll library)', 'literature', 'D1004, D1218'), ('J_mf', 'Janus-MF (jit)', 'computed', 'D1221, D1224'),
                    ('X_mmc', 'MultiModeCode (patched)', 'literature', 'D1162, D1174'), ('X_pyt', 'PyTransport 2.0', 'literature', 'D1195, D1207'),
                    ('J_nc', 'Janus-MF curved (nc-jit)', 'computed', 'D1217, D1224'), ('X_pytnc', 'PyTransport NC', 'literature', 'D1217, I25'),
                    ('J_lt', 'Janus-LT (late-time)', 'computed', 'D1029'), ('X_camb', 'CAMB', 'literature', 'D1012, D1019, D1027'),
                    ('X_cobaya', 'Cobaya MCMC', 'literature', 'D1205'), ('X_n3lo', 'N3LO slow roll (Auclair–Ringeval)', 'literature', 'D1219')):
    node(i, l, 'janus', st, r)
for a, b, ref, v, sg in (('J_core', 'X_ms', 'D1218, D1225, D1228', 'Janus |Δn_s| 2.9e-6 vs exact', 1), ('J_core', 'X_aspic', 'D1004, D1218, D1228', 'Janus ~250× more accurate, faster', 1),
                         ('J_core', 'X_n3lo', 'D1219, D1228', 'coefficients agree; ×2.88 < locked ×3', 1),
                         ('J_mf', 'X_mmc', 'D1162, D1166, D1169, D1174', 'match after MMC derivative bugs fixed', 1), ('J_mf', 'X_pyt', 'D1195, D1207', '|Δn_s| ≤ 9.3e-5', 1),
                         ('J_nc', 'X_pytnc', 'D1217, D1224', 'R=1, 1.5, 2 within 4e-5 after the a-normalisation fix', 1), ('J_nc', 'J_mf', 'D1224', 'same fix, flat limit identical', 1),
                         ('J_lt', 'X_camb', 'D1012, D1019, D1027', 'r_d 4.4e-4, H 4.6e-5, σ8 4e-6', 1), ('J_lt', 'X_cobaya', 'D1205', 'MCMC confirms Hessian', 1),
                         ('J_core', 'janus', 'D1002–D1228', 'tool behind the relation', 1), ('J_mf', 'janus', 'JMF series', 'multi-field extension', 1),
                         ('J_lt', 'R_w0wa', 'D1029–D1213', 'produces the late-time fit', 1), ('X_aspic', 'L_cmb', 'standard', 'slow-roll predictions', 1)):
    edge(a, b, 'pair', sg, ref, v)
# --- SERAPIS string sector ---
for i, l, st, r in (('S_btr', 'BTR 2209.10553 (string vacua, KK masses)', 'literature', 'fetched §3, §5'),
                    ('S_10d', '10D critical orientifold vacuum', 'computed', 'D1141'), ('S_6d', '6D subcritical vacuum (5D Mink × interval)', 'computed', 'D1015, D1015a'),
                    ('S_stab', '6D scalar sector stable (b ≥ 0)', 'computed', 'D1140'), ('S_kk10', '10D scalar KK masses: ratio ✓, absolute −4%', 'corrected', 'D1141, D1214, D1216'),
                    ('S_kk6', '6D scalar KK masses (S4e4)', 'open', 'PC job S4E4'), ('S_gs', 'Green–Schwarz tilt route (R1–R6)', 'estimate', 'D1009–D1024')):
    node(i, l, 'strings', st, r)
for a, b, ref, v, sg in (('S_btr', 'S_10d', 'BTR §3.1', '', 1), ('S_10d', 'S_kk10', 'D1141, D1214', 'two solvers agree 1e-7', 1),
                         ('S_btr', 'S_kk10', 'BTR eq. 5.14 vs ours', 'ratio 2.190 vs 2.196 ✓; absolute −4% (unstated constant, D1216)', -1),
                         ('S_6d', 'S_stab', 'D1140', '', 1), ('S_6d', 'S_kk6', 'S4e4', 'pending', 1), ('S_kk10', 'S_kk6', 'same solver', '', 1),
                         ('S_6d', 'serapis_e', 'string home of the plateau', 'open link', 1), ('S_6d', 'plateau_origin', 'D992 routes closed', '', -1),
                         ('S_gs', 'eps_tilt', 'D1009–D1024', 'tilt sign OK; magnitude needs Re S ≈ 3200', -1), ('S_gs', 'covariant', 'D1011', '', 1),
                         ('bhk_tilt', 'S_gs', 'one-loop tilt', '', 1), ('stuck_d3', 'S_6d', 'branes', '', 1)):
    edge(a, b, 'string-sector', sg, ref, v)

# --- CHRONOS (early-universe calculator) and HYPERION (late-universe + astrophysics) toolkits ---
for i, l, st, r in (('T_chronos', 'Chronos Clock (tools/janus_calc)', 'computed', 'docs/TOOL_NAMES.md'),
                    ('T_hyperion', 'Hyperion (tools/janus_lt + janus_astro)', 'computed', 'D1052–D1078; releases/hyperion-1.0'),
                    ('H_relic', 'Wino relic + Sommerfeld: 2.325 TeV vs Beneke 2.207 (+5.4%); g_*(T) suspect', 'corrected', 'D1158–D1187'),
                    ('H_line', 'γγ line vs H.E.S.S. IGS: window 0.67 to ~1–1.5 TeV', 'computed', 'D1110–D1190'),
                    ('H_bbn', 'BBN: 3 codes agree; Y_p LBT 2026; SU(2)+gaugino excluded 3.1σ', 'computed', 'D1082–D1192'),
                    ('H_mw', 'Milky Way: McMillan17 passes v_c☉, MWPotential2014 fails', 'computed', 'D1193–D1197'),
                    ('H_ns', 'Neutron stars + GW tides (6.5PN validated; 7PN open)', 'computed', 'D1090–D1115')):
    node(i, l, 'janus', st, r)
for a, b, ref, v, sg in (('T_chronos', 'J_core', 'TOOL_NAMES', 'Chronos runs Janus', 1), ('T_chronos', 'J_mf', 'TOOL_NAMES', '', 1), ('T_chronos', 'T_hyperion', 'W1 wiring D1079', 'Chronos ⇄ Hyperion', 1),
                         ('T_hyperion', 'J_lt', 'TOOL_NAMES', 'Hyperion late-time core', 1), ('T_hyperion', 'H_relic', 'D1158–D1187', '', 1), ('T_hyperion', 'H_line', 'D1110–D1190', '', 1),
                         ('T_hyperion', 'H_bbn', 'D1082–D1192', '', 1), ('T_hyperion', 'H_mw', 'D1193', '', 1), ('T_hyperion', 'H_ns', 'D1090', '', 1),
                         ('H_relic', 'wino_window', 'D784, D1153', 'thermal fraction f', 1), ('H_line', 'wino_window', 'D1125–D1190', 'line limit trims the window', -1),
                         ('H_mw', 'H_line', 'halo J-factor', 'halo choice moves the line verdict', 1), ('H_mw', 'halo_profile', 'D1189', 'cored Gaia haloes', 1),
                         ('H_bbn', 'darkrad_rho', 'D1088–D1192', 'N_eff / Y_p bound hidden sector', -1), ('H_bbn', 'C_D', 'B2 Chronos→BBN D1085', '', 1),
                         ('X_beneke', 'H_relic', 'Beneke 2009.00640', '+5.4% (no boost), +8.6% (LO Sommerfeld)', -1), ('X_hess', 'H_line', 'H.E.S.S. IGS 2026', '', 1)):
    edge(a, b, 'pair', sg, ref, v)
node('X_beneke', 'Beneke et al. relic (2009.00640)', 'janus', 'literature', 'D1185'); node('X_hess', 'H.E.S.S. Inner Galaxy Survey line limit', 'janus', 'literature', 'D1125')
edge('logderiv_plateau', 'plateau_origin', 'depends', -1, 'D822', 'killed candidate')
out = dict(nodes=list(N.values()), edges=E, lanes=['left', 'centre', 'right', 'theory', 'janus', 'strings'])
bad = [e for e in E if e['s'] not in N or e['t'] not in N]
assert not bad, bad
(ROOT / 'docs/web').mkdir(parents=True, exist_ok=True); json.dump(out, open(ROOT / 'docs/web/web.json', 'w'), indent=1, ensure_ascii=False)
print(len(N), 'nodes', len(E), 'edges')
