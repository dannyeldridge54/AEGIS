@echo off
rem Runs every locked AxiCLASS field test in WSL (about 2-3 hours on 16 cores), then scores them.
rem Add --push to send results and scores to the field-results branch. Safe to run again: finished runs are skipped.
cd /d "%~dp0.."
wsl bash -lc "cd \"$(wslpath '%CD%')\" && bash field_tests/run_pc.sh %*"
echo.
echo Results: field_tests\STATUS.md
