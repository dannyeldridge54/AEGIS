@echo off
REM AEGIS cosmos: VizieR via CfA mirror
wsl -e bash -lc "PY=/home/syndyr/micromamba/envs/aegis/bin/python; [ -x $PY ] || PY=python3; cd /mnt/c/Users/Danny/Desktop/AEGIS_cosmos && $PY -u fetch_vizier2.py"
pause
