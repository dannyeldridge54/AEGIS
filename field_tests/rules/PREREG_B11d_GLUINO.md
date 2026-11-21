# PREREG B11d — the Weave's own gluino mass and α_s(unif) (locked 21 Nov 2026 before computing)
Code under test: tools/weave_cm/weave_tools.py at git 7655cd91 (weave_rg2), plus the one-line AMSB formula below.
AMSB gaugino masses: M_a = b_a g_a²(μ) m₃/₂/(16π²), b = (33/5, 1, −3). Wino fixed at M₂ = 0.68 TeV ⇒ m₃/₂ = 16π² M₂/g₂²(M₂). Gluino: |M₃| = 3 g₃²(M₃) m₃/₂/(16π²), solved self-consistently with one-loop α₃ running (SM + wino) from α_s(M_Z) = 0.118; pole-mass correction +15 % ± 5 % (standard gluino self-energy + squark-loop size at heavy scalars, stated estimate). Report m_g̃ and α_s(unif) from weave_rg2 at m_g̃ (and at m_g̃ ± 20 %).
Verdict: CONSISTENT if |α_s(unif) − 0.1180| ≤ 0.007 at the central m_g̃.
