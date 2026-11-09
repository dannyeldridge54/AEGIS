@echo off
rem V6 restart with the Laplace step (deviation V6-D1). Stops only the first V6 chains; flagship fits keep running. Do not close.
start "V6 Laplace + chains" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/field_tests/V6/run_v6_cov.sh"
