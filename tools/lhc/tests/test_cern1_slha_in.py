import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.lhc import slha_in as I, settings as S
def test_roundtrip_with_export():
    s = I.summary(S.slha(700.0))
    assert abs(s['m_chi10_GeV'] - 700) < 1e-6 and s['model'] == 'wino'
    assert abs(s['tau_ns_file']/s['tau_ns_cern1'] - 1) < 1e-5 and abs(s['dm_MeV'] - 163.75) < 0.1
def test_nmix_classification_higgsino():
    txt = """BLOCK MASS
  1000022  3.000000E+02
  1000024  3.010000E+02
BLOCK NMIX  # neutralino mixing
  1  1   0.05
  1  2  -0.05
  1  3   0.70
  1  4  -0.71
"""
    s = I.summary(txt, 'run2'); assert s['model'] == 'higgsino' and s['sigma_fb'] > 0 and s['character']['higgsino'] > 0.99
