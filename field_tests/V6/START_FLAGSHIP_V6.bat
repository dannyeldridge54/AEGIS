@echo off
rem FLAG-1 flagship fits + V6 evidence chains (9 Nov). Starts a WSL job; safe to run again (resumes). Do not close.
start "FLAG-1 + V6" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/field_tests/V6/run_flagship_v6.sh"
