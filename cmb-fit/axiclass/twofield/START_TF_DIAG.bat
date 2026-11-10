@echo off
rem Two-field gate diagnosis (no fit). Takes a few minutes; the window closes itself.
start "TF-DIAG" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/twofield/run_tf_diag_pc.sh"
