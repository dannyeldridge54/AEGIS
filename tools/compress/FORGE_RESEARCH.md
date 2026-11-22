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

## Tick 3 (07:58Z): the LSTM / byte-mixer node on CPU (NNCP paper; cmix deepwiki; cmix-obias)
| node | hint (source) | our status | try as |
|---|---|---|---|
| **new node: byte-LSTM** | **NNCP small model** (Bellard): 3 LSTM layers × 90 cells, ~542k params, online single pass, truncated BPTT of 20 steps, batch 16, **layer normalisation (a noticeable gain)**, bounded cell output; **1.64 bpb on enwik8 alone at ~42 kB/s on one core** | none (all our nodes are counts) | an `LSTM` node fed into the final bank. It carries **independent** information (a learned state), so it passes the admission rule. Cost: enwik8 ≈ 40 min, enwik9 ≈ 6.6 h (inside the 50 h budget) |
| LSTM optimiser | cmix: Adam with β₁ = 0.025, β₂ = 0.9999, ε = 1e-6, step-based adaptive learning-rate decay | — | copy as the LSTM node's defaults; ≤ 9 knobs (cells, layers, horizon, learning rate, β's) |
| speed for the LSTM | small-matrix-multiply kernels plus a batch of 16 drove NNCP's speed-up | scalar C | SIMD kernel first (tick 2) |
| obias prior gate | cmix-obias: a PPMd prior on the byte-LSTM (g = 0.15) and a 23 kB offline fp16 correction head. **The details are not public on the model page** (they are in SUBMISSION.md, unreadable from here) | — | NULL for now; revisit if the source is attached |

**Tick 3 verdict:** not null (3 hints; 1 NULL item).

## Tick 4 (08:03Z): Wikipedia structure models (Mahoney's enwik8 test-data notes; cmix enwik9 preprocessing)
| node | hint (source) | our status | try as |
|---|---|---|---|
| **revision-header node** | ~3.2% of enwik8 is outside `<text>`: XML headers and revision metadata. revision / contributor / timestamp fields repeat ~487k times in enwik9 | HDR node (off) | a field-aware header model: predict each field from the same field in the previous header (timestamps are near-monotone, ids increment). Re-test HDR with **field-delta contexts** instead of raw bytes |
| **table / column node** | tables {…} ~2.5%, with separations of ~20–80 bytes "typical of tables"; US-township census articles form a highly compressible block | column node (on) | add a **row-stride context** (distance to the previous `\|-` / `\|` cell start) |
| templates | {{…}} ~2.0% | markup + closing stack | a template-name context: the first word after `{{` keys the rest |
| links | internal [[ ]] ~2.9%, external ~2.2%, language links ~2.4% | direction / class node | a link-target node: the hash of the text since `[[`, reset at `\|` or `]]` |
| entities | `&…;` ~2.7%. cmix converts named entities and `&#xxx;` to UTF-8 (hent / hent5) before modelling | none | entity → UTF-8 transform in prep (cheap, reversible); same as tick-1 hint, now with a size estimate |
| ordering | cmix enwik9 reorders articles by a fixed sequence; redirects are kept in a map | none | as tick 1 (needs an embedding) |
| numbers | digits '1' and '0' each appear > 5M times in enwik9 | NUM node (off) | NUM with **digit-position-in-number** and **previous-number delta** contexts (years, coordinates) |

**Tick 4 verdict:** not null (7 hints, sized by the share of enwik8 they cover).

## Tick 5 (08:09Z): priming and dictionaries within the Hutter rules (hutter1.net prize page)
| node | hint (source) | our status | try as |
|---|---|---|---|
| rule | **S = S1 + S2**: the compressor and the archive both count; `archive.exe` must rebuild enwik9 "with no other input"; decompressors "receiving any kind of outside information are forbidden" | — | **every embedded dictionary, weight file or priming text is paid for in bytes.** A primer only helps if it saves more than its own compressed size |
| limits | ≲ 50 h, **1 core**, < 10 GB RAM, < 100 GB disk; no GPU | TB24 fits | the **100 GB disk** limit makes the mmap/disk-backed model (tick 2) legal and cheap |
| dictionary | past winners (paq8hp*) used a dictionary built **from enwik8 itself**; cmix/fx2 ship a compressed dictionary inside S1 | prep2 dictionary hurt (+1.9%, D2015) | rebuild the dictionary as fx2 does (word types, frequency-sorted, reverse transform at decode) and **count its bytes**; the +1.9% was our build, not the idea |
| priming | a small offline-trained head (cmix-obias, 23 kB fp16) is allowed because its bytes are counted | none | any trained weights must beat their own size: a gate for the LSTM node (tick 3) |
| unknown | the detailed rules page (hrules.htm) was not readable here | — | Danny can attach it if needed |

**Tick 5 verdict:** not null (4 hints + 1 unknown).

## Tick 6 (08:15Z): counters and secondary estimators (ZPAQ spec v2.02)
| node | hint (source) | our status | try as |
|---|---|---|---|
| **ISSE chain** | **ISSE:** each order's bit history selects a 2-weight mixer (w₀·p_prev + w₁·64) that **refines the previous order's prediction**. A chain of ISSEs with rising order ("PAQ9A = a cascade of ISSE with increasingly higher context orders") | our orders feed the mixers in parallel; no serial refinement | `ISSE` mode: o1 → o2 → … → o6 as a cascade, each stage keyed by its own bit history. It is **independent** of the parallel mix (a different information path), so it passes the admission rule |
| ICM | bit history → adaptive probability; fixed rate 1/4 of the error; init from the history's n₀/n₁ ((2n₁ + 1)/(n₀ + n₁ + 1)) | lpaq StateMap with 1/n rate | test the **ICM init formula** for fresh states (a cheap gain on sparse contexts) |
| SSE / APM | train **only the nearer** interpolation cell; rate 1/(count + 1.5), count capped at limit·4 (start and limit are knobs) | our APM trains both cells, fixed rate | `APMNEAR` + `APMLIMIT` knobs on A1/A2 |
| rates | ISSE weight rates fixed (bias error/25; gain ∝ err·p/2¹³) | — | defaults for the ISSE node |

**Tick 6 verdict:** not null (4 hints). The topic list is now exhausted; tick 7 is the final "anything missed" sweep.

## Tick 7 (08:21Z): final sweep for anything missed. Not null.
| node | hint (source) | our status | try as |
|---|---|---|---|
| **ordering (upgraded)** | **STARLIT** (github amargaritov/starlit): Doc2Vec vectors, then a TSP path, puts similar articles side by side; **+1.8% on the record**. **The original order is recovered by sorting titles** (enwik9 titles are alphabetical), so the order costs ~0 bytes in the archive. The search runs offline and is excluded from the size | none | the cheapest big lever found: an article reorder with zero side information. Needs a local embedding (Doc2Vec trains on enwik itself: no outside data) and a TSP heuristic. CPU only |
| numbers (new transform) | **STC** (2606.03570): digit runs move to side streams grouped by length and the surrounding bytes, with placeholders in the main stream; reversible, no stored permutation; **−1.6% on enwik9 with a BWT coder** (untested with CM) | NUM node off | `STC` prep transform; measure with our CM (a gain is not assumed) |
| neural ensembles | Nacrith (2602.19626), Micro-Diffusion (tick 1) | — | already covered (Tweedie); LLM-based methods are outside the Hutter limits |

**Tick 7 verdict:** not null (2 new hints, both large). Tick 8 sweeps again.
