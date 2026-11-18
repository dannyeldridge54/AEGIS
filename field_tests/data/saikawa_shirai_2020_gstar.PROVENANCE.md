# Provenance: saikawa_shirai_2020_gstar.dat
- Source: the file `src/ptarcade/data/g_star.dat` from the PTArcade repository (github.com/andrea-mitridate/ptarcade, commit e87e77235467790043608f6ff3b639f12018ed1d), copied byte-for-byte.
- Its header names K. Saikawa and S. Shirai (2020). PTArcade's docs cite arXiv:2005.03544.
- Columns: T [GeV], f [Hz], g_*s, g_*ρ. There are 528 rows, with T from 1e-5 to 1.47e6 GeV.
- Downloaded 2026-11-18 with Danny's OK ("yes yes yes" in reply to "yes table").
- The IPMU site (member.ipmu.jp/satoshi.shirai/EOS2018) was not reachable from this sandbox's shell; its viewer showed only part of the file.
- Cross-check against the IPMU standardmodel2018.dat row read through the viewer, at T = 0.014809607 GeV:
  - IPMU: g_ρ = 10.888297, g_s = 10.862591;
  - this file, interpolated in ln T: 10.8892 and 10.8634 (agreement better than 0.01%).
