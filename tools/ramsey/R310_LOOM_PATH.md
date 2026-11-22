# R(3,10): what others have tried, how it triangulates with our toolkit, and the path (Loom, 21–22 Nov 2026)
**Question.** R(3,10) ∈ {40, 41}. Two fronts, one centre:
- **front L** (construct): find a triangle-free 40-vertex graph with α ≤ 9. That proves R = 41.
- **front U** (exclude): prove that no such graph exists. That proves R = 40.
- **centre:** the referee plus independent verification.

## 20 references, each with what it contributes
| # | Reference | Method | Result / relevance |
|---|---|---|---|
| 1 | Radziszowski, *Small Ramsey Numbers*, Dynamic Survey DS1 (EJC, rev. 18) | survey | the authority on current bounds; 40 ≤ R(3,10) ≤ 41 |
| 2 | Exoo (1989) | constructive search | R(3,10) ≥ 40: a 39-vertex graph |
| 3 | Grinstead & Roberts (1982) | case analysis | R(3,9) = 36 |
| 4 | Kalbfleisch (1966); Radziszowski & Kreher (1988) | degree/edge counting, e(3,k,n) | origin of the tile-counting identity (our D2001) |
| 5 | McKay & Radziszowski (1995), R(4,5) = 25 | **gluing** of neighbourhood sets with isomorph rejection | the template for front U |
| 6 | Goedgebeur & Radziszowski, arXiv 1210.5826 (2013) | gluing + exact e(3,k,n) tables | R(3,10) ≤ 42; the tables we use |
| 7 | Goedgebeur & Radziszowski, *R(3,K10−e)* (EJC 2013) | gluing | method and code lineage |
| 8 | Angeltveit, arXiv 2401.00392 (2024) | gluing of R(3,9,≤35) neighbourhoods, ~3 CPU-years | **R(3,10) ≤ 41.** R(3,9,34, e ≤ 130) has 5 graphs; R(3,8,27) has 477,142. "40 will be quite difficult with current techniques" |
| 9 | arXiv 2601.03572 (2026), structural properties | degree / diameter analysis | δ ≥ 4 in general; δ ≥ 6 under diameter 2 |
| 10 | McKay, *Ramsey graph data* (ANU) | lists | r38_27.g6.gz (477,142 graphs) and r39_35.g6 (the unique graph) |
| 11 | McKay, nauty/geng; canonical construction path (1998) | isomorph rejection | needed for front U enumeration |
| 12 | Codish, Frank, Itzhakov & Miller, arXiv 1510.08266 | **SAT** + degree-matrix abstraction + symmetry breaking | R(4,3,3) = 30; the SAT encoding transfers |
| 13 | Kirchweger & Szeider, *SAT Modulo Symmetries* | SAT with dynamic symmetry breaking | the generic graph-search framework for front U |
| 14 | Heule, *Schur number five* (2017); Heule, Kullmann & Marek, *Boolean Pythagorean triples* (2016) | **cube-and-conquer** + DRAT proofs | how to split a huge SAT search across cores, with certificates |
| 15 | Gauthier & Brown, arXiv 2404.01761 (2024) | HOL4 formal proof of gluing + SAT | R(4,5) = 25 formally verified: the gold standard for the centre |
| 16 | Lidický & Pfender, arXiv 1704.03592 | **flag algebras / SDP** upper bounds | new small Ramsey upper bounds; probably not sharp enough at n = 40 |
| 17 | Coniglio, Furini, Ljubić et al., arXiv 2608.18769 (2026) | **integer programming on circulants** | 25 new R(3,n) lower bounds, 24 ≤ n ≤ 49. Agrees with our D2000: no circulant at 40 |
| 18 | Nagda, Raghavan & Thakurta, arXiv 2603.09172 (2026) | **AlphaEvolve** (LLM code evolution) | R(3,13) ≥ 61, R(3,18) ≥ 100, several R(4,k). Nothing at R(3,10) |
| 19 | Wagner (2021), *Constructions in combinatorics via neural networks*; Charton, Ellenberg, Wagner & Williamson, *PatternBoost* (2024) | RL / learned generators | the counterexample-search toolkit for front L |
| 20 | *Computer-assisted graph theory: a survey*, arXiv 2508.20825 (2025) | survey | verification practice (independent implementations, certificates); Exoo's annealing for R(4,6) |

## Triangulation: which methods fit our Loom and what we have built
| Method (refs) | Fits our toolkit? | Evidence from us | Verdict |
|---|---|---|---|
| Degree-case decomposition + gluing (5, 6, 8) | ✅ | D2002/D2003 closed δ = 4 with 3 methods | **primary for front U** |
| SAT + symmetry breaking, cube-and-conquer, DRAT (12–14) | ✅ (pysat installed) | D2003 SAT cross-check | **secondary for front U** (and the certificate) |
| Exact counting / tile identity (4, 6) | ✅ | D2001: 5,002 degree patterns, e ∈ [159, 180] | pruning for every case |
| Structured symmetric constructions: circulant ILP (17); Cayley, block-circulant | ✅ | D2000: no circulant at 39/40 | **extend outward: Cayley graphs on all 14 groups of order 40, then 2- and 4-block circulants** |
| Annealing / RL / LLM-evolved generators (2, 18, 19) | partial (r310.c annealing; CubeMind M2) | the annealer stalled at hard rungs | a front-L background search; low odds, cheap |
| Flag algebras (16) | ✗ for this size | — | skip |
| Formal verification (15) | later | — | the centre, once a case closes |

**Median view, across refs 1, 8, 6 and 20:** the community expects R(3,10) = 40. The likely outcome is therefore that front U succeeds slowly while front L finds nothing. Front L is still worth running cheaply: structured classes are a finite, exhaustive search, and each null is a clean result.

## The path (each step locked first, fingerprinted into the compass, refereed)
- **L1 (now, no download):** an exhaustive Cayley-graph search over **all 14 groups of order 40**. Every one is Z5 ⋊ P with |P| = 8, because the Sylow-5 subgroup is normal.
  - Connection sets S are inverse-closed, triangle-free, with 5 ≤ |S| ≤ 9 (δ ≥ 5 from D2003; Δ ≤ 9).
  - Checked by α(Cay) ≤ 9, with a positive control: Z35 and the unique (3,9,35) graph.
- **L2:** 2-block and 4-block circulants (generalising D2000) and vertex-transitive graphs of order 40.
- **U1 (needs Danny's OK to download r38_27):** generate R(3,9,34) graphs that have a degree-6 vertex, by gluing six attachment sets onto each R(3,8,27) graph.
- **U2:** R(3,9,34) with δ ≥ 7, by SAT + symmetry breaking with lazy α-cuts. Cross-check against the 5 known graphs with e ≤ 130.
- **U3:** the degree-5 case of a (3,10,40)-graph: glue 5 sets onto every 34-vertex dual neighbourhood with e ∈ [129, 155]. Same calibration as D2002.
- **U4:** degree 6, then 7, 8 and 9 (9-regular has the most slack: dual neighbourhoods in R(3,9,30, e = 99)).
- **Centre:** every closed case gets an independent SAT check, a referee, and (later) a formal certificate.
