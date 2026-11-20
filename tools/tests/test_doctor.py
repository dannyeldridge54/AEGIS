import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tools import doctor
def test_doctor_reports_every_package_and_fix_line():
    d = doctor.check()
    assert len(d['packages']) == len(doctor.PACKAGES)
    assert all(r['installed'] for r in d['packages'] if r['package'] in ('numpy', 'scipy'))
    assert d['fix'].startswith('pip install') or d['fix'] == 'nothing to install'
