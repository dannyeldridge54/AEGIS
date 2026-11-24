# PREREG D2233 — Gmeiner-Honecker thresholds evaluated with the Weave's own numbers (pulse, breath 2). Written before computing, 23 Nov 2026.
Calibration (D2232 + source PDF 0910.0843v2 eq. 129 read directly; disclosed, done before this lock): tools/strings/gh_thresholds.py
reproduces eq. 137 at v = 30 with (sigma_c, tau_c) = (1/2, 0): SU(3)_a -33.5/-33.5/-25.7 vs -34/-34/-26; SU(2)_b -8.6/+6.0/+5.7 vs -9/+6/+7
(h3, h1-hat, none). Residual <= 1.3 in 1/alpha (none-case SU(2)) - stated, accepted as calibration tolerance for this breath.
GH relations (eq. 134-135, Table 13): 1/alpha_x,tree = (M_P/M_s) Vol_x, v = (1/2)(g_s M_P/M_s)^(2/3).
Tests, all with the Weave's own inputs (g_s = 2/sqrt3 from S = rho; alpha^-1 = 28 at M12, weave_magd7):
 T1 Weave-implied torus area: v_W = (1/2)(g_s * 28/Vol_a)^(2/3) for the published Vol_a (0.16 omega=1, 0.11 omega=2). Compare with v = 1 (tau = i).
 T2 Visible-cycle volume REQUIRED for v = 1: Vol_a* = 2^(3/2) * 28 / ... solved from T1 with v = 1 (report; compare with Table 13 scale).
 T3 delta32 = (Delta_SU3 - Delta_SU2)/4pi from eq. 128-129 at v = 1 and at v_W, for the three published cases (threshold part only;
    the published model's tree split 6 omega is NOT fixed by it - reported).
Reading fixed now: if v_W >> 1 for any realistic visible volume (Vol_a <= ~2), the identification "threshold torus area = SERAPIS tau = i"
is INCONSISTENT with the Weave's own alpha^-1 = 28 and g_s in GH normalisation -> D2225's tau = i route needs a different torus (a complex-
structure U, or a torus not tied to the gauge kinetic volume) or is closed. If v_W ~ 1 is reachable, report the needed Vol_a and continue.
