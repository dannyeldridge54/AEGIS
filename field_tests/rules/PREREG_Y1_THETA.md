# PREREG Y1 — first look: magnetised-torus Yukawas at τ = ρ (no free couplings), leptons. Locked BEFORE computing.
Construction (Cremades–Ibáñez–Marchesano, hep-th/0404229): on T² with intersection numbers I_L = I_R = 3 and I_H = 6 (three left, three right families, six Higgs modes), Y_ij^(k) ∝ ϑ[δ_ijk; 0](0, τ·I_L I_R I_H), δ_ijk = i/I_L + j/I_R + k/I_H (mod 1), ϑ[a;0](0,t) = Σ_l exp(iπ t (l + a)²). Evaluate at τ = ρ (Weave knot), Higgs in ONE mode k (no free numbers), k = 0…5.
Output for each k: the 3×3 matrix Y^(k), its singular values s₁ ≥ s₂ ≥ s₃, the ratios s₂/s₁, s₃/s₁, and the Koide Q = Σs/(Σ√s)² (masses ∝ s).
Compare with charged leptons: m_μ/m_τ = 0.0595, m_e/m_τ = 2.88e-4, Q = 2/3.
Reading (decided now): report all six k; "promising" if some k gives both ratios within a factor 3 of the leptons' (it is a first look — a single Higgs mode on a bare torus; the Z₃ orbifold with |M| = 9 is the real target).
Code theory/tests/y1_theta.py. One run.
