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
  janus "<V(phi)>" [N*]             inflation observables n_s, r, alpha_s for any potential, e.g. janus "0.5*phi**2" 60
  hyperion bbn <omega_b h^2> [dNeff]   primordial helium Y_p and D/H (PRIMAT 2021 tables; needs camb)
  hyperion orbit <ra> <dec> <dist_pc> <pmra> <pmdec> <rv> [McMillan17|MWPotential2014]
                                    3 Gyr Milky Way orbit of one star: r_peri, r_apo, z_max, eccentricity
  late dist <z> [H0 ombh2 omch2 w0 wa mnu]   comoving / angular / Hubble distances and H(z) (default Planck 2018)
  late desi [w0 wa H0 ombh2 omch2 rd]       chi-square of a w0-wa cosmology against DESI DR2 BAO (13 points)
  late growth <z> [H0 ombh2 omch2 w0 wa]    linear growth D(z)/D(0) and growth rate f(z)
  scorecard --ns <n_s> [--r <r>] [--alpha-s <a>] [--label <name>]
                                    score an inflation model against every current CMB/LSS constraint (Inflation Scorecard)
  license                           show license terms

AEGIS Community License: free for individuals, scientists, students, schools, nonprofits and public research.
Any business or for-profit use needs the AEGIS Commercial License. CERN+1 is not affiliated with or endorsed by CERN.
"""
import sys, os, json

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

def lattice(args):
    from tools.lattice import lattice_lab
    lattice_lab.main(args)

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
             ('Inflation Scorecard: score n_s and r against current data', lambda: scorecard(['--ns', input('  n_s: '), '--r', input('  r [0]: ') or '0'])),
             ('Show license', lambda: license_([]))]
    while True:
        print('\nAEGIS toolkits — free for people and science; businesses need a commercial license.')
        for i, (t, _) in enumerate(items, 1): print(f'  {i}. {t}')
        print('  0. Quit')
        ch = input('Choose: ').strip()
        if ch in ('0', 'q', ''): return
        try: items[int(ch) - 1][1]()
        except (ValueError, IndexError): print('Not a choice.')
        except Exception as e: print('Error:', e)

def main(argv=None):
    _root(); argv = sys.argv[1:] if argv is None else argv
    cmds = {'cern': cern, 'janus': janus, 'hyperion': hyperion, 'scorecard': scorecard, 'late': late, 'lattice': lattice, 'test': test, 'license': license_, 'menu': menu}
    if not argv: return menu([])
    if argv[0] in ('-h', '--help', 'help') or argv[0] not in cmds: print(__doc__); return
    try: cmds[argv[0]](argv[1:])
    except SystemExit: raise
    except IndexError:
        print('Missing a value for that command (for example: aegis cern xsec 700 14).\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)
    except (ValueError, KeyError) as e:
        print(f'Input problem: {e}\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)

if __name__ == '__main__': main()
