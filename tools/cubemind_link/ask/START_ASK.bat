@echo off
REM CubeMind Ask: questions -> local model -> validated AEGIS tools -> answer + charts (http://127.0.0.1:8765)
cd /d "%~dp0"
python cm_ask.py
pause
