@echo off
title AEGIS CMB fit - best fits (runs for hours, low priority)
cd /d "%~dp0"
rem Two CPU threads and below-normal priority: the star scanner and the PC stay responsive.
set OMP_NUM_THREADS=2
echo [%date% %time%] best-fit runs started >> run_log.txt
echo Running 4 best fits: LCDM and torsion EDE, without and with SH0ES.
echo Each can take a few hours. Progress goes to run_log.txt. You can close this window
echo and run this file again later: finished runs are kept and unfinished ones resume.
venv\Scripts\python.exe cmbfit.py minimize >> run_log.txt 2>&1
venv\Scripts\python.exe cmbfit.py report >> run_log.txt 2>&1
type results\REPORT.md
echo [%date% %time%] best-fit runs finished >> run_log.txt
pause
