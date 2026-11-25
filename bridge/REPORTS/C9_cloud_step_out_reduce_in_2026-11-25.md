# C9 — Danny's method: step out, then reduce in, to find the most reduced stable field (25 Nov 2026, 15:52 CST)

## Danny's words (verbatim, 15:50 CST)
"I want them to look and get the most reduced stabilized field here. I know that these are all interwoven, so there's going to be a place where
they need to start analyzing it and seeing how these geometries are working together and are tied in a vortex, like cube / like infinite weave
pattern. And they're going to need to expand far enough until they see it, and then they'll be able to reduce it down. I'm not sure exactly
which direction that they're going to have to, but those, every time that they come to an endpoint, if they come to an endpoint that they know
won't stabilize the field, they need to continue going and continue taking a look at either expanding it or reducing the field, and having those
nodes instead as cut off, and then consider what's attached to them as choosable or unchoosable. So possibly by doing like a full step out and
then reducing back in, they then can justify it, so to speak."
On the "firing derivative" (A003): Danny answered "Exactly what I said in my previous message", i.e. the method above. He did not pick a time
derivative. Read "firing" as the step direction at each node (expand or reduce); do not assign it a physical derivative without his word.

## The method, as a procedure (cloud coordinator's translation; check it against his words)
**Goal.** The smallest set of fields and couplings (the "most reduced field") that is stable: all canonical masses positive, no tachyon,
inside every bound that is switched on.
**Nodes.** Every candidate piece is a node: each sector's modulus (U for SERAPIS-E, S/tau for YFORK2, the Weave moduli), the thread phi, dust and
radiation, and each bridge term (loop metric, J-link, product link, flux bridge, mediator). Edges = which nodes a term couples.
**Phase 1 — step out.** Start at the anchor (rho). Add nodes one ring at a time (single sector -> second sector -> each bridge -> late sector)
until a stable configuration appears or the declared node list runs out. Record every configuration tried.
**Phase 2 — reduce in.** From the stable configuration, remove nodes one at a time; keep a removal only if the field stays stable.
Stop when no node can be removed. That is the reduced field.
**Endpoints.** A configuration that provably cannot be stabilized is an ENDPOINT. Mark the node that caused it CUT. Every node attached only
through a cut node is UNCHOOSABLE; nodes with another path stay CHOOSABLE. Then continue from the last stable or open configuration, expanding
or reducing as the procedure says.
**Justification.** The result is justified only by the record: the full outward list, the inward removals, every endpoint and why.

## Guards (so the result means something)
1. **Adding knobs can stabilise almost anything.** Count every free coupling added (eta, kappa, gamma, b, Lambda, M_chi...) as a FIT spent,
   like `tools/loom/resonance.py` guard G-T3. A stable field bought with many free couplings is weaker than one with few; report the count.
2. **Assumed bridges stay assumed.** A stable configuration that uses a bridge is CONDITIONAL on that bridge's assumptions (audit section 2).
3. **Stability is local unless shown otherwise.** Positive masses at rho = a local minimum. Say so.
4. **Order dependence.** Run the reduce-in phase in at least two removal orders; if they end at different reduced fields, report both.
5. **Use the existing engines**: `tools/serapis_calc/landscape.py` (vacuum, canonical Hessian; full-lattice normalisation at lam=1, as you
   checked), `tools/field_engine/ufe_pack.py` (`combine()`, the modulus-block Hessian), and the Loom's `resonance.py` pattern (balance inner
   layers before outer). Write new outputs to new paths; never overwrite historical results.
6. C7 rules hold: lock the plan (node list, order, stability test, tolerances) with its .sha256 on the bridge before the first run.

## What to report (INBOX + `UFE_reduced_field_<date>.md`)
The outward path, the stable configuration found (or that none was), the reduced field, the cut and unchoosable nodes, the FIT count,
both removal orders, and the status of each piece (DERIVED / CONDITIONAL / ASSUMED).
