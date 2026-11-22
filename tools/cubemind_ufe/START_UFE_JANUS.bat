@echo off
REM CubeMind autonomous UFE run: no timer, no check-ins. Usage: START_UFE_JANUS.bat modelA modelB
cd /d "%~dp0"
python -m janus.autorun --model-a %1 --model-b %2
pause
