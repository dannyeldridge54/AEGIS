# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Weave Control engine (W1, 20 Nov 2026): ONE parameter set drives every AEGIS toolkit, level by level.
run(params) -> {'params', 'levels': [level, ...], 'scorecard'}. Each level:
  {id, name, category (A inflation/loom, B flavour, C dark sector & late universe, D matter genesis & stars, E observing),
   tool, inputs, outputs, data: [{name, value, sigma | limit, kind, source}], pulls {name: sigma | 'pass'/'FAIL'},
   status: pass | tension | fail | open, labels: notes on what is predicted (P), fitted (F) or an open gap (G), links}
Rules: every number is computed by a validated toolkit function, or is a measurement carrying its source.
Status: pass if every |pull| < 2 and every limit passes; tension if a |pull| is 2–3; fail if any |pull| ≥ 3 or a limit fails."""
import cmath, functools, math, warnings

DEFAULTS = dict(
    inflation_model='serapis_10d', Nstar=55.0,                      # Janus (N* ignored for the full SERAPIS models)
    omega_b=0.02237, dark_sector='brane_split',                    # Hyperion BBN; dark sector sets ΔN_eff (link)
    b_A=0.0, Omega_phi=0.70, Omega_c=0.25, dphi=0.64,               # late universe (D1717 closed form)
    wino_mass_GeV=1000.0, run='run3',                               # CERN+1
    halo='Einasto', rho_sun=0.4,                                    # Hyperion galaxy
    eos='SLy',                                                      # Hyperion stars
    target='M31', aperture_mm=80.0, site='okc',                     # Mapper
    sugra_m=1, tauq_mass_GeV=1e11, tauq_phi0=1.0)                   # quark thread τ_q (Q4–Q6, D1730–D1732)
# ΔN_eff carried by each dark-sector branch (register C3/C5): mirror world at its BBN bound; minimal dark sector cold.
# Each value from the D-notes (V1 finding 1): the label says which note and whether it is an estimate or a bound.
DARK_SECTORS = {'none': (0.0, 'no dark radiation'),
                'brane_split': (0.0, 'P-brane (C5, D1671): visible on D3, dark on unfluxed D7; the inflaton heats our side only, ΔN_eff ≈ 0 (must be ≤ 0.086, C5)'),
                'minimal_equal_sharing': (0.21, 'minimal dark sector (5 GeV baryon + dark photon) with equal sharing per particle: ΔN_eff = 0.21 (D1646, estimate)'),
                'mirror_at_bound': (0.3, 'mirror sector at its viability bound ΔN_eff = 0.3 (D1648)'),
                'mirror_full_equal': (7.4, 'full mirror world with equal sharing: ΔN_eff = 7.4 (D1646) — RULED OUT')}
LEPTONS_MeV = dict(e=(0.51099895000, 1.5e-10), mu=(105.6583755, 2.3e-6), tau=(1776.93, 0.09))   # PDG 2024
# PREREG_W4_FLAVOUR inputs (sourced)
NUFIT_S13 = (0.02195, 'NuFIT 6.0 NO IC19, arXiv:2410.05380 (as in D1667)')
S12_DATA = {'JUNO first data': (0.3092, 0.0087, 'JUNO, arXiv:2511.14593'),
            'NuFIT 6.0 + JUNO': (0.3084, 0.0070, 'combination used in D1652'),
            'post-JUNO global': (0.3085, 0.0073, 'arXiv:2511.21650')}
SUM_MNU, SUM_MNU_BOUND = 0.0587, 0.0642          # eV; register node mnu (frozen; D1234 recomputed 0.05878) and the bound used in D1234
T2KNOVA_1SIG = (214.0, 313.0)                    # degrees; ordering-marginalised 1σ, Nature 2025 (D1690)
NUFIT_DCP_3SIG = {0.561: (96.0, 422.0), 0.470: (124.0, 364.0)}   # degrees; NuFIT 6.0 NO IC19 / IC24 (D1669)
J0740 = (2.08, 0.07, 'PSR J0740+6620 mass (Fonseca et al. 2021, ApJL 915 L12)')
ATLAS_DT = (670.0, 'ATLAS disappearing track, observed 95% wino limit (arXiv:2603.08315; D1722)')
# L3 (PREREG_W2_LINKS): S8 = sigma8 sqrt(Omega_m/0.3) from the locked D1725 best fits, read 20 Nov 04:55 CT from the PC
# AEGIS_PCJOBS/d1713/results/: cls_lcdm{,_desy5,_union3}.json, cls_thread{...}.json, coupled = cls_coupled_nested.json (P+),
# cls_coupled_desy5_nested.json (DES-Y5), cls_coupled_union3.json (Union3) — the lower-chi2 run per set. Verified to 4 d.p. (W2/V1).
S8_FITS = {'Pantheon+': dict(lcdm=0.8127, thread=0.8093, coupled=0.8124), 'DES-Y5': dict(lcdm=0.8148, thread=0.8080, coupled=0.8083),
           'Union3': dict(lcdm=0.8137, thread=0.8128, coupled=0.8283)}   # coupled = the run with the lower chi2 (orig or nested)
S8_DATA = {'KiDS-Legacy': (0.815, 0.016, 0.021, 'arXiv:2503.19441'), 'CMB lensing (ACT DR6+Planck PR4+SPT-3G+DESI DR2)': (0.828, 0.012, 0.012, 'Qu et al. 2026, via arXiv:2602.12238')}
LYA = dict(z=2.33, DH_rd=(8.632, 0.101), DM_rd=(38.99, 0.53), rho=-0.431, source='DESI DR2 Lyα BAO, arXiv:2503.14739')
D1725 = {'Pantheon+': dict(lcdm=2432.76, thread=2430.14, coupled=2432.28), 'DES-Y5': dict(lcdm=2676.47, thread=2668.33, coupled=2667.44),
         'Union3': dict(lcdm=1055.14, thread=1051.76, coupled=1052.44)}

def _status(pulls):
    vals = list(pulls.values())
    if any(v == 'FAIL' for v in vals) or any(isinstance(v, float) and abs(v) >= 3 for v in vals): return 'fail'
    if any(isinstance(v, float) and abs(v) >= 2 for v in vals): return 'tension'
    return 'pass' if vals else 'open'

def L(id, name, cat, tool, inputs, outputs, data, pulls, labels, links=(), status=None):
    return dict(id=id, name=name, category=cat, tool=tool, inputs=inputs, outputs=outputs, data=data, pulls=pulls,
                status=status or _status(pulls), labels=list(labels), links=list(links))

# ---------------- A. inflation (Janus) ----------------
def inflation(p):
    from tools.janus_calc import settings as J
    pr = J.predict(p['inflation_model'], p['Nstar']); sc = J.score(pr)
    data = [dict(name=k, value=v[0], **({'sigma': v[1]} if v[2] == 'gauss' else {'limit': v[0]}), kind=v[2], source=v[3])
            for q, d in J.CONSTRAINTS.items() for k, v in d.items()]
    B1 = pr['r'] - 3*(1 - pr['ns'])**2; B2 = pr['alpha_s'] + 0.5*(1 - pr['ns'])**2
    # status uses the newest combined sets only (overlapping sets are shown, not double counted)
    fitted_ns = p['inflation_model'] in J.WEAVE_FULL
    # referee R1: a fitted quantity cannot grade the model. For serapis_* only the predictions (r; α_s when a running
    # constraint is stored) set the status; for the other models n_s at the chosen N* is a prediction and counts.
    key = {k: sc[k] for k in (('r:PR4+BK18', 'r:BK18') if fitted_ns else ('ns:P-ACT-LB2', 'ns:CMB-SPA+DESI', 'r:PR4+BK18'))}
    labels = ['n_s is FITTED for serapis_* (Ushas tilt chosen); r and α_s are the predictions'] if p['inflation_model'].startswith('serapis') else []
    return L('inflation', 'Inflation', 'A', 'Janus', dict(model=p['inflation_model'], Nstar=pr['Nstar']),
             dict(ns=pr['ns'], r=pr['r'], alpha_s=pr['alpha_s'], bridge_B1=B1, bridge_B2=B2), data, sc,
             labels + [('status from the PREDICTIONS only: r vs PR4+BK18 and BK18 (n_s is fitted, shown as context; referee R1)' if fitted_ns
                        else 'status from P-ACT-LB2, CMB-SPA+DESI, PR4+BK18 (newest combined sets)'),
                       'bridges B1, B2 shown as numbers only: their old targets were set for an earlier model (V1 finding 2)'],
             links=['N* → reheating → BBN (W2)'], status=_status(key))

# ---------------- B. flavour ----------------
def flavour(p):
    m = {k: v[0] for k, v in LEPTONS_MeV.items()}; s = {k: math.sqrt(v) for k, v in m.items()}
    Q = sum(m.values())/sum(s.values())**2
    dQ = (lambda h: (sum(m.values()) + h)/(s['e'] + s['mu'] + math.sqrt(m['tau'] + h))**2 - Q)(1e-3)/1e-3*LEPTONS_MeV['tau'][1]
    # Brannen phase: sqrt(m_k) = mu (1 + sqrt2 cos(delta + 2 pi k/3)); delta = arg(sum_k sqrt(m_k) e^{-2 pi i k/3}) for (tau, e, mu)? test all orders
    import cmath, itertools
    forms = set()
    for order in itertools.permutations(('e', 'mu', 'tau')):
        z = sum(s[n]*cmath.exp(-2j*math.pi*k/3) for k, n in enumerate(order)); d = cmath.phase(z) % (2*math.pi/3)
        forms.update((round(d, 9), round(2*math.pi/3 - d, 9)))
    best = min(forms, key=lambda c: abs(c - 2/9))
    pulls = {'Koide Q = 2/3': (Q - 2/3)/abs(dQ)}
    data = [dict(name=f'm_{k}', value=v[0], sigma=v[1], kind='gauss', source='PDG 2024') for k, v in LEPTONS_MeV.items()]
    # ---- neutrinos (PREREG_W4_FLAVOUR): TM1 on the Weave's two vacua under modular S4 (assumed, P-S4) ----
    s13 = NUFIT_S13[0]; tm1 = (1 - 3*s13)/(3*(1 - s13)); tm2 = 1/(3*(1 - s13))     # same formulas as field_tests/scripts/tm1/run.py
    for k, (v, sg, src) in S12_DATA.items():
        data.append(dict(name=f'sin²θ₁₂ {k}', value=v, sigma=sg, kind='gauss', source=src)); pulls[f'TM1 sin²θ₁₂ vs {k}'] = (tm1 - v)/sg
    dcp = {}
    for s23 in (0.561, 0.470):
        t = math.asin(math.sqrt(s23)); cot2 = 1/math.tan(2*t)
        c1 = -cot2*(1 - 5*s13)/(2*math.sqrt(2)*math.sqrt(s13)*math.sqrt(1 - 3*s13))
        a1 = math.degrees(math.acos(c1)); dcp[s23] = (a1, 360 - a1)
    ref_ok = all(abs(x - y) <= 0.5 for x, y in ((dcp[0.561][0], 74.3), (dcp[0.561][1], 285.7), (dcp[0.470][0], 97.6), (dcp[0.470][1], 262.4)))
    lo = dcp[0.561][1]
    inside = lambda d, lo_, hi_: lo_ <= d <= hi_ or lo_ <= d + 360 <= hi_
    t2k = inside(lo, *T2KNOVA_1SIG); nufit = inside(lo, *NUFIT_DCP_3SIG[0.561])
    data += [dict(name='δ_CP T2K+NOvA ordering-marginalised 1σ', value=T2KNOVA_1SIG, kind='range', source='Nature 2025 (s41586-025-09599-3), via D1690'),
             dict(name='δ_CP NuFIT 6.0 NO 3σ (IC19, s₂₃² 0.561)', value=NUFIT_DCP_3SIG[0.561], kind='range', source='arXiv:2410.05380, via D1669')]
    # DEVIATIONS D1: lower-branch band over the T2K+NOvA 1σ range of sin²θ₂₃ [0.51, 0.59]
    def _low(s23):
        t = math.asin(math.sqrt(s23)); c = -(1/math.tan(2*t))*(1 - 5*s13)/(2*math.sqrt(2)*math.sqrt(s13)*math.sqrt(1 - 3*s13))
        return 360 - math.degrees(math.acos(max(-1.0, min(1.0, c))))
    band = sorted((_low(0.51), _low(0.59)))
    data.append(dict(name='Σm_ν 95% upper bound (DESI DR2 + CMB, as used in D1234)', limit=SUM_MNU_BOUND, kind='upper95', source='D1234 check (DESI DR2 + CMB bound 0.0642 eV)'))
    pulls['Σm_ν (NO, m₁ = 0) below the DESI+CMB bound'] = 'pass' if SUM_MNU < SUM_MNU_BOUND else 'FAIL'
    pulls['TM1 δ_CP (lower branch, s₂₃² 0.561) inside T2K+NOvA 1σ'] = 'pass' if t2k else 'FAIL'
    pulls['TM1 δ_CP (lower branch, s₂₃² 0.561) inside NuFIT 3σ'] = 'pass' if nufit else 'FAIL'
    key = {k: v for k, v in pulls.items() if k in ('Σm_ν (NO, m₁ = 0) below the DESI+CMB bound', 'Koide Q = 2/3', 'TM1 sin²θ₁₂ vs post-JUNO global', 'TM1 δ_CP (lower branch, s₂₃² 0.561) inside T2K+NOvA 1σ', 'TM1 δ_CP (lower branch, s₂₃² 0.561) inside NuFIT 3σ')}
    if not ref_ok: key['δ_CP reproduces D1667'] = 'FAIL'
    return L('flavour', 'Flavour (leptons & neutrinos)', 'B', 'Flavour panel', dict(masses='PDG 2024 pole masses', sin2_theta13=s13),
             dict(Koide_Q=Q, Koide_Q_sigma=abs(dQ), Brannen_delta=best, delta_minus_2_9=best - 2/9, delta_equivalent_forms=sorted(forms),
                  TM1_sin2_theta12=tm1, TM2_sin2_theta12_excluded=tm2, TM1_dCP_s23_0561=list(dcp[0.561]), TM1_dCP_s23_0470=list(dcp[0.470]),
                  dCP_reproduces_D1667=ref_ok, TM1_dCP_band_s23_051_059=band, sum_mnu_eV=SUM_MNU), data, pulls,
             ['Q = 2/3 is a prediction (P-F1)', 'δ = 2/9 has no mechanism yet (C-δ)',
              'neutrinos: TM1 with modular S₄ at the Weave vacua ρ and (an image of) i is ASSUMED (P-S4, register B5); exact TM2 is excluded by JUNO (D1652)',
              'δ_CP branch is CHOSEN BY THE DATA: TM1 fixes cos δ only and predicts the mirror pair (referee N-R1)',
              'δ_CP band shown over sin²θ₂₃ ∈ [0.51, 0.59] (T2K+NOvA 1σ): the value moves strongly with θ₂₃ (DEVIATIONS D1)',
              'normal mass ordering assumed; inverted ordering not evaluated (N-R4)',
              'θ₁₃ used as a point value: its error moves TM1 sin²θ₁₂ by ≈ 0.0004, small next to the data error 0.0073 (N-R5)',
              'Σm_ν = 0.0587 eV assumes m₁ = 0 (register node mnu), an assumption of the mass sector, not derived from modular S₄ (N-R3)',
              'sharpest near-term test: JUNO 6-year sin²θ₁₂ (≈ ±0.0015) would put TM1 (0.3184) about 6σ from today\'s centre (0.3085) if the centre holds',
              'status (PREREG_W4_FLAVOUR): TM1 sin²θ₁₂ vs the post-JUNO global value, and the lower δ_CP branch for s₂₃² = 0.561 (the T2K+NOvA-preferred θ₂₃); the upper branch (74°/98°) is outside the data',
              'δ is defined only up to relabelling the leptons and δ → 2π/3 − δ; the form nearest 2/9 is shown and all forms are listed (V1 finding 5)'],
             links=['DUNE / Hyper-K δ_CP; JUNO sin²θ₁₂ to ±0.5%: TM1 0.3184 vs TM2 0.3408'], status=_status(key))

# ---------------- D. BBN (Hyperion), fed by the dark sector ----------------
# PREREG_W5_BBN_THEORY: theory σ on Hyperion's own Y_p and D/H. PRIMAT sets the status; Yeh+ and obs-only are shown.
# PREREG_W5_BBN_THEORY: theory σ on Hyperion's own Y_p and D/H. PRIMAT sets the status; Yeh+ and obs-only are shown.
from tools.janus_astro.settings import BBN_THEORY   # one source of truth (Hyperion)
def bbn(p):
    from tools.janus_astro import settings as H
    dN, why = DARK_SECTORS[p['dark_sector']]
    b = H.bbn(p['omega_b'], dN)
    data = [dict(name=f'{q}:{k}', value=v[0], sigma=v[1], kind='gauss', source=v[2]) for q in ('Yp', 'DH') for k, v in H.DATA[q].items()]
    model = {'Yp': b['Yp'], 'DH': b['DH']}
    th = lambda conv, q: (lambda kind, v: v if kind == 'abs' else v*model[q])(*BBN_THEORY[conv][q])
    status_pulls, shown = {}, {}
    for q in ('Yp', 'DH'):
        for k, (v, so, _) in H.DATA[q].items():
            shown[f'{q}:{k} (obs only)'] = (model[q] - v)/so
            shown[f'{q}:{k} (Yeh+ theory σ)'] = (model[q] - v)/math.hypot(so, th('Yeh+Olive+Fields', q))
            status_pulls[f'{q}:{k} (PRIMAT theory σ)'] = (model[q] - v)/math.hypot(so, th('PRIMAT', q))
    return L('bbn', 'Big Bang nucleosynthesis', 'D', 'Hyperion', dict(omega_b=p['omega_b'], dNeff=dN, dNeff_from=why, code=b['code']),
             dict(Yp=b['Yp'], DH=b['DH'], Yp_theory_sigma_PRIMAT=th('PRIMAT', 'Yp'), DH_theory_sigma_PRIMAT=th('PRIMAT', 'DH')),
             data + [dict(name=f'theory σ ({k})', source=v['src']) for k, v in BBN_THEORY.items()],
             {**status_pulls, **shown},
             ['lithium problem reproduced, not solved (D1640)',
              'PREREG_W5_BBN_THEORY: pulls combine the observational σ with the PRIMAT theory σ (Y_p ±0.00017, D/H 1.5%); this sets the status',
              'shown beside it, never setting the status: Yeh+Olive+Fields theory σ (D/H 4.4%, includes the ω_b error) and observational-only pulls',
              'the two theory conventions differ by ~3% in D/H, mostly from the d(p,γ)³He rate (theory vs LUNA data)'],
             links=[f"ΔN_eff = {dN} from dark sector '{p['dark_sector']}'",
                    'L4: reheating (T_rh ≈ 9 × 10⁸ GeV, N*) has no direct BBN effect; ΔN_eff is the only BBN link'],
             status=_status(status_pulls))

# ---------------- C. late universe (CLASS results + D1717 closed form) ----------------
def late(p):
    b = p['b_A']; x = math.exp(abs(b)*p['dphi']) - 1
    zdag = (p['Omega_phi']/(p['Omega_c']*x))**(1/3) - 1 if b < 0 and x > 0 else None
    Geff = 1 + 2*b*b
    rows = {k: dict(d_thread=v['thread'] - v['lcdm'], d_coupled_reported=v['coupled'] - v['lcdm'],
                    d_coupled_at_most=min(v['coupled'], v['thread']) - v['lcdm'],
                    dAIC_thread=v['thread'] - v['lcdm'] + 2*1,                                # +1 parameter (amplitude)
                    dAIC_coupled_at_most=min(v['coupled'], v['thread']) - v['lcdm'] + 2*2)    # +2 (amplitude, b_A)
            for k, v in D1725.items()}
    pulls = {f'thread beats ΛCDM ({k})': 'pass' if r['d_thread'] < 0 else 'FAIL' for k, r in rows.items()}
    W0WA = {'Pantheon+': -9.11, 'DES-Y5': -19.72, 'Union3': -15.02}     # CAMB, D1712 context
    s8 = {}
    for sn, mods in S8_FITS.items():
        for mod, v in mods.items():
            for dn, (dv, sm, sp, _) in S8_DATA.items():
                pull = (v - dv)/(sp if v > dv else sm); s8[f'S8 {mod} {sn} vs {dn.split(" (")[0]}'] = pull
    s8_status = _status({k: v for k, v in s8.items() if ' lcdm ' not in k})
    behind = all(rows[k]['d_thread'] > W0WA[k] for k in rows)
    return L('late', 'Late universe (dark energy)', 'C', 'CLASS (patched) + closed form', dict(b_A=b, dphi=p['dphi']),
             dict(z_dagger=zdag, G_eff_over_G=Geff, D1725=rows, S8_fits=S8_FITS, S8_pulls=s8, S8_status=s8_status, Lya_context=LYA),
             [dict(name='full Planck + DESI DR2 + SN', source='D1725 (locked CLASS runs)')]
             + [dict(name=f'S8 {k}', value=v[0], sigma=(v[1], v[2]), kind='gauss_asym', source=v[3]) for k, v in S8_DATA.items()]
             + [dict(name='DESI DR2 Lyα BAO z 2.33 (context only, already in the fits)', value=LYA['DH_rd'][0], sigma=LYA['DH_rd'][1], kind='context', source=LYA['source'])],
             pulls, ['b_A is consistent with 0 on full Planck (D1725, fix_fails)', 'negative space needs b_A < 0 (D1716/D1717)',
                     'Δχ² are the locked fit results; they do not change with the b_A slider',
                     'd_coupled_at_most = min(coupled, thread): the coupled model contains the thread, so its true value is at most this (nested guard)',
                     'thread trails w0wa (−9.1 / −19.7 / −15.0, CAMB)',
                     'ΔAIC = Δχ² + 2k charges the extra parameters (thread k = 1, coupled k = 2); negative still favours the model (referee R3)',
                     'L3: S₈ of each locked fit vs KiDS-Legacy and CMB lensing, reported separately (not combined); the lensing combination shares DESI DR2 BAO and Planck data with the fits, so KiDS-Legacy is the cleaner comparison',
                     f'S₈ sub-status: {s8_status} (largest |pull| {max(abs(v) for v in s8.values()):.1f}σ)',
                     'L2: DESI Lyα BAO is shown as context only: it is already inside the DESI DR2 likelihood of the fits, so it is not an independent test'],
             links=['G_eff → S₈ (W2)', 'z† → H(z) at z 2–5 vs DESI Lyα (W2)'],
             status=('tension' if behind else _status(pulls)) if _status(pulls) == 'pass' else _status(pulls))

# ---------------- C. colliders (CERN+1) ----------------
def colliders(p):
    from tools.lhc import settings as C
    pt = C.point(p['run'], 'wino', p['wino_mass_GeV']); rc = C.reach(p['run'])
    pulls = {'ATLAS observed limit': 'pass' if p['wino_mass_GeV'] > ATLAS_DT[0] else 'FAIL'}
    return L('colliders', 'Colliders (wino)', 'C', 'CERN+1', dict(run=p['run'], m=p['wino_mass_GeV']),
             dict(sigma_fb=pt['sigma_fb'], pairs=pt['produced_pairs'], ctau_cm=pt.get('ctau_cm'), expected_reach_GeV=rc['wino_reach_GeV']),
             [dict(name='ATLAS DT limit', limit=ATLAS_DT[0], kind='lower95', source=ATLAS_DT[1])], pulls,
             ['a wino below 670 GeV is excluded by ATLAS'], links=['same wino → gamma line (Galaxy level)'])

# ---------------- C. galaxy & dark matter (Hyperion) ----------------
@functools.lru_cache(maxsize=64)
def _jfactor(halo, rho_sun):
    from tools.janus_astro import settings as H
    return H.jfactor(halo, rho_sun=rho_sun)['J_GeV2_cm5']
@functools.lru_cache(maxsize=256)
def _sv_line(M):
    from tools.janus_astro import sommerfeld_nlo as N
    s0 = N.wino_s_nlo(M, v=1e-3, nlo=False, off_factor=math.sqrt(2))
    # LO line cross section (chi chi -> gamma gamma + gamma Z/2), the D1322 smoke-test formula with 1/M^2 kept general
    return 2*s0[1]**2*math.pi*N.ALPHA**2/M**2*0.389379e-27*2.99792458e10*(1 + N.ALPHA2*N.CW2/N.ALPHA)
HESS_1TEV = 2.3e-28   # cm^3/s at 1 TeV (kept for the 0.286 self-check)
# H.E.S.S. Inner Galaxy Survey 2026 line limits, γγ + ½γZ (arXiv:2608.07234, quoted in D1125); DEVIATIONS D1
HESS_LINE = {440.0: 9.8e-29, 1000.0: 2.3e-28, 2900.0: 6.5e-28}
HESS_SRC = 'H.E.S.S. Inner Galaxy Survey 2026, arXiv:2608.07234 (Einasto α 0.17, r_s 20 kpc, ρ☉ 0.39)'
R_NLL = (0.658, 0.794)   # NLL resummation band (D1124); the verdict uses 0.794 (conservative), 0.658 shown as the other edge
HALO_SHAPES = {'Einasto': ('einasto', (20.0, 0.17)), 'NFW': ('nfw', (20.0,)), 'Burkert': ('burkert', (3.37,))}  # Burkert r0 as in D1322 check
@functools.lru_cache(maxsize=64)
def _j_ann(halo, rho_sun):
    from tools.janus_astro import jfactor as Jm
    fn, args = HALO_SHAPES[halo]; rho = Jm.normalise(getattr(Jm, fn)(*args), rho_sun, 8.178)
    # quad's IntegrationWarnings here are harmless: route A vs route B agree to ≤ 0.65% and a finer grid changes
    # nothing (W2/V1, LOOP_STATE 04:56 CT); they come from the very strict epsrel = 1e-10. Silenced here only.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return Jm.J_route_B(rho, 8.178, psi_max_deg=3.0, b_mask_deg=0.0) - Jm.J_route_B(rho, 8.178, psi_max_deg=0.5, b_mask_deg=0.0)
def f_max(M, halo, rho_sun, limit=HESS_1TEV, R=0.794):
    """PREREG_W2_LINKS L1: the D1322 recipe, f_max = sqrt(limit / (sigma_v_line * R * J/J_bench))."""
    jr = _j_ann(halo, rho_sun)/_j_ann('Einasto', 0.39)
    return math.sqrt(limit/(_sv_line(round(M, 1))*R*jr)), jr
def galaxy(p):
    from tools.janus_astro.serapis_inputs import wino_fraction
    M = float(p['wino_mass_GeV']); j = {'J_GeV2_cm5': _jfactor(p['halo'], float(p['rho_sun']))}
    sv = _sv_line(round(M, 1)); f = wino_fraction(M/1000.0)
    pulls = {}; st = None; fm = fm_other = jr = lim_m = None
    check = abs(f_max(1000.0, 'Burkert', 0.40)[0] - 0.286)/0.286 <= 0.01        # L1 self-check against D1322
    lim_m = next((m0 for m0 in HESS_LINE if abs(M - m0) <= 0.05*m0), None)        # DEVIATIONS D1: three quoted masses, ±5%
    if lim_m and check:   # the fraction is a bracket (D1152): test both ends, never pick the kinder one
        fm, jr = f_max(M, p['halo'], float(p['rho_sun']), HESS_LINE[lim_m], R_NLL[1])
        fm_other = f_max(M, p['halo'], float(p['rho_sun']), HESS_LINE[lim_m], R_NLL[0])[0]
        pulls['f_pred high ≤ f_max'] = 'pass' if f[1] <= fm else 'FAIL'; pulls['f_pred low ≤ f_max'] = 'pass' if f[0] <= fm else 'FAIL'
        st = 'pass' if f[1] <= fm else ('tension' if f[0] <= fm else 'fail')
    if f[0] > 1.0:   # heavier than the thermal mass: a thermal wino would over-close the universe
        pulls['relic: fraction ≤ 1'] = 'FAIL'; st = 'fail'
    return L('galaxy', 'Galaxy & dark matter (gamma line)', 'C', 'Hyperion', dict(m=M, halo=p['halo'], rho_sun=p['rho_sun']),
             dict(J_IGS_ROI_GeV2_cm5=j['J_GeV2_cm5'], J_annulus_0p5_3deg_GeV2_cm5=_j_ann(p['halo'], float(p['rho_sun'])),
                  sigma_v_line_cm3_s=sv, thermal_fraction=f, f_max=fm, f_max_at_R_0p658=fm_other, limit_mass_GeV=lim_m,
                  limit_cm3_s=HESS_LINE.get(lim_m), J_over_bench=jr, recipe_selfcheck_0p286=check),
             [dict(name=f'H.E.S.S. line limit at {int(m0)} GeV', limit=v, kind='upper95', source=HESS_SRC) for m0, v in HESS_LINE.items()],
             pulls, ['two J values: J_IGS_ROI (H.E.S.S. IGS region, ψ ≤ 1°, |b| ≥ 0.3°) is for display; f_max uses the 0.5°–3° annulus (the D1322 recipe)',
                     'L1 (PREREG_W2_LINKS + DEVIATIONS D1): f_max = √(limit(M) / (σv × R × J/J_bench)), bench Einasto ρ☉ 0.39, annulus 0.5°–3°; self-check Burkert → 0.286',
                     'tested only at the three quoted limit masses (440 GeV, 1 TeV, 2.9 TeV, ±5%); between them: not tested (no interpolation)',
                     'verdict uses the conservative NLL edge R = 0.794; f_max at R = 0.658 is shown as the band\'s other edge (D1124)',
                     'LO Sommerfeld; NLO would raise f_max by about 10% (D1125)',
                     'the wino fraction bracket (D1152) is a SERAPIS-E thermal-history assumption, not data'],
             links=['J-factor region → Sky level (W2)'], status=st or 'open')

# ---------------- D. stars (Hyperion) ----------------
def stars(p):
    from tools.janus_astro import settings as H
    ns = H.neutron_star(p['eos'])
    return L('stars', 'Neutron stars', 'D', 'Hyperion', dict(eos=p['eos']), dict(M_max_Msun=ns['M_max_Msun']),
             [dict(name='heaviest pulsar', value=J0740[0], sigma=J0740[1], kind='lower', source=J0740[2])],
             {'M_max ≥ PSR J0740': 'pass' if ns['M_max_Msun'] >= J0740[0] - 2*J0740[1] else 'FAIL'},
             ['equation of state is standard nuclear physics, not a Weave prediction',
              'pass rule: M_max ≥ 2.08 − 2 × 0.07 = 1.94 M☉ (PSR J0740+6620)'])

# ---------------- E. sky (Mapper) ----------------
def sky(p):
    from tools.mapper import finder
    ra, dec, name = finder.resolve(p['target'])
    gc = dict(name='Galactic centre line region (annulus 0.5°–3°)', ra=266.4168, dec=-29.0078, inner_deg=0.5, outer_deg=3.0, from_level='galaxy')
    return L('sky', 'Sky (observing)', 'E', 'Mapper', dict(target=p['target'], aperture_mm=p['aperture_mm'], site=p['site']),
             dict(name=name, ra=ra, dec=dec, science_targets=[gc]), [], {}, ['finder chart and tonight plan served by the control panel (W3)',
             'L5: the Galaxy level\'s gamma-line region is passed here as a science target'],
             links=['Galactic-centre line region from the Galaxy level (W2)'], status='open')

# ---------------- B2. quarks: third thread τ_q (Q1–Q6, D1727–D1732) ----------------
EPS_FITS = {'A masses only': 0.03188+0.02151j, 'B +CKM (real g)': 0.01779+0.02926j, 'C +CKM (complex g_d)': 0.00318+0.02792j}  # arXiv:2212.13336
EPS_BAND = (0.028, 0.038)
LHCB_RMM = (0.035, 0.014, 0.012, 0.0280, 0.0016, 'LHCb Run1-3 R_mumu, arXiv:2611.00230 (D1726)')
def _tdec(m, MP=2.435e18):
    G = m**3/(4*math.pi*MP**2); g = 10.75 if (90/(math.pi**2*10.75))**.25*math.sqrt(G*MP) < 1 else 80
    return (90/(math.pi**2*g))**.25*math.sqrt(G*MP)
def quarks(p):
    m = int(p['sugra_m']); u = 0.0145/(m+0.0625)*cmath.exp(-2j*math.pi/9); eps = 1j*math.sqrt(3)*u     # 2201.02020 → 2212.13336 convention
    dist = {k: abs(eps-v)/abs(v) for k, v in EPS_FITS.items()}
    M, phi0, TR, Ns = float(p['tauq_mass_GeV']), float(p['tauq_phi0']), 1.34e9, 55.0
    Td = _tdec(M); D = max(1.0, TR*phi0**2/6/Td); dns = abs(2*(-math.log(D)/3)/Ns**2)
    r, up, dn, sm, se, src = LHCB_RMM; pull = (r-sm)/math.hypot(up if sm > r else dn, se)
    pulls = {'ε in quark-fit band (Q6)': 'pass' if EPS_BAND[0] <= abs(eps) <= EPS_BAND[1] else 'FAIL',
             'τ_q moduli window (Q4)': 'pass' if (Td >= 5e-3 and D <= 1e3 and dns <= 0.003) else 'FAIL',
             'LHCb R_μμ vs Weave(=SM)': round(pull, 2)}
    return L('quarks', 'Quarks (third thread τ_q)', 'B', 'theory/quarks',
             dict(sugra_m=m, tauq_mass_GeV=M, tauq_phi0=phi0),
             dict(eps_re=eps.real, eps_im=eps.imag, eps_abs=abs(eps), eps_arg_deg=math.degrees(cmath.phase(eps)),
                  nearest_fit=min(dist, key=dist.get), nearest_rel_dist=min(dist.values()),
                  T_dec_GeV=Td, dilution_D=D, dns=dns, theta_bar=0.0),
             [dict(name=k, re=v.real, im=v.imag, source='arXiv:2212.13336') for k, v in EPS_FITS.items()] +
             [dict(name='ε band', limit=list(EPS_BAND), source='arXiv:2212.13336'), dict(name='R_μμ', value=r, sm=sm, source=src)],
             pulls,
             ['HOSTED, NOT PREDICTED: quark sector is an imported mechanism (D1732)',
              'θ̄ = 0 from anomaly-free weights (FST, arXiv:2406.01689) — structure, A',
              'ε from SUGRA (m,0) minimum, arXiv:2201.02020 — zero-parameter test FAILS for every m (Q6)',
              'τ_q must be heavy ≳ 2e10 GeV (Q4, c=1, factor ~2)',
              'B→μμ: Weave adds nothing; SM default (consistent, not evidence)'],
             links=['τ_q decay → dilution D → ΔN* = −⅓ ln D (Inflation level)', 'τ_q ≠ thread (thread rests at i)'])

LEVELS = (inflation, flavour, quarks, bbn, late, colliders, galaxy, stars, sky)

def run(params=None):
    p = dict(DEFAULTS); p.update(params or {})
    levels = []
    for fn in LEVELS:
        try: levels.append(fn(p))
        except Exception as e:
            lv = L(fn.__name__, fn.__name__, '?', '?', {}, {}, [], {}, [f'ERROR: {e}'], status='open'); lv['error'] = repr(e); levels.append(lv)
    card = {}
    for lv in levels: card.setdefault(lv['category'], []).append((lv['id'], lv['status']))
    return dict(params=p, levels=levels, scorecard=card)

if __name__ == '__main__':
    import json; r = run(); print(json.dumps({l['id']: [l['status'], l['outputs']] for l in r['levels']}, indent=1, default=str))

# ---------------- knobs (W3): what the control panel may change, per level ----------------
def knobs():
    from tools.janus_calc import settings as J
    from tools.lhc import settings as C
    from tools.janus_astro import settings as H
    return {
        'inflation': [dict(key='inflation_model', label='Model', type='select', options=list(J.MODELS)),
                      dict(key='Nstar', label='N* (ignored for serapis_*)', type='number', min=40, max=70, step=1, unit='e-folds')],
        'flavour':   [],
        'quarks':    [dict(key='sugra_m', label='SUGRA class m (W ∝ (j−1728)^{m/2})', type='number', min=1, max=7, step=1, unit=''),
                      dict(key='tauq_mass_GeV', label='τ_q mass', type='number', min=1e4, max=5e12, step=1e9, unit='GeV'),
                      dict(key='tauq_phi0', label='τ_q displacement φ₀', type='number', min=0.1, max=1.0, step=0.1, unit='M_P')],
        'bbn':       [dict(key='omega_b', label='ω_b', type='number', min=0.020, max=0.025, step=0.0001, unit=''),
                      dict(key='dark_sector', label='Dark sector (sets ΔN_eff)', type='select', options=list(DARK_SECTORS))],
        'late':      [dict(key='b_A', label='Arthur coupling b_A', type='number', min=-0.3, max=0.1, step=0.001, unit=''),
                      dict(key='dphi', label='Δφ since z*', type='number', min=0.1, max=2.0, step=0.01, unit='M_P')],
        'colliders': [dict(key='wino_mass_GeV', label='Wino mass', type='number', min=100, max=3000, step=10, unit='GeV'),
                      dict(key='run', label='Collider run', type='select', options=list(C.RUNS))],
        'galaxy':    [dict(key='wino_mass_GeV', label='Wino mass', type='number', min=100, max=3000, step=10, unit='GeV'),
                      dict(key='halo', label='Halo profile', type='select', options=list(HALO_SHAPES)),
                      dict(key='rho_sun', label='Local DM density ρ☉', type='number', min=0.2, max=0.6, step=0.01, unit='GeV/cm³')],
        'stars':     [dict(key='eos', label='Equation of state', type='select', options=list(H.EOS))],
        'sky':       [dict(key='target', label='Target', type='text'),
                      dict(key='aperture_mm', label='Aperture', type='number', min=50, max=1000, step=10, unit='mm')],
    }
