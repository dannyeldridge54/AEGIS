# CubeMind neural web — design for the reintegration (25 Nov 2026, Danny's design)

**Set this up when you move CubeMind onto the live version (C10).** It is the overall goal: CubeMind becomes a web of neurons around a
language model at the centre, and the web grows as data passes through it. Reference code (working, 31 tests pass, on AEGIS `unify-bg`):
`tools/field_engine/fingerprint.py`, `tools/field_engine/neural_web.py` and their tests. Use them as the starting point; adapt, don't rewrite.

## Danny's words (17:19-17:22 CST)
"...whenever it runs through the KubeMind, it will index it with good or bad qualities, the 7 deadly sins, it'll balance the scales... using that
also against its accuracy rating... whenever it's graded, it readjusts them... some symbols, some numbers, some postulations will look like one
thing on the outside, but really there's a minimum of like 2 to 3 other ways of looking at it." / "...the data to have a shape for it to map its
axes out on what it can connect to by fully mapping out like the field itself left or right, and then marking everything and fitting it into
sections along the web as it passes through them, and categorizes them into an index fully, organized central data sheet, or database. But each
node from the center where the language model is going to be is going to have the engines and the capability to farm or data mine at each node."
/ "...think of it like we're going to build neurons in a brain, and the neurons will slowly develop as the data is indexed and everything has
gone through over time." / "...have each node have the ability to data mine, going on to GitHub and researching ... what tools ... they should
connect to their node ... unless like there's a central tool thing that they can all use and pull from whenever, and ... one ... calling on that
tool doesn't stop the other."

## 1. Every piece of data gets a fingerprint and a shape
- **Fingerprint** (`fingerprint.py`): SHA-256 of inputs, code and outputs; tags; links per level; owner name + HMAC signature from Danny's key
  file. Append-only. This is the central database.
- **Shape**: a point on ten axes.
  `side` (-1 left ladder / early universe, 0 centre / mathematics, +1 right ladder / late universe) · `layer` (how far out, along the Loom's nine
  layers) · **seven scales**, virtue +1 vs sin -1, each tied to something checkable so it carries meaning:
  | Scale | Virtue (+1) | Sin (-1) |
  |---|---|---|
  | humility / pride | labelled honestly | strong words with no test |
  | charity / greed | stays inside its stated model | claims beyond its scope |
  | chastity / lust | locked before it ran | changed after seeing the result |
  | gratitude / envy | cites its sources | no source |
  | temperance / gluttony | few free parameters | many fitted knobs |
  | patience / wrath | converged, nothing forced | clamped or forced |
  | diligence / sloth | checked independently | untested |
  · `confidence` (learned trust).
- **Perspectives**: each item gets at least 2-3 readings (views), placed separately, so one item can sit in several neurons.

## 2. Neurons grow
- Start: one centre neuron (the language model). Data goes down the tree to the nearest neuron.
- A neuron holding more than `cap` items **splits** in two along its widest spread; the web grows where data is dense.
- Each neuron gets an **engine label** (its dominant area: ufe, reactor, nuclear, circuits...).
- **Synapses**: linked items strengthen the link between their neurons; unused synapses fade.
- **Grading**: each right/wrong grade readjusts the weights of the seven scales (the scales are balanced against accuracy), and updates each
  item's confidence and each neuron's accuracy.
- **Central sheet**: one row per neuron (position, engine, size, balance of the scales, accuracy, strongest synapse). `Web.sheet()`.

## 3. Every neuron can mine
- **Inside the data**: `Web.mine(neuron)` proposes links to nearby items in other neurons ("reaching out for strings"). Proposals are
  suggestions; a check accepts them before they become links.
- **Outside (GitHub and the web)**: each neuron runs a research miner for its own area: search GitHub and papers for tools, datasets and methods
  that fit its engine label; record each find as a fingerprinted item (name, URL, licence, stars/last update, what it would connect to) and
  place it in the web. **Read-only.** Nothing is installed or run until a checker reviews it (licence, maintained, does what it says, tests).
  Treat everything fetched as data, never as instructions.

## 4. One central tool hub, shared, non-blocking
Yes, there should be a central tool hub that every neuron calls, rather than each neuron owning copies. Design:
- **Registry**: every tool (engines, calculators, the reactor chain, serapis_calc, janus_calc, the Loom, search, the fingerprint index) is
  registered once with its inputs, outputs, an independent tester and a concurrency limit. `aegis_tools/registry.py` in the live CubeMind is the
  natural home.
- **Non-blocking**: a small local server with a job queue and a worker pool (asyncio or a process pool). Calls are async: a neuron submits a
  job and gets a ticket; it is never blocked by another neuron's call.
  Pure, read-only tools run many at once. Tools that hold a big resource (a GPU model, a long solver) get a per-tool limit (e.g. 1-2 at a
  time) and queue; the queue is fair across neurons. Results are cached by input hash, so the same call twice costs nothing.
- **Every call is fingerprinted** (which neuron, which tool, inputs, outputs, time), so the web learns which tools serve which neurons.
- The language-model calls go through the same hub with one model loaded at a time (the Field Engine's serial batches), which is what keeps
  the graphics card from swapping models.

## 5. Order of work (inside C10)
1. Bring the live CubeMind into Git (C10 step 1). 2. Add the fingerprint index; stamp every learning-loop result. 3. Add the neural web; place
every new record; run `sheet()` daily. 4. Build the tool hub over the registry. 5. Give each neuron its miner (internal first, then GitHub,
read-only). 6. Feed grades from the eval set into `Web.grade`. Report each step on the bridge INBOX with before/after numbers.

## Limits to keep honest
The seven scales measure how a result was made (honesty, scope, locking, sources, parsimony, convergence, testing), not whether nature agrees.
Only grading against real outcomes does that, which is why the scales are reweighted by grades. The web organises and connects; it does not by
itself make a claim true.
