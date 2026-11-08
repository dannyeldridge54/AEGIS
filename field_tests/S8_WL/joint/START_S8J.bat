@echo off
rem Weak-lensing tests (8 Nov). S8-J: joint fit (locked). S8-L: light angle (build + gate now; fits start by themselves once its rule is locked).
rem Each starts only once (guarded by its log file).
cd /d C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit
if not exist results\s8j_pc_log.txt start "S8-J joint fits (WSL)" /belownormal wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/field_tests/S8_WL/joint/s8j_pc.sh"
if not exist results\spiral_l_pc_log.txt start "S8-L light angle (WSL)" /belownormal wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/ula/spiral_l_pc.sh"
