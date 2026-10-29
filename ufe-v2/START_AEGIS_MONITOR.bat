@echo off
title AEGIS v2 Monitor
cd /d "%~dp0"
echo [%date% %time%] launcher started > launcher_log.txt

rem --- pick a Python: the new "py" install manager first, then plain python ---
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY (python --version >nul 2>nul && set PY=python)
if not defined PY (
  echo Python is not installed. Get it from https://www.python.org/downloads/ >> launcher_log.txt
  echo Python is not installed. Get it from https://www.python.org/downloads/
  pause & exit /b 1
)

rem --- the install manager has no runtime yet on a fresh install: add Python 3.13 ---
%PY% --version >> launcher_log.txt 2>&1
if errorlevel 1 (
  echo Installing the Python 3.13 runtime ^(answer Y if asked^)...
  echo installing runtime 3.13 >> launcher_log.txt
  py install 3.13
  set PY=py -3.13
)
%PY% --version >> launcher_log.txt 2>&1

%PY% -c "import numpy, scipy" >nul 2>nul
if errorlevel 1 (
  echo Installing numpy and scipy ^(about a minute^)...
  echo installing numpy scipy >> launcher_log.txt
  %PY% -m pip install --user numpy scipy >> launcher_log.txt 2>&1
)
echo Running acceptance tests...
%PY% tests\test_v2.py > tests_log.txt 2>&1
type tests_log.txt
echo.
echo Starting AEGIS v2 monitor at http://localhost:8765  (close this window to stop)
echo starting monitor >> launcher_log.txt
%PY% monitor_server.py
echo monitor exited with code %errorlevel% >> launcher_log.txt
pause
