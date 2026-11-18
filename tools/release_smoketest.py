# AEGIS-FP LRISJSJVSGUGBCC5 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Release smoke test for the AEGIS public toolkits. Run from the repo root:  python tools/release_smoketest.py
Checks CERN+1 (tools/lhc), Lattice Lab (tools/lattice) and the Janus inflation calculator (tools/janus_calc)
against values published in the papers. Exit code 0 = all pass."""
import sys, os, math, time
sys.path.insert(0, os.getcwd())
OK = []
def check(name, got, want, tol):
    ok = abs(got - want) <= tol; OK.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.6g} (expected {want} ± {tol})"); return ok
t0 = time.time()
from tools.lhc import xsec, lifetime, recast_dt, stats
check('CERN+1 dm(1 TeV) [MeV]', 1e3*lifetime.dm(1000.0), 164.11, 0.05)
check('CERN+1 c*tau(1 TeV) [cm]', lifetime.widths(1000.0)['ctau_cm'] if 'ctau_cm' in lifetime.widths(1000.0) else 2.99792458e10*lifetime.widths(1000.0)['tau_ns']*1e-9, 5.831, 0.01)
check('CERN+1 ATLAS 136/fb recast [GeV]', recast_dt.limit_search('ATLAS_136'), 666.6, 0.5)
check('CERN+1 ATLAS 36/fb recast [GeV]', recast_dt.limit_search('ATLAS_36'), 447.8, 0.5)
check('CERN+1 exact Poisson N95 (b=n=3)', stats.ul_poisson(3.0, 3), 5.395, 0.01)
from tools.lattice import lattice_lab as LL
check('Lattice Lab E6 energy at alpha=1.25', LL.energy('E6', [1.25])['energy'][1.25], 0.10458, 5e-5)
check('Lattice Lab hexagonal planes in E8', LL.hexagons('E8')['hexagonal_planes'], 1120, 0)
from tools.janus_calc.core import Model
V = lambda p: 0.5*p*p; dV = lambda p: p
s = Model(V, dV, 20.0).spectra(60.0)
check('Janus calc phi^2 n_s at N*=60 (exact numerical vs slow-roll 1-2/60.5)', s['ns'], 1 - 2/60.5, 2e-3)
check('Janus calc phi^2 r at N*=60 (vs slow-roll 8/60.5)', s['r'], 8/60.5, 3e-3)
print(f"\n{sum(OK)}/{len(OK)} passed in {time.time()-t0:.1f}s"); sys.exit(0 if all(OK) else 1)
