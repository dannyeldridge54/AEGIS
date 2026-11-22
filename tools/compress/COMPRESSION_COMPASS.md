# Compression compass: every knob fingerprinted with a direction and a vector (21 Nov 2026, 22:10 CT)
**Legend:** ● keep (pulls its weight); ◔ thin (helps under 0.1%); ↓! remove (hurts); ↑ needs more data (hurts small, helps big); ○ untested.
**Vector:** the measured change in compressed size when the knob is added (negative is better). Every number comes from a D-note, and the slice is named.

| # | ring | knob | vector | dir | slice | source | note |
|---|---|---|---|---|---|---|---|
| 1 | 0 | order 0–2 nodes | −0.1 to −0.3% each | ● | 1 MB dev | D2006 sweep | core |
| 2 | 0 | order 3–5 nodes | +0.1% (v2) → −0.7% (v4, per-node mixers) | ● | 1 MB dev | D2006 | needed the fractal mixer |
| 3 | 1 | order 6 node | −0.04% | ◔ | 1 MB dev | D2006 | |
| 4 | 1 | order 8 / sparse | ≈ 0 | ↓! | 1 MB dev | D2006 | slot reused for matched literal / class node |
| 5 | 1 | long-range match | −0.9% | ● | 1 MB dev | D2006 | |
| 6 | 1 | xz rep distances (4) | −0.07% | ◔ | 200 kB | D2008a | |
| 7 | 1 | xz matched literal | −0.22% | ● | 200 kB | D2008a | |
| 8 | 1 | xz event state (final-mixer context) | +0.36% at 200 kB → −0.30% at 3 MB | ↑ | H | D2008b | needs data |
| 9 | 1 | **direction node** (open/close/separate/end/toggle/reset) | **−0.38%** | ● | H (held-out) | D2008 | locked PASS |
| 10 | 1 | Phoenician letter points | −0.08%, but ≤ random partitions | ↓! | H | D2007 | locked NULL |
| 11 | 1 | vowel/consonant classes | −0.21% | ◔ | H | D2007 | superseded by #9 |
| 12 | 2 | word node | −3.2% | ● | 1 MB dev | D2006 | strongest single node |
| 13 | 2 | word pair | −0.23% | ● | 1 MB dev | D2006 | |
| 14 | 2 | word trigram | +0.08% | ↓! | G (10 MB) | D2010 | |
| 15 | 2 | column + char above | −0.25% | ● | 1 MB dev | D2006 | |
| 16 | 2 | line type | −0.06% | ◔ | 1 MB dev | D2006 | |
| 17 | 2 | markup state | −0.4% | ● | 1 MB dev | D2006 | |
| 18 | 3 | outer byte rings 12/16/24/32 | +0.17% (3 MB), +0.33% (10 MB), +33% time | ↓! | F, G | D2010 | overlaps the match node |
| 19 | spin | three spin speeds per node | +1.2% raw → ≈ 0 with per-node mixers | ◔ | 1 MB dev | D2006 | |
| 20 | mix | per-node + per-ring (fractal) mixers | −1.1% | ● | 1 MB dev | D2006 v4 | fixed the dilution |
| 21 | mix | final-mixer learning rate 1 (vs 2) | −0.2% | ● | 1 MB dev | D2006 | |
| 22 | lens | SSE lenses (2) | −1.0% | ● | 1 MB dev | D2006 | |
| 23 | prep | entity → single byte | −0.06% | ◔ | 1 MB dev | D2006 | |
| 24 | — | LSTM, dictionary transform, article reordering, hash confirmation, bit-history states | — | ○ | — | literature (cmix / fx2-cmix / STARLIT) | next |

## Scales, live (loomz7c COMPASS line, bits per char on one MB of G)
| scale | bpc |
|---|---|
| order 2 alone | 2.957 |
| ring 0 (orders 0–3) | 2.352 |
| ring 1 (orders 4–8, match, rep, class) | 2.201 |
| ring 2 (words, axes) | 2.065 |
| global mixer M1 | 1.952 |
| fast mixer | 2.140 |
| context mixer M2 | 2.026 |
| final mixer MF | 1.882 |
| after the lenses | **1.869** |

Each scale is below the one before it, so every layer pulls. The words ring is the strongest ring. The fast mixer is the weakest mixer, so it is a candidate to drop.

**Best build:** v7 + direction node + event state.
- 2,129,689 bytes on G (10 MB), vs xz 2,731,076 (−22%).
- Full enwik8 with v1: 20,923,436.
