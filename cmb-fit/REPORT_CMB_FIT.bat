@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: e729129799525368
cd /d "%~dp0"
venv\Scripts\python.exe cmbfit.py report
pause
