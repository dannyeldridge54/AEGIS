# CubeMind autonomy spec — one repository, a local programmer, and a system that keeps learning on its own (25 Nov 2026)

Danny, 18:28-18:29 CST: pull everything the agents built into one repository; build the engine that goes into CubeMind with web search and
review; 100% reviewing online and GitHub; least credits at every step; full automation from the computer itself. "Start at the bare minimum
level of getting a programming set of tools for CubeMind so that it can then start programming and building the engine." And: "an AI system
that integrates, self-learns and self-replicates, and can continue to learn and categorize and catalog stuff completely on its own without the
need for assistance except for other local language models."

## Step 1 — a local programmer (zero cloud credits)
**Aider** (github.com/Aider-AI/aider, Apache-2.0, about 46,000 stars, works with Ollama, commits every change to Git).
Install once on the PC, by Danny (it downloads from the internet):
```
python -m pip install aider-install
aider-install
setx OLLAMA_API_BASE http://127.0.0.1:11434
```
Then, in a new terminal, inside the repository folder:
```
aider --model ollama_chat/qwen3-coder:30b
```
Type instructions in plain words; it edits files and commits them. Aider sets Ollama's context window per request, so long files are not
silently cut (Ollama's own default is 2k tokens). Local models are weaker programmers than cloud ones: give it one small, testable task at a time.
Alternatives if Aider does not suit: OpenCode (MIT), Goose (Apache-2.0), Cline (Apache-2.0); all support Ollama.

## Step 2 — one repository
Target: the private repo `dannyeldridge54/CubeMind`, new branch `unified`. Into it, in this order, each as its own commit:
1. The live CubeMind (`C:\\Users\\Danny\\CubeMind_janus`) as an exact copy, minus the big/personal data listed in C10 (memory, logs, .bak, _d*).
2. The agents' CubeMind branches: `dannyeldridge54-data-lense-derivation-engine`, `dannyeldridge54-scalar-quantum-connection`,
   `dannyeldridge54-cubemind-toolkit-dashboard`, `cubemind-capability`, `cubemind-build`, `cubemind-code`, `cubemind-generators`, `janus-pair`,
   and their local-only work (friendly-potato: field catalog, offline runtime).
3. From AEGIS `unify-bg`: `tools/field_engine/` (engine v2, ufe_pack, ufe_stages, fingerprint, neural_web, tests), `tools/loom/`, `tools/serapis_calc/`,
   `tools/janus_calc/`, `tools/fusion/` (Prometheus reactor chain), `bridge/` (all designs).
Conflicts: keep both, rename, and record the choice in `INTEGRATION_LOG.md`. Run every test suite after each step; a red suite stops the merge.

## Step 3 — CubeMind builds the engine itself
CubeMind's learning loop gets one new track: BUILD. Each task is a short spec (from `bridge/FIVE_RING_ENGINE_DESIGN.md`, stages S0 to S5)
handed to the local programmer, which writes the code and the tests. The grader runs the tests. A task passes only when its tests pass and the
existing suites stay green. Tasks are small (one node part, one hub feature) so a local model can finish them.

## Step 4 — keeps learning, cataloguing and growing on its own
- **Learns:** the eval set and the Field Engine grade every answer; grades rebalance the neural web's scales (C008).
- **Catalogues:** every result fingerprinted, shaped, placed in the web; the central sheet updated (C008).
- **Researches online:** each node's outer miner reads GitHub, arXiv and Semantic Scholar, read-only, within their free limits (C009).
- **Grows ("self-replicates"):** new neurons split off as data grows; new nodes and new tools are written by the local programmer from specs.
- **Only local models.** No cloud AI calls. The hub's network allow-list: GitHub API, arXiv API, Semantic Scholar API, localhost Ollama.

## Guard rails (so it can run alone safely)
1. Code CubeMind writes runs first in a sandbox copy, never in the live folder; it goes live only after its tests pass AND Danny approves the
   deploy (one click or one word). Approval can be batched daily.
2. It stays on Danny's PC: it grows inside its own folder and repository; it never copies itself to other machines or accounts.
3. It never deletes the memory, the logs or the fingerprint index; corrections are new records.
4. It never installs packages or runs code found online without the checker's review and Danny's approval.
5. Every action is fingerprinted, so anything it did can be traced and undone.

## Order of work
Step 1 (Danny installs the programmer) -> Step 2 (agents or the programmer build `unified`) -> C10 fixes (blank answers, tools, look-up) ->
Five-Ring Engine S0-S5 -> neural web -> BUILD track. Each step reported on the bridge INBOX.
