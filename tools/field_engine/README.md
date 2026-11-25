# AEGIS Field Engine — design and wiring (24 Nov 2026)

One loop that covers the field map, pushes outward from points it has mastered, and corrects and teaches itself. CubeMind sits at the
centre as planner, record keeper and referee; language models sit on the axes as derivers. Code in `engine.py`, tests in `test_engine.py`.

## The roles (what was added to lenser / fitter / deriver)
| Role | Job | Done by |
|---|---|---|
| Planner | picks the next point: weakest area first, then one ring further out where mastery is solid; 15% random exploration | code |
| Lenser | frames the point: task, inputs, tolerance, pass rule | code |
| Lock | hashes the frame into the ledger before any model is called | code |
| Derivers (the axes) | two or more models derive the number blind, in parallel | LLMs |
| Fitter | the validated tool computes the reference value | code |
| **Tester** | an independent method or invariance check must agree with the fitter, or the point is void | code |
| Referee | scores each deriver; records whether the derivers agreed with each other | code |
| Corrector | one retry on a miss, told the kind of error, never the answer; logged | LLM |
| Librarian | keeps worked steps and pitfalls per tool, feeds them back; tracks mastery | code |
| Auditor | hash-chained ledger: every attempt kept, tampering detectable (`verify_ledger`) | code |

## Why it is wired this way (from the research)
- Models propose, code verifies. Surveys of autonomous research agents find most closed loops grade themselves on internal metrics and
  that model-judging-model favours persuasive over true answers. Here the outside check (fitter + independent tester) decides.
- Agreement is the trust signal. CubeMind's own Phase 5 test: accuracy 97.7% when two models agree; confidence-picking lost.
- Pre-register and log everything: lock before the call, every attempt and retry in the ledger, no silent discards.
- Generate / debate / evolve with asynchronous tasks (the Google co-scientist pattern) maps to derivers / referee / planner rings.

## Speed
- asyncio: all derivers for a point are asked at once; tools run in-process (microseconds).
- One semaphore per model (ENGINE_PARALLEL, default 2) so calls queue per model instead of making Ollama swap models in VRAM.
- Answers cached by prompt hash; `keep_alive` 30 min keeps models loaded; short JSON-only prompts, 500-token cap.
- Ollama side: set OLLAMA_NUM_PARALLEL=2 and OLLAMA_MAX_LOADED_MODELS to the number of axis models that fit in VRAM together;
  parallel slots multiply context memory, so prefer two small models that both stay loaded over one large one that swaps.
- Standard library only: nothing to install.

## Run
    python engine.py --models qwen3:14b qwen3-coder:30b --cycles 40 --home field_engine_data
    python -m unittest -v test_engine        (no models needed)

## Adding a field
Add one line to TOOLS: area, task text, fitter, independent tester, tolerance, and an args builder that widens with the ring number.
A tool without an independent tester should not be added.

## Limits
The points are numeric derivations with a known reference; open-ended theory building still needs the lock-referee process with a
human or cloud reviewer. The eight starter tools are small; the CubeMind registry tools can be added the same way.
Tested with mock models only as of 24 Nov 2026 (8 tests); first run on real local models is still to do.
