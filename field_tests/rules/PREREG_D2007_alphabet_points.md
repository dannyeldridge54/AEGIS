# PREREG D2007: Placing the alphabet on its ancestral points. Does a letter-lineage symbol map help compression? Locked before code and runs.
**Danny's idea (21 Nov 2026).**
- The Latin alphabet evolved from an older Semitic one.
- Put each letter on its ancestral "point" and test whether that structure gives the field directional links that improve prediction.
- *Historical note:* Latin descends from the 22-letter Phoenician abjad, via Greek and Etruscan. Hebrew is a sister script of the same family. The map below uses the standard Phoenician ancestry.

**Node under test.** A class-context node: the classes of the last 4 symbols, plus the partial byte, hashed. It replaces the "sparse" node (index 10, measured ≈ 0 in the D2006 sweep). Engine: loomz4 with LR2 = 1. Everything else is fixed.

**Maps (letters are case-folded; non-letters always get the same 6 classes):** digit, space, newline, punctuation, markup `[]{}<>|=`, other/high byte.

| map | letter classes |
|---|---|
| **PHOEN** (ancestral) | A·aleph, B·beth, CG·gimel, D·daleth, E·he, FUVWY·waw, Z·zayin, H·heth, IJ·yodh, K·kaph, L·lamedh, M·mem, N·nun, O·ayin, P·pe, Q·qoph, R·resh, S·shin, T·taw, X (Greek chi, own class): **20 classes** |
| PHON (phonetic control) | vowels AEIOU; Y; stops BDGKPTCQ; fricatives FVSZHX; nasals MN; liquids LR; glides WJ |
| VC (vowel/consonant) | AEIOUY vs the rest |
| RAND1–3 (null controls) | random partitions of the 26 letters into 20 classes (seeds 1, 2, 3), same class count as PHOEN |
| NONE | node off (the original sparse node) |

**Data.**
- Held-out slice H = enwik8 bytes [50,000,000, 53,000,000). It was never used for tuning; D2006 tuning used the first 2 MB.
- Every map is scored by its compressed size on H.

**Verdict (fixed now).**
- **PHOEN helps** only if it is smaller than **all three** RAND controls **and** than NONE by at least 0.05%.
- If PHOEN beats NONE but not the RAND controls, the gain is from having *a* class node, not from ancestry.
- PHON and VC are reported for comparison.
- Every run must round-trip exactly; the PHOEN run is checked by decompressing.
