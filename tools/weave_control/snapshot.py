# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Weave Control OFFLINE snapshot (W10, acceptance rule X4). A phone cannot run the Python engine, so the APK ships the
engine's results precomputed over a stated grid. Each level depends only on its own knobs, so each level is stored on its
own grid and the page composes them: no interpolation, and knob values outside the grid are not offered.
Run: python3 -m tools.weave_control.snapshot [out_dir]  → snapshot.json (+ finder_<n>.png for the listed sky targets)."""
import itertools, json, os, sys, time
from tools.weave_control import engine as E

GRID = {   # level id: {knob: [values]}; every other knob stays at its default
    'inflation': dict(inflation_model=None, Nstar=[50.0, 55.0, 60.0]),
    'flavour':   {},
    'bbn':       dict(omega_b=[0.0220, 0.02237, 0.0226], dark_sector=None),
    'late':      dict(b_A=[-0.1, -0.06, -0.041, -0.02, 0.0, 0.02], dphi=[0.64]),
    'colliders': dict(wino_mass_GeV=[440.0, 700.0, 1000.0, 1500.0, 2000.0, 2900.0], run=None),
    'galaxy':    dict(wino_mass_GeV=[440.0, 700.0, 1000.0, 1500.0, 2000.0, 2900.0], halo=None, rho_sun=[0.3, 0.4]),
    'stars':     dict(eos=None),
    'sky':       dict(target=['M31', 'M42', 'M45', 'M13', 'M57', '266.4168,-29.0078'], aperture_mm=[80.0]),
}
FNS = {f.__name__: f for f in E.LEVELS}

def grid_for(level):
    kn = {k['key']: k for k in E.knobs()[level]}
    g = {}
    for k, v in GRID[level].items(): g[k] = v if v is not None else kn[k]['options']
    return g

def build(out_dir):
    os.makedirs(out_dir, exist_ok=True); t0 = time.time()
    from tools.prov_block import provenance
    snap = dict(kind='weave_control_offline_snapshot', defaults=E.DEFAULTS, knobs=E.knobs(), grid={}, levels={},
                provenance=provenance('Weave Control offline snapshot', {}, [], ['W10', 'PREREG_W2_LINKS']))
    for lid in [f.__name__ for f in E.LEVELS]:
        g = grid_for(lid); keys = list(g); snap['grid'][lid] = g; snap['levels'][lid] = {}
        for combo in itertools.product(*[g[k] for k in keys]) if keys else [()]:
            p = dict(E.DEFAULTS); p.update(dict(zip(keys, combo)))
            try: lv = FNS[lid](p)
            except Exception as e: lv = E.L(lid, lid, '?', '?', {}, {}, [], {}, [f'ERROR: {e}'], status='open'); lv['error'] = repr(e)
            snap['levels'][lid][json.dumps([p[k] for k in keys])] = lv
    if 'sky' in snap['levels']:
        from tools.mapper import finder
        for i, t in enumerate(GRID['sky']['target']):
            finder.chart(t, field_deg=6, fov_arcmin=(60,), out=os.path.join(out_dir, f'finder_{i}.png'), invert=False)
    snap['seconds'] = round(time.time() - t0, 1)
    json.dump(snap, open(os.path.join(out_dir, 'snapshot.json'), 'w'), default=lambda o: float(o) if hasattr(o, '__float__') else str(o))
    n = sum(len(v) for v in snap['levels'].values()); print(f'snapshot: {n} level states in {snap["seconds"]} s → {out_dir}')
    return snap

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui'))
