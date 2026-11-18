<!-- AEGIS-FP AZZLTQOIOGNTOBU3 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Referee response — Lattice Champions (18 Nov 2026)
Referee verdict: NOT READY (textual fixes only; every number reproduced). All 12 required fixes applied:
1 flip rule → Proposition with Poisson proof; constancy on α>1 labelled numerical; "isometric to dual" defined.
2 "champion" = best among tested families at sampled α; theorems (Montgomery d=2, CKMRV d=8,24) separated from conjectural cases.
3 "rule is modularity" removed; self-Poisson identity stated as a dual property (Z^d counterexample noted).
4 hexagon claim restricted to D4,E6,E7,E8,BW16,Leech; BCC, D5*, E7* have none; /12 exactness argument added; "tiles" removed (title changed).
5 BW16 square count 923,400 added; squares-per-hexagon defined.
6 2D section rephrased via elliptic points of PSL(2,Z); "exactly two" labelled numerical at α=0.5,1,2.
7 Epstein convention defined; s=d/4 tie from functional equation; Rankin/Cassels/Ennola/Diananda cited.
8 Conway uniqueness theorem stated; det-1 explained (2×glue vector supplies 2·1).
9 truncation bounds stated per lattice; Leech uses literature shells.
10 citations added (Milnor, Montgomery, Rankin, Cassels, Ennola, Diananda, Sarnak–Strömbergsson, Bétermin, Coulangeon, Coulangeon–Schürmann, Cohn–Kumar, Angelinos–Chakraborty–Dymarsky, Conway).
11 every abstract item labelled known / numerical / new.
12 3D flow stated as 8/8 starts at α=1.6 and 0.6 (seed 1297).
Optional: SERAPIS moved to a "Speculative" section.

## Pass 2 — second-pass referee (18 Nov 2026)
Verdict: READY (after the changes below). All 12 round-1 fixes confirmed in the text. Numbers re-checked against
field_tests/results/*2026-11-18*.txt and tools/lattice/lattice_lab.py: d=6 energies, dual ties (<1e-13), E8/E4, E8+E8 = D16+ (2.5e-14),
BW16 vs heterotic, Leech shells/E8^3, hexagon and square counts, E(rho,2)/E(i,2), Epstein sign changes, 8/8 3D flow — all reproduce.
Changes:
1. BW16 truncation corrected: omitted shells beyond Q=6 contribute ~5e-4 at alpha=1 (recomputed with Q=7.5: 0.70763 -> 0.70812), not 1e-2.
2. 2D critical-point scan: stated as a grid scan truncated at Im tau <= 3 (as in the code); gradient bound 2e-11 -> 3e-11 (max found 2.2e-11).
3. Ennola (Cambridge 1964) proved FCC and BCC are LOCAL minima for all s>0; removed the attribution of an FCC/BCC "switch" to Ennola
   (Epstein section and 3D flow). The 3D flow is now compared with the Sarnak–Strömbergsson conjecture.
4. Added Ennola, Proc. Glasgow Math. Assoc. 6, 198 (1964) (the 2D lemma) for the 2D Epstein minimum.
5. d=3 status: the Sarnak–Strömbergsson conjecture now cites a posted proof (Luo–Wei, arXiv:2609.17356, preprint); still labelled N.
6. CKMRV: "among all periodic configurations" -> "among all point configurations of the same density"; Montgomery "among lattices".
7. Coulangeon criticality: "spherical 4-designs", critical "among lattices of fixed covolume".
8. Leech code step: "11-dimensional even subcode" (wrong: every Golay word is even) -> 11-dim subcode (2048 words) lacking the all-ones word.
9. E8/Leech hexagon counts: "classical" -> "follow from the classical inner-product distributions [CS]". Square-plane /8 exactness stated.
10. LaTeX: Epstein continuation split over three lines (fixes 18.7pt overfull box); Lambda_L defined.
Bibliography verified (web): Montgomery GMJ 30, 75 (1988); Ennola PCPS 60, 855 (1964); Diananda PGMA 6, 202 (1964); Rankin 1, 149;
Cassels 4, 73; Sarnak–Strömbergsson Invent. 165, 115; Bétermin SIAM J. Math. Anal. 48, 3236 (2016); Coulangeon IMRN 2006, 49620;
Coulangeon–Schürmann IMRN 2012, 829; Cohn–Kumar JAMS 20, 99; Angelinos–Chakraborty–Dymarsky JHEP 11 (2022) 118.
Build: pdflatex x2, no undefined references or overfull boxes; one benign revtex "float is stuck" warning (Table I is placed on p. 2).
