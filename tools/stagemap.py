"""STAGE MAP (STAGEMAP_GOALPOSTS): every stage marked in one run. python3 tools/stagemap.py [tag]"""
import json, math, os, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, 'field_tests', 'results')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'rings')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'fusion'))
def mk(st, val, band, note=''): return dict(status=st, value=val, band=band, note=note)
def gauss(v, mu, s):
    p = (v - mu) / s; return ('IN' if abs(p) <= 1 else 'EDGE' if abs(p) <= 2 else 'OUT'), round(p, 2)
def rel(v, t, tol):   # R106: within the last 10% of the band counts as EDGE
    r = v / t - 1; return ('IN' if abs(r) <= 0.9 * tol else 'EDGE' if abs(r) <= tol + 0.10 else 'OUT'), round(r, 3)
M = {}
# A. Hexagon
import hex as H, bandmap1 as BM
E = H.evaluate(dict(H.ADOPTED))
for k, (st, v) in BM.marks(E).items(): M[f'A.{k}'] = mk(st, v, 'Bloom/PRIMAT band')
# B. Fusion tree (scratch copy so locked results are never overwritten)
tmp = tempfile.mkdtemp(); shutil.copytree(os.path.join(ROOT, 'tools', 'fusion'), os.path.join(tmp, 'tools', 'fusion'), ignore=shutil.ignore_patterns('ndata', '__pycache__'))
os.makedirs(os.path.join(tmp, 'field_tests', 'results')); [shutil.copy(os.path.join(RES, f), os.path.join(tmp, 'field_tests', 'results')) for f in os.listdir(RES) if f.endswith('.json')]
_f = os.path.join(tmp, 'field_tests', 'results', 'prom9_tree_rerun.json'); os.remove(_f)   # R106: never fall back to a stale result
_r = subprocess.run([sys.executable, 'test_prom9_tree_rerun.py'], cwd=os.path.join(tmp, 'tools', 'fusion'), capture_output=True, timeout=900)
if _r.returncode != 0 or not os.path.exists(_f): raise SystemExit('fusion tree rerun failed: ' + _r.stderr.decode()[-400:])
T = json.load(open(_f))['layers']
for k, v in T.items():
    M[f'B.{k}'] = mk('IN' if v['pass_'] else 'OUT', {x: y for x, y in v.items() if x != 'pass_' and not isinstance(y, dict)}, 'PROM-9 DEV-corrected goalposts')
s3 = T['L3_S3_ITER']; M['B.L3_S3_ITER']['status'] = 'EDGE' if not s3['pass_'] and abs(s3['tau500'] / 3.4 - 1) <= 0.25 else M['B.L3_S3_ITER']['status']
# C. Neutron ladder (locked result files)
L = lambda f: json.load(open(os.path.join(RES, f)))
n1 = L('n1_rerun.json')['rows']; M['C.N1_birth'] = mk('IN' if all(abs(r['r_FWHM_var']) <= .02 and abs(r['r_shift']) <= .05 for r in n1.values()) else 'OUT', {T_: round(r['r_shift'], 4) for T_, r in n1.items()}, 'shift 5%, FWHM 2%')
g = L('n3n4_rerun.json')['goals']; M['C.N3N4_data_resonances'] = mk('IN' if all(g.values()) else 'OUT', g, 'locked D1 D2 R1-R4')
g = L('n5_rerun.json')['goals']; M['C.N5_doppler'] = mk('IN' if all(g.values()) else 'OUT', g, 'locked P1-P4')
b = L('n6n8_rerun.json')['base']; st, r_ = rel(b['TBR'], 1.0266, .05); M['C.N8_TBR'] = mk(st, round(b['TBR'], 4), '1.0266 +-5%', f'rel {r_}')
n9 = L('n9n10_rerun.json'); st, _ = ('IN' if 1.05 <= n9['M_local'][0] * 14.06 / 14.0 <= 1.35 else 'OUT', 0); M['C.N9_M'] = mk(st, round(n9['M_local'][0] * 14.06 / 14.0, 3), '1.05-1.35', 'D2207a source-energy correction')
st, r_ = rel(n9['dpa_front_cm'], 10.0, .30); M['C.N10_front_dpa'] = mk(st, round(n9['dpa_front_cm'], 2), '10 +-30% dpa/fpy per MW/m2', f'rel {r_}')
he = n9['he_appm_per_dpa_Fe_only']; M['C.N10_He_per_dpa_Fe'] = mk(('EDGE' if he < 7.9 or he > 15.1 else 'IN') if 7 <= he <= 16 else 'OUT', round(he, 2), '7-16 appm/dpa', 'R106: within 10% of the band edge')
g = L('n11_activation.json')['goals']; M['C.N11_activation'] = mk('EDGE' if all(g.values()) else 'OUT', g, 'R100/R106: goalposts too weak to count as IN (A4 tautology, A2 by half-life)')
g = L('n12_rerun.json')['goals']; M['C.N12_closed_loop'] = mk('IN' if all(g.values()) else 'OUT', g, 'C1 algebra, C2 hold/double')
# D. JET (live, current beam-target model)
import beam_target as BT
fr = (0.53, 0.33, 0.14); p71 = BT.P_bt(26.5, 108.0, fr, 6.5, 6e19, 0.85, 0.85, Ti_keV=9.0); p522 = BT.P_bt(30.0, 108.0, fr, 6.5, 6e19, 0.80, 0.85, Ti_keV=9.0)
c3 = json.load(open(os.path.join(RES, 'stagemap_cycle3_sparc.json')))['rerun']['engine_npk13']   # D2217: cycle 3 code-to-code (cfspopcon PRD cell), EDGE ceiling
M['B.L4_S3_SPARC'] = mk(c3['B_L4'], dict(P_fus=round(c3['P_fus'], 1), P_aux_req=round(c3['P_aux_req'], 2)), 'cfspopcon PRD cell 115.8 MW, P_aux+ohm 8.29 MW, +-25% (EDGE ceiling)', f"cycle 3: dP {c3['dP_fus']:+.3f}, dPaux {c3['dPaux_vs_abs_plus_ohmic']:+.3f}; literal 140/Q11 clause FAILED (goalpost, DEV-1)")
st, r_ = rel(p71, 8.7, .40); M['D.JET_99971'] = mk(st, round(p71, 2), '8.7 MW +-40%', f'rel {r_}')
st, r_ = rel(p522, 11.6, .40); M['D.JET_104522'] = mk(st, round(p522, 2), '11.6 MW +-40%', f'rel {r_}')
DIAG = json.load(open(os.path.join(RES, 'stagemap_diagnoses.json'))) if os.path.exists(os.path.join(RES, 'stagemap_diagnoses.json')) else {}
for k, why in DIAG.items():   # R106: a diagnosis explains a miss; it never changes the status
    if k in M: M[k]['note'] = (M[k]['note'] + ' | ' if M[k]['note'] else '') + 'DIAGNOSIS: ' + why.replace('BLOCKED: ', '')
tag = sys.argv[1] if len(sys.argv) > 1 else 'map'
cnt = {s: sum(v['status'] == s for v in M.values()) for s in ('IN', 'EDGE', 'OUT', 'BLOCKED')}
json.dump(dict(counts=cnt, markers=M), open(os.path.join(RES, f'stagemap_{tag}.json'), 'w'), indent=1, default=str)
print(tag, cnt)
for k, v in M.items():
    if v['status'] != 'IN': print(f"  {v['status']:7s} {k}: {str(v['value'])[:90]}  [{v['band']}] {v['note']}")
