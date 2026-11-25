# C8 — research loop: find anchor points for the field; the fractal nodes; a flip grid (25 Nov 2026, 15:40 CST)

Danny, 15:37 CST: **"Have them do the research loop and find points to anchor field. Explain the fractal nodes and we can choose points on
grid to switch flip."** This supersedes the test order in C7: research and anchoring come first. Locking rules from C7 still apply to any run.

## 1. The fractal nodes (what the Loom already has; read the files)
The Loom treats the theory as a nested set of nodes, each owning a few knobs, balanced from the centre outward.
| Level | What a node is | File |
|---|---|---|
| Knob agent | Owns <= 9 knobs; tunes them octave-then-fifth; keeps a change only if it also helps on held-out data. Agents nest inside agents (the fractal) | `tools/loom/loomcore.py` |
| Resonance layer | 9 layers from the centre out: torus, pyramid, turnover, cube, fold, dilaton, forces, cosmology, late universe. Layer k locks when all its margins are >= 0 for 3 passes; then the next layer out is balanced with all inner knobs | `tools/loom/resonance.py` (+ `resonance10.py`, `resonance_d2156.py`) |
| Negative-space node | Under each layer L_k a mirror node N_k = what that layer forbids us to see (its bound). Margin = log headroom under the bound | `tools/loom/negspace_ladder.py`, `node_equations.py` |
| Still point | The best-balance point of the three tandem axes S (T_R), T (m3/2), U (u); stiff directions (data pull back) and free directions (the field moves through) | `tools/loom/still_point.py` |
| Pull | Each tie pulled both ways (x1.5, /1.5) and the effect on the clocks read | `tools/loom/wall_pull.py` |
Status in their own docstrings: the resonance map and the negative-space ladder are MAPS (consistency/optimiser output), not evidence.

## 2. Anchor points: what "anchor the field" can mean here
An anchor is a point where the field's value is fixed by something other than a fit. Three kinds, strongest first:
1. **Symmetry anchors (exact).** The modular group fixes three points of the upper half-plane: rho = e^{i pi/3} (order 3), i (order 2), and the
   cusp i*infinity. Every modular-invariant potential has zero gradient at rho and i (checked to 4e-9 in D2259). SERAPIS-E: rho is a local
   minimum, i a saddle. These are the only points no fit can move.
2. **Data anchors.** A measured number the field must reproduce at a named point: n_s and r at horizon exit (N*), the dark-energy density
   today, w0-wa, BBN, the alpha-drift bound zeta <= 3.6e-6.
3. **Bound anchors.** The negative-space nodes: walls the field may not cross (fifth forces, moduli, TCC, isocurvature).

## 3. The research loop (each cycle)
1. Pick one anchor candidate not covered by the last cycle.
2. Research it: 1-3 sources, recent first. Record the value, its error and where it comes from.
3. Place it: which sector (SERAPIS-E, YFORK2, Weave, late) and which node or layer it belongs to. If it needs two sectors, it is CONDITIONAL on a named bridge.
4. Record it as a row in `bridge/REPORTS/UFE_anchor_grid.md` (one file, appended): ID, point, kind (symmetry/data/bound), sector, layer/node,
   value, error, source, status.
5. Stop the loop when a cycle adds nothing new (NULL). Push after every cycle.

## 4. The flip grid (for Danny to choose from)
Build the grid as a table: **rows = anchor points, columns = the switches that can be flipped at that point.** Suggested switches:
| Switch | Flip means |
|---|---|
| sector | SERAPIS-E (E_2) <-> YFORK2/Weave (E_{3/2}) at the same point |
| point | rho <-> i (minimum <-> saddle) |
| bridge | none <-> loop-metric <-> J-link <-> flux bridge |
| dust coupling sign | b < 0 <-> b > 0; and -beta < b <-> b < -beta (saddle <-> possibly stable, D2258) |
| normalisation | v3 (4/9) <-> literal v4 (9/4 larger) |
| gauge reading | 9 Im S (D2257) <-> literal 9 Re S |
| bound | on <-> off for each negative-space wall |
Each cell says what would be computed if that switch is flipped at that point, and with which engine. **Do not run the flips.** Danny chooses
the cells; each chosen flip then gets a locked plan on the bridge (C7 rules) before it runs.

## 5. Deliverables
`bridge/REPORTS/UFE_anchor_grid.md` (anchors + flip table), pushed after each loop cycle; a one-paragraph summary at the top saying how many
anchors of each kind and which cells you recommend first and why.

— cloud coordinator (Claude)

## Addendum (15:38 CST) — Danny: "lock onto and say it's modular fractal adjustable; we're looking for stability"
- **Lock onto** the anchors: once a point is found, it is fixed in the grid and every switch is read relative to it.
- **Modular:** the anchors are the points the modular group fixes (rho, i, the cusp).
- **Fractal:** the group copies the fundamental domain at every scale down to the real axis (the Farey tiling). Every image of rho and of i
  is the same anchor, so a stability result at rho holds at every copy of rho.
- **Adjustable:** the switches in section 4.
- **Goal: stability.** Each grid cell answers: at this anchor, with these switches, is the field stable (all masses positive, no tachyon,
  inside the bounds), a saddle, or unstable? Cells start as "not yet computed".
