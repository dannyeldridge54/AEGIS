@echo off
rem AEGIS validation data collector (8 Nov 2026): Gaia stream samples (Sagittarius, GD-1) for the dark-matter-vs-stars
rem test, then a daily arXiv watch for DESI DR3 / Euclid DR1 / Gaia DR4 / Simons Observatory. Low priority; one ESA job
rem at a time; runs beside the star mapper. Output: ufe-v2\data\validation\ (collect_log.txt, status.json).
title AEGIS validation collector
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY set PY=python
start "AEGIS validation collector" /belownormal /min cmd /c "%PY% -m aegis.validation_collect >> data\validation_collector_console.txt 2>&1"
