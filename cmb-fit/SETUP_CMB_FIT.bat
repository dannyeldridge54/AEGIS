@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 73c07d6fd77f262b
title AEGIS CMB fit - setup
cd /d "%~dp0"
echo [%date% %time%] setup started > setup_log.txt
rem Separate Python environment in this folder: nothing here touches the running star scanner.
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY (python --version >nul 2>nul && set PY=python)
if not defined PY (echo Python not found. & echo Python not found >> setup_log.txt & pause & exit /b 1)

if not exist venv\Scripts\python.exe (
  echo Creating a private Python environment...
  %PY% -m venv venv >> setup_log.txt 2>&1
)
set VPY=venv\Scripts\python.exe
echo Installing CAMB, Cobaya and GetDist (several minutes)...
%VPY% -m pip install --upgrade pip >> setup_log.txt 2>&1
%VPY% -m pip install camb cobaya getdist >> setup_log.txt 2>&1
%VPY% -c "import camb, cobaya; print('camb', camb.__version__, 'cobaya', cobaya.__version__)" >> setup_log.txt 2>&1

set OMP_NUM_THREADS=2
echo.
echo Step 1/3: validating CAMB against its documented example (expect H0 = 73.2113)...
%VPY% cmbfit.py validate > validate_log.txt 2>&1
type validate_log.txt

echo.
echo Step 2/3: downloading Planck 2018, DESI DR2 and Pantheon+ likelihood data...
venv\Scripts\cobaya-install yaml\ede_noshoes.yaml yaml\ede_shoes.yaml -p packages --skip-global >> setup_log.txt 2>&1
echo data install exit code %errorlevel% >> setup_log.txt

echo.
echo Step 3/3: one full-likelihood evaluation at the paper's n=3 point (timing check)...
%VPY% cmbfit.py point > point_log.txt 2>&1
type point_log.txt
echo.
echo Setup finished. Logs: setup_log.txt, validate_log.txt, point_log.txt
echo [%date% %time%] setup finished >> setup_log.txt
pause
