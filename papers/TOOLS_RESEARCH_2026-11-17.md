# New tools that fit the Janus method (fast face + exact face, locked comparison) — research 17 Nov 2026

The Janus method = a fast approximate route that is only trusted after a locked comparison with an exact reference. Three outside tools follow
exactly that pattern and fit our gaps.

## 1. Speculative decoding for CubeMind (Janus inside the LLM) — HIGHEST VALUE
A small "draft" model guesses several tokens; the big model checks them in one pass and keeps only what it would have produced itself. Output is
identical to the big model alone (lossless), typically 20–50% faster (same-family pairs, e.g. Qwen2.5 0.5B drafting for Qwen2.5 14B; ~0.6–1.1 GB extra
VRAM; 5–8 draft tokens). [insiderllm.com guide, Feb 2026] Not exposed in Ollama yet (GitHub issue #4643); available in llama.cpp (`-md`), LM Studio, vLLM.
Janus check we can lock: same prompts → token-identical answers with and without the draft, plus measured speedup on the 300-item suite.
Needs: llama.cpp server on the PC + a 0.5B draft model download (Danny's OK — desk item).

## 2. Stop Ollama model swapping (cheap, immediate)
M1 runs at ~2 min/item because the grader and M1 use different models and Ollama swaps them. Ollama keeps up to OLLAMA_MAX_LOADED_MODELS models
loaded (default 3, or 3 × GPUs) only if they fit in memory; unused models unload after OLLAMA_KEEP_ALIVE (default 5 min); OLLAMA_NUM_PARALLEL
(default 1) requests per model. Set on Windows as user environment variables, then restart Ollama. [docs.ollama.com FAQ] With models of 9–18 GB the
limit is GPU memory, so the real fix is scheduling: don't run two different Ollama models at once (pause the grader while M1/M2/P7 run, or run them
on the grader's current model). Proposed: a runner rule "Ollama jobs run one at a time, between grader cycles".

## 3. Emulators for Janus-LT / Hyperion (Janus for Boltzmann codes)
CosmoPower (arXiv 2405.07903): neural emulators of CAMB/CLASS — CMB spectra sub-percent, P(k) a few percent, background/derived quantities;
~0.1 s vs ~20 s per CAMB call (chains ~20 min vs ~10 h); pre-built ΛCDM, +N_eff, +Σmν, +w0wa; validation against held-out CAMB runs and full-posterior
comparisons; can be trained on a customised Boltzmann code. Fit for us: an emulator of our own torsion/F(a) expansion histories would be the fast face, CAMB
the exact face, with a locked accuracy test (e.g. within 10% of cosmic variance) before any chain uses it. Caveat from the paper: the w0wa emulator has
small-scale CMB outliers up to ~80% of cosmic variance — exactly why the lock matters.
Related: Capse.jl (arXiv 2307.14339), differentiable CMB emulation in Julia.

## Recommended order
1) Ollama scheduling rule (no install, frees M1/M2/P7 now). 2) Speculative-decoding test S1 on the PC (needs a small download → Decision Desk).
3) CosmoPower trial on Janus-LT (pip install; compare its w0wa background quantities with L7/L10 on a locked grid).
