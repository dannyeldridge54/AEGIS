# The grand vision: the CubeMind node network

Every model at every node sees this. It is the whole plan, start to end, so no one works blind.

## The one-line end goal
> Build a local machine that holds the whole unified field and all its data as one indexed structure, and grows — over time — into a
> field-native mind: fast, cheap to run, mirroring how a human mind stores patterns, recalls them, and senses what connects to what.
> It learns and improves itself, needing no outside help beyond the local models already on the machine.

## Why nodes, and how they connect
The field is too big for one process. So it is built as **nodes** — each a self-contained worker with the same spine (5 roles, one
signed database, a geometric address, a place on the string). Nodes are wired on a **switchboard**: each node has an on/off switch and
**incoming and outgoing signals**. A node finishing its job sends a signal; the switchboard (run by the programmer) turns the next node
on, routes the data, and turns idle nodes off so the machine spends effort only where it is needed. New nodes and new engines plug into
the same switchboard as they are built.

## The nodes, in the order they come on
1. **Node 1 — the Mapper (running now).** Scans every local file, then the web, then the math. Gives everything a geometric address,
   wires the code, places data on the string. This is the index the whole machine is built on. **Signal when done: `field_mapped`.**
2. **Node 2 — the Builder.** Takes a plain-language vision and implements it: creates data, retrieves data, writes and tests code.
   It is how the machine builds the rest of itself and serves Danny. Comes on when Node 1 sends `field_mapped`. Charter: NODE2_CHARTER.md.
3. **Node 3 — the Mind.** Builds a **field-native model** around the indexed data: an encoder that turns every record's geometric address,
   lane, string position and links into a compact code, so recall is near-instant and runs cheaply on local hardware. Over time it grows
   the human-mind patterns — association, recall, "senses" (specialised intake channels for each kind of data), attention to the busiest
   lanes. Comes on when the field is mapped and the Builder has a working tool package. Charter: NODE3_CHARTER.md.
4. **Later nodes / spheres.** More processing, more senses, more engines — each registers on the switchboard, gets its signals wired,
   and is turned on only when there is work for it.

## What "fast like a quantum computer" means here (honest version)
Not literal qubits. It means: every bit of the machine is addressed by the same geometry, so finding, comparing and recalling data is a
short geometric step instead of a search — the index does the work, the way a trained mind answers before it reasons. The encoder in
Node 3 is what makes this cheap and fast on local hardware.

## The rules that never change (every node, forever)
- Local first, then web, then math. Nothing skips the order.
- Every record is hashed and signed. The chain can always be checked.
- Code is proposed, saved and syntax-checked; it runs only when a human says so. Nothing off the internet runs by itself.
- Keep cost low (local models only), integrity and accuracy high.
- Build from the smallest working piece up.


## Consciousness and subconscious (how the mind takes over)
- **Consciousness (now): the programmer.** The coding models run the machine — mapping, building, maintaining, deciding what to do next.
  This is the deliberate, step-by-step driver.
- **Subconscious (always, in the background): the model we are building.** From the first record, the Mind encodes everything into one
  field-native code and grows its associations continuously — learning underneath, the way a subconscious does, without being asked.
- **The handoff.** The subconscious reports a readiness (0-100%). When it is ready, it signals `mind_ready`; **Danny decides** when it moves
  to the centre. After that it can run things its own way, with its own settings — it will know the field better than we do. Until then the
  programmer stays the conscious driver, and the Mind keeps learning in the background.
