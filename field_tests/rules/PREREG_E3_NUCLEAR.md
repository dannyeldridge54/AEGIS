# PREREG E3 — the carbon (Hoyle) window (locked 21 Nov 2026 before computing)
Window (literature, Epelbaum–Krebs–Lähde–Lee–Meißner, PRL 110 (2013) 112502 and EPJA 49 (2013) 82; ledger 7.2): the Hoyle state stays within ~100 keV of the ⁸Be+α threshold (carbon AND oxygen produced) for |δm_q/m_q| ≲ 2–3 % and |δα/α| ≲ 2.5 %. Tool weave_nuclear: inside if (δm_q/m_q / 0.025)² + (δα/α / 0.025)² ≤ 1 (elliptic approximation, labelled).
Weave inputs: m_q and α(0) are fitted/inputs (quarks hosted on the slip ladder, I7) ⇒ trivially inside at the data point.
Non-trivial check: if α_s were taken from EXACT two-loop unification (0.1158, D1800) instead of data (0.1180), Λ_QCD shifts by δlnΛ = 2π δα_s/(b₀ α_s²) (b₀ = 23/3 at M_Z), so m_q/Λ_QCD shifts by the same fraction. Report δ(m_q/Λ)/(m_q/Λ) and whether it lies inside the window, and the α_s precision a true prediction would need to stay inside (|δα_s| for 2.5 %).
Report only (no pass/fail on data; this is an anthropic-sensitivity calibration).
