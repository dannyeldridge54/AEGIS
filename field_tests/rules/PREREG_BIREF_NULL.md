LOCKED 2026-11-13 01:40 CT by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_BIREF_NULL — the Twist's birefringence null

## Hypothesis
The Twist's angle couples to fermions only through the derivative Nieh–Yan coupling (c_A = sqrt(3/8)). With all charged
fermions heavy compared with CMB photons, the low-energy phi F F~ coupling vanishes (Quevillon & Smith 2019), so the
Twist predicts **no isotropic cosmic birefringence: beta = 0** (Development 14). Even if the full anomaly term survived,
beta <= 0.075 deg (FLAG-1 with DESI) — the strict bound used here is the anomaly-free value beta = 0.

## Status of data when locked (context only, not scored)
ACT + Planck joint (Eskilt, arXiv:2608.06480, Aug 2026): beta = 0.277 +/- 0.057 deg, 4.8 sigma from zero. That
analysis fixes the instrument angle with priors and the Galactic foreground assumption; the null and the measurement
are in 4.9 sigma tension today. This rule judges only **future** measurements.

## Data that will be scored (first to appear wins; each scored separately when it appears)
1. Any CMB measurement of isotropic beta whose polarization-angle calibration does **not** rely on assuming the Galactic
   foreground is unrotated (artificial calibrator, Crab/Tau A, drone or wire grid; e.g. Simons Observatory, BICEP/Keck,
   SPT-3G, LiteBIRD), published after this lock.
2. Combined error on beta (stat + calibration) must be <= 0.10 deg to be scored; otherwise recorded as "not decisive".

## Readings (beta in degrees, sigma = the published total error)
- **SUPPORTED**: |beta| / sigma < 2.
- **NOT SUPPORTED**: beta / sigma >= 5 (nonzero at 5 sigma or more).
- **PARTIAL / TENSION**: 2 <= |beta| / sigma < 5.
A NOT SUPPORTED reading is final for the anomaly-free Twist; the anomaly route (b) is then recorded as the only
remaining option and must be checked against its own bound (beta <= 0.075 deg for FLAG-1 with DESI; > 0.075 deg at
>= 3 sigma rules it out too).

## Failure handling
No reruns, no re-reading. Corrections only through PREREG_BIREF_NULL_DEVIATIONS.md, written before any rescoring.
