@echo off
title AEGIS Optimizer — Installer
color 0A
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║  ⚡ AEGIS Optimizer — Windows Installer v1.0.0               ║
echo  ║  The engine that discovered the Unified Field Equation.      ║
echo  ║  Copyright (c) 2012-2026 Danny Lee Eldridge.                 ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

:: Check for Node.js
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo  [!] Node.js not found. Please install from https://nodejs.org
    echo      Minimum version: 18.0.0
    echo.
    pause
    exit /b 1
)

:: Check Node version
for /f "tokens=1 delims=v" %%a in ('node -v') do set NODE_VER=%%a
echo  [✓] Node.js found: v%NODE_VER%

:: Set install directory
set INSTALL_DIR=%LOCALAPPDATA%\AEGIS-Optimizer
echo  [→] Installing to: %INSTALL_DIR%
echo.

:: Create install directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy files
echo  [1/4] Copying engine files...
xcopy /E /Y /Q "%~dp0engine\*" "%INSTALL_DIR%\" >nul 2>nul
echo  [✓] Engine files copied

:: Install dependencies
echo  [2/4] Installing dependencies...
cd /d "%INSTALL_DIR%"
call npm install --omit=dev --silent 2>nul
echo  [✓] Dependencies installed

:: Create launch scripts
echo  [3/4] Creating launch scripts...

:: Main app launcher
(
echo @echo off
echo title AEGIS Optimizer
echo cd /d "%INSTALL_DIR%"
echo node app.js
echo pause
) > "%INSTALL_DIR%\AEGIS.bat"

:: CLI wrapper
(
echo @echo off
echo cd /d "%INSTALL_DIR%"
echo node sdk/cli.js %%*
) > "%INSTALL_DIR%\aegis.bat"

:: Add to PATH
echo  [4/4] Adding to PATH...
setx AEGIS_HOME "%INSTALL_DIR%" >nul 2>nul

:: Check if already in PATH
echo %PATH% | findstr /I "%INSTALL_DIR%" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    setx PATH "%PATH%;%INSTALL_DIR%" >nul 2>nul
    echo  [✓] Added to PATH (restart terminal to use 'aegis' command)
) else (
    echo  [✓] Already in PATH
)

:: Create Desktop shortcut
echo.
set /p SHORTCUT="  Create desktop shortcut? (Y/n): "
if /i "%SHORTCUT%" neq "n" (
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'AEGIS Optimizer.lnk')); $sc.TargetPath = '%INSTALL_DIR%\AEGIS.bat'; $sc.WorkingDirectory = '%INSTALL_DIR%'; $sc.Description = 'AEGIS Optimizer - Dual Engine Optimization'; $sc.IconLocation = 'shell32.dll,13'; $sc.Save()"
    echo  [✓] Desktop shortcut created
)

:: Create Start Menu shortcut
powershell -Command "$startMenu = [Environment]::GetFolderPath('StartMenu'); $folder = Join-Path $startMenu 'Programs\AEGIS Optimizer'; if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; $ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut((Join-Path $folder 'AEGIS Optimizer.lnk')); $sc.TargetPath = '%INSTALL_DIR%\AEGIS.bat'; $sc.WorkingDirectory = '%INSTALL_DIR%'; $sc.Description = 'AEGIS Optimizer'; $sc.IconLocation = 'shell32.dll,13'; $sc.Save(); $sc2 = $ws.CreateShortcut((Join-Path $folder 'AEGIS CLI.lnk')); $sc2.TargetPath = 'cmd.exe'; $sc2.Arguments = '/k cd /d %INSTALL_DIR% & echo AEGIS CLI Ready. Type: aegis --help'; $sc2.WorkingDirectory = '%INSTALL_DIR%'; $sc2.Save()" 2>nul
echo  [✓] Start Menu shortcuts created

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║  ✅ Installation Complete!                                    ║
echo  ║                                                               ║
echo  ║  To launch the app:                                           ║
echo  ║    • Double-click "AEGIS Optimizer" on your Desktop           ║
echo  ║    • Or run: AEGIS.bat                                        ║
echo  ║                                                               ║
echo  ║  CLI usage (open new terminal):                               ║
echo  ║    aegis optimize --config task.json                          ║
echo  ║    aegis dual --config task.json                              ║
echo  ║    aegis benchmark                                            ║
echo  ║    aegis serve --port 3000                                    ║
echo  ║                                                               ║
echo  ║  Installed to: %INSTALL_DIR%                                  ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
pause
