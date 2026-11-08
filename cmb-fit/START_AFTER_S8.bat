@echo off
rem After the S8-J / S8-L fits finish: restart the 4 interrupted bracket jobs, then run POWER_N n = 1 once its plan is locked.
rem Starts once (guarded by its log). Leave the window open; it waits on its own.
cd /d C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit
if not exist results\after_s8_log.txt start "After S8: bracket + n=1 (WSL)" /belownormal wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/after_s8_pc.sh"
