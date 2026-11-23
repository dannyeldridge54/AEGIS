@echo off
cd /d "%~dp0"
set WEAVE_PKGS=C:\Users\Danny\ufe_data\packages
"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\venv312\Scripts\python.exe" check_env.py > env_check_venv.txt 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_weave_pc.ps1" > start_log.txt 2>&1
echo STARTED >> start_log.txt
