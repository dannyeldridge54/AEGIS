@echo off
title Install AEGIS autostart (one time)
REM Double-click once. Registers a Windows scheduled task that runs AEGIS_Watchdog.bat every 10 minutes (hidden), and a Startup-folder
REM entry so it also runs when you sign in. No admin rights needed. To undo: run UNINSTALL_AEGIS_AUTOSTART.bat.
set W=%USERPROFILE%\Desktop\AEGIS_Watchdog.bat
if not exist "%W%" ( echo AEGIS_Watchdog.bat is not on the Desktop. Tell Claude. & pause & exit /b 1 )
schtasks /create /tn "AEGIS Watchdog" /tr "conhost.exe --headless cmd /c \"%W%\"" /sc minute /mo 10 /f
if errorlevel 1 ( echo Could not create the scheduled task. Tell Claude what it said above. & pause & exit /b 1 )
copy /y "%W%" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AEGIS_Watchdog.bat" >nul
echo.
echo Installed. Running it once now...
call "%W%"
echo Done. The runner, grading loop and Ollama will now restart on their own if they stop. You can close this window.
pause
