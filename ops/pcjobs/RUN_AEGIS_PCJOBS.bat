@echo off
REM AEGIS PC jobs J1-J3 (Twist-M capture, Twist-M grid, Twist-2 FI capture map). Results: Desktop\AEGIS_PCJOBS\results\*.txt and run_log.txt
wsl -e bash -lc "cd /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS && python3 -c 'import scipy,numpy;print(scipy.__version__)' && python3 -u run_jobs.py 2>&1 | tee run_log.txt"
pause
