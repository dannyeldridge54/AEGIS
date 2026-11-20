# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Weave Control engine (W1, 20 Nov 2026): ONE parameter set drives every AEGIS toolkit, level by level.
run(params) -> {'params', 'levels': [level, ...], 'scorecard'}. Each level:
  {id, name, category (A inflation/loom, B flavour, C dark sector & late universe, D matter genesis & stars, E observing),
   tool, inputs, outputs, data: [{name, value, sigma | limit, kind, source}], pulls {name: sigma | 'pass'/'FAIL'},
   status: pass | tension | fail | open, labels: notes on what is predicted (P), fitted (F) or an open gap (G), links}
Rules: every number is computed by a validated toolkit function, or is a measurement carrying its source.
Status: pass if every |pull| < 2 and every limit passes; tension if a |pull| is 2–3; fail if any |pull| ≥ 3 or a limit fails."""
import functools, math

DEFAULTS = dict(
    inflation_model='serapis_10d', Nstar=55.0,                      # Janus (N* ignored for the full SERAPIS models)
    omega_b=0.02237, dark_sector='brane_split',                    # Hyperion BBN; dark sector sets ΔN_eff (link)
    b_A=0.0, Omega_phi=0.70, Omega_c=0.25, dphi=0.64,               # late universe (D1717 closed form)
    wino_mass_GeV=1000.0, run='run3',                               # CERN+1
    halo='Einasto', rho_sun=0.4,                                    # Hyperion galaxy
    eos='SLy',                                                      # Hyperion stars
    target='M31', aperture_mm=80.0, site='okc')                     # Mapper
# ΔN_eff carried by each dark-sector branch (register C3/C5): mirror world at its BBN bound; minimal dark sector cold.
# Each value from the D-notes (V1 finding 1): the label says which note and whether it is an estimate or a bound.
DARK_SECTORS = {'none': (0.0, 'no dark radiation'),
                'brane_split': (0.0, 'P-brane (C5, D1671): visible on D3, dark on unfluxed D7; the inflaton heats our side only, ΔN_eff ≈ 0 (must be ≤ 0.086, C5)'),
                'minimal_equal_sharing': (0.21, 'minimal dark sector (5 GeV baryon + dark photon) with equal sharing per particle: ΔN_eff = 0.21 (D1646, estimate)'),
                'mirror_at_bound': (0.3, 'mirror sector at its viability bound ΔN_eff = 0.3 (D1648)'),
                'mirror_full_equal': (7.4, 'full mirror world with equal sharing: ΔN_eff = 7.4 (D1646) — RULED OUT')}
LEPTONS_MeV = dict(e=(0.51099895000, 1.5e-10), mu=(105.6583755, 2.3e-6), tau=(1776.93, 0.09))   # PDG 2024
J0740 = (2.08, 0.07, 'PSR J0740+6620 mass (Fonseca et al. 2021, ApJL 915 L12)')
ATLAS_DT = (670.0, 'ATLAS disappearing track, observed 95% wino limit (arXiv:2603.08315; D1722)')
# L3 (PREREG_W2_LINKS): S8 = sigma8 sqrt(Omega_m/0.3) from the locked D1725 best fits (PC results/cls_*.json, read 20 Nov 04:55 CT)
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
    return L('flavour', 'Flavour (leptons)', 'B', 'Flavour panel (new)', dict(masses='PDG 2024 pole masses'),
             dict(Koide_Q=Q, Koide_Q_sigma=abs(dQ), Brannen_delta=best, delta_minus_2_9=best - 2/9, delta_equivalent_forms=sorted(forms)), data, pulls,
             ['Q = 2/3 is a prediction (P-F1)', 'δ = 2/9 has no mechanism yet (C-δ)',
              'δ is defined only up to relabelling the leptons and δ → 2π/3 − δ; the form nearest 2/9 is shown and all forms are listed (V1 finding 5)'],
             links=['TM1 δ_CP band 262°–286° (W4)'])

# ---------------- D. BBN (Hyperion), fed by the dark sector ----------------
def bbn(p):
    from tools.janus_astro import settings as H
    dN, why = DARK_SECTORS[p['dark_sector']]
    b = H.bbn(p['omega_b'], dN)
    data = [dict(name=f'{q}:{k}', value=v[0], sigma=v[1], kind='gauss', source=v[2]) for q in ('Yp', 'DH') for k, v in H.DATA[q].items()]
    return L('bbn', 'Big Bang nucleosynthesis', 'D', 'Hyperion', dict(omega_b=p['omega_b'], dNeff=dN, dNeff_from=why, code=b['code']),
             dict(Yp=b['Yp'], DH=b['DH']), data, b['pulls'], ['lithium problem reproduced, not solved (D1640)',
             'pulls use the OBSERVATIONAL σ only: the nuclear-rate theory error (a few % on D/H) is not yet included, so the D/H tension is overstated (referee R2; fix in W5 rate Monte Carlo)'],
             links=[f"ΔN_eff = {dN} from dark sector '{p['dark_sector']}'",
                    'L4: reheating (T_rh ≈ 9 × 10⁸ GeV, N*) has no direct BBN effect; ΔN_eff is the only BBN link'])

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
                     'L3: S₈ of each locked fit vs KiDS-Legacy and CMB lensing, reported separately (not combined)',
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
HESS_1TEV = 2.3e-28   # cm^3/s, the H.E.S.S. IGS line limit at 1 TeV used by D1322 (with the 0.794 factor and J/J_bench)
HALO_SHAPES = {'Einasto': ('einasto', (20.0, 0.17)), 'NFW': ('nfw', (20.0,)), 'Burkert': ('burkert', (3.37,))}  # Burkert r0 as in D1322 check
@functools.lru_cache(maxsize=64)
def _j_ann(halo, rho_sun):
    from tools.janus_astro import jfactor as Jm
    fn, args = HALO_SHAPES[halo]; rho = Jm.normalise(getattr(Jm, fn)(*args), rho_sun, 8.178)
    return Jm.J_route_B(rho, 8.178, psi_max_deg=3.0, b_mask_deg=0.0) - Jm.J_route_B(rho, 8.178, psi_max_deg=0.5, b_mask_deg=0.0)
def f_max(M, halo, rho_sun):
    """PREREG_W2_LINKS L1: the D1322 recipe, f_max = sqrt(2.3e-28 / (sigma_v_line * 0.794 * J/J_bench))."""
    jr = _j_ann(halo, rho_sun)/_j_ann('Einasto', 0.39)
    return math.sqrt(HESS_1TEV/(_sv_line(round(M, 1))*0.794*jr)), jr
def galaxy(p):
    from tools.janus_astro.serapis_inputs import wino_fraction
    M = float(p['wino_mass_GeV']); j = {'J_GeV2_cm5': _jfactor(p['halo'], float(p['rho_sun']))}
    sv = _sv_line(round(M, 1)); f = wino_fraction(M/1000.0)
    pulls = {}; st = None; fm = jr = None
    check = abs(f_max(1000.0, 'Burkert', 0.40)[0] - 0.286)/0.286 <= 0.01        # L1 self-check against D1322
    if abs(M - 1000.0) <= 50 and check:   # the fraction is a bracket (D1152): test both ends, never pick the kinder one
        fm, jr = f_max(M, p['halo'], float(p['rho_sun']))
        pulls['f_pred high ≤ f_max'] = 'pass' if f[1] <= fm else 'FAIL'; pulls['f_pred low ≤ f_max'] = 'pass' if f[0] <= fm else 'FAIL'
        st = 'pass' if f[1] <= fm else ('tension' if f[0] <= fm else 'fail')
    return L('galaxy', 'Galaxy & dark matter (gamma line)', 'C', 'Hyperion', dict(m=M, halo=p['halo'], rho_sun=p['rho_sun']),
             dict(J_GeV2_cm5=j['J_GeV2_cm5'], sigma_v_line_cm3_s=sv, thermal_fraction=f, f_max=fm, J_over_bench=jr, recipe_selfcheck_0p286=check),
             [dict(name='H.E.S.S. inner Galaxy line limit', source='used at 1 TeV in D1322 (2.3e-28 cm³/s, Einasto); full mass curve not yet stored')],
             pulls, ['L1 (PREREG_W2_LINKS): f_max = √(2.3e-28 / (σv × 0.794 × J/J_bench)), bench Einasto ρ☉ 0.39, annulus 0.5°–3°; self-check Burkert → 0.286',
                     'LO Sommerfeld (no NLO, no endpoint); limit curve vs mass is map item 2 (open)',
                     'the only stored limit is at 1 TeV (Einasto); away from 1 TeV no pass/fail is given (V1 finding 6)'],
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

LEVELS = (inflation, flavour, bbn, late, colliders, galaxy, stars, sky)

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
