@echo off
REM AEGIS cosmos: cross-match flagged stars (SIMBAD, Gaia) + retry earlier downloads
wsl -e bash -lc "PY=/home/syndyr/micromamba/envs/aegis/bin/python; [ -x $PY ] || PY=python3; cd /mnt/c/Users/Danny/Desktop/AEGIS_cosmos && $PY -u fetch_xmatch.py; $PY -u fetch_vizier.py; $PY -u fetch_cosmos.py"
pause
