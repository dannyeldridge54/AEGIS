# PREREG D2085: the effective SUSY threshold from v4's split spectrum, then two-loop α_s for exact unification. Locked before computing.

**Formula** (Carena–Pokorski–Wagner hep-ph/9303202, Eq. 16, quoted):
T_SUSY = m_H̃ (m_W̃/m_g̃)^{28/19} (m_l̃/m_q̃)^{3/19} (m_H/m_H̃)^{3/19} (m_W̃/m_H̃)^{4/19}

It is valid when all masses are > M_Z, at one-loop threshold level, and is used with two-loop running (as in that paper).

**v4 inputs** (D1762, D713, bloom_data):
- m_W̃ = 0.687 TeV, m_g̃ = 4.93 TeV;
- m_H̃ = μ ∈ [0.25, 0.7] PeV (the v4 band), with the centre taken as the geometric mean;
- heavy Higgs m_H = μ, and m_l̃/m_q̃ = 1. These are assumptions, stated; the dependence is a 3/19 power.

**Run:** tools/seed/twoloop.py `predict(T_SUSY)` at the two band ends and the centre.

**Score:** pull against 0.1180 ± 0.0009.

**Labelled HYBRID:** this pairs the D2083 exactly unified PS brane model with v4's soft spectrum. They are different string constructions, so the result tests "exact unification + v4 spectrum", **not** v4 as a whole.
