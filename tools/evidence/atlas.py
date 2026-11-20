# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Evidence Atlas (queue item L; rules locked in field_tests/rules/PREREG_EVIDENCE_ATLAS.md).
One row per quantity, generated from the live engine and toolkits. Labels: P prediction · F fitted · A assumed ·
S standard physics (not a Weave test) · G open. Only P rows count as evidence; fails are kept.
Run: python3 -m tools.evidence.atlas [out_dir]  → atlas.json, atlas.csv, atlas_<toolkit>.csv"""
import csv, json, math, os, re, sys

def _st(p):
    if isinstance(p, str): return 'pass' if p == 'pass' else 'fail'
    if p is None: return 'open'
    a = abs(p); return 'pass' if a < 2 else 'tension' if a < 3 else 'fail'

def rows():
    from tools.weave_control import engine as E
    from tools.janus_calc import settings as J
    R = []
    def add(**k):
        k.setdefault('pull', None); k.setdefault('status', _st(k['pull'])); k.setdefault('dnote', ''); R.append(k)
    lv = {l['id']: l for l in E.run()['levels']}

    # ---- inflation (Janus): full Weave prediction vs every CMB set; headline = newest combined sets ----
    pr = J.predict('serapis_10d'); sc = J.score(pr)
    for q, sets in J.CONSTRAINTS.items():
        for k, (v, s, kind, src) in sets.items():
            head = k in ('P-ACT-LB2', 'PR4+BK18')
            add(id=f'infl-{q}-{k}', category='cosmological parameter', toolkit='Janus', quantity=f'{"n_s" if q == "ns" else "r"} vs {k}',
                weave=pr[q], label='F' if q == 'ns' else 'P', data=f'{v} ± {s}' if kind == 'gauss' else f'< {v} (95%)', source=src,
                pull=sc[f'{q}:{k}'], headline=head and q == 'r', dnote='J3b; register A2/A5')
    add(id='infl-alpha_s', category='cosmological parameter', toolkit='Janus', quantity='running α_s', weave=pr['alpha_s'], label='P',
        data='no measurement at this precision yet (CMB-S4 + SPHEREx σ ≈ 2e-3)', source='register A1 / plan #4', status='open', headline=False)
    add(id='infl-r-ladder', category='cosmological parameter', toolkit='Janus', quantity='r(6D) / r(10D) = 2', weave=round(J.predict('serapis_6d')['r']/pr['r'], 3),
        label='P', data='no detection of r yet (LiteBIRD, CMB-S4)', source='register A2/A3', status='open', headline=False)

    # ---- flavour: each row with its own measurement and one source ----
    f = lv['flavour']; o = f['outputs']
    from tools.weave_control.engine import S12_DATA, LEPTONS_MeV, SUM_MNU, SUM_MNU_BOUND, T2KNOVA_1SIG, NUFIT_DCP_3SIG
    FL = {'Koide Q = 2/3': (o['Koide_Q'], f"2/3 (m_τ {LEPTONS_MeV['tau'][0]} ± {LEPTONS_MeV['tau'][1]} MeV)", 'PDG 2024 lepton masses', 'P', True)}
    for k, (v, sg, src) in S12_DATA.items():
        FL[f'TM1 sin²θ₁₂ vs {k}'] = (o['TM1_sin2_theta12'], f'{v} ± {sg}', src, 'P', k == 'post-JUNO global')
    FL['TM1 δ_CP (lower branch, s₂₃² 0.561) inside T2K+NOvA 1σ'] = (o['TM1_dCP_s23_0561'][1], f'{T2KNOVA_1SIG[0]:.0f}°–{T2KNOVA_1SIG[1]:.0f}° (1σ)', 'T2K+NOvA, Nature 2025 (s41586-025-09599-3)', 'P', True)
    FL['TM1 δ_CP (lower branch, s₂₃² 0.561) inside NuFIT 3σ'] = (o['TM1_dCP_s23_0561'][1], f'{NUFIT_DCP_3SIG[0.561][0]:.0f}°–{NUFIT_DCP_3SIG[0.561][1]:.0f}° (3σ)', 'NuFIT 6.0, arXiv:2410.05380', 'P', False)
    FL['Σm_ν (NO, m₁ = 0) below the DESI+CMB bound'] = (SUM_MNU, f'< {SUM_MNU_BOUND} eV (95%)', 'DESI DR2 + CMB bound as used in D1234', 'A', False)
    for k, v in f['pulls'].items():
        w, dat, src, lab, head = FL[k]
        add(id='flav-' + re.sub(r'\W+', '-', k)[:40], category='particle' if 'Koide' in k else 'neutrino', toolkit='Flavour', quantity=k,
            weave=w, label=lab, data=dat, source=src, pull=v, headline=head and lab == 'P', dnote='D1652, D1667, D1669, D1690; PREREG_W4_FLAVOUR')
    add(id='flav-TM2', category='particle', toolkit='Flavour', quantity='exact TM2 sin²θ₁₂ (an earlier Weave assignment)', weave=f['outputs']['TM2_sin2_theta12_excluded'],
        label='P', data='0.3092 ± 0.0087 (JUNO)', source='JUNO arXiv:2511.14593; D1652', pull=(f['outputs']['TM2_sin2_theta12_excluded'] - 0.3092)/0.0087,
        headline=True, dnote='D1652: the only future-data test so far; FAILED; superseded by TM1')

    # ---- light elements (Hyperion) ----
    b = lv['bbn']
    from tools.janus_astro import settings as H
    for k, v in b['pulls'].items():
        if '(PRIMAT' not in k: continue
        q, ds = k.split(' (')[0].split(':'); val, sg, src = H.DATA[q][ds]
        el = 'helium-4 (Y_p)' if q == 'Yp' else 'deuterium (D/H)'
        add(id='bbn-' + re.sub(r'\W+', '-', k)[:40], category='nucleus & element', toolkit='Hyperion', quantity=f'{el} vs {ds}',
            weave=b['outputs'][q], label='P', data=f'{val} ± {sg}', source=src, pull=v, headline=True,
            dnote='pull includes PRIMAT theory σ (PREREG_W5_BBN_THEORY); D1651')
    li_w, li_d, li_s, li_th = 4.35e-10, 1.6e-10, 0.3e-10, 0.72e-10
    add(id='bbn-li7', category='nucleus & element', toolkit='Hyperion', quantity='lithium-7 (⁷Li/H) — the lithium problem',
        weave=li_w, label='P', data='(1.6 ± 0.3) × 10⁻¹⁰ (Spite plateau)', source='D1100 (arXiv:2508.09821); Weave value D1640; theory σ 0.72e-10 (D1100)',
        pull=(li_w - li_d)/math.hypot(li_s, li_th), headline=True, dnote='D1640: NOT solved (shared with standard BBN)')
    for el in ('helium-3', 'carbon and heavier (stellar)'):
        add(id='elem-' + el.split()[0], category='nucleus & element', toolkit='Hyperion', quantity=el, weave=None, label='G',
            data='not yet modelled' if 'stellar' in el else 'no primordial measurement used yet', source='register D3', status='open', headline=False)

    # ---- dark sector & late universe ----
    late = lv['late']['outputs']
    for sn, r in late['D1725'].items():
        add(id=f'late-thread-{sn}', category='cosmological parameter', toolkit='CLASS/Weave Control', quantity=f'reverse thread Δχ² vs ΛCDM ({sn})',
            weave=round(r['d_thread'], 2), label='P', data='Planck 2018 + DESI DR2 + SN', source='D1725 (locked CLASS runs)',
            pull='pass' if r['d_thread'] < 0 else 'FAIL', headline=False, dnote=f'ΔAIC {r["dAIC_thread"]:.1f}; trails w0wa')
    aic = [r['dAIC_thread'] for r in late['D1725'].values()]
    add(id='late-thread-all', category='cosmological parameter', toolkit='CLASS/Weave Control', quantity='reverse thread beats ΛCDM after the parameter penalty (ΔAIC < 0 on all 3 SN sets)',
        weave=' / '.join(f'{a:.1f}' for a in aic), label='P', data='Planck 2018 + DESI DR2 + Pantheon+ / DES-Y5 / Union3', source='D1725',
        pull='pass' if all(a < 0 for a in aic) else 'FAIL', headline=True, dnote='rule 5: one headline row for the three overlapping fits')
    add(id='late-coupling', category='cosmological parameter', toolkit='CLASS/Weave Control', quantity='Arthur-field coupling b_A detected?',
        weave='b_A = +0.004 / +0.020 / −0.041', label='P', data='consistent with 0', source='D1725', pull='FAIL', headline=True, dnote='D1725 fix_fails')
    add(id='late-w0wa', category='cosmological parameter', toolkit='CLASS/Weave Control', quantity='thread vs flexible w0wa',
        weave='−2.6 / −8.1 / −3.4', label='P', data='w0wa −9.1 / −19.7 / −15.0', source='D1712 (CAMB)', status='tension', pull=None, headline=True, dnote='thread behind w0wa')
    for k, v in late['S8_pulls'].items():
        if ' lcdm ' in k: continue
        add(id='late-' + re.sub(r'\W+', '-', k)[:40], category='cosmological parameter', toolkit='CLASS/Weave Control', quantity=k,
            weave=None, label='P', data='KiDS-Legacy / CMB lensing', source='arXiv:2503.19441; arXiv:2602.12238', pull=v,
            headline=False, dnote='PREREG_W2_LINKS L3')
    tk = {k: v for k, v in late['S8_pulls'].items() if k.startswith('S8 thread') and 'KiDS' in k}
    worst = max(tk.values(), key=abs)
    add(id='late-S8-thread', category='cosmological parameter', toolkit='CLASS/Weave Control', quantity='S₈ of the thread fits vs KiDS-Legacy (worst of 3)', weave=None,
        label='P', data='0.815 +0.016/−0.021', source='arXiv:2503.19441', pull=worst, headline=True, dnote='rule 5: one headline row')

    # ---- colliders & dark matter ----
    c = lv['colliders']; g = lv['galaxy']
    add(id='lhc-wino', category='collider limit', toolkit='CERN+1', quantity=f'wino at {E.DEFAULTS["wino_mass_GeV"]:.0f} GeV vs ATLAS disappearing tracks',
        weave=E.DEFAULTS['wino_mass_GeV'], label='A', data='> 670 GeV excluded below', source=E.ATLAS_DT[1], pull=c['pulls']['ATLAS observed limit'], headline=False,
        dnote='mass is a chosen benchmark, not a prediction')
    for m in (440.0, 1000.0, 2900.0):
        for h in ('Einasto', 'Burkert'):
            gl = [l for l in E.run({'wino_mass_GeV': m, 'halo': h})['levels'] if l['id'] == 'galaxy'][0]
            add(id=f'gline-{int(m)}-{h}', category='astrophysical object', toolkit='Hyperion', quantity=f'wino gamma line at {int(m)} GeV, {h} halo',
                weave=gl['outputs'].get('thermal_fraction'), label='P', data=f"H.E.S.S. limit, f_max {gl['outputs'].get('f_max') and round(gl['outputs']['f_max'], 3)}",
                source=E.HESS_SRC, status=gl['status'], pull=None, headline=(m == 1000.0 and h == 'Einasto'), dnote='PREREG_W2_LINKS L1 + DEVIATIONS D1')
    add(id='dm-12.8', category='particle', toolkit='Hyperion', quantity='dark particle (sarion) mass 12.8 GeV from chemical equilibrium', weave=12.8, label='P',
        data='xenon limits survive; dark photon cut to ε ≲ 3e-9–8e-7', source='D1676, D1677', status='pass', pull=None, headline=True, dnote='LZ curve at 13 GeV not yet sourced (D1678)')

    # ---- stars, neutrinos ----
    st = lv['stars']
    add(id='ns-mmax', category='astrophysical object', toolkit='Hyperion', quantity='max neutron-star mass (SLy)', weave=st['outputs']['M_max_Msun'], label='S',
        data='PSR J0740+6620 2.08 ± 0.07', source=E.J0740[2], pull=st['pulls'][list(st['pulls'])[0]], headline=False, dnote='standard nuclear physics')
    for q, v in (('relic neutrino number density (cm⁻³)', 336), ('relic neutrino temperature (K)', 1.945), ('Ω_ν h²', 6.31e-4)):
        add(id='nu-' + re.sub(r'\W+', '-', q)[:30], category='neutrino', toolkit='Hyperion', quantity=q, weave=v, label='S' if 'Ω' not in q else 'A',
            data='not directly measured (PTOLEMY-type capture needed)', source='standard cosmology; masses from register node mnu', status='open', headline=False, dnote='queue K1')
    return R

# DEVIATIONS D1: timing / kind / inherited, with a one-line reason each (prefix match on row id)
CLASSIFY = [  # (id prefix, timing, kind, inherited, reason)
    ('infl-ns', 'post-hoc', 'match', False, 'n_s is fitted by the Ushas tilt'),
    ('infl-r', 'locked', 'bound', False, 'r follows from the locked species-plateau curve; the bound data predate the model'),
    ('infl-alpha', 'locked', 'match', False, 'no measurement yet'),
    ('flav-Koide', 'locked', 'match', True, 'Koide 1982 relation, inherited'),
    ('flav-TM1-sin', 'post-hoc', 'match', True, 'TM1 adopted after JUNO excluded TM2 (D1667); TM1 is a known pattern'),
    ('flav-TM1-', 'locked', 'match', True, 'TM1 sum rule is inherited; branch chosen by data'),
    ('flav-m', 'locked', 'bound', False, 'mass sum assumes m1 = 0'),
    ('flav-TM2', 'future-data', 'match', False, 'exact TM2 was on record before JUNO first data (Nov 2025 data vs earlier assignment)'),
    ('bbn-Yp', 'locked', 'match', True, 'standard BBN at ΔN_eff ≈ 0: the Weave leaves it unchanged'),
    ('bbn-DH', 'locked', 'match', True, 'standard BBN at ΔN_eff ≈ 0'),
    ('bbn-li7', 'locked', 'match', True, 'standard BBN failure, inherited'),
    ('elem-', 'locked', 'match', False, 'open'),
    ('late-thread', 'locked', 'comparison', False, 'PREREG_PLANCK_CLASS locked before the fits; data public'),
    ('late-coupling', 'locked', 'match', False, 'PREREG_PLANCK_CLASS'),
    ('late-w0wa', 'locked', 'comparison', False, 'D1712'),
    ('late-S8', 'locked', 'match', False, 'PREREG_W2_LINKS L3'),
    ('late-', 'locked', 'match', False, 'PREREG_W2_LINKS L3'),
    ('lhc-', 'locked', 'bound', False, 'benchmark mass'),
    ('gline-', 'locked', 'bound', False, 'PREREG_W2_LINKS L1'),
    ('dm-', 'locked', 'bound', False, 'PREREG_Q9/Q11: survives limits'),
    ('ns-', 'locked', 'bound', True, 'standard nuclear physics'),
    ('nu-', 'locked', 'match', True, 'standard cosmology'),
]
def classify(R):
    for r in R:
        for pre, t, k, inh, why in CLASSIFY:
            if r['id'].startswith(pre):
                r.update(timing=t, kind=k, inherited=inh, why=why); break
        else: r.update(timing='locked', kind='match', inherited=False, why='default')
        if r['id'] == 'bbn-Yp-Aver2021-PRIMAT-theory-' or r['id'].startswith('bbn-Yp-Aver'): r['headline'] = False   # one helium headline (LBT 2026)
        r['evidence'] = bool(r.get('headline') and r['label'] == 'P' and r['timing'] != 'post-hoc' and not r['inherited'])
    return R

def summary(R):
    out = {'rows': len(R), 'by_label': {}, 'by_status': {}, 'headline_P': {}, 'evidence': {}, 'evidence_by_kind': {}, 'consistent_not_evidence': {}}
    for r in R:
        out['by_label'][r['label']] = out['by_label'].get(r['label'], 0) + 1
        out['by_status'][r['status']] = out['by_status'].get(r['status'], 0) + 1
        if r['label'] == 'P' and r.get('headline'):
            out['headline_P'][r['status']] = out['headline_P'].get(r['status'], 0) + 1
            bucket = out['evidence'] if r.get('evidence') else out['consistent_not_evidence']
            bucket[r['status']] = bucket.get(r['status'], 0) + 1
            if r.get('evidence'):
                kk = out['evidence_by_kind'].setdefault(r['kind'], {}); kk[r['status']] = kk.get(r['status'], 0) + 1
    return out

def build(out_dir):
    from tools.prov_block import provenance
    os.makedirs(out_dir, exist_ok=True); R = classify(rows()); S = summary(R)
    doc = dict(provenance=provenance('Evidence Atlas', {}, [], ['PREREG_EVIDENCE_ATLAS']), summary=S, rows=R)
    json.dump(doc, open(os.path.join(out_dir, 'atlas.json'), 'w', encoding='utf-8'), indent=1, default=lambda o: float(o) if hasattr(o, '__float__') else str(o), ensure_ascii=False)
    cols = ['id', 'category', 'toolkit', 'quantity', 'weave', 'label', 'timing', 'kind', 'inherited', 'evidence', 'data', 'source', 'pull', 'status', 'headline', 'why', 'dnote']
    def w(path, rs):
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            c = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); c.writeheader(); c.writerows(rs)
    w(os.path.join(out_dir, 'atlas.csv'), R)
    for tk in sorted({r['toolkit'] for r in R}): w(os.path.join(out_dir, 'atlas_' + re.sub(r'\W+', '_', tk) + '.csv'), [r for r in R if r['toolkit'] == tk])
    print(json.dumps(S, indent=1)); return doc

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'))
