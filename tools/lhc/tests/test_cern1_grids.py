import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.lhc import grids as G, importers as I
def test_grid_shape_and_lifetime_peak():
    g = G.grid(masses=(600,), taus_ns=(0.003, 0.2, 100.0))
    row = g['acc_eff'][0]
    assert row[1] > row[0] and row[1] > row[2]     # too short decays before the tracker, too long passes through it
def test_hepdata_2d_reads_back():
    g = G.grid(masses=(400, 800), taus_ns=(0.1, 1.0)); t = I.load_hepdata_table(G.hepdata_2d(g))
    assert len(t['x']) == 4 and len(next(iter(t['y'].values()))['values']) == 4
