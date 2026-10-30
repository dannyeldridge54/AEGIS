# Star survey audit (ESA Gaia DR3)

The AEGIS galaxy sweep stored every Gaia DR3 star with `parallax_over_error > 5`, tile by tile, in 12,288 HEALPix
level-5 tiles (192,208,838 stars). This audit re-checks **every tile**, three ways: a fresh `COUNT(*)` from the ESA
Gaia archive with the same filter, the count AEGIS recorded when it swept the tile, and the number of rows actually on
disk. A tile passes only if all three agree. Tool: [verify_all_tiles.py](./verify_all_tiles.py).

**Status at 29 October 2026, 21:38 CT (still running):** 10,200 of 12,288 tiles checked; **10,200 agree on all three
counts; 0 mismatches**; 144,062,180 stars confirmed directly by ESA. Earlier random spot-checks: 200 of 200 matched.

What this shows: the catalogue is a faithful copy of ESA's data. What it does not show: anything about the Twist. The
star-count direction found in the survey points toward the Galactic Centre (ordinary Milky Way structure), not a
cosmological signal.