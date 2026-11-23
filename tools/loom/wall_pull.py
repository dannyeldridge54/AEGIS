"""D2143: pull every negative-space tie both ways; read the early clock N* and the late clock t0 (age). PREREG_D2143."""
import json, math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'weave_cm_v5')); os.environ.setdefault('WEAVE_DATA', '/tmp/claude-0/cobaya_pkgs/data/')
import weave_engine as W
p = json.load(open('field_tests/weave_lcdm/knob_dovekie.json'))['0.0']['p']; wb, wc, lVL, ui = p
GYR = 977.8   # 1/H in Gyr for H = 1 km/s/Mpc
def age(wb=wb, wc=wc, VL=math.exp(lVL), ui=ui, b=0.0, extra_rad=0.0):
    sol = W.solve(wb, wc, VL, ui, b, a0=1e-8)
    if sol is None: return float('nan'), float('nan')
    N = np.linspace(math.log(1e-8), 0, 6000); a = np.exp(N); Y = sol.sol(N); phi, v, rc = Y[0], Y[1], np.exp(Y[2])
    rn = np.array([W.nu(x)[0] for x in a]); V = VL*(1 - W.A*np.exp(-W.BETA*phi))
    E2 = (W.OG*(1 + extra_rad*0.2271)/a**4 + rn + wb/a**3 + rc + V)/(1 - v*v/6); H = 100*np.sqrt(E2)
    return float(np.trapezoid(1/H, N))*GYR, float(H[-1])
t_base, H_base = age()
Nst = 2/(1 - 0.9706); out = dict(base=dict(age_Gyr=t_base, H0=H_base, Nstar=Nst), nodes=[])
def rec(node, knob, up, dn, unit):
    resp, thrust = (up - dn)/2, (up + dn)/2
    lim = 0.01 if unit == 'e-folds' else 1e-3
    ties = abs(resp) >= lim; th = ties and abs(thrust) >= 0.1*abs(resp)
    out['nodes'].append(dict(node=node, knob=knob, clock=unit, d_up=up, d_down=dn, response=resp, thrust=thrust,
                             ties_through_time=ties, thrust_seen=th))
f = 1.5
rec('N4 (tau_q dilution D)', 'D x/÷ 1.5', -math.log(f)/3, math.log(f)/3, 'e-folds')
rec('N6 (r, CMB wall)', 'r x/÷ 1.5', -Nst/2*math.log(f)*0 + (Nst/math.sqrt(f) - Nst), (Nst*math.sqrt(f) - Nst), 'e-folds')   # r ∝ N^-2 exactly
rec('N8 (T_R reheating)', 'T_R x/÷ 1.5', math.log(f)/3, -math.log(f)/3, 'e-folds')
rec('N9/N13 (thread start u_i)', 'u_i x/÷ 1.5', age(ui=min(ui*f, 0.21))[0] - t_base, age(ui=ui/f)[0] - t_base, 'Gyr')
KB = json.load(open('field_tests/weave_lcdm/knob_dovekie.json'))
def agep(bb):
    q = KB[str(bb)]['p']; return age(wb=q[0], wc=q[1], VL=math.exp(q[2]), ui=q[3], b=bb)[0]
rec('N9 (coupling b, best fits)', 'b = +/-0.025', agep(0.025) - t_base, agep(-0.025) - t_base, 'Gyr')
rec('N8/N10 (dark radiation dNeff)', 'dNeff = 0.14 / 0', age(extra_rad=0.14)[0] - t_base, 0.0, 'Gyr')
rec('N10 (H0 shell: V_L)', 'V_L x/÷ 1.5', age(VL=math.exp(lVL)*f)[0] - t_base, age(VL=math.exp(lVL)/f)[0] - t_base, 'Gyr')
for n in ('N1 rung states', 'N2 neutrinos (Sigma m_nu: mass tie, H(z) shift < 0.1%)', 'N3 leptons', 'N5 m3/2 / wino', 'N7 forces / proton',
          'N11 swampland', 'N12 QG consistency', 'N14 before the beginning', 'N15 vacuum selection', 'N16 tadpole'):
    out['nodes'].append(dict(node=n, clock='none', ties_through_time=False, note='ties through mass or charge, not time (no numeric clock tie)'))
json.dump(out, open('field_tests/results/d2143_wall_pull.json', 'w'), indent=1)
print('base age %.3f Gyr H0 %.2f N* %.1f' % (t_base, H_base, Nst))
for n in out['nodes']:
    if n['clock'] == 'none': print(n['node'], '| no clock tie')
    else: print(n['node'], '|', n['clock'], '| up %+.4f down %+.4f | response %+.4f thrust %+.4f | time-tie %s thrust %s' % (n['d_up'], n['d_down'], n['response'], n['thrust'], n['ties_through_time'], n['thrust_seen']))
