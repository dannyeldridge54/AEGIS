# D500 DEVIATIONS (written before rerunning)
D1. The first run crashed before any output (scipy event root-finding failed at the V-shaped kink: "f(a) and f(b) must have different signs"). Fix: no solver events. Crossings
are counted as sign changes of φ between the solver's own internal steps, and the crossing state is linearly interpolated. All physics and readings are unchanged.
D2. The rerun was killed (exit 137, memory) after ~7 min with no output: storing every solver step over a fast late-time oscillation grew without bound. Fix: integrate in chunks of ΔN = 0.05,
keep only running crossing counts, remnant sums and min/max x; stop at the locked crossing cap (20000, reported as 'cap hit' with N, |ln x| and amplitude at that point) or at N = 42. Physics and readings unchanged.
