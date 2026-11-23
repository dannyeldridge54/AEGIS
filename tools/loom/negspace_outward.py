"""D2138 MAP (not derived; Danny 19:19): pulse OUTWARD through negative space, starting at N11 (the string-theory wall).
Each ring = the constraints on the ring inside it. A pulse adds a node only if it brings (a) a new class of forbidden thing AND
(b) a number or joint that touches the Weave. A ring with neither is NULL; stop at the first NULL ring (map, not a search)."""
import json, math
MP = 2.435e18; As, r = 2.1e-9, 5.4e-4
H = math.pi*math.sqrt(As*r/2)*MP                     # Hubble during inflation from r (standard)
A = 16*1.6449340668482264/(3*1.2020569031595942); beta = 2*math.sqrt(2)
slope = lambda u: beta*u/(1 - u)                     # |V'|/V of the thread at u = A e^{-beta phi}
nodes = [
 dict(node='N11', ring='string-theory swampland wall', forbids='TCC (r < ~1e-30), stable de Sitter, axion f > M_P, large field ranges',
      weave='r = 5.4e-4 violates TCC (FLAG); Lambda is an input (TRUST)', joint='r -> L6/N6'),
 dict(node='N12', ring='quantum-gravity consistency', forbids='global symmetries; more light species than (M_P/H)^2; H above the species scale',
      weave=f'H_inf = {H:.2e} GeV; species room N < (M_P/H)^2 = {(MP/H)**2:.1e}; the residual Z3 at rho is part of SL(2,Z), a gauge symmetry in string theory (PASS, literature)',
      joint='species plateau of inflation -> L6; residual Z3 -> L3/L4'),
 dict(node='N13', ring='de Sitter / horizon entropy (the far future)', forbids='an eternal stable de Sitter; refined dS: |V\'|/V >= c ~ O(1)',
      weave=f'the thread rolls toward the knot i, so there is no eternal dS (structural PASS); thread slope |V\'|/V = {slope(0.157):.2f} at start (u_i 0.157), smaller today: c ~ 0.5 is MARGINAL',
      joint='u_i -> L9 (the same knob D2133/D2134 fitted)'),
 dict(node='N14', ring='before the beginning (initial conditions)', forbids='an inflaton that never starts; pre-inflation remnants larger than the horizon',
      weave='E10 billiard / Te Kore OPEN; dimension at horizon exit read from r (r_D = r_10 * 8/(D-2))', joint='r -> L6 (third use of r)'),
 dict(node='N15', ring='vacuum selection (the landscape)', forbids='a vacuum chosen by hand',
      weave='rho is the minimum of every lattice sum at fixed area (Montgomery 1988, theorem): selection PASSES without anthropics', joint='rho -> L1 (the centre)'),
 dict(node='N16', ring='mathematical consistency of the fold', forbids='uncancelled anomalies; K-theory charge; tadpoles beyond the tadpole conjecture',
      weave='anomalies + K-theory PASS (PS seed, D2110-D2129); |M| = 9 flux tadpole (D3 charge 46) FAILS the tadpole conjecture (ENDPOINTS B2: intersection families would remove it)',
      joint='|M| = 9 -> L5/L7 (families and f_vis = T + 9S)'),
 dict(node='N17', ring='beyond consistency (logic / axioms)', forbids='-', weave='no physical number; no joint', joint='NULL'),
]
out = dict(note='MAP, not derived (D2138)', start='N11', nodes=nodes, n_new_nodes=sum(1 for n in nodes[1:] if n['joint'] != 'NULL'),
           stopped_at='N17 (NULL ring)', H_inf_GeV=H, thread_slope_start=slope(0.157))
json.dump(out, open('field_tests/results/d2138_negspace_outward.json', 'w'), indent=1)
for n in nodes: print(n['node'], '|', n['ring'], '|', n['weave'][:110], '|', n['joint'])
print('new nodes beyond N11:', out['n_new_nodes'], '; stopped at', out['stopped_at'])
