@echo off
rem AEGIS job runner: start once and leave the minimized window open. Claude queues jobs; no more double-clicks.
start "AEGIS-RUNNER" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/method/runner/aegis_runner.sh"
