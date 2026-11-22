# PREREG D2017: Hash confirmation at TB24. Locked before scoring.
- **Engine:** loomz15 at TB24.
- **Runs:** CONFIRM = 0, 1 (check byte) and 2 (check byte plus a backup slot), on slice K.
- **Keep rule:** keep a setting if it is ≥ 0.03% smaller than CONFIRM = 0.
- **Round-trip:** check TB24 at CONFIRM = 0 (this closes D2016), and also the best setting.
