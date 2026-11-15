# D500 DEVIATIONS (written before rerunning)
D1. The first run crashed before any output (scipy event root-finding failed at the V-shaped kink: "f(a) and f(b) must have different signs"). Fix: no solver events. Crossings
are counted as sign changes of φ between the solver's own internal steps, and the crossing state is linearly interpolated. All physics and readings are unchanged.
D2. The rerun was killed (exit 137, memory) after ~7 min with no output: storing every solver step over a fast late-time oscillation grew without bound. Fix: integrate in chunks of ΔN = 0.05,
keep only running crossing counts, remnant sums and min/max x; stop at the locked crossing cap (20000, reported as 'cap hit' with N, |ln x| and amplitude at that point) or at N = 42. Physics and readings unchanged.
D3. The D2 run was stopped by me at ~2 min (memory 1.4 GB and rising, no output): late on, the V-shaped trap's oscillation is so fast that one ΔN = 0.05 chunk holds millions of steps. Fix: an adaptive chunk length (halved whenever the previous chunk had > 200 crossings, floor 1e-9), so the locked 20000-crossing cap is reached with bounded memory. Physics and readings unchanged.
