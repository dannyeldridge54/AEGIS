# PREREG D779: Z₃ charges of the ρ heavy sector and the rank of m_ν for singlet leptons
Locked 2026-11-16 before computing. Script: theory/modular/rho_charges_d779.py. Output: field_tests/results/rho_charges_d779.txt.
Step 1: diagonalise the ST action on the Γ₂ doublet. Derive it from Y(ρ) ∝ (1, i): the doublet components along the null vector n = (1, −i) and along Y define the eigenbasis. Express M_R (D724, c = 1) in that basis and read off which entries are non-zero, i.e. which N combinations pair: Majorana (q = 0) or Dirac-type (q, −q).
Step 2: light leptons as three singlets with common charge q_L = −q_H (needed for any Weinberg mass, D778). Dirac entries L–N_j are allowed only for q_Nj = 0. Build the general Z₃-allowed M_D (random complex entries on the allowed slots), and compute rank(m_ν) for 1000 random draws.
K4: M_R in the eigenbasis reproduces singular values (c, c, √2).
Decision:
- REMEDY WORKS if rank(m_ν) = 3 generically.
- If rank = 1: FAIL, then report the minimal extension (the number of extra q = 0 heavy singlets needed for rank 3) by recomputing the rank with 1 and 2 added q = 0 singlet N's carrying generic Majorana masses.
