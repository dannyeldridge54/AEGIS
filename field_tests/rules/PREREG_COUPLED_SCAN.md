# PREREG_COUPLED_SCAN — quick look while PREREG_COUPLED_THREAD runs (locked D1709, 2026-11-20 01:52 UTC)
A profile scan of the same likelihood (BAO + SN + CMB). For b_c ∈ {−1, −0.5, −0.25, −0.1, 0, 0.1, 0.25, 0.5, 1}, minimise over (Ω_m, h, ω_b, amp) with Nelder–Mead from the thread best fit (D1694). Report χ²(b_c) − χ²_ΛCDM.
Purpose: a fast picture of whether ANY coupling sign helps and how strongly. It does not replace the locked full fit; if the two disagree, the full fit (D1708) is the result, and the scan is noted as a profile check.
Script: field_tests/scripts/realdata/coupled_scan.py (parallel processes)
