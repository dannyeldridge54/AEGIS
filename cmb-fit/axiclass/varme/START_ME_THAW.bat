@echo off
rem TWIST-ME physical-version check (no fit). Run after the TWIST-ME fits finish.
start "ME-THAW" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/varme/run_me_thaw_pc.sh"
