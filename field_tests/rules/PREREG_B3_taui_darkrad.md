# PREREG B3 — τ=i dark-radiation bookkeeping (Djl B; open item from D1085) — locked 2026-11-17
Inventory from the D-notes, as reasoning:
- (1) Heavy N doublet at i: massive. D726 singular values are 0.3016 each, non-zero. They decay; no dark radiation.
- (2) Lightest neutrino nearly massless (D601). This is an SM ν, already inside N_eff = 3.044; it adds no ΔN.
- (3) Enhanced-symmetry states that become massless at the self-dual point (D-notes near lines 5350 and 6156). This is the ONLY candidate. If they stay massless in the vacuum and are populated, they are hidden radiation. If SUSY breaking gives them mass (D626-type), they are not.
Bookkeeping, derived from entropy conservation (the hidden sector decouples from the SM at T_dec ≥ T_R; SM entropy is conserved separately):
- ΔN_eff = (4/7) g_h (10.75/g*s,SM(T_dec))^{4/3}, with g*s,SM = 106.75 (the soft masses ~1e9 GeV exceed T_R ≲ 1e6 GeV, so the SM is the only content).
- g_h counts bosonic dof; fermions count 7/8.
Cases:
- (a) Not populated: the inflaton is sterile to equal-mass pairs (D601), and gauge bosons of an enhanced group are such pairs. ΔN = 0.
- (b) Populated, U(1) (g_h = 2).
- (c) Populated, SU(2) (g_h = 6).
- (d) Populated, SU(2) plus a gaugino triplet (g_h = 6 + 6·7/8).
- (e) Dark-radiation dominance (as D723): excluded by construction, not computed.
Test (scored): each case vs D1082's BBN window [−0.04, 0.41]. Report also σ(N_eff) ≈ 0.03 (CMB-S4 target, stated as a literature figure from memory; labelled).
Script theory/wiring/b3_taui_darkrad.py (written after this lock).
