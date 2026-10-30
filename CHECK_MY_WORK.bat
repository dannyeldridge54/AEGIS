@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use.
title Check Danny's work - AEGIS / the Twist
cd /d "%~dp0"
echo.
echo  ============================================================
echo   CHECK MY WORK  -  every number, re-derived on your own PC
echo  ============================================================
echo.
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY (python --version >nul 2>nul && set PY=python)
if not defined PY (
  echo Python is not installed. Get it free from https://www.python.org/downloads/
  echo then double-click this file again.
  pause & exit /b 1
)
echo [1/3] Installing the two maths libraries it needs (numpy, scipy)...
%PY% -m pip install --quiet --user numpy scipy >nul 2>&1
echo.
echo [2/3] Re-deriving the model's numbers from scratch (no AEGIS code used):
echo ------------------------------------------------------------
%PY% ufe-v2\recheck_math.py
echo.
echo [3/3] Running the honesty guardrails (fits, pre-registrations, theory maths, sigils, claim wall):
echo ------------------------------------------------------------
pushd ufe-v2
%PY% -c "import aegis.guardrails as g; r=g.run_all(); [print(('PASS ' if c['ok'] else 'WAIT ' if c['ok'] is None else 'FAIL '), c['name'], '-', c['plain']) for c in r['checks']]; print(); print(r['passed'],'pass,',r['failed'],'fail,',r['waiting'],'waiting (Star data waits unless the star scanner is running)')"
popd
echo.
echo  Done. To redo the full cosmology fits yourself (hours, uses CAMB + Cobaya):
echo    1. double-click  cmb-fit\SETUP_CMB_FIT.bat
echo    2. double-click  cmb-fit\RUN_CMB_FIT.bat
echo  To check all 192 million stars against ESA:  ufe-v2\START_AEGIS_MONITOR.bat
echo  Found a mistake? Please say so publicly. That is how science works.
echo.
pause
