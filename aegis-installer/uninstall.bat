@echo off
title AEGIS Optimizer — Uninstaller
color 0C
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║  AEGIS Optimizer — Uninstaller                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

set INSTALL_DIR=%LOCALAPPDATA%\AEGIS-Optimizer

if not exist "%INSTALL_DIR%" (
    echo  [!] AEGIS Optimizer is not installed.
    pause
    exit /b 0
)

set /p CONFIRM="  Remove AEGIS Optimizer from %INSTALL_DIR%? (y/N): "
if /i "%CONFIRM%" neq "y" (
    echo  Cancelled.
    pause
    exit /b 0
)

echo  [1/3] Removing files...
rmdir /S /Q "%INSTALL_DIR%" 2>nul
echo  [✓] Files removed

echo  [2/3] Removing desktop shortcut...
del "%USERPROFILE%\Desktop\AEGIS Optimizer.lnk" 2>nul
echo  [✓] Shortcut removed

echo  [3/3] Removing Start Menu entry...
rmdir /S /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\AEGIS Optimizer" 2>nul
echo  [✓] Start Menu entry removed

echo.
echo  ✅ AEGIS Optimizer has been uninstalled.
echo  (PATH entry will be cleaned up on next login)
echo.
pause
