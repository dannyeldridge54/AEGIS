# The Field Machine — integration plan (24 Nov 2026)

Working name only; Danny has not chosen a name. Goal: the field, the tools and the full record packaged in one machine that runs on
Danny's PC with no internet, answers by look-up and computation, and labels every claim with its status.

Status labels in this file: DONE = built and tested here; BUILT-UNTESTED = code exists, never run on real local models;
PLANNED = not built. The PC was offline when this was written, so nothing below has been measured on it.

## 1. The shape: one centre, four rings
```
                 question / next point
                        |
                 [ CubeMind centre ]  planner, lock, ledger, librarian   (code)
                  /      |        \
        LOOK-UP      DERIVERS      TOOLS
     knowledge pack  2 local models  registry + reactor chain + field tools
     (search, no LLM) (blind, k samples each)  (compute, no LLM)
                  \      |        /
                 [ CHECK ]  fitter + independent tester, test wire          (code)
                        |
                 answer + status label + ledger entry
```
Rule for every question: (1) look it up; (2) if it is a number, compute it with a tool; (3) only then ask the models, blind and
independently; (4) code checks; (5) the answer carries its label (PASS / FAIL / ESTIMATE / UNTESTED / model-only).
Why: CubeMind's own memory quiz scored 0.20 from model memory and 0.75 from look-up.

## 2. What changed in the engine today (v2) — DONE, 11 tests pass with mock models
| Change | Why (source) |
|---|---|
| Each model answers each point k = 3 times on its own; its answer is its most common value, its confidence the share that agree | SLM-MUX: debate between small models lowered accuracy by up to 5.5%; independent sampling plus confidence selection gained up to 6.7% over the best single model |
| The engine's own answer = the most confident model's answer (ties: better track record); its accuracy is logged beside single-model accuracy | same; and the boosting paper: the selector, not the number of samples, is what recovers the gain |
| Samples capped at 3 | boosting paper: doubling 8 to 16 samples moved the ceiling 79.0% to 79.2% |
| Batches: lock several points, then model A answers all, then model B | a card that cannot hold both models loads each once per batch instead of once per point; CPU-resident layers run about 10x slower |
| A batch covers different tools | keeps coverage; no tool is asked twice in one batch |
| Ollama is asked for JSON matching a schema | no unparseable replies, fewer wasted retries |

CAUTION, kept on purpose: CubeMind's Phase 5 test found that picking by a model's *stated* confidence lost to the agreement gate.
The v2 confidence is different (how often a model repeats its own answer), but it is unproven on these models. So the agreement
gate stays the trust signal, both numbers are logged, and the first real run decides which is kept. No claim until then.

## 3. Build order for CubeMind (each step is small and testable)
| # | Piece | What it is | Status |
|---|---|---|---|
| 1 | Engine v2 | above | DONE (mock) / BUILT-UNTESTED (real models) |
| 2 | First real run | `Field_Engine.bat` on the PC, 40 points; records speed, single-model accuracy, selected accuracy, agreement gate | waits for Danny |
| 3 | Ollama settings | flash attention on, cache type q8_0, models kept loaded; parallel slots only if memory allows (each slot multiplies context memory) | PLANNED; changes a system setting, needs Danny's OK |
| 4 | Knowledge pack | one SQLite file: every D-note, lock, result, paper and catalog split into 256-512 token pieces, each with its status label and source path; keyword index (FTS5) first, vectors added second, fused by rank | PLANNED |
| 5 | Look-up before models | CubeMind's ask path queries the pack first and quotes the source and label | PLANNED; needs its own lock (the memory fix) |
| 6 | Tools as callable steps | the CubeMind registry tools get the same (fitter, independent tester, tolerance, range) line as the 8 starter tools; a tool with no independent tester is not added | PLANNED |
| 7 | Test wire in a scratch copy | all section tests run before the engine starts; areas with failing tests are held back | BUILT-UNTESTED (first full run overwrote tracked files; restored) |
| 8 | Locked exam | a held-back question set, locked before the run; the machine ships only if it beats C+ (about 65%) with look-up on | PLANNED |
| 9 | Package | one folder: models, pack, tools, console .exe; hash list and signed release | PLANNED |
| 10 | Fine-tune | a small adapter, only if step 8 shows look-up falls short; its payoff is speed (a tuned 8B matched an untuned 14B at a third of the memory), not knowledge | LATER |

## 4. Encoding the field itself
The field enters the machine three ways, in this order of trust:
1. As TOOLS — each derived relation with a formula becomes a fitter with an independent tester (two derived relations are in
   already: the Koide ratio and the plateau tensor ratio). This is the strongest encoding: it cannot drift.
2. As RECORDS in the knowledge pack — the derivation text, with its label. The local agents' five-field model enters here as
   "derived, untested, no common compactification yet".
3. As LESSONS — worked steps the models got right, fed back as hints. Weakest: helps the models, proves nothing.
Nothing derived-but-untested is ever stored without that label.

## 5. Speed, in order of expected gain (all unmeasured on this PC)
1. No model swapping: serial batches (done); confirm with `ollama ps` that each model shows 100% GPU.
2. Fewer model calls: look-up and tools answer first; the cache answers repeats.
3. Right-sized context: the memory is reserved up front; oversizing pushes layers onto the CPU.
4. Ollama flags (step 3 above). Ollama itself costs about 3-10% against raw llama.cpp: not worth a switch.
5. vLLM is ruled out: its gain is at many simultaneous users on data-centre cards; single-user speed is comparable.

## 6. Sources
- SLM-MUX: Orchestrating Small Language Models for Reasoning — arXiv:2510.05077
- Agentic Systems as Boosting Weak Reasoning Models — arXiv:2605.14163
- Searching for Best Practices in Retrieval-Augmented Generation — arXiv:2407.01219
- HPC-LLM: Practical Domain Adaptation and RAG — arXiv:2605.16347
- Ollama FAQ — https://docs.ollama.com/faq.md
- Red Hat, llama.cpp vs vLLM (15 Jun 2026) — https://developers.redhat.com/articles/2026/06/15/llamacpp-vs-vllm-choosing-right-local-llm-inference-engine
- Ollama speed guide — https://runaihome.com/blog/ollama-slow-speed-up-tokens-per-second-2026/
- Hybrid search in one SQLite file — https://dev.to/soytuber/building-a-hybrid-rag-in-200-lines-sqlite-fts5-sqlite-vec-rrf-38h1
