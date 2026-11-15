# D609 deviations (written before rerun)
D1: crash (ZeroDivisionError) in jy(y) at large y. q = −e^{−2πy} underflows to 0. Only the vacuum checks had printed; no inflation results were seen.
Fix: for 2πy > 300, use the cusp form ln|j| = 2πy (with I_ρ = 2(ln|j| − ln 1728)/4π). This mirrors Ljm in earlier scripts. No other change.
