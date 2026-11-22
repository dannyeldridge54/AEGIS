# PREREG D1987: two detectors per node (engine v3). Locked at this commit, before any v3 calibration or run.
Follows D1986's O2 FAIL. Everything in D1986 is kept except the detector:
- the goalposts (the same goalposts.json, same sha256);
- bounded knobs, visible split and hysteresis;
- the scoring of goalposts;
- the bars A1–A5;
- the event schedule and quiet windows;
- held-out seed 2026 and the strict DONE rule.

## Detector A: deterministic margins (no data stream feeds them)
These are quark_window, MN_bottom, MN_top, nu_ratio, split_natural and gravitino_box.
- Each pulse: residual r = M_now − (M_prev + J·Δx_self), where Δx_self is the engine's own applied moves.
- **Event** if \|r\| > 1e-3. A second-order residual of a 0.2 % step is ~1e-5, so the event threshold is 100× above it.
- Re-arm when \|r\| < 1e-4. No statistics, no tuning.

## Detector B: data margins (rung_agreement, wino, n_s, alpha_s, leptogenesis)
- Whitened w (as D1986 DEVIATIONS 1), **self-normalised**: w / running robust scale (1.4826 × the exponentially weighted median absolute w, α = 0.001, start 1).
- Two-sided CUSUM with **k ∈ {0.08, 0.16, 0.25} × h ∈ {12, 20, 30, 40, 60}**.
- Probes: **2 sd in z (0.32 per pulse in w) for 400 pulses**, every 1,000 pulses in calibration and every 2,000 in the shadows.

## Calibration O2 (same training seeds 1–5 × 5 s, no events)
- A config is admissible if its false-alarm rate is ≤ 1e-5 per data-margin-pulse **and** it misses ≤ 20 % of probes.
- Start = the admissible config with the lowest mean delay.
- Detector A is calibrated only by its own false-alarm rate on those seeds. Bar: ≤ 1e-5 per deterministic-margin-pulse.
- **If either detector has no admissible config, the scored run is not performed, and that is reported.**

## Online tuning O3
As in D1986: shadows on iid N(0, 1) plus probes, the admissible best copied every 5 s. It applies to detector B only.

## Scored run O4
60 s, seed 2026, bars A1–A5 as locked in D1986.

## Priors (written now)
- If detector B behaves as Siegmund's ARL approximation says, k ≈ 0.16 with h ≈ 30–40 gives ARL0 ≥ 1e5 and a delay of about 175–250 pulses for the probe.
- The scored events are large: n_s 3σ is about 37 sd in z, and Y_B −30 % is about 450 sd. They should be detected within a few pulses.
- Data heavy tails could still sink the false-alarm bar.
