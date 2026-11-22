# PREREG D2096: the chiral-exotics filter on the D2083 Pati-Salam models. Locked before computing.

**Definition:** a completion is exotic-free iff every (hidden h, visible v ∈ {a, b, c}) pair has I_hv = 0 **and** I_hv′ = 0. Intersection numbers follow D2083/He–Li–Sun.

**Data:**
- all 8 PS (topology, χ) points of D2083;
- for each, **every** hidden completion (tadpole + K-theory exact), enumerated explicitly with the same DP logic (tools/seed/exotics.py).

**Report:**
- per point: the number of completions and the number exotic-free;
- in particular, the unified model (Re z = 6, 6, 6).

**Verdict:**
- **PASS** if the unified model has ≥ 1 exotic-free completion;
- **FAIL** otherwise. A FAIL means its exotics are unavoidable within this space.

**Not done here (stated):** vector-like pairs (I = 0 but non-chiral matter), and the hidden–hidden and visible adjoint/symmetric/antisymmetric counts.
