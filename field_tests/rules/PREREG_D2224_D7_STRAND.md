# PREREG D2224 — D7 strand sweep for the forces ring (Danny 15:56: "get that whole strand done ... every point where it's stable ... then
# adjust the twist and the torque and the flux"). Written before computing, 23 Nov 2026.
Engine: theory/tests/d2224_strand_engine.py = the D2221 alpha_s engine (2-loop gauge + top Yukawa, MS->DR at m_s, top decoupled) with
non-universal thresholds at M12: alpha1^-1 - alpha2^-1 = delta12 defines M12, alpha3^-1 - alpha2^-1 = delta32 there. Guard: (0,0) -> 0.114456.
Strand (discrete, every point enumerated, nothing picked):
  delta_a = c * m_a^2 * Re S  (flux; Re S = sqrt3/2; m2 = 3 anchors alpha^-1 = 28; m1, m3 in 1..5; c in {1, 1/(2 pi)} = the two D2212 readings)
          + (b_a^{N=2}/(4 pi)) * L,  L = -ln(Re T |eta(T)|^4)  (Dixon-Kaplunovsky-Louis one-loop N=2 threshold; Delta b32, Delta b12 in -6..6)
  Re T = 28 - 9 Re S = 20.2058 (the model's own value, weave_magd7; NOT a knob) -> L = 18.153.
Axis spin: Im T in {0, 0.25, 0.5, 0.75} (axion); its effect is e^{-2 pi Re T} ~ 1e-55 and is reported, not used.
Stable point (all required): |alpha_s - 0.1180| / sqrt(0.0009^2 + 0.00057^2) <= 2; M12 >= 1.145e16 x (2.4/16)^(1/4) = 7.12e15 GeV (Super-K
2.4e34 y with tau_p ∝ M12^4 from the stored 16e34 y); Hoyle window inside at the new alpha_s (weave_nuclear). Wino/gluino are unaffected (thresholds
sit at M12). Method: linear map from the engine at 3 points pre-filters (|linear pull| <= 4); every survivor is run exactly in the engine.
Report: number of strand points, number stable, the stable list, the fraction stable, and the NATURAL point fixed now = universal flux
(m1 = m2 = m3 = 3) with the smallest |Db32| + |Db12| that is stable (if any). Reading fixed now: stable fraction > 10% -> "landscape allows it,
not a prediction"; zero stable -> forces ring cannot balance on this strand; the natural point stable -> CONDITIONAL on deriving that Delta b
from the Z2 x Z6' spectrum. Twist/torque/flux continuous adjustment: only Im T exists in the model at this layer (no Wilson lines) - reported.
Referee after; DEVIATIONS before any fix; one rerun.
