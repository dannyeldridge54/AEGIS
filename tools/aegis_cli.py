# AEGIS-FP ONOHRDBYMCLONMKW · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""AEGIS toolkits — one command-line program (also built as a standalone executable).

Usage (from the repo root:  python -m tools.aegis_cli <command> ...,  or the executable:  aegis <command> ...)
  menu                              interactive menu (default when started with no command, e.g. by double-click)
  test                              run the release smoke test (9 checks against published values)
  cern xsec <mass_GeV> [sqrt_s_TeV] wino pair cross sections (fb), default 13.6 TeV
  cern life <mass_GeV>              chargino-neutralino mass splitting, lifetime, decay length
  cern limit [ATLAS_136|ATLAS_36]   disappearing-track recast limit with theory band
  cern higgsino <mass_GeV> [TeV]    higgsino pair cross sections (fb), 100-1500 GeV
  cern future                       HL-LHC / HE-LHC / FCC-hh wino reach
  lattice <command> [args]          Lattice Lab (e.g. lattice hexagons E8, lattice energy E6 1.25)
  string kk|stable [D=..] [gamma=..] [fd]  10D/6D string vacua: scalar KK masses (10D critical, D1214), stability (D1140)
  string modint [T=2i] [U=i]                 DKL threshold over F: numeric vs closed form (string-calc S5a)
  janus "<V(phi)>" [N*]             inflation observables n_s, r, alpha_s for any potential, e.g. janus "0.5*phi**2" 60
  hyperion bbn <omega_b h^2> [dNeff]   primordial helium Y_p and D/H (PRIMAT 2021 tables; needs camb)
  hyperion orbit <ra> <dec> <dist_pc> <pmra> <pmdec> <rv> [McMillan17|MWPotential2014]
                                    3 Gyr Milky Way orbit of one star: r_peri, r_apo, z_max, eccentricity
  late dist <z> [H0 ombh2 omch2 w0 wa mnu]   comoving / angular / Hubble distances and H(z) (default Planck 2018)
  late desi [w0 wa H0 ombh2 omch2 rd]       chi-square of a w0-wa cosmology against DESI DR2 BAO (13 points)
  late growth <z> [H0 ombh2 omch2 w0 wa]    linear growth D(z)/D(0) and growth rate f(z)
  serapis predict <C>               SERAPIS-E n_s, r, alpha_s at BHK tilt C (fast emulator, valid 1.0-1.6e-6)
  serapis meter <n_s> [sigma]       inverse meter: the C and Im S*Im rho a measured n_s implies (postulate PW6)
  serapis j <x> <y>                 Klein j-invariant at tau = x + iy (j(i) = 1728)
  serapis eisenstein <x> <y> [s]    non-holomorphic Eisenstein series E(tau, s), two independent methods
  serapis test                      SERAPIS calculator self-test (independent cross-checks)
  wavelength line <ion> <n_low> <n_up>   hydrogen-like line, vacuum and air wavelength (H, He+, Li2+)
  wavelength convert <value> <unit>      nm / um / m / Hz / MHz / GHz / eV -> wavelength, frequency, energy, band, colour
  wavelength 21cm                        hydrogen hyperfine line (Fermi formula with (1 + a_e); 5.6e-5 of the measured value)
  power solar [Iph I0 n Rs Rsh cells]    solar-panel I-V: Voc, Isc, max power, fill factor (single-diode model)
  power rc <f_Hz> <R_ohm> <C_F>          RC low-pass gain, phase and corner frequency (also: power rl <f> <R> <L_H>)
  sound tone <Hz> <seconds> <file.wav> [sine|triangle|square|saw]   write a tone as a WAV file
  aion <new|lock|deviate|check> ...    pre-registration kit: write a lock, hash it, record deviations, audit a repo
  tracker [--out DIR]               SERAPIS prediction tracker: every frozen prediction vs the latest data
  scorecard --ns <n_s> [--r <r>] [--alpha-s <a>] [--label <name>]
                                    score an inflation model against every current CMB/LSS constraint (Inflation Scorecard)
  license                           show license terms

AEGIS Community License: free for individuals, scientists, students, schools, nonprofits and public research.
Any business or for-profit use needs the AEGIS Commercial License. CERN+1 is not affiliated with or endorsed by CERN.
"""
import sys, os, json
VERSION = '2026.11.18'

def _root():
    base = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base not in sys.path: sys.path.insert(0, base)
    return base

def _show(x): print(json.dumps(x, indent=1, default=lambda o: float(o) if hasattr(o, '__float__') else str(o)))

def cern(args):
    from tools.lhc import xsec, lifetime, theory_band, future
    if not args: print(__doc__); return
    c = args[0]
    if c == 'xsec':
        m = float(args[1]); rs = float(args[2]) if len(args) > 2 else 13.6
        out = {p: xsec.sigma_best(m, p, rs) for p in ('C1N2p', 'C1N2m', 'C1C1')}
        out['total_fb'] = sum(v['sigma_fb'] for v in out.values()); out['mass_GeV'] = m; out['sqrt_s_TeV'] = rs
        out['note'] = 'interpolation/scaling error ~1%; add the Resummino PDF+scale uncertainty (5-15%)'; _show(out)
    elif c == 'life':
        m = float(args[1]); w = lifetime.widths(m); w['dm_MeV'] = 1e3*lifetime.dm(m); _show(w)
    elif c == 'limit':
        _show(theory_band.band(args[1] if len(args) > 1 else 'ATLAS_136'))
    elif c == 'higgsino':
        from tools.lhc import higgsino as H
        m = float(args[1]); rs = args[2] if len(args) > 2 else '13.6'
        if rs in ('13', '13.6'): out = {p: H.sigma(m, p, rs) for p in H.PROCS}
        else: out = {p: H.sigma_scaling(m, p, float(rs)) for p in H.PROCS}
        out.update(total_fb=sum(out.values()), mass_GeV=m, sqrt_s_TeV=float(rs), note='Resummino aNNLO+NNLL tables (2304.11915 Tab. 4); other energies by Drell-Yan scaling'); _show(out)
    elif c == 'future':
        _show(future.table())
    else: print(__doc__)

def janus(args):
    from tools.janus_calc import anyV, core
    if not args: print(__doc__); return
    N = float(args[1]) if len(args) > 1 else 55.0
    if not 1 <= N <= 200: raise ValueError('N* (e-folds) should be between 1 and 200; 50-60 is usual')
    try: model = anyV.from_formula(args[0])
    except Exception as e:
        if 'does not end' in str(e): raise ValueError(f'with V = {args[0]} inflation never ends (slow roll is never violated), so N* = {N:g} has no meaning. Try a potential that steepens, e.g. "0.5*phi**2"')
        raise ValueError(f'could not read the potential "{args[0]}". Write it in phi with * and **, e.g. "0.5*phi**2" or "1-exp(-sqrt(2/3)*phi)"')
    try: s = core.spectra3(model, N)
    except Exception as e:
        if 'does not end' in str(e): raise ValueError(f'with V = {args[0]} inflation never ends (slow roll is never violated), so N* = {N:g} has no meaning. Try a potential that steepens, e.g. "0.5*phi**2"')
        raise
    _show({'V': args[0], 'N_star': N, **{k: v for k, v in s.items() if k in ('ns', 'r', 'alpha_s', 'beta_s')}})

def hyperion(args):
    if not args: print(__doc__); return
    if args[0] == 'bbn':
        try: from tools.janus_astro import bbn
        except ImportError: print('hyperion bbn needs the camb package:  pip install camb'); return
        ob = float(args[1]); dN = float(args[2]) if len(args) > 2 else 0.0
        if not 0.005 < ob < 0.05: raise ValueError('omega_b h^2 should be between 0.005 and 0.05 (Planck: 0.0224)')
        _show({'omega_b_h2': ob, 'dNeff': dN, 'Y_p_nucleon': bbn.Yp(ob, dN), 'Y_p_mass': bbn.Yp_mass(ob, dN), 'D/H': bbn.DH(ob, dN),
               'note': 'PRIMAT 2021 tables via CAMB; Y_p_nucleon = 4 n_He/n_b, Y_p_mass = helium mass fraction'})
    elif args[0] == 'orbit':
        import numpy as np
        from tools.janus_astro import mapper_feed as F, mapper_orbits as MO
        if len(args) < 7: raise ValueError('orbit needs 6 numbers: ra dec dist_pc pmra pmdec rv   e.g. aegis hyperion orbit 269.452 4.6934 1.8266 -802.8 10362.4 -110.5')
        ra, dec, d_pc, pmra, pmdec, rv = (float(a) for a in args[1:7]); model = args[7] if len(args) > 7 else MO.DEFAULT_MODEL
        if model not in MO.MODELS: raise ValueError('model must be McMillan17 or MWPotential2014')
        if not 0 < d_pc < 2e5: raise ValueError('distance must be in parsecs, 0 to 200000')
        if not 0 <= ra <= 360: raise ValueError('ra must be in degrees, 0 to 360')
        if not -90 <= dec <= 90: raise ValueError('dec must be in degrees, -90 to 90')
        if abs(rv) > 1500 or max(abs(pmra), abs(pmdec)) > 2e4: raise ValueError('rv (km/s) or proper motion (mas/yr) looks wrong: |rv| < 1500, |pm| < 20000')
        M = MO.MODELS[model]; A = lambda x: np.array([x])
        l, b = F.icrs_to_galactic(A(ra), A(dec))
        p, v = F.galactocentric(A(ra), A(dec), A(d_pc/1000.0), A(pmra), A(pmdec), A(rv), r0_xy=M['r0'], v_sun=M['v_sun'])
        if model == 'MWPotential2014':
            from tools.janus_astro import fast; o = fast.orbits_fast(*p, *v)
        else:
            try: o = F.orbit_params_galpy(*p, *v, pot=model)
            except ImportError: print('McMillan17 orbits need galpy:  pip install galpy astropy   (or add MWPotential2014)'); return
        _show({'model': model, 'l_deg': float(l[0]), 'b_deg': float(b[0]), 'xyz_kpc': [float(q[0]) for q in p], 'v_kms': [float(q[0]) for q in v],
               'r_peri_kpc': float(o['rperi'][0]), 'r_apo_kpc': float(o['rapo'][0]), 'z_max_kpc': float(o['zmax'][0]), 'eccentricity': float(o['ecc'][0])})
    else: print(__doc__)

def scorecard(args):
    p = os.path.join(_root(), 'tools', 'scorecard')
    if os.path.isdir(p) and p not in sys.path: sys.path.insert(0, p)
    try: from inflation_scorecard.cli import scorecard_main
    except ImportError as e: print(f'The Inflation Scorecard needs pyyaml:  pip install pyyaml   ({e})'); return
    if not args: args = ['--help']
    scorecard_main(args)

LATE_DEF = dict(H0=67.66, ombh2=0.02242, omch2=0.11933, w0=-1.0, wa=0.0, mnu=0.06)
def _late_cosmo(vals, keys):
    from tools.janus_lt.background import Cosmo
    p = dict(LATE_DEF); p.update({k: float(v) for k, v in zip(keys, vals)})
    if not 20 < p['H0'] < 120: raise ValueError('H0 should be in km/s/Mpc, 20 to 120')
    if not (0 < p['ombh2'] < 0.1 and 0 < p['omch2'] < 0.5): raise ValueError('ombh2 and omch2 are physical densities (Planck: 0.0224 and 0.120)')
    return Cosmo(p['H0'], p['ombh2'], p['omch2'], w0=p['w0'], wa=p['wa'], mnu=p['mnu'], Neff=3.046), p

def late(args):
    if not args or args[0] not in ('dist', 'desi', 'growth'): print(__doc__); return
    c = args[0]
    if c == 'dist':
        if len(args) < 2: raise ValueError('dist needs a redshift, e.g. aegis late dist 1.0')
        z = float(args[1]);
        if not 0 <= z <= 1e4: raise ValueError('redshift must be between 0 and 10000')
        C, p = _late_cosmo(args[2:], ['H0', 'ombh2', 'omch2', 'w0', 'wa', 'mnu'])
        DM = C.DM(z); DH = C.DH(z) if z > 0 else C.DH(0)
        _show({'z': z, 'params': p, 'D_M_comoving_Mpc': DM, 'D_A_angular_Mpc': DM/(1 + z), 'D_L_luminosity_Mpc': DM*(1 + z), 'D_H_Mpc': DH, 'H_z_kms_Mpc': C.H(z),
               'note': 'flat FLRW, photons + 3.046 neutrino species (one massive), CPL dark energy w0 + wa(1-a); agrees with astropy Planck18 to 3e-5'})
    elif c == 'desi':
        from tools.janus_lt import desi
        vals = args[1:]; rd = float(vals[5]) if len(vals) > 5 else 147.09
        C, p = _late_cosmo(vals[:5], ['w0', 'wa', 'H0', 'ombh2', 'omch2'])
        rows = desi.load(); x2 = desi.chi2(C, rd, rows); n = sum(1 if r[5] != r[5] else 2 for r in rows)
        _show({'params': p, 'r_d_Mpc': rd, 'chi2': x2, 'n_points': n, 'data': 'DESI DR2 BAO, arXiv:2503.14738 Table IV',
               'note': 'r_d fixed (default Planck 2018: 147.09 Mpc); no fitting is done here'})
    else:
        if len(args) < 2: raise ValueError('growth needs a redshift, e.g. aegis late growth 0.5')
        from tools.janus_lt.growth import growth
        z = float(args[1]); C, p = _late_cosmo(args[2:], ['H0', 'ombh2', 'omch2', 'w0', 'wa'])
        D, f = growth(C, [z])[z]
        _show({'z': z, 'params': p, 'D_over_D0': float(D), 'growth_rate_f': float(f), 'note': 'scale-independent linear growth (no neutrino free-streaming)'})

def serapis(args):
    if not args: print(__doc__); return
    c = args[0]
    if c == 'predict':
        from tools.serapis_calc import emulator as E
        if len(args) < 2: raise ValueError('predict needs C, e.g. aegis serapis predict 1.15e-6')
        C = float(args[1])
        if not 1.0e-6 <= C <= 1.6e-6: raise ValueError('the emulator is valid for C between 1.0e-6 and 1.6e-6 (the frozen band)')
        out = E.emulate(C); out['label'] = 'SERAPIS-E model prediction (frozen band D693; scored only on future data)'; _show(out)
    elif c == 'meter':
        from tools.serapis_calc import meter as M
        if len(args) < 2: raise ValueError('meter needs n_s, e.g. aegis serapis meter 0.9728 0.0027')
        ns = float(args[1]); sig = float(args[2]) if len(args) > 2 else None
        if not 0.95 < ns < 0.99: raise ValueError('n_s should be between 0.95 and 0.99')
        _show(M.meter(ns, sig))
    elif c == 'j':
        from tools.serapis_calc import modular as J
        x, y = float(args[1]), float(args[2])
        if y <= 0: raise ValueError('tau must be in the upper half-plane (y > 0)')
        v = complex(J.j(complex(x, y))); _show({'tau': [x, y], 'j_real': v.real, 'j_imag': v.imag})
    elif c == 'eisenstein':
        from tools.serapis_calc import eisenstein as EI
        x, y = float(args[1]), float(args[2]); s_ = float(args[3]) if len(args) > 3 else 2.0
        if y <= 0: raise ValueError('tau must be in the upper half-plane (y > 0)')
        a, b = float(EI.E_fourier(x, y, s_)), float(EI.E_lattice(x, y, s_))
        _show({'tau': [x, y], 's': s_, 'E_fourier': a, 'E_lattice_sum': b, 'agreement': abs(a/b - 1)})
    elif c == 'test':
        import runpy
        try: runpy.run_module('tools.serapis_calc.selftest', run_name='__main__')
        except SystemExit: pass
    else: print(__doc__)

UNITS = {'nm': ('lam_m', 1e-9), 'um': ('lam_m', 1e-6), 'mm': ('lam_m', 1e-3), 'cm': ('lam_m', 1e-2), 'm': ('lam_m', 1.0),
         'hz': ('nu_hz', 1.0), 'khz': ('nu_hz', 1e3), 'mhz': ('nu_hz', 1e6), 'ghz': ('nu_hz', 1e9), 'thz': ('nu_hz', 1e12), 'ev': ('E_eV', 1.0), 'kev': ('E_eV', 1e3)}
def wavelength(args):
    from tools.chem import wavelength as W
    if not args: print(__doc__); return
    c = args[0]
    if c == 'line':
        ion = args[1] if len(args) > 1 else 'H'
        if ion not in W.ZOF: raise ValueError('ion must be H, He+ or Li2+')
        lo, up = int(args[2]) if len(args) > 2 else 2, int(args[3]) if len(args) > 3 else 3
        if not 1 <= lo < up: raise ValueError('need 1 <= n_low < n_up, e.g. aegis wavelength line H 2 3 (H-alpha)')
        lv = W.line(ion, lo, up); _show({'ion': ion, 'n_low': lo, 'n_up': up, 'series': W.SERIES.get(lo, ''), 'vacuum_nm': lv,
              'air_nm': W.air(lv) if lv > 200 else None, **{k: v for k, v in W.convert(lam_m=lv*1e-9).items() if k != 'lam_m'},
              'note': 'Bohr levels with reduced mass; fine structure ~1e-5 not included'})
    elif c == 'convert':
        if len(args) < 3 or args[2].lower() not in UNITS: raise ValueError('give a value and a unit: nm, um, mm, cm, m, Hz, kHz, MHz, GHz, THz, eV, keV')
        k, f = UNITS[args[2].lower()]; v = float(args[1])
        if v <= 0: raise ValueError('value must be positive')
        _show(W.convert(**{k: v*f}))
    elif c == '21cm':
        v = W.hydrogen_21cm(); _show({'nu_MHz': v/1e6, 'lam_cm': 2.99792458e10/v, 'measured_MHz': 1420.405751768, 'relative_difference': v/1420405751.768 - 1,
              'note': 'Fermi formula, reduced mass, (1 + a_e); missing Breit/QED/recoil/proton-structure terms (CH1b)'})
    else: print(__doc__)

def power(args):
    from tools.power import circuits as P
    if not args: print(__doc__); return
    c = args[0]
    if c == 'solar':
        keys = ['Iph', 'I0', 'n', 'Rs', 'Rsh', 'cells']; kw = {k: (int(v) if k == 'cells' else float(v)) for k, v in zip(keys, args[1:])}
        r = P.solar_iv(**kw); _show({k: v for k, v in r.items() if not hasattr(v, '__len__')})
    elif c in ('rc', 'rl'):
        if len(args) < 4: raise ValueError(f'{c} needs f R {"C" if c == "rc" else "L"}, e.g. aegis power {c} 1000 1000 {"1e-6" if c == "rc" else "0.1"}')
        f, R, X = (float(a) for a in args[1:4])
        if min(f, R, X) <= 0: raise ValueError('frequency, resistance and C/L must be positive')
        _show((P.rc_lowpass if c == 'rc' else P.rl_lowpass)(f, R, X))
    else: print(__doc__)

def sound(args):
    from tools.sound import engine as S
    if len(args) < 4 or args[0] != 'tone': raise ValueError('usage: aegis sound tone <Hz> <seconds> <file.wav> [sine|triangle|square|saw]')
    hz, dur = float(args[1]), float(args[2]); kind = args[4] if len(args) > 4 else 'sine'
    if not (20 <= hz <= 20000 and 0 < dur <= 600): raise ValueError('frequency 20-20000 Hz, duration up to 600 s')
    _show(S.write_wav(args[3], S.note(hz, dur, kind=kind)))

def aion(args):
    p = os.path.join(_root(), 'tools', 'aion')
    if os.path.isdir(p) and p not in sys.path: sys.path.insert(0, p)
    from aion.cli import main as amain
    sys.argv = ['aion'] + (args or ['--help']); r = amain()
    if r: sys.exit(r)

def tracker(args):
    import runpy
    sp = os.path.join(_root(), 'tools', 'scorecard')
    if os.path.isdir(sp) and sp not in sys.path: sys.path.insert(0, sp)
    sys.argv = ['track.py'] + args
    runpy.run_path(os.path.join(_root(), 'tools', 'tracker', 'track.py'), run_name='__main__')

def lattice(args):
    from tools.lattice import lattice_lab
    lattice_lab.main(args)

def string(args):
    """string kk [D=10] [gamma=1.5] [fd]   — scalar KK masses on a BTR vacuum (10D critical by default; validated D1214)
       string stable [D=6] [gamma=2]       — scalar stability of a subcritical vacuum (D1140)"""
    sub = args[0] if args else 'kk'; kv = dict(a.split('=', 1) for a in args[1:] if '=' in a)
    if sub == 'stable':
        import sympy as sp
        from tools.kaluza.background import vacuum
        from tools.kaluza.stability import scalar_condition
        r = scalar_condition(vacuum(int(kv.get('D', 6)), sp.nsimplify(kv.get('gamma', '2'))))
        print(f"{int(kv.get('D', 6))}D vacuum, γ = {kv.get('gamma', '2')}: scalar condition min {r['min']:.6f} vs threshold {r['threshold']} → {'STABLE' if r['stable'] else 'UNSTABLE'}")
        return
    if sub == 'modint':
        from tools.serapis_calc.modint import dkl, dkl_closed
        T = complex(kv.get('T', '2j').replace('i', 'j')); U = complex(kv.get('U', '1j').replace('i', 'j'))
        n, c = dkl(T, U, n1q=24, n2q=80), dkl_closed(T, U)
        print(f"DKL threshold at T = {T}, U = {U}: numeric {n:.8f}, closed form {c:.8f}, |diff| {abs(n - c):.1e}"); return
    if sub != 'kk': print(string.__doc__); return
    from tools.kaluza.scalar import kk_scalar
    r = kk_scalar(int(kv.get('D', 10)), float(kv.get('gamma', 1.5)), method='fd' if 'fd' in args else 'pruefer')
    print(f"{r['D']}D {r['kind']} vacuum (γ = {r['gamma']:g}), {r['method']}: m² = {', '.join(f'{v:.7f}' for v in r['m2'])}")
    print(f"  interval L = {r['L']:.6f}; m L/π = {', '.join(f'{v:.5f}' for v in r['mL_over_pi'])}; ratio m₂²/m₁² = {r['ratio']:.5f}")
    print('  note: S4e convention — open −4% gap vs BTR 2209.10553 (D1141/D1214)')

def test(args):
    import runpy
    try: runpy.run_path(os.path.join(_root(), 'tools', 'release_smoketest.py'), run_name='__main__')
    except SystemExit as e:
        if args == ['--exit']: raise

def license_(args):
    p = os.path.join(_root(), 'LICENSE'); print(open(p, encoding='utf-8').read() if os.path.exists(p) else __doc__)

def menu(args):
    items = [('Run the self-test', lambda: test([])),
             ('CERN+1: wino cross sections at a mass', lambda: cern(['xsec', input('  mass in GeV: '), input('  energy in TeV [13.6]: ') or '13.6'])),
             ('CERN+1: higgsino cross sections at a mass', lambda: cern(['higgsino', input('  mass in GeV (100-1500): '), input('  energy in TeV [13.6]: ') or '13.6'])),
             ('CERN+1: chargino lifetime at a mass', lambda: cern(['life', input('  mass in GeV: ')])),
             ('CERN+1: ATLAS disappearing-track limit with theory band', lambda: cern(['limit', input('  ATLAS_136 or ATLAS_36 [ATLAS_136]: ') or 'ATLAS_136'])),
             ('CERN+1: future-collider reach', lambda: cern(['future'])),
             ('Lattice Lab: hexagonal planes in a lattice', lambda: lattice(['hexagons', input('  lattice (D4, E6, E7, E8, BW16, Leech): ')])),
             ('Lattice Lab: energy of a lattice', lambda: lattice(['energy', input('  lattice (e.g. E6): '), input('  alpha values, comma separated: ')])),
             ('Janus: inflation observables for a potential', lambda: janus([input('  V(phi), e.g. 0.5*phi**2: '), input('  N* [55]: ') or '55'])),
             ('Hyperion: primordial helium and deuterium', lambda: hyperion(['bbn', input('  omega_b h^2 [0.02237]: ') or '0.02237', input('  extra N_eff [0]: ') or '0'])),
             ('Hyperion: Milky Way orbit of one star', lambda: hyperion(['orbit'] + [input(f'  {q}: ') for q in ('ra (deg)', 'dec (deg)', 'distance (pc)', 'pmra (mas/yr)', 'pmdec (mas/yr)', 'radial velocity (km/s)')])),
             ('Late universe: distances to a redshift (Planck 2018)', lambda: late(['dist', input('  redshift z: ')])),
             ('Late universe: score w0, wa against DESI DR2 BAO', lambda: late(['desi', input('  w0 [-1]: ') or '-1', input('  wa [0]: ') or '0'])),
             ('SERAPIS: predictions at a tilt C', lambda: serapis(['predict', input('  C [1.15e-6]: ') or '1.15e-6'])),
             ('SERAPIS: what a measured n_s implies (inverse meter)', lambda: serapis([a for a in ['meter', input('  n_s: '), input('  sigma [none]: ')] if a])),
             ('Wavelength: a hydrogen line', lambda: wavelength(['line', input('  ion [H]: ') or 'H', input('  lower level [2]: ') or '2', input('  upper level [3]: ') or '3'])),
             ('Wavelength: convert a wavelength, frequency or energy', lambda: wavelength(['convert'] + (input('  value and unit, e.g. 656.3 nm: ').split() + ['', ''])[:2])),
             ('Power: solar panel curve', lambda: power(['solar'])),
             ('Sound: write a tone to a WAV file', lambda: sound(['tone', input('  frequency Hz [432]: ') or '432', input('  seconds [3]: ') or '3', input('  file [tone.wav]: ') or 'tone.wav'])),
             ('Inflation Scorecard: score n_s and r against current data', lambda: scorecard(['--ns', input('  n_s: '), '--r', input('  r [0]: ') or '0'])),
             ('Show license', lambda: license_([]))]
    while True:
        print(f'\nAEGIS toolkits {VERSION} — free for people and science; businesses need a commercial license.')
        for i, (t, _) in enumerate(items, 1): print(f'  {i}. {t}')
        print('  0. Quit')
        ch = input('Choose: ').strip()
        if ch in ('0', 'q', ''): return
        try: items[int(ch) - 1][1]()
        except (ValueError, IndexError): print('Not a choice.')
        except Exception as e: print('Error:', e)

def main(argv=None):
    for st in (sys.stdout, sys.stderr):   # Windows consoles default to cp1252, which cannot print α, σ, ⁻¹
        try: st.reconfigure(encoding='utf-8', errors='replace')
        except Exception: pass
    _root(); argv = sys.argv[1:] if argv is None else argv
    cmds = {'aion': aion, 'tracker': tracker, 'wavelength': wavelength, 'power': power, 'sound': sound, 'serapis': serapis, 'cern': cern, 'janus': janus, 'hyperion': hyperion, 'scorecard': scorecard, 'late': late, 'lattice': lattice, 'string': string, 'test': test, 'license': license_, 'menu': menu}
    if not argv: return menu([])
    if argv[0] in ('--version', 'version'): print('aegis', VERSION); return
    if argv[0] in ('-h', '--help', 'help') or argv[0] not in cmds: print(__doc__); return
    try: cmds[argv[0]](argv[1:])
    except SystemExit: raise
    except IndexError:
        print('Missing a value for that command (for example: aegis cern xsec 700 14).\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)
    except (ValueError, KeyError) as e:
        print(f'Input problem: {e}\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)

if __name__ == '__main__': main()
