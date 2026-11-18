"""CERN+1 model-vs-collider panel: the SERAPIS wino window (read-only from the theory map) against CERN+1 collider reach."""
import pathlib, re
from . import recast_dt
def window():
    root = pathlib.Path(__file__).resolve().parents[2]
    try:
        t = (root / 'theory/map/map.yaml').read_text(encoding='utf-8')
        m = re.search(r'id: wino_window.*?title: Wino ([0-9.]+)[–-]([0-9.]+) TeV', t, re.S)
        if m: return float(m.group(1))*1e3, float(m.group(2))*1e3, 'theory/map/map.yaml (wino_window, D784)'
    except Exception: pass
    return 670.0, 1850.0, 'fallback D784'
def panel():
    lo, hi, src = window()
    run2 = recast_dt.limit(); hl = recast_dt.hl_lhc()['m_limit_GeV']
    cov = lambda m: max(0.0, min(m, hi) - lo)/(hi - lo)
    return {'window_GeV': [lo, hi], 'window_source': src, 'run2_limit_GeV': run2, 'hl_lhc_reach_GeV': hl,
            'run2_covers': cov(run2), 'hl_lhc_covers': cov(hl), 'untested_above_GeV': hl,
            'note': 'CERN+1 is independent (not affiliated with CERN); HL-LHC is a like-for-like extrapolation'}
