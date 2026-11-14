# PREREG D410 — CROWN: do the five senses agree on one Twist-2 parameter set? (locked 16:40 CT 14 Nov 2026, before running)

Danny (16:20–16:22): "five different senses all at once collapsing into one experience … set this up".
Senses: sight = CMB-SPA (Planck low-ℓ, ACT DR6, SPT-3G D1, ACT lensing); hearing = DESI DR2 BAO; smell = Pantheon+ SNe; touch = clocks +
MICROSCOPE; taste = birefringence β (and particle data, held at Σm_ν = 0.06 eV).
Model (Twist-2 joint branch, D402–D404): thawing dark energy on the line wa = −1.58 (1 + w0) (thawing relation verified in D393),
w0 ∈ [−1, −0.5]; n_s fixed at the Twist value 0.9651 (THAW_TWIST) or free (THAW_FREE). Code: theory/crown/crown_d410.py (+ run script),
copied unchanged to the PC's cmb-fit/axiclass/; references from stored fits cmp_ax_spa_lcdm_halofit (ΛCDM) and cmp_ax_spa_w0wa_halofit.
Agreement criteria (all must pass for "CROWN AGREES"):
- C1 (sight+hearing+smell with the Twist's n_s): χ²(THAW_TWIST) − χ²(THAW_FREE) ≤ 4.
- C2 (no single sense rebels): for each block (CMB, BAO, SN), χ²_block(THAW_TWIST) − χ²_block(ΛCDM) ≤ 4.
- C3 (touch): passes by construction for the axion branch (no α drift); stated, not tested.
- C4 (taste): the photon coupling needed for β = 0.261° at THAW_TWIST's w0, c_γ/f = 0.261/√(2.5×10⁻³ (1 + w0)), must be ≤ 30 (M_P units).
Also reported: n_s at THAW_FREE (the n_s refit in a thawing background), w0 at both. Otherwise "SENSES DISAGREE" naming the failing sense(s).
Stated now (pre-run), from stored, non-locked fits on these likelihoods: ΛCDM n_s = 0.9737, free w0–wa n_s = 0.9720, CMB-only n_s = 0.9711;
so C1 is at risk. No reruns to chase; crash/location fixes only via PREREG_D410_CROWN_DEVIATIONS.md written first.
