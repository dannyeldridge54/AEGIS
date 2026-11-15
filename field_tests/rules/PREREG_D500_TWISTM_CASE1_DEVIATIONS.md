# D500 DEVIATIONS (written before rerunning)
D1. The first run crashed before any output (scipy event root-finding failed at the V-shaped kink: "f(a) and f(b) must have different signs"). Fix: no solver events. Crossings
are counted as sign changes of φ between the solver's own internal steps, and the crossing state is linearly interpolated. All physics and readings are unchanged.
