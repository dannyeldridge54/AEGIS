@echo off
rem S8-J joint weak-lensing fits (PREREG_S8_JOINT.md, locked 8 Nov). Gate first, then 6 fits in WSL.
start "S8-J joint fits (WSL)" /belownormal wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/field_tests/S8_WL/joint/s8j_pc.sh"
