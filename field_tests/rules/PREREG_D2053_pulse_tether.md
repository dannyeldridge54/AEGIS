# PREREG D2053: a 1-minute live pulse of the UFE with the tether added (Danny 02:48). Locked before running.
**Model:** the D2039 battery (same goalposts G1–G5, same cost, same one-loop approximation), with **sq no longer a free knob**.
- sq = leak_rel/17.8, where leak_rel = |ln(A_d/A_v)|/x (the tether, D2051).

**Knobs:**
- `rA` = A_d/A_v (start 1; a natural prior is [0.1, 10], and moving it costs a knob only if it leaves [0.64, 1.57]);
- `d3`;
- `boost`;
- `m32`.

**Run:** the Centre with multi-start (the D2039 lesson), repeated pulses until 60 s of wall time. Every kept poke is printed live.

**Read-out:** the goalpost status and the moved knobs (fitted). Expected before running: d3 and boost move, rA stays natural.
