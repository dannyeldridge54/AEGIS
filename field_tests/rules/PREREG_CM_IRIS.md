# PREREG CM-IRIS — animated chart generator for CubeMind Ask (locked before build/run)

Date: 2026-11-23. Scope: a renderer (iris.js) that turns any engine chart spec
{title,x_label,y_label,logy,series[{name,x,y}]} into an animated, art-styled canvas chart,
plus a "Chart Studio" panel that calls /api/tool directly (no language model; instant).
Numbers are never changed by the renderer: it only draws engine output.

Optimisation steps (the speed rung): (1) LTTB decimation to <= 2 points per device pixel
column per series; (2) one projection pass into Float32Array + cumulative arc length;
(3) per frame, draw only the new arc fraction onto a cached layer (O(new points)).

Tests (headless Chromium, cloud):
- I1 fidelity: for each test series (exp decay 20k pts, Bateman bump 20k pts, noisy 20k pts,
  log-y 5 decades), the decimated polyline's max vertical deviation from the full-resolution
  polyline, sampled at every device-pixel column, is <= 1.5 device px. Endpoints, global max and
  global min of every series are kept exactly.
- I2 final frame: the last animation frame equals the static render (finish()) to within
  0.5% of pixels differing by > 8/255 in any channel.
- I3 speed: 5 series x 20k points; mean frame time <= 8 ms and prep (decimate+project) <= 60 ms.
- I4 chart values: tooltip/readout at x returns the engine's y (linear interpolation on the
  FULL series) to 1e-12 relative.
Pass = all four. Fails are recorded as failed-as-locked; fixes go in a DEVIATIONS file first.
