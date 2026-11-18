@echo off
rem Janus launcher: runs the Janus app with your installed Python (signed by the Python Software Foundation), so Smart App Control does not block it.
cd /d "%USERPROFILE%\Desktop\AEGIS_PCJOBS\aegis_studio"
start "" pythonw app.py
