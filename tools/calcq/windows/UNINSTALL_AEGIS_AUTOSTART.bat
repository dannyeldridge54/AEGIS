@echo off
schtasks /delete /tn "AEGIS Watchdog" /f
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AEGIS_Watchdog.bat" 2>nul
echo AEGIS autostart removed. Running windows are left as they are.
pause
