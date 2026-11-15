@echo off
REM AEGIS cosmos: VizieR catalogs via TAP (approved)
wsl -e bash -lc "PY=/home/syndyr/micromamba/envs/aegis/bin/python; [ -x $PY ] || PY=python3; cd /mnt/c/Users/Danny/Desktop/AEGIS_cosmos && $PY -u fetch_vizier.py"
pause
