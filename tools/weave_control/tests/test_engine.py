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
    a = E.run({'dark_sector': 'none'}); b = E.run({'dark_sector': 'minimal_equal_sharing'})
    ya = [l for l in a['levels'] if l['id'] == 'bbn'][0]['outputs']['Yp']; yb = [l for l in b['levels'] if l['id'] == 'bbn'][0]['outputs']['Yp']
    assert yb > ya + 0.002            # ΔN_eff = 0.21 raises helium by ~0.003 (D1646)
    m = E.run({'dark_sector': 'mirror_full_equal'}); assert [l for l in m['levels'] if l['id'] == 'bbn'][0]['status'] == 'fail'
def test_late_closed_form_and_guard_ceiling():
    o = [l for l in E.run({'b_A': -0.041})['levels'] if l['id'] == 'late'][0]['outputs']
    assert 3.6 < o['z_dagger'] < 3.8 and abs(o['G_eff_over_G'] - (1 + 2*0.041**2)) < 1e-12   # D1725 Union3: 3.71
    assert LV['late']['outputs']['D1725']['Pantheon+']['d_coupled_at_most'] <= LV['late']['outputs']['D1725']['Pantheon+']['d_thread']
def test_collider_limit_flag():
    assert [l for l in E.run({'wino_mass_GeV': 600})['levels'] if l['id'] == 'colliders'][0]['status'] == 'fail'

def test_v1_fixes():
    assert LV['late']['status'] == 'tension'                       # beats ΛCDM, trails w0wa
    assert any('1.94' in s for s in LV['stars']['labels'])
    assert len(LV['flavour']['outputs']['delta_equivalent_forms']) >= 2
    assert set(E.DARK_SECTORS) == {'none', 'brane_split', 'minimal_equal_sharing', 'mirror_at_bound', 'mirror_full_equal'}

def test_referee_r1_r3():
    assert any('PREDICTIONS only' in s for s in LV['inflation']['labels'])
    st = [l for l in E.run({'inflation_model': 'starobinsky', 'Nstar': 55})['levels'] if l['id'] == 'inflation'][0]['status']
    assert st == 'fail'                                              # Starobinsky N*=55: n_s −3.4σ from P-ACT-LB2 (a prediction there)
    d = LV['late']['outputs']['D1725']['DES-Y5']; assert abs(d['dAIC_thread'] - (d['d_thread'] + 2)) < 1e-9
    assert any('OBSERVATIONAL' in s for s in LV['bbn']['labels'])

def test_w2_links():
    g = LV['galaxy']['outputs']; assert g['recipe_selfcheck_0p286'] and g['f_max'] is not None
    assert abs(E.f_max(1000.0, 'Burkert', 0.40)[0] - 0.286) < 0.003            # D1322 smoke-test value
    late = LV['late']['outputs']; assert 'S8 coupled Union3 vs KiDS-Legacy' in late['S8_pulls'] and late['Lya_context']['z'] == 2.33
    assert any('Galactic centre' in t['name'] for t in LV['sky']['outputs']['science_targets'])

def test_w2_e2():
    g = LV['galaxy']['outputs']; assert 'J_annulus_0p5_3deg_GeV2_cm5' in g and 'J_IGS_ROI_GeV2_cm5' in g
    assert any(s.startswith('S₈ sub-status: pass') for s in LV['late']['labels'])
