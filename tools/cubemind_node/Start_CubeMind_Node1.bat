@echo off
title CubeMind Node 1
cd /d "%~dp0"
echo CubeMind Node 1 - local models only. Status page: node1_data\status.html
:loop
python node1.py
echo Node 1 stopped. Restarting in 3 seconds. Close this window to stop it.
timeout /t 3 /nobreak >nul
goto loop
