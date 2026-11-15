@echo off
title AEGIS map feed (Star Mapper -> Sky Map)
cd /d "%~dp0"
echo Feeding the AEGIS Sky Map from the Star Mapper. Classroom review CSVs go in cosmos_map\reviews_in\ first.
where py >nul 2>nul && (py -3 -m aegis.map_feed %* & pause & goto :eof)
python -m aegis.map_feed %*
pause
