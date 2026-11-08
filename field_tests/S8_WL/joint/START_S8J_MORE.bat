@echo off
rem S8-J deviation D3: two extra restarts for each LCDM+S8 reference. Starts once (guarded by its log).
cd /d C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit
if not exist results\s8j_more_pc_log.txt start "S8-J extra LCDM restarts (WSL)" /belownormal wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/field_tests/S8_WL/joint/s8j_more_pc.sh"
