# S8-LNL deviations (logged before any DES Y3 shear chi2 with the new model)

## D1, 2026-11-08 (execution fix, before any shear chi2): G2 compared against the wrong total
The first G2 run compared the component sum with CLASS's `d_tot`, which in this build includes the dark-energy field's
perturbations (so it is not the matter total); it reported ~970% and stopped, as the rule requires. Fix: G2 now builds
the total-matter transfer from CDM, baryons, the ULA and massive neutrinos, multiplies by the primordial spectrum, and
compares with CLASS's own linear matter power (identical to the stored pk files, checked to 4 digits). Component weights
use the same matter total. No rule text, threshold, data or flag changed.

## D2, 2026-11-08 (found by G2, before any shear chi2): the stored S8-L linear power leaves out the ULA
With D1's fix, G2 still missed by 10% at k = 10 h/Mpc (0.06% at k <= 0.1). Test: rebuilding CLASS's matter power from
CDM + baryons + massive neutrinos **without** the ULA reproduces it to 0.04% at all k and z (0-3). So in this AxiCLASS
build the ULA is booked as a "fluid" and left out of the matter P(k) and sigma8. The stored pk_spiralL*.npz linear power
(used by the halofit Part 2 run) is therefore the cold + neutrino power, while its omega_m includes the ULA.
For S8-LNL: G2 is applied to what the stored file actually contains (cold + neutrinos: PASS, 0.04%), and the halo model
gets the true total (ULA included) as `power_total`, with `power_cold` and `power_axion` from the same transfers. This
is what the rule's method asks for (per-component power, the ULA included); only the G2 comparison target is restated.
Consequence for earlier results (reported, nothing edited): the stored S8-L sigma8 and S8 (spiral_l_score.json) and the
halofit Part 2 run used the cold-matter power, not the total.

## D3, 2026-11-08 (execution fix, before any shear chi2): numpy 2 compatibility in axionHMcode
`axion_density_profile.py` converts scipy's size-1 root array with float(), which numpy 2 refuses. Changed to
float(np.ravel(x)[0]) (same number). Added to the patch file. No physics or setting changed.

## D4, 2026-11-08 — APPROVED by Danny ("Approve: use 'basic'") (method setting): use version = 'basic', not 'dome'
Found by a code-path check (path_check.py), before any shear chi2 with the new model. Same linear power fed to both
paths; the ULA path should match the cold (HMcode-2020) path as the ULA share goes to 0.
- 'dome' (the locked setting), ULA share 0.001: off by up to 2.6% at z = 0 and **6.6% at z = 1**; at share 0.06 with
  no suppression in the input it swings from -18% to +18%. It does not reduce to HMcode-2020, so ULA side vs LCDM side
  would differ by code path alone, not physics. Its own README says 'dome' is calibrated for 1 < z < 8 only; DES Y3
  lensing comes mostly from z < 1.
- 'basic', ULA share 0.001: matches the cold path to 0.1% at every k and z tested.
Proposal: switch to 'basic' for both sides; everything else unchanged. The rule's own assumption ("the model then
reduces to HMcode-2020") holds only for 'basic'. Applied after his approval, before any shear chi2.
