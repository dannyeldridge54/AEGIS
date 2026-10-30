# Star survey audit (ESA Gaia DR3)

The AEGIS galaxy sweep stored every Gaia DR3 star with `parallax_over_error > 5`, tile by tile, in 12,288 HEALPix
level-5 tiles (192,208,838 stars). This audit re-checks **every tile**, three ways: a fresh `COUNT(*)` from the ESA
Gaia archive with the same filter, the count AEGIS recorded when it swept the tile, and the number of rows actually on
disk. A tile passes only if all three agree. Tool: [verify_all_tiles.py](./verify_all_tiles.py).

**Status at 29 October 2026, 22:02 CT:** 11,900 of 12,288 tiles checked against ESA; **11,900 agree on all three counts;
0 mismatches**; 186,130,581 stars confirmed directly by ESA. A separate local check of all 12,288 tile files found all
192,208,838 stored stars match the recorded counts (0 mismatches). Earlier random spot-checks: 200 of 200 matched.
star-count direction found in the survey points toward the Galactic Centre (ordinary Milky Way structure), not a
cosmological signal.