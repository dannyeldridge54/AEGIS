from tools.weave_control import engine as E
R = E.run()
LV = {l['id']: l for l in R['levels']}
def test_all_levels_present_and_no_errors():
    assert set(LV) == {'inflation', 'flavour', 'bbn', 'late', 'colliders', 'galaxy', 'stars', 'sky'}
    assert not any(any('ERROR' in s for s in l['labels']) for l in R['levels'])
    assert all(l['status'] in ('pass', 'tension', 'fail', 'open') and l['category'] in 'ABCDE' for l in R['levels'])
def test_flavour_koide_and_brannen():
    o = LV['flavour']['outputs']
    assert abs(o['Koide_Q'] - 2/3) < 1e-5 and abs(o['Brannen_delta'] - 2/9) < 1e-4
def test_inflation_full_serapis_and_link_values():
    o = LV['inflation']['outputs']; assert abs(o['ns'] - 0.97065) < 1e-4 and abs(o['r'] - 5.41e-4) < 1e-5
def test_dark_sector_feeds_bbn():
    a = E.run({'dark_sector': 'none'}); b = E.run({'dark_sector': 'minimal_dNeff_0.2'})
    ya = [l for l in a['levels'] if l['id'] == 'bbn'][0]['outputs']['Yp']; yb = [l for l in b['levels'] if l['id'] == 'bbn'][0]['outputs']['Yp']
    assert yb > ya + 0.002            # ΔN_eff = 0.2 raises helium by ~0.0027
def test_late_closed_form_and_guard_ceiling():
    o = [l for l in E.run({'b_A': -0.041})['levels'] if l['id'] == 'late'][0]['outputs']
    assert 3.6 < o['z_dagger'] < 3.8 and abs(o['G_eff_over_G'] - (1 + 2*0.041**2)) < 1e-12   # D1725 Union3: 3.71
    assert LV['late']['outputs']['D1725']['Pantheon+']['d_coupled'] <= LV['late']['outputs']['D1725']['Pantheon+']['d_thread']
def test_collider_limit_flag():
    assert [l for l in E.run({'wino_mass_GeV': 600})['levels'] if l['id'] == 'colliders'][0]['status'] == 'fail'
