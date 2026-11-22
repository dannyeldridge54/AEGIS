# PREREG D1993: speed with exactness (Danny 19:51: "crank it as quickly as possible, keep it accurate"). Locked before the fast engine is written.
1. **Virtual clock.** Add a vclock option to engine v4 (the reference): t = pulse × dt, with dt = 1/2800 s. No sleeping. This makes a run reproducible.
2. **Engine v5** (tools/loom/loom_rt5.py) makes only output-preserving changes:
   - median of 3 or 5 numbers in pure Python;
   - an explicit bound test with numpy.isclose's exact formula;
   - obs() once per pulse;
   - one SVD per lens;
   - per-layer goalpost lists computed once;
   - live goalposts only, per pulse.
   It carries the D1992 restart in both engines.
3. **Accuracy bar: exact equivalence.** For seeds 501, 502 and 503, vclock runs of 20,000 pulses each. Engine v5 must reproduce engine v4's outputs **exactly**:
   - the alarm list (pulse, layer);
   - the status transitions;
   - goalpost label counts;
   - the final knobs (bitwise float equality);
   - fits_spent.
   **Any difference = FAIL**, and v5 is not adopted.
4. **Speed:** report pulses per second for v4 and v5 (wall clock, same seeds). Two CPU cores are available, so independent triangulation seeds run 2 at a time in parallel.
5. **Then the D1992 tests on v5**, unchanged in content: 60 s seed 2033, 20 s seed 2034, replay seed 2035. Wall clock, as before.
