# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""aegis doctor (H1e): which optional packages are installed, their versions, and exactly what each one unlocks.
Answers the most common complaint about astro/HEP stacks (installation pain) with one command and the pip line to fix it."""
import importlib, sys
PACKAGES = [   # (import name, pip name, toolkit, what it unlocks)
    ('numpy', 'numpy', 'all', 'everything (required)'),
    ('scipy', 'scipy', 'all', 'everything (required)'),
    ('sympy', 'sympy', 'Janus', 'any-potential inflation (aegis janus score "<V(phi)>")'),
    ('numba', 'numba', 'Janus / Hyperion', 'compiled fast paths (multi-field Janus, fast orbits)'),
    ('camb', 'camb', 'Hyperion', 'BBN tables (hyperion pulls), halo mass function'),
    ('galpy', 'galpy', 'Hyperion / Mapper', 'Milky Way referee + McMillan17 orbits (Star Mapper)'),
    ('colossus', 'colossus', 'Hyperion', 'halo/cosmology referee checks'),
    ('lalsimulation', 'lalsuite', 'Hyperion', 'IMRPhenomD GW horizons, detector PSDs (O4, A+, ET, CE)'),
    ('linx', 'linx-bbn', 'Hyperion', 'BBN network engine (bbn_net)'),
    ('pyhf', 'pyhf', 'CERN+1', 'published ATLAS likelihoods, CLs limits, pyhf export'),
    ('yaml', 'pyyaml', 'CERN+1', 'reading HEPData YAML tables'),
    ('astropy', 'astropy', 'Mapper', 'observing planner, VOTable/ECSV export, coordinates'),
    ('cobaya', 'cobaya', 'Janus (full Planck)', 'full-likelihood fits with CAMB/CLASS'),
]
EXTRAS = {'core': ['numpy', 'scipy', 'sympy'], 'cern': ['pyhf', 'pyyaml'], 'astro': ['camb', 'galpy', 'colossus', 'astropy', 'numba'],
          'gw': ['lalsuite'], 'full': ['numpy', 'scipy', 'sympy', 'numba', 'camb', 'galpy', 'colossus', 'lalsuite', 'linx-bbn', 'pyhf', 'pyyaml', 'astropy', 'cobaya']}
def check():
    rows = []
    for mod, pipname, tk, what in PACKAGES:
        try:
            m = importlib.import_module(mod); v = getattr(m, '__version__', 'installed'); ok = True
        except Exception:
            v, ok = None, False
        rows.append(dict(package=pipname, toolkit=tk, installed=ok, version=v, unlocks=what))
    missing = [r['package'] for r in rows if not r['installed']]
    return dict(python=sys.version.split()[0], packages=rows, missing=missing,
                fix=('pip install ' + ' '.join(missing)) if missing else 'nothing to install',
                profiles={k: 'pip install ' + ' '.join(v) for k, v in EXTRAS.items()})
