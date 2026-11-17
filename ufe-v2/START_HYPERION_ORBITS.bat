@echo off
title Hyperion orbits (Star Mapper -> Sky Map)
cd /d "%~dp0\.."
echo Hyperion: computing Milky Way orbits for Star Mapper stars that have radial velocities.
echo Reads ufe-v2\cosmos_map\tiles (read-only), writes ufe-v2\cosmos_map\hyperion and apps\skymap\data\hyperion_orbits.json.
echo Safe to stop and restart: finished tiles are skipped.
set PY=python
where py >nul 2>nul && set PY=py -3
%PY% -c "import numpy, scipy, numba" 2>nul || %PY% -m pip install --user numpy scipy numba galpy
%PY% -m tools.janus_astro.mapper_orbits --cosmos-map ufe-v2\cosmos_map --skymap apps\skymap %*
pause
