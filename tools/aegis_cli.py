# AEGIS-FP ONOHRDBYMCLONMKW · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""AEGIS toolkits — one command-line program (also built as a standalone executable).

Usage (from the repo root:  python -m tools.aegis_cli <command> ...,  or the executable:  aegis <command> ...)
  menu                              interactive menu (default when started with no command, e.g. by double-click)
  test                              run the release smoke test (9 checks against published values)
  cern xsec <mass_GeV> [sqrt_s_TeV] wino pair cross sections (fb), default 13.6 TeV
  cern life <mass_GeV>              chargino-neutralino mass splitting, lifetime, decay length
  cern limit [ATLAS_136|ATLAS_36]   disappearing-track recast limit with theory band
  cern future                       HL-LHC / HE-LHC / FCC-hh wino reach
  lattice <command> [args]          Lattice Lab (e.g. lattice hexagons E8, lattice energy E6 1.25)
  janus "<V(phi)>" [N*]             inflation observables n_s, r, alpha_s for any potential, e.g. janus "0.5*phi**2" 60
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
    elif c == 'future':
        _show(future.table())
    else: print(__doc__)

def janus(args):
    from tools.janus_calc import anyV, core
    if not args: print(__doc__); return
    N = float(args[1]) if len(args) > 1 else 55.0
    s = core.spectra3(anyV.from_formula(args[0]), N)
    _show({'V': args[0], 'N_star': N, **{k: v for k, v in s.items() if k in ('ns', 'r', 'alpha_s', 'beta_s')}})

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
             ('CERN+1: chargino lifetime at a mass', lambda: cern(['life', input('  mass in GeV: ')])),
             ('CERN+1: ATLAS disappearing-track limit with theory band', lambda: cern(['limit', input('  ATLAS_136 or ATLAS_36 [ATLAS_136]: ') or 'ATLAS_136'])),
             ('CERN+1: future-collider reach', lambda: cern(['future'])),
             ('Lattice Lab: hexagonal planes in a lattice', lambda: lattice(['hexagons', input('  lattice (D4, E6, E7, E8, BW16, Leech): ')])),
             ('Lattice Lab: energy of a lattice', lambda: lattice(['energy', input('  lattice (e.g. E6): '), input('  alpha values, comma separated: ')])),
             ('Janus: inflation observables for a potential', lambda: janus([input('  V(phi), e.g. 0.5*phi**2: '), input('  N* [55]: ') or '55'])),
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
    cmds = {'cern': cern, 'janus': janus, 'lattice': lattice, 'test': test, 'license': license_, 'menu': menu}
    if not argv: return menu([])
    if argv[0] in ('-h', '--help', 'help') or argv[0] not in cmds: print(__doc__); return
    try: cmds[argv[0]](argv[1:])
    except SystemExit: raise
    except IndexError:
        print('Missing a value for that command (for example: aegis cern xsec 700 14).\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)
    except (ValueError, KeyError) as e:
        print(f'Input problem: {e}\nRun "aegis help" for the list of commands and examples.'); sys.exit(2)

if __name__ == '__main__': main()
