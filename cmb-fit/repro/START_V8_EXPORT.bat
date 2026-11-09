@echo off
rem V8: records the exact fit environment (read-only; a few minutes; safe while fits run).
start "V8 export" /min wsl bash -lc "bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/repro/export_pc_env.sh"
