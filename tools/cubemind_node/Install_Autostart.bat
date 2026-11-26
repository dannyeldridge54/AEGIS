@echo off
rem Makes CubeMind Node 1 start by itself, minimised, every time you log in to Windows.
set TARGET=%~dp0Start_CubeMind_Node1.bat
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
(echo @echo off& echo start "CubeMind Node 1" /min cmd /c "%TARGET%") > "%STARTUP%\CubeMind_Node1.bat"
echo Done. Node 1 will start by itself when you log in.
echo To undo: delete "%STARTUP%\CubeMind_Node1.bat"
pause
