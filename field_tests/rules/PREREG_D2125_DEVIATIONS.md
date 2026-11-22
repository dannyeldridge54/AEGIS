# D2125 DEVIATIONS (written before the rerun)
The first run crashed at JSON serialisation (numpy bool) before any output was printed. **Fix:** cast to bool and float. Nothing else changed.
