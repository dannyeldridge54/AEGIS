@echo off
rem TWIST-DR: gate G-DR-PC, then 3 fits (PREREG_TWIST_DR.md). Do not close.
start "TWIST-DR" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/darkrad/run_dr_pc.sh"
