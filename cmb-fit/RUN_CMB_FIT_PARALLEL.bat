@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 9e2a73614369d966
title AEGIS CMB fit (CAMB) - 4 fits in parallel
cd /d "%~dp0"
rem Runs the four Planck 2018 best fits at the same time (3 CPU threads each) with CAMB,
rem an independent code from the AxiCLASS used in the cloud. Run SETUP_CMB_FIT.bat once first.
if not exist venv\Scripts\python.exe (echo Please run SETUP_CMB_FIT.bat first. & pause & exit /b 1)
if not exist results mkdir results
set OMP_NUM_THREADS=3
for %%R in (lcdm_noshoes ede_noshoes lcdm_shoes ede_shoes) do (
  start "AEGIS fit %%R" /belownormal cmd /c "venv\Scripts\python.exe cmbfit.py minimize %%R >> results\%%R_log.txt 2>&1"
)
echo Four fits started in their own windows (they close when done; several hours).
echo When all four are finished, double-click REPORT_CMB_FIT.bat for the comparison table.
pause
