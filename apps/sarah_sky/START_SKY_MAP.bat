@echo off
title AEGIS Sky Map
cd /d "%~dp0"
where py >nul 2>nul && (py -3 serve.py %* & goto :eof)
where python >nul 2>nul && (python serve.py %* & goto :eof)
echo Python 3 is needed to run the Sky Map from this folder.
echo Install it from https://www.python.org/downloads/ (tick "Add to PATH"), or use the hosted version - see INSTALL.md.
pause
