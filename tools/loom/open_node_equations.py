"""D2145: equations for the three OPEN negative-space nodes (N1, N14, N16). Danny 19:36 "make an equation for each of them"."""
import json, math
C = 0.0251; eps = lambda m: C/(m + 1/16)
# N1: a hidden family on rung m: m2/m3 = eps_m, m1/m3 = eps_m^2 [R rung rule, O(1) smear x3]; a light thermal hidden Weyl fermion adds
# dNeff = (4/7)(7/8)(2)(10.75/g*s(T_dec))^(4/3) [S]; wall: total dNeff < 0.14 (ACT)
dN_weyl = (4/7)*(7/8)*2*(10.75/106.75)**(4/3)
n1 = dict(eq='m1/m3 = eps_m^2, m2/m3 = eps_m, eps_m = 0.0251/(m+1/16); light hidden Weyl fermion: dNeff = 1.0*(10.75/g*s(T_dec))^(4/3)',
          rung11=dict(eps=eps(11), m1_over_m3=eps(11)**2), dNeff_per_light_weyl_decoupled_above_EW=dN_weyl,
          max_light_weyl_species=int(0.14/dN_weyl),
          example='if a hidden rung-11 family had m3 = 12.8 GeV [A], m1 = %.3g keV -> light -> counts as dark radiation' % (12.8e6*eps(11)**2))
# N14: pre-inflation wall. Enough inflation: N_tot >= N* + (1/2) ln(Omega_k,i / 1e-3) [S], Omega_k,i ~ 1; TCC: N_tot < ln(M_P/H) [lit]
MP = 2.435e18; H = math.pi*math.sqrt(2.1e-9*5.4e-4/2)*MP; Ns = 2/(1 - 0.9706)
n14 = dict(eq='N* + (1/2) ln(Omega_k,i/1e-3) <= N_tot <= ln(M_P/H_inf) (TCC)', N_min=Ns + 0.5*math.log(1e3), N_TCC_max=math.log(MP/H),
           verdict='no solution: the window is empty (the TCC wall N11 again)')
# N16: D3 tadpole in the IIB orientifold [S]: N_D3 + N_flux/2 + sum_a N_a (induced charge of magnetised D7_a) = chi/24 ; record numbers
n16 = dict(eq='N_D3 + (1/2) int G3^G3bar + sum_a Q_ind(D7_a, F_a) = chi(X)/24, chi = 48 -> 2 [S]; record: |M| = 9 family flux gives Q_ind = 46 [R]',
           budget=48/24, record_charge=46, excess=46 - 2,
           B2_route='families from intersections I_ab = prod_i (n_a^i m_b^i - m_a^i n_b^i) with no extra D3 flux; the PS seed closes its charge exactly (D2110-D2129)')
out = dict(N1=n1, N14=n14, N16=n16); print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d2145_open_node_equations.json', 'w'), indent=1)
