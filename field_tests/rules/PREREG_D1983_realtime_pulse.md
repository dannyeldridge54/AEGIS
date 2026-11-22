# PREREG D1983: real-time layered pulsing with a referee per layer (Danny 18:46, 18:47). Locked 22 Nov 2026 ~00:52Z, before building.
## The engine: tools/loom/loom_rt.py, in one process
Every pulse runs **layers 1 → 9 in order, in real time**; there is no batch wave.

The data stream: each pulse, each data-type observable gets **three independent noisy readings** at its quoted σ:
- n_s: 0.9728 ± 0.0027;
- α_s: 0.1180 ± 0.00107;
- the lepton slip: 0.0253 ± 0.0003;
- the wino limit: 700 ± 20 GeV;
- Y_B: 0.87e-10 ± 1 %.

Their median is the pulse's bearing (triangulation). Each layer keeps an exponential running estimate (α = 0.05). Fixed bounds stay fixed: the quark window, the M_N bounds, the gravitino box. Windows (L3, L9) pass through.

**The referee of layer L, every pulse:**
1. Compute the layer's margins from the running estimates and the current knobs. The formulas are those of resonance.py.
2. **Categorise** each margin: IN (≥ 0), PULL (−0.5 to 0), OUT (< −0.5).
3. **Status:** RESONANT after 3 consecutive pulses with all margins ≥ 0 ("lock where it's 3"). **LOST** at the first pulse a RESONANT layer fails; this is logged with the pulse number and the time. Otherwise NO LOCK, OPAQUE (rank 0, from its lens) or WINDOW.
4. **Shift detector:** an event when |margin − baseline| > 4 sd, where the baseline and sd are a slow running mean and spread (sd floor 1e-6).
5. **Active balance, only while RESONANT or trying to reach resonance:** one small gradient step (≤ 0.2 % in ln) on the layer's own **free** knobs, raising its minimum margin.
   - A knob is free when no inner RESONANT layer uses it (inside-out) and it is not held.
   - Held: u by L1 (N0: freeze the rung step).
   - Every knob more than 1 % off its derived value is counted as a **FIT** (G-T3) and reported. Balancing is a consistency map, not evidence (D1948).
6. **Feed forward:** the updated knobs and the layer's lens go to the next layer **in the same pulse**.

**Every pulse is a data point:** pulse number, time, and per layer: status, minimum margin, categories, event.

## The 60-second run (as fast as possible), with injected events at fixed times
| time | event | expected detecting layers |
|---|---|---|
| 10–20 s | n_s data shifts by +3σ (new release) | {6} |
| 25–35 s | knob kick m₃/₂ × 1.05 (external) | the layers whose \|J_L Δx\| exceeds 4 × their sd at t = 24 s (computed from the lens at run time, before the kick, and logged) |
| 45–55 s | the Y_B measurement shifts by −30 % | {8} |
A layer that detects **nothing** in a quiet window and **nothing outside** its predicted events is clean.

## Accuracy (fixed bars, never loosened)
- **A1 numerical validation:** every 200 pulses, recompute every layer's margins through resonance.margins at the same knobs with the nominal targets, compared with the engine run at nominal targets. Bar: max \|Δ\| < 1e-9.
- **A2 detection:**
  - recall = 1 (every predicted layer detects within 0.5 s of the event start);
  - precision ≥ 0.9 (detecting layers ⊂ predicted, counted over the 3 events);
  - latency reported in pulses and in ms.
- **A3 false alarms:** ≤ 1e-3 shift events per layer-pulse in the quiet windows (0–10, 20–25, 35–45, 55–60 s), excluding the first 2 s (warm-up).
- **A4 recovery:** each event's layers return to their pre-event status within 3 s after it ends.
- **Throughput:** pulses per second over the 60 s.

## The real-time adjustment controller (Danny 18:47), locked now, acting during the run, logged with timestamps
Every 1 s window, per layer:
- If A1 failed, or the layer's false-alarm rate in that window is above 1e-3: **escalate** that layer. Lens refresh every pulse (instead of every 10th), readings 3 → 5, and the global pace throttled by 2×, down to a floor of 60 Hz.
- After 5 clean windows in a row: **de-escalate** one step, and un-throttle.
- The controller may change only work and pace. It **may not** change the bars, the 4-sd rule, the 3-pulse rule, the targets or the event schedule.

## Verdict
- **PASS:** A1–A4 all met over the full run.
- The **sustainable rate** is the throughput reached while every bar held.
- If a bar fails, the run is reported **FAIL**, with the first failing window and what the controller did there.
