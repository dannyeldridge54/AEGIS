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
node('L_bridge', 'Twist-era bridges B1 r−3(1−n_s)², B2 α_s+½(1−n_s)² — NOT SERAPIS nulls (D1252); SERAPIS null = Janus relation', 'left', 'corrected', 'twin-ladder B1/B2, D1252')
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
node('C_nstar', 'Shared N*: SERAPIS-E 50.07–51.22 (ρ, MSSM g*), τ=i 50.40–50.45 (audited)', 'centre', 'corrected', 'D1235, D1247, D1252, D1262'); node('C_dm', 'Shared DM mass ∝ dilution D', 'centre', 'estimate', 'twin-ladder')
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
# --- WIRING: one shared toolkit registry feeds the Janus app and CubeMind; every result flows into CubeMind's memory (Danny 18 Nov 2026: "wire them together") ---
for i, l, st, r in (('W_registry', 'Shared toolkit registry (aegis_tools): 12 tools incl. serapis_point / serapis_ms', 'computed', 'cubemind a1351d8'),
                    ('W_app', 'Janus app + link (live scans, tool calls, waves)', 'computed', 'apps/aegis_studio'),
                    ('W_claude', 'Claude loops (Djl / Jl): locks, D-notes, audits', 'computed', 'D1233–D1252'),
                    ('CM_mem', 'CubeMind memory (MindMem): D-notes + every Janus result as EVIDENCE', 'computed', 'mindmem ingest'),
                    ('CM_eval', 'CubeMind evals: P7 (+aegis WIN vs plain), P8 physics track', 'computed', 'PREREG_PHASE7/8')):
    node(i, l, 'wiring', st, r)
for a, b, ref, v, sg in (('J_core', 'W_registry', 'serapis_point, serapis_spectra, janus_single', 'registered', 1), ('X_ms', 'W_registry', 'serapis_ms', 'registered', 1),
                         ('J_mf', 'W_registry', 'janus_mf', 'registered', 1), ('J_lt', 'W_registry', 'janus_lt', 'registered', 1),
                         ('S_10d', 'W_registry', 'kaluza_tensor / kaluza_stable', 'registered', 1), ('janus', 'W_registry', 'janus_relation', 'registered', 1),
                         ('nstar_e', 'W_registry', 'nstar_match', 'registered', 1), ('serapis_e', 'W_registry', 'serapis potential (pipeline)', 'registered', 1),
                         ('W_registry', 'W_app', 'link cmd tool{name,args}', 'Janus app runs any toolkit', 1), ('W_registry', 'CM_eval', '+aegis arm (P7), physics track (P8)', 'CubeMind calls the same tools', 1),
                         ('W_app', 'CM_mem', 'to_cubemind()', 'every scan / tool result → EVIDENCE record', 1), ('W_claude', 'W_app', 'janus_link inbox / feed', 'Claude drives the app live', 1),
                         ('W_claude', 'CM_mem', 'DERIVATION_LOG ingest', 'every D-note → memory', 1), ('CM_mem', 'CM_eval', 'retrieval', 'memory informs answers', 1),
                         ('CM_eval', 'W_claude', 'RESULTS.md', 'scores feed the next lock', 1), ('W_app', 'band_e', 'live scans PW1/PW2', 'the app computed the audited box and the point', 1),
                         ('W_claude', 'serapis_e', 'NA1–NA16 audit', 'audited every node', 1)):
    edge(a, b, 'wire', sg, ref, v)
node('X_beneke', 'Beneke et al. relic (2009.00640)', 'janus', 'literature', 'D1185'); node('X_hess', 'H.E.S.S. Inner Galaxy Survey line limit', 'janus', 'literature', 'D1125')
edge('logderiv_plateau', 'plateau_origin', 'depends', -1, 'D822', 'killed candidate')
# ---- LATTICE lane (Danny 2026-11-18: "keep mapping out all the other parts of the lattices") ----
# Every flat torus is a lattice; champions by dimension and how they hand over with scale (Poisson duality).
for i, l, st, r in (
    ('X_rule', 'Flip rule: a champion lattice hands over with scale iff it is not self-dual; swap exactly at the self-dual scale α=1 (Poisson)', 'computed', 'D1277, D1278, D1282, D1286'),
    ('X_d2', 'd=2 hexagonal A2 (τ=ρ): wins at every scale; square τ=i is a saddle', 'computed', 'D1276, D1277, D1279'),
    ('X_d3', 'd=3 FCC (α>1) / BCC (α<1): swap at α=1, tie 0.231536', 'computed', 'D1277'),
    ('X_d4', 'd=4 D4: self-dual, wins at every scale', 'computed', 'D1278'),
    ('X_d5', 'd=5 D5 / D5*: swap at α=1, tie 0.348752', 'computed', 'D1278'),
    ('X_d6', 'd=6 E6 / E6*: beat Z, D, D*, A, A* at every scale; swap at α=1', 'computed', 'D1282, D1286'),
    ('X_d7', 'd=7 E7 / E7*: beat Z, D, D*, A, A* at every scale; swap at α=1', 'computed', 'D1282, D1286'),
    ('X_d8', 'd=8 E8: unimodular, never flips; universally optimal (CKMRV 2022)', 'computed', 'D1278, D1282'),
    ('X_d16', 'd=16 heterotic tie: E8⊕E8 and D16⁺ — different shapes, identical shells 1,480,61920,1050240 and energy at every scale (Milnor isospectral)', 'computed', 'D1288'),
    ('X_bw16', 'd=16 champion: Barnes–Wall BW16 — kissing 4320, similar to its dual (never flips), beats E8⊕E8 = D16⁺ at every scale, 100,800 hexagons inside', 'computed', 'D1298'),
    ('X_d24', 'd=24 Leech: built from scratch — no roots, 196560 norm-4 vectors, self-dual (never flips), beats E8³ at every scale', 'computed', 'D1289'),
    ('X_mod', 'Upward link: self-dual champions are Eisenstein modular forms — θ_E8 = E4, θ_E8⊕E8 = E4², θ_Leech = E4³−720Δ; flip rule = modularity', 'computed', 'D1291'),
    ('X_mellin', 'E(τ,s) = Mellin transform of the Gaussian lattice energy: SERAPIS-E’s E(τ,2) is the all-scale integral; hex wins every scale ⇒ every s', 'computed', 'D1291'),
    ('X_crit', 'd=2: only two stationary shapes at every scale — τ=i saddle, τ=ρ minimum (no hidden third)', 'computed', 'D1292'),
    ('X_tool', 'Lattice Lab tool (tools/lattice/lattice_lab.py; registry lattice_lab): shells, energy, flip, champion, modular, epstein, critical', 'computed', 'D1292'),
    ('X_epstein', 'Epstein (SERAPIS-type) energy: dual handover at exponent s=d/4 — the Mellin image of the self-dual scale α=1', 'computed', 'D1293'),
    ('X_hexin', 'The SERAPIS-E hexagon is the tile inside every champion: 16 in D4, 120 in E6, 336 in E7, 1120 in E8, 75,348,000 in Leech', 'computed', 'D1294'),
    ('X_rings', 'τ=i = Gaussian integers Z[i] (4 units, 8 symmetries), τ=ρ = Eisenstein integers Z[ω] (6 units, 12 symmetries): extra rotations force every shape-energy to be stationary there', 'computed', 'D1295'),
    ('X_sqin', 'The saddle square (τ=i) also sits inside every champion: 18 (D4), 270 (E6), 945 (E7), 3780 (E8), 2,288,695,500 (Leech); square/hex ratio rises with d', 'computed', 'D1296'),
    ('X_flow3', 'd=3 flow: any 3-torus flows to FCC (rhombic dodecahedron cells) at large scale, BCC (truncated octahedra) at small scale; the cube never', 'computed', 'D1297'),
    ('X_nest', 'Nesting chain A2 ⊂ D4 ⊂ E8 ⊂ Leech (sections of the next champion)', 'literature', 'D1276'),
    ('X_moduli', 'Torus shape moduli d(d+1)/2−1: circle 0, 2, 5, 9, 14 … 35 (d=8), 299 (d=24)', 'computed', 'D1279'),
    ('X_narain', 'String lattices (Narain) are even self-dual; T-duality = the Poisson map → never flip', 'literature', 'D1283, arXiv:2206.14825'),
    ('X_su3', 'c=2 max-gap Narain point SU(3): hexagonal shape (matches SERAPIS-E vacuum), string-scale size (does not)', 'literature', 'D1283'),
    ('X_trap', 'Moduli trapping at enhanced-symmetry points selects shape+size together, not shape alone', 'literature', 'D1285, hep-th/0403001')):
    node(i, l, 'lattice', st, r)
for a, b, ref, v, sg in (
    ('X_d2', 'X_d3', 'dimension chain', '', 1), ('X_d3', 'X_d4', 'dimension chain', '', 1), ('X_d4', 'X_d5', 'dimension chain', '', 1),
    ('X_d5', 'X_d6', 'dimension chain', '', 1), ('X_d6', 'X_d7', 'dimension chain', '', 1), ('X_d7', 'X_d8', 'dimension chain', '', 1),
    ('X_d8', 'X_d16', 'E8 ⊕ E8', '', 1), ('X_d16', 'X_d24', 'dimension chain', '', 1), ('X_rule', 'X_d16', 'D1288', 'no flip; two champions tie', 1), ('X_d16', 'X_narain', 'D1288', 'heterotic gauge lattices', 1),
    ('X_rule', 'X_d3', 'D1277', 'flips (not self-dual)', 1), ('X_rule', 'X_d5', 'D1278', 'flips', 1), ('X_rule', 'X_d6', 'D1282', 'flips (predicted first)', 1),
    ('X_rule', 'X_d7', 'D1282', 'flips (predicted first)', 1), ('X_rule', 'X_d2', 'D1277', 'no flip (self-dual)', 1), ('X_rule', 'X_d4', 'D1278', 'no flip', 1),
    ('X_rule', 'X_d8', 'D1282', 'no flip', 1), ('X_rule', 'X_d24', 'D1278, D1289', 'no flip (confirmed)', 1),
    ('X_d2', 'X_nest', 'A2', '', 1), ('X_d4', 'X_nest', 'D4', '', 1), ('X_d8', 'X_nest', 'E8', '', 1), ('X_d24', 'X_nest', 'Leech', '', 1),
    ('X_rule', 'X_mod', 'D1291', 'no flip ⇔ modular form', 1), ('X_d8', 'X_mod', 'D1291', 'θ = E4', 1), ('X_d16', 'X_mod', 'D1291', 'θ = E4² (forced tie)', 1),
    ('X_d24', 'X_mod', 'D1291', 'θ = E4³ − 720Δ', 1), ('X_mod', 'X_mellin', 'D1291', 'same Eisenstein family', 1), ('X_mellin', 'serapis_e', 'D1291', 'E(τ,2) = scale-integral of lattice energy', 1),
    ('X_d2', 'X_mellin', 'D1276, D1277, D1291', 'hex wins every scale ⇒ every s', 1),
    ('X_crit', 'X_d2', 'D1292', 'complete list', 1), ('X_crit', 'vac_i', 'D1292', 'saddle', -1), ('X_crit', 'vac_rho', 'D1292', 'minimum', 1),
    ('X_tool', 'X_rule', 'D1292', 'computes every lattice result', 1), ('X_tool', 'W_registry', 'registry', 'lattice_lab', 1),
    ('X_rule', 'X_epstein', 'D1293', 'α ↔ 1/α becomes s ↔ d/2−s', 1), ('X_mellin', 'X_epstein', 'D1293', 'functional equation', 1), ('X_epstein', 'serapis_e', 'D1293', 'd=2, s=2: no handover', 1),
    ('X_d2', 'X_hexin', 'D1294', 'τ=ρ tile', 1), ('X_hexin', 'X_d4', 'D1294', '16', 1), ('X_hexin', 'X_d6', 'D1294', '120', 1), ('X_hexin', 'X_d7', 'D1294', '336', 1),
    ('X_hexin', 'X_d8', 'D1294', '1120', 1), ('X_hexin', 'X_d24', 'D1294', '75,348,000', 1), ('X_hexin', 'X_nest', 'D1294', 'exact counts', 1), ('X_hexin', 'vac_rho', 'D1294', 'same shape', 1),
    ('X_rings', 'X_crit', 'D1295', 'symmetry ⇒ stationary', 1), ('X_rings', 'vac_i', 'D1295', 'Z[i]', 1), ('X_rings', 'vac_rho', 'D1295', 'Z[ω]', 1),
    ('X_sqin', 'X_hexin', 'D1296', 'saddle vs minimum multiplicity', 1), ('X_sqin', 'vac_i', 'D1296', 'same shape', 1), ('X_sqin', 'X_d8', 'D1296', '3780', 1), ('X_sqin', 'X_d24', 'D1296', '2.29e9', 1),
    ('X_flow3', 'X_d3', 'D1297', 'destination switches at α=1', 1), ('X_moduli', 'X_flow3', 'D1279, D1297', '5 shape moduli', 1), ('X_rule', 'X_flow3', 'D1297', 'flip rule seen as a flow', 1),
    ('X_d8', 'X_bw16', 'dimension chain', '', 1), ('X_bw16', 'X_d16', 'D1298', 'beats the heterotic pair', 1), ('X_bw16', 'X_d24', 'dimension chain', '', 1), ('X_rule', 'X_bw16', 'D1298', 'similar-to-dual ⇒ no flip', 1), ('X_hexin', 'X_bw16', 'D1298', '100,800', 1),
    ('X_moduli', 'X_d2', 'D1279', 'first dimension with a shape choice', 1),
    ('X_rule', 'X_narain', 'D1283', 'T-duality = Poisson', 1), ('X_narain', 'X_su3', 'arXiv:2206.14825', '', 1),
    ('X_su3', 'X_d2', 'D1283', 'same hexagonal shape', 1), ('X_trap', 'X_su3', 'D1285', 'selects shape+size', 1),
    ('X_d2', 'vac_rho', 'D1280, D1287', 'SERAPIS-E vacuum = hexagonal (V monotone in E(τ,2))', 1),
    ('X_d2', 'vac_i', 'D1280, D1287', 'square τ=i is a saddle', -1),
    ('X_su3', 'serapis_e', 'D1283', 'shape matches, size does not', -1)):
    edge(a, b, 'lattice', sg, ref, v)
# ---- LHC lane (Janus-LHC, 2026-11-18: "do everything they're doing, but better") ----
for i, l, st, r in (
    ('Q_xsec', 'Wino cross sections: ln–ln spline of Resummino tables (LOO max 0.3%) + Drell–Yan scaling route (no PDF file), universal κ ≈ −0.163', 'computed', 'D1299; Zenodo 24342227'),
    ('Q_resummino', 'Resummino aNNLO+NNLL tables, 13 & 13.6 TeV (their standard)', 'literature', 'arXiv:2304.11915'),
    ('Q_life', 'Wino lifetime engine: δm(m) two-loop, cτ(1 TeV) = 5.83 cm, BR(π) 97.9%', 'computed', 'D1300'),
    ('Q_stats', 'CLs limits: pyhf + exact Poisson (asymptotics off ≤8% at low counts)', 'computed', 'docs/LHC_TOOLKIT.md'),
    ('Q_dt', 'Disappearing-track recast: wino excluded < 666.6 GeV (ATLAS 660); HL-LHC ≈ 975 GeV', 'computed', 'D1301'),
    ('Q_atlas', 'ATLAS disappearing-track search, 136 fb⁻¹', 'literature', 'arXiv:2201.02472'),
    ('Q_dt36', 'Second validation: ATLAS 36.1 fb⁻¹ reproduced, 447.8 vs 460 GeV, same method, no retuning', 'computed', 'D1303'),
    ('Q_panel', 'Model vs collider: SERAPIS wino window 0.67–1.85 TeV starts at the LHC limit; HL-LHC tests 26%', 'computed', 'D1304'),
    ('Q_pdf', 'Own LO cross section with a PDF set (blocked: CERN file needs one click at home)', 'open', 'docs/LHC_TOOLKIT.md')):
    node(i, l, 'lhc', st, r)
for a, b, ref, v, sg in (
    ('Q_resummino', 'Q_xsec', 'D1299', 'reproduced to 0.3%', 1), ('Q_xsec', 'Q_dt', 'D1301', 'signal yield', 1), ('Q_life', 'Q_dt', 'D1301', 'decay window', 1),
    ('Q_stats', 'Q_dt', 'D1301', 'N95', 1), ('Q_atlas', 'Q_dt', 'D1301', 'limit reproduced (1%)', 1), ('Q_pdf', 'Q_xsec', 'next', 'independent check', 1),
    ('Q_dt36', 'Q_dt', 'D1303', 'method validated twice', 1), ('Q_dt', 'Q_panel', 'D1304', 'reach', 1), ('Q_panel', 'wino_window', 'D1304', 'read-only overlay', 1), ('Q_panel', 'tests_lhc', 'D1304', 'HL-LHC 26% of window', 1),
    ('Q_dt', 'tests_lhc', 'D1301', 'HL-LHC reach ≈ 975 GeV', 1), ('Q_xsec', 'W_registry', 'registry', 'lhc_xsec', 1), ('Q_dt', 'W_registry', 'registry', 'lhc_dt_limit', 1)):
    edge(a, b, 'lhc', sg, ref, v)
out = dict(nodes=list(N.values()), edges=E, lanes=['left', 'centre', 'right', 'theory', 'janus', 'strings', 'wiring', 'lattice', 'lhc'])
bad = [e for e in E if e['s'] not in N or e['t'] not in N]
assert not bad, bad
(ROOT / 'docs/web').mkdir(parents=True, exist_ok=True); json.dump(out, open(ROOT / 'docs/web/web.json', 'w'), indent=1, ensure_ascii=False)
print(len(N), 'nodes', len(E), 'edges')
