# N3+N4 DEVIATIONS
- DEV-0 (pre-result; the locked run crashed before any value was computed) the OpenMC HDF5 files keep 0 K data only for ELASTIC
  scattering (resonance upscattering); capture exists at 250 K and above. R1/R2 are therefore judged on elastic only; our 0 K capture is
  reported against the 294 K evaluated capture for information (Doppler-affected; the proper capture test moves to N5 with broadening).
## After the first completed run (D1, D2, R1, R2, R4 PASS; R3 FAIL) — written before the rerun
Referee R94 (sonnet, read-only; probe in /tmp):
- DEV-1 (BUG, mine) resonance.py grouped spin groups by |AJ|; the Mn-55 tape uses the SIGN of AJ to mark the channel spin (l=1: AJ = -3,-2,-1,2,3,4
  = six groups). Merging J=2 and J=3 across channel spins made them interfere coherently and set the potential-scattering fill g-sum to 2 instead
  of 3. Worst points were in a deep interference minimum at 118.97-119.01 keV (0.024 vs 0.036 b). Fix: group by signed AJ. R94 /tmp probe:
  median 4.1e-7, p95 1.1e-6, max 1.8e-5. The locked R1 PASS stands but understated the error source; rerun reports the fixed code.
- DEV-2 (my goalpost) R3's 336 eV was unsourced (hint H12): the tape has ER = 340.7875 eV (Gn 23.68 eV, Gg 0.41 eV); ours = evaluated at the peak
  (3192.157 vs 3192.155 b). R3 relocked to: peak within 1 eV of the tape's ER and height within 2%. The locked R3 FAIL stays on the record.
- Notes: no circularity (h5 0 K grid = NJOY reconr; MF3 background zero in the RRR). Capture vs 294 K: median 1e-4 below 300 eV (Doppler negligible),
  only above ~3 keV does Doppler dominate -> capture formula confirmed; temperature belongs to N5.
