# RESONANCE RUN 1 — method note (23 Nov 2026 14:45 CT). EXPLORATORY: no goalposts, at Danny's instruction 14:35
("don't go by layer ... don't set the markers ... do the full run and sit at the home and tune the knobs while it's going, then pass it to the referee").
Engine: tools/rings/hex.py (six rings settle on a bus). Centre tunes all knobs together while every evaluation re-settles the whole hexagon:
C (inflation), T_R (reheat), s_m32 (gravitino-mass lever: moves wino, gluino, alpha_s, proton), and NEW d_as = additive alpha_s correction at M_Z from
two-loop Yukawa/threshold effects, bounded to +-0.004 (weave_rg2's own stated uncertainty); it is charged as a knob like the others.
Score at the centre: the Bloom likelihood with the Forces ring's alpha_s as LIVE, minus the BIC charge for every moved knob. Reported, not gated:
every ring's settled values and pulls, the Hoyle resonance window, Y_p and D/H. Result is post-hoc/exploratory and labelled so; the referee judges it.

## Referee R104 (after the run)
- d_as = +0.00378 is a one-parameter FIT to the measured alpha_s (gain 8.91 - 1.52 BIC = 7.39 nats; Hoyle restates the same pull, DEV-3).
- The repo already computed the two-loop Yukawa term (D1804, D1944: -0.0002 to -0.0003; R104 /tmp: -0.0002 to -0.0006 for tan beta 2-50):
  WRONG SIGN and ~10x too small. The +-0.004 bound was a stale label. The Weave's own alpha_s is 0.1140-0.1147 (~3.7 sigma low).
- +0.0038 needs a threshold Delta(alpha_3^-1 - alpha_U^-1) ~ -0.27 at M12: plausible size, sign/magnitude never computed.
- Optimizer: from the plain start it stays put; result depended on a seed near the answer. C, s_m32 fairly explored; T_R unscored.
- D/H -2.5 sigma: real, independent (only omega_b and PRIMAT rates), not in the Bloom likelihood.
- Inconsistency: d_as does not feed M12, alpha^-1 or proton lifetime.
- Next derivation: sign and size of Delta_3 from the N = 6 magnetised-D7 stack, then its effect on M12 and tau_p.
