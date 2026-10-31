@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: e729129799525368
cd /d "%~dp0"
venv\Scripts\python.exe cmbfit.py report
pause
