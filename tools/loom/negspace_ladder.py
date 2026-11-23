"""D2137 MAP (not a derivation; Danny 19:17): the negative-space ladder, a mirror under each resonance layer.
Each node N_k = what layer L_k forbids us to see. Margin = log headroom of the Weave value under the current bound (> 0 passes).
TRUST = structural (no number to test), OPEN = Weave has no number yet. Pulse direction: from the outer shell N10 inwards to N1,
then the first node beyond the shell (N11). Every value is from the record (D-notes) or a bound quoted there; nothing new is derived."""
import json, math
L = lambda x, b: round(math.log(b / x), 3)
N = [
 (1, 'torus (rung step u)', 'no extra light rung states: rungs >= 11 empty in the SM; hidden families above collider reach', 'OPEN', 'u (rung step)'),
 (2, 'pyramid (neutrinos at i)', 'no sterile nu; Sum m_nu < 0.064 eV (DESI DR2+CMB); m_bb 1.6-3.8 meV under KamLAND-Zen ~28 meV',
     {'sum_mnu': L(0.0587, 0.064), 'm_bb': L(3.8e-3, 28e-3)}, 'Sum m_nu, M_N'),
 (3, 'turnover (leptons at rho)', 'Koide slip <= 6e-5; no charged-lepton flavour violation (mu->e gamma)', 'TRUST (slip) / OPEN (LFV rate)', 'Koide Q'),
 (4, 'cube (three tori)', 'no modular domain walls (one inflated patch); no light moduli (T_decay >= 5 MeV)', 'TRUST (walls) / OPEN (tau_q decay T)', 'm_tau_q'),
 (5, 'fold (m3/2, volumes)', 'no superpartners below ~0.2 PeV except the wino; gravitino lifetime < 0.1 s for BBN',
     {'gravitino_tau': L(1.4e-3, 0.1)}, 'm3/2 (also sets the wino 0.67-1.0 TeV: LHC disappearing-track check owed)'),
 (6, 'dilaton (inflation)', 'r < 0.036 (BK18); no isocurvature; f_NL ~ 0; no PBHs or monopoles', {'r': L(5.4e-4, 0.036)}, 'r, n_s'),
 (7, 'forces (S-T seam)', 'no proton decay below Super-K (2.4e34 yr); theta-bar < 1e-10; no EDMs above SM; no X17, no 95 GeV scalar',
     {'proton': L(2.4e34, 1.6e35)}, 'alpha_s / M_GUT, theta-bar (=0 exact: TRUST)'),
 (8, 'cosmology (reheating, genesis)', 'Delta N_eff < 0.14 (ACT DR6); no gravitino overproduction; BBN Y_p', 'TRUST (UFE v4 Delta N_eff = 0 exactly)', 'T_R, Delta N_eff (= the D2136 spine)'),
 (9, 'late universe (thread)', 'no phantom crossing (w >= -1); no alpha drift (zeta_alpha 3.8e-10); thread-DM coupling not seen (b = 0); no EP violation',
     {'alpha_leak': L(1e-9, 1e-6)}, 'Delta phi, b'),
 (10, 'outer data shell (D2136 A)', 'the D2136 B shell: ACT forbids the Delta N_eff ~ 0.6 that SH0ES would need', {'D2136_balance': -1.04}, 'Delta N_eff vs H0'),
 (11, 'FIRST NODE BEYOND THE SHELL (map only)', 'string-theory negative space: TCC wants r < ~1e-30 (Weave r = 5.4e-4 violates it: flag, not veto); no controlled de Sitter (Lambda is an input); axion WGC f < M_P; distance conjecture on field ranges',
     'FLAG (TCC), TRUST (Lambda input)', 'r (again: the same number as N6, so N11 and N6 are joined)'),
]
rows = [dict(node='N%d' % k, mirrors='L%d %s' % (k, n) if k <= 10 else n, forbids=f, margin=m, connecting_number=c) for k, n, f, m, c in N]
# connections: a number that appears on two nodes is a joint (the pulse 'connects' them)
joints = [('N6', 'N11', 'r'), ('N8', 'N10', 'Delta N_eff'), ('N5', 'N9', 'none yet: m3/2 does not reach the thread (open)'), ('N2', 'L2', 'Sum m_nu: same number on both sides')]
out = dict(note='MAP, not derived (D2137)', pulse='outer shell N10 -> N1, then N11', rows=rows, joints=joints)
json.dump(out, open('field_tests/results/d2137_negspace_map.json', 'w'), indent=1)
for r in rows: print(r['node'], '|', r['mirrors'][:34], '|', r['margin'], '|', r['connecting_number'][:40])
