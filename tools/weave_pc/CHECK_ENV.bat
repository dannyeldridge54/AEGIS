@echo off
cd /d "%~dp0"
python check_env.py > env_check_log.txt 2>&1
echo DONE >> env_check_log.txt
