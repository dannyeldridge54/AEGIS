@echo off
rem Two-field Twist: build, gate G-TF-PC, 3 fits (PREREG_TWOFIELD.md; needs the lock). Do not close.
start "TWO-FIELD" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/twofield/run_tf_pc.sh"
