# D2136 DEVIATIONS
## DEV-1 (2026-11-22). Crash before any output
The addendum edit replaced the whole `H0_BASE = …; S_H0 = …` line and dropped the definition of S_H0, so every variant stopped with a NameError before computing anything. The fix restores `S_H0 = median(5.0, 6.2, 7.0)` exactly as locked. No other change.
