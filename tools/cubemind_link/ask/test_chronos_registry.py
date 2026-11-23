"""C3 (CM-NUCLEAR): the PC registry worker reproduces the referee-cleared Chronos numbers. Run from the CubeMind folder: python ask\\test_chronos_registry.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.environ['AEGIS_NOCACHE'] = '1'
from aegis_tools.registry import call
exp = [('chronos_make_now', {'nuclide': 'F-18', 'A_needed': 370, 'hours': 2.5}, 'make_now', 954.0195616592), ('chronos_generator', {'parent': 'Mo-99'}, 'peak_hours', 22.84702241),
       ('chronos_release_age', {'pair': 'Cs-134/Cs-137', 'ratio_now': 0.05, 'ratio_at_release': 1}, 'years', 9.58362825), ('chronos_nickel_mass', {'L_erg_s': 1e41, 'days': 200, 'mode': 'tail', 't0_days': 40}, 'M_Ni_Msun', 0.5956508450),
       ('chronos_wd_merger', {'period_s': 765, 'm1': 0.26, 'm2': 0.5}, 'merger_Myr', 1.10932051), ('chronos_pu_age', {'am_over_pu_activity': 0.02}, 'years', 9.82615890),
       ('chronos_tritium', {'grams': 1000, 'years': 1}, 'left_g', 945.29148768), ('chronos_star_age', {'pair': 'Th/Eu', 'log_eps_observed': -0.52, 'production_ratio': 0.45}, 'age_Gyr', 8.05559322)]
bad = 0
for n, a, k, v in exp:
    r = call(n, a); ok = 'error' not in r and abs(r[k] / v - 1) < 1e-8; bad += not ok; print('PASS' if ok else 'FAIL', n, r.get(k, r.get('error')))
print('C3', 'PASS' if not bad else f'FAIL ({bad})'); open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'C3_result.txt'), 'w').write('PASS' if not bad else f'FAIL {bad}')
