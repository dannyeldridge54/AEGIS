# Forge research loop (3-minute ticks, from 22 Nov 2026 01:47): optimisation hints per node. Research only; the Forge compute stays paused.
**Rule:** one research cycle per tick. Each find is filed under the Forge node it serves. The loop stops after a NULL tick (no new usable hint).

## Tick 1 (01:47): fx2-cmix code review (github kaitz/fx2-cmix) and Micro-Diffusion (arXiv 2603.08771)
| node | hint (source) | our status | try as |
|---|---|---|---|
| word node | **four word streams**: raw, sentence-stemmed, paragraph-stemmed with function words filtered, fully stemmed. Word limit 256; new word types (article, conjunction, adposition, conjunctive adverb) | one word node + word pair | `WSTEM` knob: add a stemmed-stream node (admission rule: independent info) |
| word node | words dropped from streams 2–3 inside templates, tags, links and parentheses | we have markup and closing-stack nodes | gate the stemmed stream by the closing stack |
| match node | **sparse match model**: gap 1–2 bytes, minimum length 3–6 (mostly escaped UTF-8) | dense match + reps | `SPARSE` node |
| mixer | **skip weight updates when the error is below a threshold** (speed); regulariser removed | always update | `ESKIP` knob, a speed rung |
| mixer | **dictionary index of the partly decoded word as a mixer context** | mixer contexts: c0, match state, event state | `DICTX` context in MV |
| hash tables | slot size chosen by memory: 32 / 64 / 128 B | fixed slots plus confirm-2 | the table ladder already gave −1.75%; a slot-size rung is next |
| state tables | generated at runtime; one table replaced | lpaq-style adaptive StateMap | low priority |
| preprocessing | single-pass Wikipedia transform; HTML entities → UTF-8; math/pre/nowiki detection | prep2 (capital flag + dictionary: the dictionary hurt, +1.9%) | an entity transform is cheap: try it |
| ordering | articles reordered by an embedding plus 1-D t-SNE, clustered, then reversed | none | big known lever (topic locality); needs an embedding we can run locally (permission + compute) |
| final calibration | **Tweedie / James–Stein calibration as the last layer**: +2.6–2.8% in their PPM setting; it **competes with SSE** (stacking hurt) | two APMs | `TWEEDIE` as an APM *substitute*, not an addition |

**Tick 1 verdict:** not null (10 hints).

## Tick 2 (07:52Z): CPU speed and memory (cmix-hp README; SIMD survey 1502.01916)
| node | hint (source) | our status | try as |
|---|---|---|---|
| ppm/order nodes | **one large order-25 PPM model swapped to disk via mmap** (the "most substantial" cmix-hp change; slower) | hashed orders 0–6, TB24 in RAM | a disk-backed TB26+ rung if RAM caps us (the PC has more disk than RAM) |
| mixer | **export fewer predictions to the final mixer; drop weak mixers** (speed; v3 restored two for compression) | MV bank of 8 shadows | prune shadows with near-zero selection (ledger) — a speed rung |
| memory | rebalance memory toward the word model | equal TB per node | per-node TB sizes as knobs (word bigger) |
| mixer maths | SIMD dot products (AVX2) for the mixers (1502.01916; paq8px uses SSE2/AVX2) | scalar C loops | `-O3 -march=native` first, then intrinsics — a speed ladder to null |
| build | PGO + LTO single build with a shipped profile (cmix-obias, tick 0) | plain -O2 | `-fprofile-generate/-use`, bit-exact check |
| **result folded in** | **D2025 PASS: clocked ring bus (RCTX) −0.20% / −0.21% on 1 MB / 3 MB; bypass traces nothing at scale** | — | next build: RCTX on, SKIP off |

**Tick 2 verdict:** not null (5 hints + 1 result).
