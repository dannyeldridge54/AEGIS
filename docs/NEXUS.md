# Nexus — how every track connects

The hub view for the Janus app and the one-page map of what shares what. Each link is labelled: **physics** (from the theory), **numerics** (same math machinery, no physics claim), **tool** (standard science/engineering), **art** (a sonification/visual mapping, not a claim). Palette as the rest of Janus.

## The rings (tracks)
SERAPIS-E theory · Janus calculators · Toolkits (registry) · Chemistry · Sound/Janus Loops · Power · Sarah's app · CubeMind · The web/ladder · Papers.

## What actually connects them
| From → To | Link | Label |
|---|---|---|
| SERAPIS-E → Janus core (spectra3) | the potential V(φ) feeds N*, n_s, r, α_s | physics |
| SERAPIS-E → exact MS (ms_jit, U1b) | same background, ripple-free α_s | physics |
| Janus core ↔ exact MS | cross-check (TK1: Δn_s ≤ 1.1e-6) | physics |
| Theory → string meter (PW5/PW6) | n_s ↔ Im S·Im ρ (inverse meter) | physics (postulate) |
| All solvers → aegis_tools registry | one shared call surface (12+ tools) | tool |
| registry → Janus app + CubeMind | app runs tools; results → MindMem | tool |
| D-notes → MindMem | every result is a memory record | numerics |
| ODE/root-find/spectra math → Chemistry (PySCF), Power (circuits), Janus-LT recomb | the SAME numerical machinery | numerics |
| Epstein/lattice-sum minimum (hexagonal) → Chemistry (close packing, graphene) | shared lattice mathematics | physics-math shared |
| Spectra, torus y(N), wavelength lines → Sound | data → pitch/rhythm/timbre | art |
| Theory timeline → Matter-formation ribbon | reheating→BBN→recombination→first light | physics (ours) + literature |
| CubeMind (proposer) → Claude loop (verifier) | proposals (HYPOTHESIS) → locked D-notes | numerics |
| Everything → the web/ladder | nodes, status, ripple flags | numerics |
| Verified results → Papers (Zenodo) | only on Danny's "Publish" | — |

## The spine (what the whole thing rests on)
1. **Lock before compute** — every number has a pre-registered test with a hash committed before it ran.
2. **One registry** — the physics tools are called the same way by the app, CubeMind and the eval.
3. **One memory** — MindMem holds the D-notes and tool results; CubeMind learns from it.
4. **Honest labels** — physics vs numerics vs tool vs art, everywhere, so nothing oversells.
5. **Proposer/verifier** — CubeMind may search and postulate; only Claude + the referee turn a proposal into a locked result; nothing self-publishes.

## Not connected (on purpose)
- SERAPIS gives **no** chemistry or energy breakthrough; the Chemistry and Power tracks share only *math*, never a physical claim.
- Astrology/tarot in Sarah's app are **traditions**, not astronomy; the real sky underneath is computed.

_Built by the X slot of the loop; kept in step with docs/HANDOFF_LOOP.md. A 3-D Nexus view (rings + glowing link threads that light when a tool runs) is the next X pass._
