# Star survey audit (ESA Gaia DR3)

The AEGIS galaxy sweep stored every Gaia DR3 star with `parallax_over_error > 5`, tile by tile, in 12,288 HEALPix
level-5 tiles (192,208,838 stars). This audit re-checks **every tile**, three ways: a fresh `COUNT(*)` from the ESA
Gaia archive with the same filter, the count AEGIS recorded when it swept the tile, and the number of rows actually on
disk. A tile passes only if all three agree. Tool: [verify_all_tiles.py](./verify_all_tiles.py).

**Result (completed 29 October 2026, about 22:04 CT):** all **12,288 of 12,288 tiles agree on all three counts; 0 mismatches.**
**192,208,838 stars** confirmed directly by ESA. A separate local check of every tile file agrees (0 mismatches), and
200 of 200 earlier random spot-checks matched.
cosmological signal.