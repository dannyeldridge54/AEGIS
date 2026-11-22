# PREREG D2024: Esoteric systems as the ring structure of the field (compressor test bed). Locked before scoring.
**Idea (Danny 00:44).** Give each section a meaning from world esoteric traditions, and test whether those groupings structure the field better than chance. As in D2007, a symbol system counts only if it beats random groupings of the same shape.

**Test bed.** loomz17 = loomz15 with the ring partition as a knob (RINGS). The default partition reproduces v15 exactly (45,841 on d200k), and a 4-group partition round-trips. The env is the best build (D2017).
**Slice.** enwik8 [30, 31) MB, never used.

**Node meanings, fixed now:**
- 0–6: byte orders 0–6
- 7: matched literal
- 8: word
- 9: word pair
- 10: direction class
- 11: column
- 12: line type
- 13: markup
- 14: closing stack
- 15: gap
- 16: header (off)
- 17: indirect
- 18: number (off)
- 19: UTF (off)
- 20: match

**Systems (group per node, 0..20):**
- **BASE** (the original S/T/U-style 3 rings): 0,0,0,0,1,1,1,1,2,2,1,2,2,2,1,1,2,1,2,2,1
- **E4**, Empedocles / Platonic. Earth = cube (structure), Water = icosahedron (flow), Air = octahedron (relation/pointer), Fire = tetrahedron (transformation/direction).
  - Earth {0,1,2,11,12}; Water {3,4,5,6,8,9}; Air {7,15,16,17,20}; Fire {10,13,14,18,19}
- **W5**, Wu Xing.
  - Wood {1,2,3}; Fire {4,5,6,7}; Earth {8,9,11,12}; Metal {10,13,14,15,16}; Water {0,17,18,19,20}
- **G3**, the gunas.
  - tamas {0,1,2,3,11,12}; rajas {4,5,6,7,15,17,20}; sattva {8,9,10,13,14,16,18,19}
- **Y2**, taiji yin/yang.
  - yin {0–6,8,9,11,12,17,20}; yang {7,10,13,14,15,16,18,19}
- **Controls:** for each system, 3 random partitions with identical group sizes (seeds 1, 2, 3).

**Pass.** A system passes only if it is smaller than **all 3** of its random controls **and** smaller than BASE by at least 0.03%. Otherwise NULL. The best system is round-trip checked.
