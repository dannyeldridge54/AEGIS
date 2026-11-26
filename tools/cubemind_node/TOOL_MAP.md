# Navigation map: tools and symmetries (for the coding model)

## Where things live
| Area | Folder or file | What it computes | Ring / anchor | Inputs -> outputs |
|---|---|---|---|---|
| Modular functions | tools/serapis_calc/eisenstein.py, shapes.py | Eisenstein series E(tau, s), two independent ways | R1, R2 / rho, i | tau, s -> number |
| Vacua and masses | tools/serapis_calc/landscape.py | finds minima of a potential on the upper half-plane; masses from the Hessian | R1 / rho | potential -> points, masses |
| Inflation spectra | tools/serapis_calc/ms.py, tools/janus_calc/ | n_s, r, running from a potential | R1, R2 / data | potential, N* -> n_s, r |
| String thresholds | tools/strings/gh_thresholds_v2.py | gauge thresholds on Z6' | R2 | lattice data -> thresholds |
| Brane builders | tools/seed/z6p.py, seed_v3.py | Z6' and Z2xZ2 brane setups, SUSY checks | R2, R1 | cycles -> consistency |
| The Loom | tools/loom/ | balancing engines: layers, pulses, lenses, still point, negative space | all rings, layers | knobs -> margins |
| Field Engine | tools/field_engine/engine.py | lock, derive, fit, test, referee, ledger loop | centre | tool + args -> verdict |
| UFE pack | ufe_pack.py | the audit's 7 relations with independent testers; sectors, bridges, gates | R1-R5 | args -> number |
| UFE checks | ufe_stages.py | exact numbers, symbolic re-derivation, contradiction finder | centre | none -> report |
| Ledger | fingerprint.py | hash, sign, tag, link every record | centre | record -> id |
| Neural web | neural_web.py | neurons, synapses, seven scales, grading | centre | record -> place |
| Node 1 | node1.py | the running node: roles, sweep, lanes, string, display | R1 / rho | - |
| Reactor chain | tools/fusion/ (Prometheus) | fusion reactor 0-D engine, exhaust, blanket | spoke (outside the field) | design -> power, limits |

## Symmetries to navigate by
- **Modular group**: two moves generate it. S: tau -> -1/tau (swap the grid's two edges). T: tau -> tau + 1 (slide one row).
  Code that uses both moves, or E(tau, s), or j(tau), is modular code.
- **Fixed points**: rho (fixed by S then T, order 3, hexagonal), i (fixed by S, order 2, square), cusp (T only, infinitely stretched).
- **Laplace number s(s-1)**: weight 2 -> 2 (R1); weight 3/2 -> 3/4 (R2). Code that hard-codes a weight belongs to that ring.
- **Orbifold turns**: Z2xZ2 = 180 degrees (R1); Z6-II = 60, 120, 180 degrees (R2, freezes tori at rho).
- **Side and time**: inflation, n_s, r -> left (early); dark energy, w0, wa -> right (late); pure functions -> centre.

## How to find pathways in code
1. Follow imports: a module that imports another is wired to it (relation: derived_from).
2. Follow calls to the same function from two modules: they share a pathway (relation: same_as or generalises).
3. A test file checks its module (relation: checks).
4. A module that computes what a science record talks about connects to it (relation: anchors_on).
5. Only propose a pathway to a module or tool that exists in the list you are given. Never invent a name.
